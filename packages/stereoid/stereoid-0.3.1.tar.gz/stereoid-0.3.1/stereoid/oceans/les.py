"""les provides functions that handle les_surface results"""
import glob
import os
import re

import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from scipy import ndimage


def read_les_surface(directory, filemsk="fielddum*.nc"):
    fls = glob.glob(os.path.join(directory, filemsk))
    yind = []
    for fl in fls:
        bsnm = os.path.basename(fl)
        found = re.findall('\d\d\d', bsnm)
        yind.append(found[1])
    inds = np.argsort(yind)
    sfls = np.array(fls)[inds]
    # read fist u
    fs1 = xr.open_dataset(sfls[0])
    u = fs1.u[:, 0, :, :]
    v = fs1.v[:, 0, :, :]
    for ind in range(1, len(sfls)):
        try:
            with xr.open_dataset(sfls[ind]) as fs:
                u = xr.concat([u, fs.u[:, 0, :, :]], 'yt')
                v = xr.concat([v, fs.v[:, 0, :, :]], 'ym')
        except FileNotFoundError as err:
            print(f"File {sfls[ind]} was not found: {err}")
            raise
        # FIXME: bare excepts should be avoided as they can mask a
        # programming error
        except:
            print("%s cannot be read" % sfls[ind])
    return xr.merge([u/1000, v/1000])


def les_rotate(uv, angle, tind):
    """Project uv data to radar coordiantes.

    Parameters
    ----------
    uv: xarray.Dataset
        DataSet with u (East to West) and v (North to South) wind components for
        a number of times as output by DALES.
    angle: float
        Heading of satellite
    rind: integer
        Time step to use.

    Returns
    -------
    tuple
        the rotated u and v components.
    """
    uu = uv.u.values[tind]
    vv = uv.v.values[tind]
    uu[np.isnan(uu)] = np.nanmean(uu)
    vv[np.isnan(vv)] = np.nanmean(vv)
    u = ndimage.rotate(uu, angle)
    v = ndimage.rotate(vv, angle)
    ur = u * np.cos(np.radians(angle)) + v * np.sin(np.radians(angle))
    vr = - u * np.sin(np.radians(angle)) + v * np.cos(np.radians(angle))
    return ur, vr


#%%
if __name__ == '__main__':
    from stereoid.oceans import FwdModel, SceneGenerator, RetrievalModel
    from stereoid.oceans import ObsGeo, RadarModel
    import stereoid.sar_performance as strsarperf
    import stereoid.utils.config as st_config
    from drama import geo as sargeo
    paths = st_config.parse(section="Paths")
    main_dir = paths["main"]
    datadir = paths["data"]
    pardir = paths["par"]
    parfile = os.path.join(pardir, 'Hrmny_2020_1.cfg')
    main_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
    lesdata = '/Users/plopezdekker/LocalDATA/LES/CONSTRAIN_ForwardShear'
    datadir = "/Users/plopezdekker/Documents/WORK/STEREOID/DATA/ScatteringModels/Oceans"
    pardir = "/Users/plopezdekker/Documents/CODE/STEREOID/PAR"
    fname = "C_band_nrcs_dop_ocean_simulation.nc"
    fnameisv = "C_band_isv_ocean_simulation.nc"
    # obsgeo = ObsGeo(35, 36, 40)
    swth_bst = sargeo.SingleSwathBistatic(par_file=parfile) #, companion_delay=300e3)
