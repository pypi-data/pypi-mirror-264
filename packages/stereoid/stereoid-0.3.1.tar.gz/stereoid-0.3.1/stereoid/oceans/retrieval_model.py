import os
import numpy as np
from typing import Optional, Tuple

from numba import njit
from drama import constants as cnst
import drama.utils as drtls

# import stereoid.utils.tools as tools
from stereoid.oceans import ObsGeo
from stereoid.oceans.forward_model import ind_clip

__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

# %% RetrievalModel class
G = 9.81
X_0 = 22E3


def add_dim_pol(lut_shp: Tuple, var_fwdm: np.ndarray, m_ind: int,
                incm_ind: int, d_c1_ind: int, d_c2_ind: int) -> np.ndarray:
    var_lut = np.zeros(lut_shp)
    var_lut[:, :, :, 0] = var_fwdm[m_ind, :, :, incm_ind, :, :].copy()
    var_lut[:, :, :, 1] = var_fwdm[d_c1_ind, :, :, incm_ind, :, :].copy()
    if d_c2_ind is not None:
        var_lut[:, :, :, 2] = var_fwdm[d_c2_ind, :, :, incm_ind, :, :].copy()
    return var_lut


def add_dim_car(lut_shp: tuple, var_fwdm: np.ndarray, mono_ind: int,
                d_c1_ind: int, d_c2_ind: int) -> np.ndarray:
    var_lut = np.zeros(lut_shp)
    var_lut[..., 0] = var_fwdm[mono_ind, :, :, :, :, :].copy()
    var_lut[..., 1] = var_fwdm[d_c1_ind, :, :, :, :, :].copy()
    if d_c2_ind is not None:
        var_lut[..., 2] = var_fwdm[d_c2_ind, :, :, :, :, :].copy()
    return var_lut


