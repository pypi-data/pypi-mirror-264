import os
import numpy as np
import xarray as xr
import logging
from typing import Optional, Tuple
from scipy.ndimage import gaussian_filter
from stereoid.oceans import RetrievalModel, FwdModelRIM
import stereoid.oceans.tools.read_tools as read_tools
from drama.utils.filtering import smooth1d
import drama.utils as drtls
from scipy.signal import medfilt


# Define logger level for debug purposes
logger = logging.getLogger(__name__)
logging.getLogger('numba').setLevel(logging.WARNING)

def smooth2d(data: np.ndarray, s: int) -> np.ndarray:
    return smooth1d(smooth1d(data, s, axis=0), s, axis=1)


def read_lut(list_lut: dict) -> dict:
    ''' Read Lookup tables '''
    for key in list_lut.keys():
        list_lut[key]['xarray'] = xr.open_dataset(list_lut[key]['file'])
    return list_lut


def read_L1(ifile: str, var: str, normalise_imacs: bool = False
            ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    ''' Read L1 data from pickle or dictionnary'''
    if os.path.splitext(ifile)[1] == '.nc':
        list_var = [var, 'longitude', 'latitude', 'inc']
        dic = read_tools.read_netcdf(ifile, list_var=list_var)
    else:
        dic = read_tools.read_pickle(ifile)
    array = dic[var]
    lon = dic['longitude']
    lat = dic['latitude']
    inc = dic['inc'][:, 0]
    if var == 'imacs':
        if normalise_imacs == True:
            list_var = ['rmacs', 'longitude', 'latitude', 'inc']
            dic = read_tools.read_netcdf(ifile, list_var=list_var)
            array=array/dic['rmacs']

    return array, lon, lat, inc


def read_model(ifile: str, var: str
               ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    ''' Read L1 data from pickle or dictionnary'''
    if os.path.splitext(ifile)[1] == '.nc':
        list_var = [var, 'longitude', 'latitude']
        dic = read_tools.read_netcdf(ifile, list_var=list_var)
    else:
        dic = read_tools.read_pickle(ifile)
    array = dic[var]
    lon = dic['longitude']
    lat = dic['latitude']
    return array, lon, lat


def fwd_model_rim(list_lut: dict, obs_geo, dx: float, normalise_imacs: bool):
    ''' Compute forward model for RIM '''
    nrcs = list_lut['nrcs']['xarray']
    dop = list_lut['dop']['xarray']
    imacs = list_lut['imacs']['xarray']
    cut_off = list_lut['cut_off']['xarray']

    fwdm = FwdModelRIM(nrcs, dop, imacs, cut_off, None, dspd=2,
                       duvec=0.25, model="RIM", normalise_imacs=normalise_imacs)

    # # Instantiate retrieval model
    retm = RetrievalModel(fwdm, obs_geo.concordia, obs_geo.discordia,
                          grid_spacing=dx, cartesian=True)

    return fwdm, retm


def mask_invalid_retrieval(w_u: np.ndarray, w_v: np.ndarray, j1a:np.ndarray,
                           j1d0: np.ndarray, threshold_j: float,
                           ) -> Tuple[np.ndarray, np.ndarray]:
    """Mask invalid values when values retrieved are outside the range of the
    LUTs"""
    shape0, shape1 = np.shape(w_u)
    if logger.getEffectiveLevel() == logging.DEBUG:
        shape3 = np.shape(j1a)[2]
        j1a2 = j1a.reshape((shape0, shape1, shape3, shape3))
        j1d02 = j1d0.reshape((shape0, shape1, shape3, shape3))
        j1min = np.nanmin(np.nanmin(j1a2 + j1d02, axis=2), axis=2)
    else:
        j1min = (j1a + j1d0).reshape((shape0, shape1))
    w_u[np.where(j1min > threshold_j)] = float("nan")
    w_v[np.where(j1min > threshold_j)] = float("nan")
    return w_u, w_v


def mask_invalid_nrcs(w_u: np.ndarray, w_v: np.ndarray, nrcs: np.ndarray,
                      filter_factor: int, threshold_nrcs: float
                      ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """ Mask values where nrcs for S1 is outside the valid range """
    if (filter_factor % 2) == 0:
        filter_factor += 1
    for ind in range(3):
        nrcs_db = drtls.db(nrcs[:, :, ind])
        lr_nrcs_db = medfilt(nrcs_db, filter_factor)
        hr_nrcs_db = nrcs_db - lr_nrcs_db

        w_u[np.where(hr_nrcs_db > threshold_nrcs)] = float("nan")
        w_v[np.where(hr_nrcs_db > threshold_nrcs)] = float("nan")
    return w_u, w_v


def filter_nrcs(nrcs: np.ndarray, wnd_dir: np.ndarray, wnd_norm: np.ndarray,
                imacs: np.ndarray, cut_off: np.ndarray, incm: np.ndarray, rfac: int
                ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    shp_nrcs = (np.round(nrcs.shape[0] / rfac), np.round(nrcs.shape[1] / rfac))
    shape = (int(shp_nrcs[0]), int(shp_nrcs[1]), nrcs.shape[2])
    lr_nrcs = np.full(shape, np.nan)
    lr_imacs = np.full(shape, np.nan)
    lr_cut_off = np.full(shape, np.nan)
    for ind in range(3):
        tmp = gaussian_filter(drtls.db(nrcs[:, :, ind]), sigma=(rfac / 2))
        lr_nrcs[:, :, ind] = 10**(tmp[::rfac, ::rfac] / 10)
        tmp = gaussian_filter(imacs[:, :, ind], sigma=(rfac / 2))
        lr_imacs[:, :, ind] = + tmp[::rfac, ::rfac]
        tmp = gaussian_filter(cut_off[:, :, ind], sigma=(rfac / 2))
        lr_cut_off[:, :, ind] = + tmp[::rfac, ::rfac]
    tmp = gaussian_filter(wnd_dir[:, :], sigma=(rfac / 2))
    lr_wnd_dir = + tmp[::rfac, ::rfac]
    tmp = gaussian_filter(wnd_norm[:, :], sigma=(rfac / 2))
    lr_wnd_norm = + tmp[::rfac, ::rfac]
    lr_incm = + incm[::rfac]
    return lr_nrcs, lr_wnd_dir, lr_wnd_norm, lr_imacs, lr_incm, lr_cut_off


def retrieve_wind(dic_l1: dict, retm, fetch: float,
                  dir0: Optional[np.ndarray] = None,
                  norm0: Optional[np.ndarray] = None,
                  pol: Optional[str] = 'V',
                  sigma_norm0: Optional[list] = [1.7, 0.8],
                  sigma_imacs: Optional[list] = [0.03e-4, 0.08e-4],
                  sigma_dir0: Optional[list] = [1, 10],
                  sigma_dca: Optional[float] = 5,
                  rfac: Optional[list] = [10, 1],
                  threshold_j: Optional[float] = 40,
                  threshold_nrcs: Optional[float] = 1,
                  filter_nrcs_length: Optional[int] = 5,
                  weight_imacs: Optional[list] = [[0.5, 1., 1.], [1., 1., 1.]],
                  weight_nrcs: Optional[list] = [[0.5, 1., 1.], [1., 1., 1.]],
                  retrieval_type: Optional[str] = 'two_step',
                  mask_invalid: Optional[bool] = True,
                  ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    ''' Wind stress retrieval '''
    if pol == 'V':
        pol_ind = 1
    else:
        pol_ind = 0
    if logger.getEffectiveLevel() == logging.DEBUG:
        debug = True
    else:
        debug = False
    nrcs = dic_l1['nrcs'][:, :, :, pol_ind]
    imacs = dic_l1['imacs'][:, :, :, pol_ind]
    cut_off = dic_l1['cut_off'][:, :, :, pol_ind]
    dir0 = np.degrees(dir0)
    wnd_dir = dir0.copy()
    wnd_norm = norm0.copy()

    # pyramidal processing, the index goes through the pyramidal levels
    for ind in range(len(sigma_norm0)):

        # filtering applied for the pyramid levels
        logger.info(f'process level {ind} of pyramid with {rfac[ind]} filtering')
        if rfac[ind] != 1:
            _res = filter_nrcs(nrcs, wnd_dir, wnd_norm, imacs, cut_off, retm.incm_ind,
                               rfac[ind])
            lr_nrcs, lr_wnd_dir, lr_wnd_norm, lr_imacs, retm.incm_ind_lr, lr_cut_off = _res
        else:
            lr_nrcs = nrcs.copy()
            lr_wnd_dir = wnd_dir.copy()
            lr_wnd_norm = wnd_norm.copy()
            lr_imacs = imacs.copy()
            lr_cut_off = cut_off.copy()
            retm.incm_ind_lr = retm.incm_ind.copy()

        # select retrieval method (standard is two-step)
        if retrieval_type == 'two_step':
            _res = retm.retrieval_2(lr_nrcs, lr_imacs, lr_cut_off, dir0=lr_wnd_dir,
                                    norm0=lr_wnd_norm, sigma_nrcs_db=0.2,
                                    sigma_imacs=sigma_imacs[ind],
                                    sigma_dir0=sigma_dir0[ind],
                                    sigma_norm0=sigma_norm0[ind],
                                    weight_imacs=weight_imacs[ind],
                                    weight_nrcs=weight_nrcs[ind], window=None,
                                    debug=debug)
        else:
            _res = retm.retrieval_1(lr_nrcs, lr_imacs, fetch, dir0=lr_wnd_dir,
                                    norm0=lr_wnd_norm, sigma_nrcs_db=0.2,
                                    sigma_imacs=sigma_imacs[ind],
                                    sigma_dir0=sigma_dir0[ind],
                                    sigma_norm0=sigma_norm0[ind],
                                    weight_imacs=weight_imacs[ind],
                                    weight_nrcs=weight_nrcs[ind], window=None,
                                    debug=debug)
        w_u, w_v, j1a, j1b, j1d0, dca_fwd = _res

        # debugging
        if logger.getEffectiveLevel() == logging.DEBUG:
            import pickle
            _dic = {'wnd_u': w_u, 'wnd_v': w_v, 'dca': dca_fwd}
                    #  'j1a': j1a, 'j1b': j1b, 'j1d0': j1d0}
            with open(f'l{ind}_rfac_{rfac[ind]}.pyo', 'wb') as f:
                pickle.dump(_dic, f)

        # temporary storage for pyramidal retrieval
        if rfac[ind] != 1:
            w_u_tmp = np.repeat(np.repeat(w_u, rfac[ind], axis=0), rfac[ind],
                                axis=1)
            w_v_tmp = np.repeat(np.repeat(w_v, rfac[ind], axis=0), rfac[ind],
                                axis=1)
        else:
            w_u_tmp = w_u
            w_v_tmp = w_v

        # update first-guess wind speed and direction
        wnd_dir = np.rad2deg(np.arctan2(w_v_tmp, w_u_tmp))
        wnd_norm = np.sqrt(w_u_tmp**2 + w_v_tmp**2)

    # clear NaN's
    if mask_invalid == True:
        w_u, w_v = mask_invalid_retrieval(w_u, w_v, j1a, j1d0, threshold_j)
        w_u, w_v = mask_invalid_nrcs(w_u, w_v, lr_nrcs, filter_nrcs_length,
                                 threshold_nrcs)

    # apply filter to estimated Dopplers
    filt_dca_fwd = np.full(np.shape(dca_fwd), np.nan)
    for ind in range(3):
        filt_dca_fwd[:, :, ind] = gaussian_filter(dca_fwd[:, :, ind],
                                                  sigma=sigma_dca)

    # output wind vector and wave-Dopplers
    return w_u, w_v, filt_dca_fwd


def retrieve_tsc(dic_l1: dict, retm, dca_fwd: np.ndarray
                 ) -> Tuple[np.ndarray, np.ndarray]:
    ''' TSC retrieval '''
    # obsgeo.bist_ang.shape
    # mskout = np.sum(wind, axis=-1) < 39
    # dca_fwd = dca_fwd * mskout[:,:, np.newaxis]
    dca_fwd[dca_fwd == 0] = np.nan
    dca = dic_l1['dop'][:, :, :, 1]
    print(dca.shape)
    print(dca_fwd.shape)
    tscv, a, b025 = retm.tscv(dca, dca_fwd, s1_weight=0.25)
    return tscv[:, :, 0], tscv[:, :, 1]