# Incident angle
    inc_m = 37
    obsgeo = ObsGeo.from_swath_geo(inc_m, swth_bst, ascending=True)
    # Radar model_parameters
    run_id = '2020_1'
    prod_res = 250
    mode = "IWS"
    az_res_dct = {"WM":5, "IWS":20}
    az_res = az_res_dct["IWS"]
    rx_ati_name = 'tud_2020_half'  # name of system in parameter file
    rx_dual_name = 'tud_2020_dual6m' # full system, will have 3 dB better NESZ, etc.
    fstr_dual = strsarperf.sarperf_files(main_dir, rx_dual_name, mode=mode, runid=run_id, parpath=parfile)
    fstr_ati = strsarperf.sarperf_files(main_dir, rx_ati_name, mode=mode, runid=run_id, parpath=parfile)
    fstr_s1 = strsarperf.sarperf_files(main_dir, 'sentinel', is_bistatic=False, mode=mode, runid=run_id, parpath=parfile)
    radarm = RadarModel(obsgeo, fstr_s1, fstr_dual, fstr_ati, az_res=az_res, prod_res=prod_res, b_ati=9)
    # %%
    fwdm = FwdModel(datadir, os.path.join(datadir, fnameisv), dspd=2, duvec=0.5, model="SSAlin")
    # fwdm.nrcs_crt.shape
    fwdm.at_distance = 350e3
    #%%
    uv = read_les_surface(lesdata)
    # fs1 = xr.open_dataset(sfls[0])
    uv.to_netcdf(os.path.join(lesdata, "surface_wind.nc"))
    #%%
    # Read surface winds file geneerated from LES
    uv = xr.open_dataset(os.path.join(lesdata, "surface_wind.nc"))
    #%%
    grid_spacing = uv.ym.values[1] - uv.ym.values[0]
    u, v = les_rotate(uv, 10, 10)
    scene_size = u.shape[0] * grid_spacing
    obsgeo.set_swath(35, np.arange(u.shape[1]).reshape((1, u.shape[1])) * grid_spacing)
    #%%
    extent = [0, scene_size/1e3, 0, scene_size/1e3]
    plt.figure()
    plt.imshow(u, origin='lower', vmin=-5, vmax=5, extent=extent)
    plt.colorbar()
    plt.figure()
    plt.imshow(v+4, origin='lower', vmin=0, vmax=12, extent=extent)
    plt.colorbar()
    # %% Scene
    vp = v + 4
    v.mean()
    u.mean()
    u_mag = np.sqrt(u**2 + vp**2)
    u_dir = np.degrees(np.arctan2(vp, u))
    sgm = SceneGenerator(fwdm, u.shape, wspd=u_mag, wdir=u_dir, cartesian=True,
                         grid_spacing=grid_spacing)
    #%%
    # %% Run scene generator
    # sgm.wdir = 0
    fwdm.sigma_nrcs_db = 0.1
    snrcs, sdca = sgm.l1(obsgeo)
    snrcs.shape
    obsgeo.inc_m.shape
    r_nrcs, r_dca, r_isv = radarm.add_errors(snrcs, sdca, np.zeros_like(sdca))
    snrcs.shape
    plt.figure()
    plt.imshow(r_nrcs[:, :, 0], origin='lower', extent=extent)
    plt.colorbar()
    snrcs.min()
    plt.figure()
    plt.imshow(r_nrcs[:, :, 1], origin='lower', extent=extent)
    plt.colorbar()
    snrcs.min()
    plt.figure()
    plt.imshow(r_nrcs[:, :, 0] - snrcs[:, :, 0], origin='lower', extent=extent)
    plt.colorbar()
    # %% Retrieval model
    ret = RetrievalModel(fwdm, obsgeo, cartesian=True)
    # %% run retrieval
    w_u, w_v, dca_fwd = ret.retrieval_1(snrcs, 0, dir0=90)
    w_u_r, w_v_r, dca_fwd_r = ret.retrieval_1(r_nrcs, 0, dir0=90)
    w_u.mean(), w_v.mean()
    #%%
    plt.figure()
    plt.imshow(w_u, origin='lower', vmin=-5, vmax=5, extent=extent)
    plt.colorbar()
    plt.figure()
    plt.imshow(w_v, origin='lower', vmin=0, vmax=12, extent=extent)
    plt.colorbar()
    plt.figure()
    plt.imshow(w_u_r, origin='lower', vmin=-5, vmax=5, extent=extent)
    plt.colorbar()
    plt.figure()
    plt.imshow(w_v_r, origin='lower', vmin=0, vmax=12, extent=extent)
    plt.colorbar()
    kk = np.arange(3*4*5).reshape((3,4,5))
    ind0 = np.array([[0, 1]])
    ind1 = np.array([[0,2], [0,2]])
    kk[ind0, ind1, ind1]
    np.zeros((2,3)).astype(int)