class RetrievalModel(object):
    def __init__(self, fwd_model, obs_geo_a, obs_geo_b,
                 grid_spacing: Optional[float] = 1e3,
                 wave_doppler_corr_length: Optional[float] = 20e3,
                 cartesian: Optional[bool] = True,
                 pol: Optional[int] = 1,
                 progress_bar: Optional[bool] = True):
        self.progress_bar = progress_bar
        self.f0 = 5.4e9
        self.fwdm = fwd_model
        self.obs_geo_a = obs_geo_a
        self.obs_geo_b = obs_geo_b
        self.cartesian = cartesian
        # Set inc to smallest in LUT
        self.incm = 0
        self.incb = 0
        # Set wave age to the mean value in LUT
        self.waveage = self.fwdm.waveagev
        self.stereo = self.fwdm.stereo
        # read from obs_geo
        self.__inc_m = self.obs_geo_a.inc_m
        if self.obs_geo_a.degrees:
            self.__inc_m_d = self.__inc_m
        else:
            self.__inc_m_d = np.degrees(self.__inc_m)
        # self.incm_ind = np.abs(self.fwdm.incv - self.__inc_m).argmin()
        self.incm_ind = ind_clip(np.round((self.__inc_m_d - self.fwdm.inc_min)
                                          / self.fwdm.inc_step).astype(np.int),
                                 self.fwdm.incv.size)
        self.__inc_b = self.obs_geo_a.inc_b
        self.__inc_b_a = self.obs_geo_a.inc_b
        self.__inc_b_b = self.obs_geo_b.inc_b
        # The following is to work with a monostatic equivalent,
        # which should be phased out
        self.__incb_eq = (self.__inc_b + self.__inc_m) / 2
        # self.incb_ind = np.abs(self.fwdm.incv - self.__incb_eq).argmin()
        self.incb_ind = ind_clip(np.round((self.__incb_eq - self.fwdm.inc_min)
                                          / self.fwdm.inc_step).astype(np.int),
                                 self.fwdm.incv.size)
        self.__bist_ang_az = self.obs_geo_a.bist_ang
        self.__inc_b_a = self.obs_geo_a.inc_b
        self.__inc_b_b = self.obs_geo_b.inc_b
        if type(self.__bist_ang_az) == np.ndarray:
            self.bist_wdir_indoff = (np.round(self.__bist_ang_az / 2
                                     / self.fwdm.wdir_step)).astype(np.int)
        else:
            self.bist_wdir_indoff = int(np.round(self.__bist_ang_az / 2
                                                 / self.fwdm.wdir_step))
        self.luts_ready = False
        self.grid_spacing = grid_spacing
        self.wave_doppler_corr_length = wave_doppler_corr_length
        self.pol = pol

    def check_obs_geo(self):
        uptodate = (np.all(self.obs_geo_a.inc_m == self.__inc_m) and
                    np.all(self.obs_geo_a.inc_b == self.__inc_b) and
                    np.all(self.obs_geo_a.bist_ang == self.__bist_ang_az))
        if uptodate:
            return True
        else:
            self.__inc_m = self.obs_geo_a.inc_m
            # self.incm_ind = np.abs(self.fwdm.incv - self.__inc_m).argmin()
            self.incm_ind = ind_clip(np.round((self.__inc_m - self.fwdm.inc_min)
                                              / self.fwdm.inc_step).astype(np.int),
                                     self.fwdm.incv.size)
            self.__inc_b = self.obs_geo_a.inc_b
            self.__inc_b_a = self.obs_geo_a.inc_b
            self.__inc_b_b = self.obs_geo_b.inc_b
            self.__incb_eq = (self.__inc_b + self.__inc_m) / 2
            self.incb_ind = np.abs(self.fwdm.incv - self.__incb_eq).argmin()
            self.__bist_ang_az = self.obs_geo_a.bist_ang
            self.__bist_ang_az_a = self.obs_geo_a.bist_ang
            self.__bist_ang_az_b = self.obs_geo_b.bist_ang
            self.bist_wdir_indoff = int(np.round(self.__bist_ang_az / 2
                                                 / self.fwdm.wdir_step))
            self.luts_ready = False
            return False

    @property
    def waveage(self):
        return self.__waveage

    @waveage.setter
    def waveage(self, waveage):
        self.__waveage = waveage
        try:
            _diff = self.fwdm.isv_waveagev - waveage
            self.isv_waveage_ind = np.abs(_diff).argmin()
        except:
            print("No ISV data")
        self.luts_ready = False

    def prepare_luts(self):
        if self.cartesian:
            self.__prepare_luts_cart()
        else:
            self.__prepare_luts_polar()

    def __prepare_luts_cart(self):
        if self.fwdm.fwdm_type == 'monostatic_proxy':
            print("Monostatic proxy not implemented in cartesian approach...")
        else:
            if self.stereo:
                lut_shp = self.fwdm.nrcs_crt[0, :, :, :, :, :].shape + (3,)
                d_c2_ind = self.fwdm.at_distance_c2_ind
            else:
                lut_shp = self.fwdm.nrcs_crt[0, :, :, :, :, :].shape + (2,)
                d_c2_ind = None

            self.nrcs_lut = add_dim_car(lut_shp, self.fwdm.nrcs_crt,
                                        self.fwdm.monostatic_ind,
                                        self.fwdm.at_distance_c1_ind, d_c2_ind)
            self.dca_lut = add_dim_car(lut_shp, self.fwdm.dca_crt,
                                       self.fwdm.monostatic_ind,
                                       self.fwdm.at_distance_c1_ind, d_c2_ind)
            self.imacs_lut = add_dim_car(lut_shp, self.fwdm.imacs_crt,
                                         self.fwdm.monostatic_ind,
                                         self.fwdm.at_distance_c1_ind,
                                         d_c2_ind)
            self.cut_off_lut = add_dim_car(lut_shp, self.fwdm.cut_off_crt,
                                           self.fwdm.monostatic_ind,
                                           self.fwdm.at_distance_c1_ind,
                                           d_c2_ind)
            self.luts_ready = True

    def __prepare_luts_polar(self):
        if self.fwdm.fwdm_type == 'monostatic_proxy':
            if self.stereo:
                lut_shp = self.fwdm.nrcsm[:, :, self.incm_ind, :, :].shape + (3,)
            else:
                lut_shp = self.fwdm.nrcsm[:, :, self.incm_ind, :, :].shape + (2,)
            self.nrcs_lut = np.zeros(lut_shp)
            self.nrcs_lut[:, :, :, 0] = self.fwdm.nrcsm[:, :, self.incm_ind,
                                                        :, :]
            tmp = self.fwdm.nrcsm[:, :, self.incm_ind, :, :]
            self.nrcs_lut[:, :, :, 1] = np.roll(tmp, -self.bist_wdir_indoff,
                                                axis=1)
            if self.stereo:
                self.nrcs_lut[:, :, :, 2] = np.roll(tmp, self.bist_wdir_indoff,
                                                    axis=1)

            self.isv_im_lut = np.zeros(lut_shp)
            self.isv_im_lut[:, :, :, 0] = self.fwdm.isv_im[:, :, self.incm_ind,
                                                           :, :]
            tmp = self.fwdm.isv_im[:, :, self.incm_ind, :, :]
            self.isv_im_lut[:, :, :, 1] = np.roll(tmp, -self.bist_wdir_indoff,
                                                  axis=1)
            if self.stereo:
                self.isv_im_lut[:, :, :, 2] = np.roll(tmp,
                                                      self.bist_wdir_indoff,
                                                      axis=1)

            self.dca_lut = np.zeros(lut_shp)
            self.dca_lut[:, :, :, 0] = self.fwdm.dcam[:, :, self.incm_ind,
                                                      :, :]
            tmp = self.fwdm.dcam[:, :, self.incm_ind, :, :]
            self.dca_lut[:, :, :, 1] = np.roll(tmp, -self.bist_wdir_indoff,
                                               axis=1)
            if self.stereo:
                self.dca_lut[:, :, :, 2] = np.roll(tmp, self.bist_wdir_indoff,
                                                   axis=1)

            self.luts_ready = True
        else:
            if self.stereo:
                lut_shp = self.fwdm.nrcsm[0, :, :, self.incm_ind, :, :].shape + (3,)
                d_c2_ind = self.fwdm.at_distance_c2_ind
            else:
                lut_shp = self.fwdm.nrcsm[0, :, :, self.incm_ind, :, :].shape + (2,)
                d_c2_ind = None

            self.nrcs_lut = add_dim_pol(lut_shp, self.fwdm.nrcsm,
                                        self.fwdm.monostatic_ind,
                                        self.incm_ind,
                                        self.fwdm.at_distance_c1_ind, d_c2_ind)
            self.isv_im_lut = np.zeros(lut_shp)
            self.isv_im_lut[:, :, :, 0] = self.fwdm.isv_im[:, :, self.incm_ind,
                                                           :, :]
            tmp = self.fwdm.isv_im[:, :, self.incb_ind, :, :]
            _bist = self.bist_wdir_indoff
            self.isv_im_lut[:, :, :, 1] = np.roll(tmp, -_bist, axis=1)
            if self.stereo:
                self.isv_im_lut[:, :, :, 2] = np.roll(tmp, _bist, axis=1)

            self.dca_lut = add_dim_pol(lut_shp, self.fwdm.dcam,
                                       self.fwdm.monostatic_ind, self.incm_ind,
                                       self.fwdm.at_distance_c1_ind, d_c2_ind)

            self.luts_ready = True

    def retrieval_2(self, nrcs_v: np.ndarray, imacs_v: np.ndarray, cut_off_v: np.ndarray,
                    sigma_nrcs_db: Optional[float] = 1,
                    sigma_imacs: Optional[float] = 0.05e-3,
                    sigma_dir0: Optional[float] = 1,
                    pol_ind: Optional[int] = 1,
                    dir0: Optional[np.ndarray] = None,
                    norm0: Optional[np.ndarray] = None,
                    sigma_norm0: Optional[float] = 7,
                    dir0_spr: Optional[float] = np.pi/2,
                    weight_nrcs: Optional[list] = (0.5, 1, 1),
                    weight_imacs: Optional[list] = (0.5, 1, 1),
                    window: Optional[str] = 'blackman',
                    debug: Optional[bool] = False):
        if self.cartesian:
            return self.__retr_l2_cart(nrcs_v, imacs_v, cut_off_v, sigma_nrcs_db,
                                       sigma_imacs, sigma_dir0, pol_ind, dir0,
                                       dir0_spr, window, debug,
                                       weight_nrcs=weight_nrcs,
                                       weight_imacs=weight_imacs,
                                       sigma_norm0=sigma_norm0, norm0=norm0)
        else:
            print("Polar not implemented!")
            return 0

    @staticmethod
    @njit
    def __ret_l2_cart_loop(nrcs_f: np.ndarray, imacs_f: np.ndarray,
                           cut_off_f: np.ndarray, sigma_nrcs_scl: float,
                           weight_nrcs: np.ndarray,
                           sigma_imacs: float, weight_imacs: np.ndarray,
                           pol_ind: int, inc_ind: int,
                           dir0_f: np.ndarray, dir0_spr: float,
                           sigma_dir0: float, norm0: np.ndarray,
                           sigma_norm0: float, nrcs_lut: np.ndarray,
                           dca_lut: np.ndarray, imacs_lut: np.ndarray,
                           cut_off_lut: np.ndarray, w_u_v: np.ndarray,
                           w_v_v: np.ndarray,
                           progress_bar: Optional[bool] = True,
                           debug: Optional[bool] = False
                           ) -> Tuple[np.ndarray, np.ndarray, np.ndarray,
                                      np.ndarray, np.ndarray, np.ndarray]:
        # TODO remove w_u_v
        """Estimate wind using brute force loop."""
        ww_u = np.zeros((nrcs_f.shape[0]), dtype=np.float64)
        ww_v = np.zeros((nrcs_f.shape[0]), dtype=np.float64)
        wdir = np.arctan2(w_v_v.reshape((w_v_v.size, 1)),
                          w_u_v.reshape((1, w_u_v.size,)))

        # output cost functions if debug is on
        if debug:
            j1amat = np.full((nrcs_f.shape[0], wdir.shape[0], wdir.shape[1]),
                             np.nan)
            j1bmat = np.full((nrcs_f.shape[0], wdir.shape[0], wdir.shape[1]),
                             np.nan)
            j1d0mat = np.full((nrcs_f.shape[0], wdir.shape[0], wdir.shape[1]),
                              np.nan)
        else:
            j1amat = np.full((nrcs_f.shape[0], 1, 1), np.nan)
            j1bmat = np.full((nrcs_f.shape[0], 1, 1), np.nan)
            j1d0mat = np.full((nrcs_f.shape[0], 1, 1), np.nan)

        fdca = np.zeros(nrcs_f.shape)
        nus = nrcs_lut.shape[3]
        # pg = progress_bar
        # for ind in tools.progress(0, nrcs_f.shape[0], step=1,
        #                           progress_bar=pg):

        # go through all pixels
        for ind in range(nrcs_f.shape[0]):

            # cost function for first-guess estimate
            if dir0_f is None:
                j1d0 = np.zeros((1, 1))
            elif norm0 is None:
                _angle = np.angle(np.exp(1j * (wdir - dir0_f[ind])))
                j1d0 = np.abs(_angle) > dir0_spr
                j1d0 = 1e4 / sigma_dir0**2 * j1d0  # .reshape((j1d0.size, 1))
            else:
                u0 = norm0[ind] * np.cos(dir0_f[ind])
                v0 = norm0[ind] * np.sin(dir0_f[ind])
                w_u_vf = w_u_v.reshape((1, w_u_v.size))
                w_v_vf = w_v_v.reshape((w_v_v.size, 1))
                j1d0 = (np.sqrt((w_u_vf - u0)**2 + (w_v_vf - v0)**2)
                        / sigma_norm0**2)

            # in the first guess we assume iwa=0.84 (fully developed) as nrcs has a weak dependence on wave age
            # we take therefore a cut-off index of 0 (cut-off at fully developed sea)
            cut_off_ind = 0

            # two-step retrieval
            it_max = 2
            v_temp = 10
            for it in range (0,it_max):
                cut_off_tv = cut_off_f[ind]

                # cost function for the NRCS
                nrcs_tv = nrcs_f[ind]
                var_nrcs = (sigma_nrcs_scl * nrcs_tv) ** 2
                _diff = (nrcs_lut[cut_off_ind, pol_ind, inc_ind[ind]] - nrcs_tv)**2
                j1a = np.sum(_diff * weight_nrcs**2 / var_nrcs, axis=-1)

                # cost function for the iMACS
                # in the first round we set the iMACS cost function to nearly zero, because iMACS needs a 'good' IWA
                imacs_tv = imacs_f[ind]
                var_imacs = sigma_imacs ** 2
                _diff = (imacs_lut[cut_off_ind, pol_ind, inc_ind[ind]] - imacs_tv) ** 2
                j1b = np.sum(_diff * weight_imacs ** 2 / var_imacs, axis=-1)
                if it == 0:
                    j1b = np.zeros(j1a.shape)
                else:
                    # FIXME: these settings are a bit arbitrary
                    if np.logical_and(np.mean(cut_off_tv) < 70,np.mean(cut_off_tv) > 0):
                        j1b = np.zeros(j1a.shape)

                # total cost function (NRCS + iMACS + first guess)
                j1 = j1a + j1b + j1d0
                indind = np.argmin(j1)
                u_ind = indind % nus
                v_ind = int(indind / nus)

                # find an updated estimate of the iwa from the cut-off and iterate one more time
                if it == 0:
                    v_temp = np.sqrt(w_u_v[u_ind] ** 2 + w_v_v[v_ind] ** 2)
                    j2 = np.sum((cut_off_lut[:, pol_ind, inc_ind[ind], v_ind, u_ind] - cut_off_tv) ** 2, axis=-1)
                    if np.mean(cut_off_tv) < 70:
                        j2=np.sum((cut_off_lut[:, pol_ind, inc_ind[ind], v_ind, u_ind] - np.ones(3)*70) ** 2, axis=-1)
                    cut_off_ind = np.argmin(j2)

                    # for whenever you do not want to use the cutoff (in par file set no_iwa=1)
                    if np.mean(cut_off_tv) == 0:
                        cut_off_ind = 0

            # get stress-equivalent wind speed
            # v_ind, u_ind = np.unravel_index(np.nanargmin(j1), j1.shape)
            ww_u[ind] = w_u_v[u_ind]
            ww_v[ind] = w_v_v[v_ind]

            # get wave-Doppler
            fdca[ind] = dca_lut[cut_off_ind, pol_ind, inc_ind[ind], v_ind, u_ind]

            # output cost functions if debug is on
            if debug:
                j1amat[ind, :, :] = j1a
                j1bmat[ind, :, :] = j1b
                j1d0mat[ind, :, :] = j1d0
            else:
                j1amat[ind, 0, 0] = np.nanmin(j1a)
                j1bmat[ind, 0, 0] = np.nanmin(j1b + j1b)
                j1d0mat[ind, 0, 0] = np.nanmin(j1a + j1b + j1d0)

        return ww_u, ww_v, fdca, j1amat, j1bmat, j1d0mat

    def __retr_l2_cart(self, nrcs_v: np.ndarray, imacs_v: np.ndarray, cut_off_v: np.ndarray, sigma_nrcs_db: float,
                       sigma_imacs: float, sigma_dir0: float, pol_ind: int,
                       dir0: np.ndarray, dir0_spr: float,
                       window: str, debug: bool,
                       weight_nrcs: Optional[list] = (1., 1., 1.),
                       weight_imacs: Optional[list] = (1., 1., 1.),
                       norm0: Optional[np.ndarray] = None,
                       sigma_norm0: Optional[float] = 7):
        """

        Parameters
        ----------
        nrcs_v
        imacs_v
        cut_off_v
        sigma_nrcs_db
        sigma_imacs
        sigma_dir0
        pol_ind
        dir0
        dir0_spr
        window
        debug
        weight_nrcs
        weight_imacs
        norm0
        sigma_norm0

        Returns
        -------

        """
        weight_nrcs = np.array(weight_nrcs)
        weight_imacs = np.array(weight_imacs)
        if not (self.check_obs_geo() and self.luts_ready):
            # print("Updating retrieval LUTs")
            self.prepare_luts()
        if dir0 is None:
            dir0d = None
        else:
            dir0d = np.radians(dir0)
        if nrcs_v.ndim > 1:
            # 'vectorize' inputs
            shp_in = nrcs_v.shape
            nrcs_f = nrcs_v.reshape((int(nrcs_v.size/nrcs_v.shape[-1]),
                                     nrcs_v.shape[-1]))
            cut_off_f = cut_off_v.reshape((int(nrcs_v.size / nrcs_v.shape[-1]),
                                     nrcs_v.shape[-1]))
            dir0_f = dir0d.reshape((int(nrcs_v.size/nrcs_v.shape[-1])))
            norm0_f = None
            if norm0 is not None:
                norm0_f = norm0.reshape((int(nrcs_v.size/nrcs_v.shape[-1])))
            imacs_f = imacs_v.reshape((int(imacs_v.size / imacs_v.shape[-1]),
                                       imacs_v.shape[-1]))
            sigma_nrcs_scl = (10**(sigma_nrcs_db/10) - 1)

            # take care of NaNs
            #w_u = np.zeros(nrcs_f.shape[0])
            #w_v = np.zeros(nrcs_f.shape[0])
            #wdir = np.arctan2(self.fwdm.w_v.reshape((self.fwdm.w_v.size, 1)),
            #                  self.fwdm.w_u.reshape((1, self.fwdm.w_u.size,)))
            n_lut = np.where(np.isnan(self.nrcs_lut), 1e3, self.nrcs_lut)
            d_lut = np.where(np.isnan(self.dca_lut), 1e3, self.dca_lut)
            i_lut = np.where(np.isnan(self.imacs_lut), 1e3, self.imacs_lut)
            c_lut = np.where(np.isnan(self.cut_off_lut), 1e3, self.cut_off_lut)
            inc_ind = self.incm_ind_lr + np.zeros_like(nrcs_v[..., 0]).astype(int)
            inc_ind = inc_ind.flatten()

            # retrieve wind vectors, wave-Dopplers and output cost functions
            _res = self.__ret_l2_cart_loop(nrcs_f, imacs_f, cut_off_f,
                                           sigma_nrcs_scl, weight_nrcs,
                                           sigma_imacs, weight_imacs,
                                           pol_ind, inc_ind, dir0_f, dir0_spr,
                                           sigma_dir0, norm0_f, sigma_norm0,
                                           n_lut, d_lut, i_lut, c_lut,
                                           self.fwdm.w_u, self.fwdm.w_v,
                                           debug=debug)
            w_u, w_v, fdca, j1a, j1b, j1d0 = _res

            # apply some filtering if you want
            fdca = fdca.reshape(shp_in)
            if fdca.ndim == 3:
                if window is not None:
                    for it in range(shp_in[-1]):
                        ws = int(np.floor(self.wave_doppler_corr_length
                                 / self.grid_spacing))
                        fdca[:, :, it] = drtls.smooth(fdca[:, :, it], ws,
                                                      window=window)
            return (w_u.reshape(shp_in[:-1]), w_v.reshape(shp_in[:-1]), j1a,
                    j1b, j1d0, fdca)

        else:
            print("Not implemented!")
            return 0

    def retrieval_1(self, nrcs_v: np.ndarray, imacs_v: np.ndarray,
                    fetch: float, sigma_nrcs_db: Optional[float] = 1,
                    sigma_imacs: Optional[float] = 0.05e-3,
                    sigma_dir0: Optional[float] = 1,
                    pol_ind: Optional[int] = 1,
                    dir0: Optional[np.ndarray] = None,
                    norm0: Optional[np.ndarray] = None,
                    sigma_norm0: Optional[float] = 7,
                    dir0_spr: Optional[float] = np.pi/2,
                    weight_nrcs: Optional[list] = (0.5, 1, 1),
                    weight_imacs: Optional[list] = (0.5, 1, 1),
                    window: Optional[str] = 'blackman',
                    debug: Optional[bool] = False):
        if self.cartesian:
            return self.__retr_l1_cart(nrcs_v, imacs_v, fetch, sigma_nrcs_db,
                                       sigma_imacs, sigma_dir0, pol_ind, dir0,
                                       dir0_spr, window, debug,
                                       weight_nrcs=weight_nrcs,
                                       weight_imacs=weight_imacs,
                                       sigma_norm0=sigma_norm0, norm0=norm0)
        else:
            return self.__retr_l1_polar(nrcs_v, imacs_v, sigma_nrcs_db,
                                        sigma_imacs, sigma_dir0, pol_ind, dir0,
                                        dir0_spr, window, debug)

    @staticmethod
    @njit
    def __ret_l1_cart_loop(nrcs_f: np.ndarray, imacs_f: np.ndarray,
                           fetch: float, sigma_nrcs_scl: float,
                           weight_nrcs: np.ndarray,
                           sigma_imacs: float, weight_imacs: np.ndarray,
                           pol_ind: int, inc_ind: int,
                           dir0_f: np.ndarray, dir0_spr: float,
                           sigma_dir0: float, norm0: np.ndarray,
                           sigma_norm0: float, nrcs_lut: np.ndarray,
                           dca_lut: np.ndarray, imacs_lut: np.ndarray,
                           iwa_lut: np.ndarray, w_u_v: np.ndarray,
                           w_v_v: np.ndarray,
                           progress_bar: Optional[bool] = True,
                           debug: Optional[bool] = False
                           ) -> Tuple[np.ndarray, np.ndarray, np.ndarray,
                                      np.ndarray, np.ndarray, np.ndarray]:
        # TODO remove w_u_v
        """Estimate wind using brute force loop."""
        ww_u = np.zeros((nrcs_f.shape[0]), dtype=np.float64)
        ww_v = np.zeros((nrcs_f.shape[0]), dtype=np.float64)
        wdir = np.arctan2(w_v_v.reshape((w_v_v.size, 1)),
                          w_u_v.reshape((1, w_u_v.size,)))
        if debug:
            j1amat = np.full((nrcs_f.shape[0], wdir.shape[0], wdir.shape[1]),
                             np.nan)
            j1bmat = np.full((nrcs_f.shape[0], wdir.shape[0], wdir.shape[1]),
                             np.nan)
            j1d0mat = np.full((nrcs_f.shape[0], wdir.shape[0], wdir.shape[1]),
                              np.nan)
        else:
            j1amat = np.full((nrcs_f.shape[0], 1, 1), np.nan)
            j1bmat = np.full((nrcs_f.shape[0], 1, 1), np.nan)
            j1d0mat = np.full((nrcs_f.shape[0], 1, 1), np.nan)

        fdca = np.zeros(nrcs_f.shape)
        nus = nrcs_lut.shape[3]
        # pg = progress_bar
        # for ind in tools.progress(0, nrcs_f.shape[0], step=1,
        #                           progress_bar=pg):
        for ind in range(nrcs_f.shape[0]):
            if dir0_f is None:
                j1d0 = np.zeros((1, 1))
            elif norm0 is None:
                iwa = np.min(iwa_lut)
                _angle = np.angle(np.exp(1j * (wdir - dir0_f[ind])))
                j1d0 = np.abs(_angle) > dir0_spr
                j1d0 = 1e4 / sigma_dir0**2 * j1d0  # .reshape((j1d0.size, 1))
            else:
                X = fetch * G / norm0[ind]**2
                iwa = 0.84 * np.tanh((X / X_0)**0.4)**(-0.75)
                u0 = norm0[ind] * np.cos(dir0_f[ind])
                v0 = norm0[ind] * np.sin(dir0_f[ind])
                w_u_vf = w_u_v.reshape((1, w_u_v.size))
                w_v_vf = w_v_v.reshape((w_v_v.size, 1))
                j1d0 = (np.sqrt((w_u_vf - u0)**2 + (w_v_vf - v0)**2)
                        / sigma_norm0**2)

            iwa_diff = np.abs(iwa_lut - iwa)
            iwa_ind = np.argmin(iwa_diff)
            nrcs_tv = nrcs_f[ind]
            imacs_tv = imacs_f[ind]
            var_nrcs = (sigma_nrcs_scl * nrcs_tv)**2
            var_imacs = sigma_imacs**2
            _diff = (nrcs_lut[iwa_ind, pol_ind, inc_ind[ind]] - nrcs_tv)**2
            j1a = np.sum(_diff * weight_nrcs**2 / var_nrcs, axis=-1)
            _diff = (imacs_lut[iwa_ind, pol_ind, inc_ind[ind]] - imacs_tv)**2
            j1b = np.sum(_diff * weight_imacs**2 / var_imacs, axis=-1)
            j1 = j1a + j1b + j1d0
            indind = np.argmin(j1)
            u_ind = indind % nus
            v_ind = int(indind / nus)
            # v_ind, u_ind = np.unravel_index(np.nanargmin(j1), j1.shape)
            ww_u[ind] = w_u_v[u_ind]
            ww_v[ind] = w_v_v[v_ind]
            fdca[ind] = dca_lut[iwa_ind, pol_ind, inc_ind[ind], v_ind, u_ind]
            if debug:
                j1amat[ind, :, :] = j1a
                j1bmat[ind, :, :] = j1b
                j1d0mat[ind, :, :] = j1d0
            else:
                j1amat[ind, 0, 0] = np.nanmin(j1a)
                j1bmat[ind, 0, 0] = np.nanmin(j1b + j1b)
                j1d0mat[ind, 0, 0] = np.nanmin(j1a + j1b + j1d0)
        return ww_u, ww_v, fdca, j1amat, j1bmat, j1d0mat

    def __retr_l1_cart(self, nrcs_v: np.ndarray, imacs_v: np.ndarray,
                       fetch: float, sigma_nrcs_db: float,
                       sigma_imacs: float, sigma_dir0: float, pol_ind: int,
                       dir0: np.ndarray, dir0_spr: float,
                       window: str, debug: bool,
                       weight_nrcs: Optional[list] = (1., 1., 1.),
                       weight_imacs: Optional[list] = (1., 1., 1.),
                       norm0: Optional[np.ndarray] = None,
                       sigma_norm0: Optional[float] = 7):
        """Estimate wind from NRCS.
        TODO: Number of return arrays should not vary in a function
        TODO: Pass dir0 in radians
        :param nrcs_v:
        :param imacs_v:
        :param dir0: force wind direction to be in half plane defined by dir0
        :return:
        """
        weight_nrcs = np.array(weight_nrcs)
        weight_imacs = np.array(weight_imacs)
        if not (self.check_obs_geo() and self.luts_ready):
            # print("Updating retrieval LUTs")
            self.prepare_luts()
        if dir0 is None:
            dir0d = None
        else:
            dir0d = np.radians(dir0)
        if nrcs_v.ndim > 1:
            shp_in = nrcs_v.shape
            nrcs_f = nrcs_v.reshape((int(nrcs_v.size/nrcs_v.shape[-1]),
                                     nrcs_v.shape[-1]))
            dir0_f = dir0d.reshape((int(nrcs_v.size/nrcs_v.shape[-1])))
            norm0_f = None
            if norm0 is not None:
                norm0_f = norm0.reshape((int(nrcs_v.size/nrcs_v.shape[-1])))
            imacs_f = imacs_v.reshape((int(imacs_v.size / imacs_v.shape[-1]),
                                       imacs_v.shape[-1]))
            sigma_nrcs_scl = (10**(sigma_nrcs_db/10) - 1)

            w_u = np.zeros(nrcs_f.shape[0])
            w_v = np.zeros(nrcs_f.shape[0])
            wdir = np.arctan2(self.fwdm.w_v.reshape((self.fwdm.w_v.size, 1)),
                              self.fwdm.w_u.reshape((1, self.fwdm.w_u.size,)))
            n_lut = np.where(np.isnan(self.nrcs_lut), 1e3, self.nrcs_lut)
            d_lut = np.where(np.isnan(self.dca_lut), 1e3, self.dca_lut)
            i_lut = np.where(np.isnan(self.imacs_lut), 1e3, self.imacs_lut)
            inc_ind = self.incm_ind_lr + np.zeros_like(nrcs_v[..., 0]).astype(int)
            inc_ind = inc_ind.flatten()
            _res = self.__ret_l1_cart_loop(nrcs_f, imacs_f, fetch,
                                           sigma_nrcs_scl, weight_nrcs,
                                           sigma_imacs, weight_imacs,
                                           pol_ind, inc_ind, dir0_f, dir0_spr,
                                           sigma_dir0, norm0_f, sigma_norm0,
                                           n_lut, d_lut, i_lut, self.waveage,
                                           self.fwdm.w_u, self.fwdm.w_v,
                                           debug=debug)
            w_u, w_v, fdca, j1a, j1b, j1d0 = _res
            fdca = fdca.reshape(shp_in)
            if fdca.ndim == 3:
                # it is an image
                # dca_fwd_f = np.zeros_like(fdca)
                # this is not really correct, we should estimate the wind,
                # filter it, and then estimate the
                # dca_fwd, as the wind to dca relation is not linear.
                # But this should be fine if
                # it doesn't vary too much around the local mean value
                if window is not None:
                    for it in range(shp_in[-1]):
                        ws = int(np.floor(self.wave_doppler_corr_length
                                 / self.grid_spacing))
                        fdca[:, :, it] = drtls.smooth(fdca[:, :, it], ws,
                                                      window=window)
            return (w_u.reshape(shp_in[:-1]), w_v.reshape(shp_in[:-1]), j1a,
                    j1b, j1d0, fdca)

        else:
            var_nrcs = ((10**(sigma_nrcs_db/10) - 1) * nrcs_v)**2
            j1a = np.sum((ret.nrcs_lut[pol_ind] - nrcs_v)**2 / var_nrcs,
                         axis=-1)
            # j1b = np.sum((ret.isv_im_lut[pol_ind] - isv_im_v)**2,
            #              axis=-1) / sigma_isv**2
            j1 = j1a + j1d0
            dirind, spdind = np.unravel_index(j1.argmin(), j1.shape)
            windv = (self.fwdm.wspeedv[spdind], self.fwdm.wdirv[dirind])
            fdca = self.dca_lut[pol_ind, dirind, spdind]
            if debug is True:
                return windv, self.dca_lut[pol_ind, dirind, spdind], j1a, j1b
            else:
                return windv[0], windv[1], fdca

    def __retr_l1_polar(self, nrcs_v, isv_im_v, sigma_nrcs_db, sigma_isv,
                        pol_ind, dir0, dir0_spr,
                        window, debug):
        """
        WARNING: this function has not been updated with the varying iwa and
        wind and is obsolete compared to the cartesian one
        :param nrcs_v:
        :param isv_im_v:
        :param dir0: force wind direction to be in half plane defined by dir0
        :return:
        """
        if not (self.check_obs_geo() and self.luts_ready):
            # print("Updating retrieval LUTs")
            self.prepare_luts()
        if dir0 is None:
            j1d0 = 0
        else:
            # TODO angle in degrees in the code?
            _angle = np.angle(np.exp(1j * np.radians(self.fwdm.wdirv - dir0)))
            j1d0 = np.abs(_angle) > dir0_spr
            j1d0 = 1e4 * j1d0.reshape((j1d0.size, 1))
        if nrcs_v.ndim > 1:
            shp_in = nrcs_v.shape
            nrcs_f = nrcs_v.reshape((int(nrcs_v.size/nrcs_v.shape[-1]),
                                     nrcs_v.shape[-1]))
            # isv_im_f = isv_im_v.reshape((int(nrcs_v.size / nrcs_v.shape[-1]),
            #                              nrcs_v.shape[-1]))
            sigma_nrcs_scl = (10**(sigma_nrcs_db/10) - 1)
            wdir = np.zeros(nrcs_f.shape[0])
            wspd = np.zeros(nrcs_f.shape[0])
            fdca = np.zeros(nrcs_f.shape)

            for ind in range(nrcs_f.shape[0]):
                nrcs_tv = nrcs_f[ind]
                # isv_im_tv = isv_im_f[ind]
                var_nrcs = (sigma_nrcs_scl * nrcs_tv)**2
                _diff_lut = (self.nrcs_lut[pol_ind] - nrcs_tv) ** 2
                j1a = np.sum(_diff_lut / var_nrcs, axis=-1)
                # j1b = np.sum(np.abs(self.isv_im_lut[pol_ind] - isv_im_tv)**2,
                #              axis=-1) / sigma_isv ** 2
                j1 = j1a + j1d0
                dirind, spdind = np.unravel_index(j1.argmin(), j1.shape)
                wdir[ind] = self.fwdm.wdirv[dirind]
                wspd[ind] = self.fwdm.wspeedv[spdind]
                fdca[ind] = self.dca_lut[pol_ind, dirind, spdind]
            fdca = fdca.reshape(shp_in)
            if fdca.ndim == 3:
                # it is an image
                # dca_fwd_f = np.zeros_like(fdca)
                # this is not really correct, we should estimate the wind,
                # filter it, and then estimate the
                # dca_fwd, as the wind to dca relation is not linear.
                # But this should be fine if
                # it doesn't vary too much around the local mean value
                if self.wave_doppler_corr_length > 0:
                    for it in range(shp_in[-1]):
                        ws = int(np.floor(self.wave_doppler_corr_length
                                          / self.grid_spacing))
                        fdca[:, :, it] = drtls.smooth(fdca[:, :, it], ws,
                                                      window=window)
            return wspd.reshape(shp_in[:-1]), wdir.reshape(shp_in[:-1]), fdca

        else:
            var_nrcs = ((10**(sigma_nrcs_db/10) - 1) * nrcs_v)**2
            j1a = np.sum(np.abs(ret.nrcs_lut[pol_ind] - nrcs_v)**2 / var_nrcs,
                         axis=-1)
            j1b = np.sum(np.abs(ret.isv_im_lut[pol_ind] - isv_im_v) ** 2,
                         axis=-1) / sigma_isv**2
            j1 = j1a + j1b + j1d0
            dirind, spdind = np.unravel_index(j1.argmin(), j1.shape)
            windv = (self.fwdm.wspeedv[spdind], self.fwdm.wdirv[dirind])
            fdca = self.dca_lut[pol_ind, dirind, spdind]
            if debug:
                return windv, self.dca_lut[pol_ind, dirind, spdind], j1a, j1b
            else:
                return windv[0], windv[1], fdca

    def tscv(self, dca_radar: np.ndarray, dca_fwd: np.ndarray,
             s1_weight: Optional[float] = 1,
             weighted: Optional[bool] = True,
             sigma_dca: Optional[float] = None,
             cov_geo: Optional[np.ndarray] = None
             ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """

        :param dca_radar: estimated geophysical Doppler
        :param dca_fwd: estimated wave-Doppler
        :return: a tuple with the estimated tscv, and the forward and inverse
                 matrices relating LoS Doppler with TSC
        """
        if weighted and not (sigma_dca is None):
            s1_weight = 1  # Weight is derived from sigma_dca
        else:
            weighted = False
        wl = cnst.c / self.f0
        inc_m_r_ = (self.obs_geo_a.inc_m)
        inc_b_a_r_ = (self.obs_geo_a.inc_b)
        inc_b_b_r_ = (self.obs_geo_b.inc_b)
        bist_ang_a_r_ = (self.obs_geo_a.bist_ang)
        bist_ang_b_r_ = (self.obs_geo_b.bist_ang)
        if type(inc_m_r_) is np.ndarray:
            inc_m_r = inc_m_r_
            inc_b_a_r = inc_b_a_r_
            bist_ang_a_r = bist_ang_a_r_
            inc_b_b_r = inc_b_b_r_
            bist_ang_b_r = bist_ang_b_r_
        else:
            inc_m_r = np.array(inc_m_r_)
            inc_b_a_r = np.array(inc_b_a_r_)
            bist_ang_a_r = np.array(bist_ang_a_r_)
            inc_b_b_r = np.array(inc_b_b_r_)
            bist_ang_b_r = np.array(bist_ang_b_r_)
            if dca_radar.ndim == 2:
                inc_m_r = inc_m_r.reshape((1, 1))
                inc_b_a_r = inc_b_a_r.reshape((1, 1))
                bist_ang_a_r = bist_ang_a_r.reshape((1, 1))
                inc_b_b_r = inc_b_b_r.reshape((1, 1))
                bist_ang_b_r = bist_ang_b_r.reshape((1, 1))
        if self.stereo:
            a = np.zeros(inc_m_r.shape + (3, 2))
            a[..., 2, 0] = - 1 / wl * (np.sin(inc_m_r) + np.sin(inc_b_b_r)
                                     * np.cos(bist_ang_b_r))
            a[..., 2, 1] = 1 / wl * np.sin(inc_b_b_r) * np.sin(bist_ang_b_r)
        else:
            a = np.zeros(inc_m_r.shape + (2, 2))

        # The product with  np.sqrt(s1_weight) is a hack,
        # we make the signal smaller
        # so that it weights less in the inversion
        a[..., 0, 0] = - 1 / wl * 2 * np.sin(inc_m_r) * np.sqrt(s1_weight)
        a[..., 0, 1] = 0
        a[..., 1, 0] = - 1 / wl * (np.sin(inc_m_r) + np.sin(inc_b_a_r)
                                 * np.cos(bist_ang_a_r))
        a[..., 1, 1] = 1 / wl * np.sin(inc_b_a_r) * np.sin(bist_ang_a_r)
        if weighted:
            if self.stereo:
                cov = np.zeros(dca_radar.shape + (3,))
            else:
                cov = np.zeros(dca_radar.shape + (2,))
            for i_s in range(cov.shape[-1]):
                # Here we
                cov[..., i_s, i_s] = (sigma_dca[..., i_s])**2
            if not (cov_geo is None):
                cov = cov + cov_geo
            W = np.linalg.inv(cov)
            # TODO out of the function ?

            def pseudo_weighted_inverse(A, W):

                AtW = np.einsum('...ji,...jk->...ik', A, W)
                AtWA = np.einsum('...ij,...jk->...ik', AtW, A)
                AtWA_inv = np.linalg.inv(AtWA)
                Awpseudoi = np.einsum('...ij,...jk->...ik', AtWA_inv, AtW)
                return Awpseudoi

            b = pseudo_weighted_inverse(a, W)
        else:
            # Pseudo inverse of a
            b = np.linalg.pinv(a)

        d_dca = dca_radar - dca_fwd
        # To complete the hack... we also make the observation
        # smaller. s1_weight is set to 1 if we are doing a proper
        # weighting...
        d_dca[..., 0] = d_dca[..., 0] * np.sqrt(s1_weight)
        if d_dca.ndim > 1:
            tscv = np.einsum("...ij,...j->...i", b, d_dca)
        else:
            tscv = np.einsum("ij,j->i", b, d_dca)
        return tscv, a, b

    def tscv2doppler(self):
        wl = cnst.c / self.f0
        inc_m_r = (self.obs_geo_a.inc_m)
        inc_b_r_a = (self.obs_geo_a.inc_b)
        bist_ang_r_a = (self.obs_geo_a.bist_ang)
        if self.stereo:
            inc_b_r_b = (self.obs_geo_b.inc_b)
            bist_ang_r_b = (self.obs_geo_b.bist_ang)
            a = np.zeros((3, 2))
            _col1 = np.sin(inc_m_r) + np.sin(inc_b_r_b) * np.cos(bist_ang_r_b)
            _col2 = np.sin(inc_b_r_b) * np.sin(bist_ang_r_b)
            a[2, :] = 1 / wl * np.array([_col1, _col2])
        else:
            a = np.zeros((2, 2))
        a[0, :] = 1 / wl * np.array([2 * np.sin(inc_m_r), 0])
        _col1 = np.sin(inc_m_r) + np.sin(inc_b_r_a) * np.cos(bist_ang_r_a)
        a[1, :] = 1 / wl * np.array([_col1,
                                     np.sin(inc_b_r_a) * np.sin(bist_ang_r_a)])
        return a


# %% End of class
if __name__ == '__main__':
    # %% Prepare....
    from stereoid.oceans import FwdModel, SceneGenerator
    datadir = "/Users/plopezdekker/Documents/WORK/STEREOID/DATA/ScatteringModels/Oceans"
    fname = "C_band_nrcs_dop_ocean_simulation.nc"
    fnameisv = "C_band_isv_ocean_simulation.nc"
    obsgeo = ObsGeo(35, 36, 40)
    # %% Forward model, this takes some time
    fwdm = FwdModel(datadir, os.path.join(datadir, fnameisv),
                    dspd=2, duvec=0.25)
    # fwdm = FwdModelMonostaticProxy(os.path.join(datadir, fname),
    #                               os.path.join(datadir, fnameisv), dspd=0.25)
    # %% Retrieval model
    ret = RetrievalModel(fwdm, obsgeo, cartesian=True)
    # %% Scene
    U = 8
    Udir = 0
    sgm = SceneGenerator(fwdm, (10, 10), wspd=U, wdir=Udir, cartesian=True)
    fwdm.inc_min
    fwdm.inc_step
    # %% Run scene generator
    sgm.wdir = 0
    fwdm.sigma_nrcs_db = 0.1
    snrcs, sdca = sgm.l1(obsgeo)
    snrcs[0, 2]
    # snrcs[0]
    # %% run retrieval
    w_u, w_v, dca_fwd = ret.retrieval_1(snrcs, 0, dir0=10)
    obsgeo.inc_m
    ret.incm_ind
    fwdm.incv[30]
    w_u[9, 3], w_v[9, 3]
    w_u.mean(), w_v.mean()
