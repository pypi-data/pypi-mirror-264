__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

import os
import numpy as np
#from collections import namedtuple
from matplotlib import pyplot as plt
import drama.utils as drtls
from drama import constants as cnst
from stereoid.oceans import ObsGeo


class SceneGenerator(object):
    def __init__(self, fwdm, shp, wspd=6, wdir=45, tsc=0,
                 grid_spacing=1e3, wave_doppler_corr_length=20e3, cartesian=True):
        """

        :param fwdm:
        :param shp:
        :param wspd:
        :param wdir:
        :param tsc:
        :param grid_spacing: resolution of generated scene
        :param wave_doppler_corr_length: spatial filtering applied to wind to obtain wave-Doppler
        """
        self.shp = shp
        self.fwdm = fwdm
        self.__wdir = 0
        self.wspd = wspd
        self.wdir = wdir
        self.tsc = 0
        self.f0 = 5.4e9
        self.grid_spacing = grid_spacing
        self.wave_doppler_corr_length = wave_doppler_corr_length
        self.cart = cartesian

    @property
    def wdir(self):
        return self.__wdir

    @wdir.setter
    def wdir(self, wdir):
        self.__wdir = np.zeros(self.shp) + wdir
        self.w_x = self.wspd * np.cos(np.radians(self.wdir))
        self.w_y = self.wspd * np.sin(np.radians(self.wdir))

    @property
    def wspd(self):
        return self.__wspd

    @wspd.setter
    def wspd(self, wspd):
        self.__wspd = np.zeros(self.shp) + wspd
        self.w_x = self.wspd * np.cos(np.radians(self.wdir))
        self.w_y = self.wspd * np.sin(np.radians(self.wdir))

    @property
    def tsc(self):
        return self.__tsc

    @tsc.setter
    def tsc(self, tsc):
        self.__tsc = np.zeros(self.shp + (2,)) + tsc

    def __correlate_geonoise(self, gns, obs_geo, model='cosine'):
        if model == 'cosine':
            shp = gns.shape
            coh = np.cos(np.radians(obs_geo.bist_ang/2))
            # gns = gns.reshape((int(gns.size/shp[-1]), shp[-1]))
            gns[..., 1] = coh * gns[..., 0] + np.sqrt(1-coh**2) * gns[..., 1]
            if shp[-1] == 3:
                gns[..., 2] = coh * gns[..., 0] + np.sqrt(1 - coh ** 2) * gns[..., 2]
            return gns  #.reshape(shp)
        else:
            # default, no correlation
            return gns

    def geonoise_cohmatrix(self, obs_geo, model='cosine'):
        """ Returns de  coherency matrix for the geophysical Noise
        Parameters
        ----------
        obs_geo: ObsGeo
        model: string
            'cosine' for a cosine-dependent correlation (high correlation).
            Any other value will produce the identity matrix
        """
        coh = np.cos((obs_geo.bist_ang/2))
        cohm = np.zeros(coh.shape + (3, 3))
        for i_s in range(3):
            cohm[..., i_s, i_s] = 1
        if model == 'cosine':
            cohm[..., 0, 1] = coh
            cohm[..., 1, 2] = coh**2
            cohm[..., 1, 0] = coh
            cohm[..., 2, 1] = coh**2
            cohm[..., 0, 2] = coh
            cohm[..., 2, 0] = coh
        return cohm

    def l1_polar(self, obs_geo, obs_geo_b, correlation_model='cosine', pol=1):
        if obs_geo.degrees:
            inc_m_d = obs_geo.inc_m
        else:
            inc_m_d = np.degrees(obs_geo.inc_m)
        tnrcs, tdca, tisv = self.fwdm.fwd(pol, self.w_x, self.w_y,
                                          inc_m_d, obs_geo.inc_b, obs_geo.bist_ang)
        nsmp = tnrcs.size
        shp = tnrcs.shape
        # Now filter wind and recompute tdca
        if len(shp) == 2:
            wspd_x = drtls.smooth(self.w_x,
                                  int(np.floor(self.wave_doppler_corr_length/self.grid_spacing)),
                                  window='blackman')
            wspd_y = drtls.smooth(self.w_y,
                                  int(np.floor(self.wave_doppler_corr_length / self.grid_spacing)),
                                  window='blackman')
            wspd_f = np.sqrt(wspd_x**2 + wspd_y**2)
            wdir_f = np.degrees(np.arctan2(wspd_y, wspd_x))
            # Here we assume that both tdca and tisv are linked to filtered wind
            aux, tdca, tisv = self.fwdm.fwd(pol, wspd_f, wdir_f,
                                            inc_m_d, obs_geo.inc_b, obs_geo.bist_ang)
        # Add tsc Doppler
        inc_m_r = np.radians(obs_geo.inc_m)
        inc_b_r = np.radians(obs_geo.inc_b)
        bist_ang_r = np.radians(obs_geo.bist_ang)
        wl = cnst.c / self.f0
        if self.fwdm.stereo:
            # FIXME this assumes fixed geometry, will have to be fixed
            a = np.zeros((3, 2))
            a[2, :] = 1 / wl * np.array([np.sin(inc_m_r) +
                                         np.sin(inc_b_r) * np.cos(bist_ang_r),
                                         -np.sin(inc_b_r) * np.sin(bist_ang_r)])
        else:
            a = np.zeros((2, 2))
        a[0, :] = 1 / wl * np.array([2 * np.sin(inc_m_r), 0])
        a[1, :] = 1 / wl * np.array([np.sin(inc_m_r) +
                                     np.sin(inc_b_r) * np.cos(bist_ang_r),
                                     np.sin(inc_b_r) * np.sin(bist_ang_r)])
        if len(self.shp) == 2:
            tsc_dop = np.einsum('ij,mnj->mni', a, self.tsc)
        elif len(self.shp) == 1:
            tsc_dop = np.einsum('ij,mj->mi', a, self.tsc)
        else:
            tsc_dop = 0

        errm = (10**(self.fwdm.sigma_nrcs_db/10) - 1) * (np.random.rand(nsmp) - 0.5) / np.sqrt(2 * 0.5**3 / 3)
        delta_nrcs = self.__correlate_geonoise(tnrcs * errm.reshape(shp), obs_geo, correlation_model)
        delta_isv = self.__correlate_geonoise(np.random.randn(nsmp).reshape(shp) * self.fwdm.sigma_isv, obs_geo, correlation_model)
        delta_dca = self.__correlate_geonoise(np.random.randn(nsmp).reshape(shp) * self.fwdm.sigma_dca, obs_geo, correlation_model)
        return tnrcs + delta_nrcs, tsc_dop + tdca + delta_dca, tisv + delta_isv

    def l1_cart(self, obs_geo_a, obs_geo_b, correlation_model='cosine', pol=1):
        if obs_geo_a.degrees:
            inc_m_d = obs_geo_a.inc_m
        else:
            inc_m_d = np.degrees(obs_geo_a.inc_m)
        tnrcs = self.fwdm.fwd_crt(pol, self.w_x, self.w_y,
                                  inc_m_d, obs_geo_a.inc_b, obs_geo_a.bist_ang, what='nrcs')

        nsmp = tnrcs.size
        shp = tnrcs.shape
        # Set low values to zero
        if len(shp) == 3:
            # lows = np.where(self.w_x**2 + self.w_y**2 <= self.fwdm.wspd_min)
            mask = ((self.w_x**2 + self.w_y**2) <= ((self.fwdm.wspd_min + 0.1)**2))
            for ind in range(shp[2]):
                tnrcs[:, :, ind] = np.where(mask,
                                            0, tnrcs[:, :, ind])
        # Now filter wind and recompute tdca
        if len(shp) == 3:
            wspd_x = drtls.smooth(self.w_x,
                                  int(np.floor(self.wave_doppler_corr_length/self.grid_spacing))) #,
                                  # window='blackman')
            wspd_y = drtls.smooth(self.w_y,
                                  int(np.floor(self.wave_doppler_corr_length / self.grid_spacing))) # ,
                                  # window='blackman')
            # Here we assume that both tdca and tisv are linked to filtered wind
            tdca = self.fwdm.fwd_crt(pol, wspd_x, wspd_y,
                                     inc_m_d, obs_geo_a.inc_b, obs_geo_a.bist_ang, what='dca')
            imacs = self.fwdm.fwd_crt(pol, wspd_x, wspd_y,
                                     inc_m_d, obs_geo_a.inc_b, obs_geo_a.bist_ang, what='imacs')
            cutoff = self.fwdm.fwd_crt(pol, wspd_x, wspd_y,
                                       inc_m_d, obs_geo_a.inc_b, obs_geo_a.bist_ang, what='cut_off')
        else:
            tdca = self.fwdm.fwd_crt(pol, self.w_x, self.w_y,
                                     inc_m_d, obs_geo_a.inc_b, obs_geo_a.bist_ang, what='dca')
            imacs = self.fwdm.fwd_crt(pol, self.w_x, self.w_y,
                                     inc_m_d, obs_geo_a.inc_b, obs_geo_a.bist_ang, what='imacs')
            cutoff = self.fwdm.fwd_crt(pol, self.w_x, self.w_y,
                                     inc_m_d, obs_geo_a.inc_b, obs_geo_a.bist_ang, what='cut_off')
        if len(shp) == 3:
            mask = ((wspd_x**2 + wspd_y**2) <= ((self.fwdm.wspd_min + 0.1)**2))
            for ind in range(shp[2]):
                tdca[:, :, ind] = np.where(mask, 0, tdca[:, :, ind])
                imacs[:, :, ind] = np.where(mask, 0, imacs[:, :, ind])
                cutoff[:, :, ind] = np.where(mask, 0, cutoff[:, :, ind])
        # Add tsc Doppler
        inc_m_r = obs_geo_a.inc_m
        inc_b_a_r = obs_geo_a.inc_b
        inc_b_b_r = obs_geo_b.inc_b
        bist_ang_a_r = obs_geo_a.bist_ang
        bist_ang_b_r = obs_geo_b.bist_ang

        wl = cnst.c / self.f0
        nsat = 3 if self.fwdm.stereo else 2
        if type(inc_m_r) == np.ndarray:
            a = np.zeros(inc_m_r.shape + (nsat, 2))
            a[..., 0, 0] = 2 / wl * np.sin(inc_m_r)
            a[..., 1, 0] = 1 / wl * (np.sin(inc_m_r) + np.sin(inc_b_a_r) * np.cos(bist_ang_a_r))
            a[..., 1, 1] = 1 / wl * np.sin(inc_b_a_r) * np.sin(bist_ang_a_r)
            if self.fwdm.stereo:
                a[..., 2, 0] = 1 / wl * (np.sin(inc_m_r) + np.sin(inc_b_b_r) * np.cos(bist_ang_b_r))
                a[..., 2, 1] = 1 / wl * np.sin(inc_b_b_r) * np.sin(bist_ang_b_r)
        else:
            a = np.zeros((nsat, 2))
            if self.fwdm.stereo:
                a[2, :] = 1 / wl * np.array([np.sin(inc_m_r) +
                                             np.sin(inc_b_b_r) * np.cos(bist_ang_b_r),
                                             -np.sin(inc_b_b_r) * np.sin(bist_ang_b_r)])
            a[0, :] = 1 / wl * np.array([2 * np.sin(inc_m_r), 0])
            a[1, :] = 1 / wl * np.array([np.sin(inc_m_r) +
                                         np.sin(inc_b_a_r) * np.cos(bist_ang_a_r),
                                         np.sin(inc_b_a_r) * np.sin(bist_ang_a_r)])
        tsc_dop = np.einsum('...ij,...j->...i', a, self.tsc)
        # if len(self.shp) == 2:
        #     tsc_dop = np.einsum('ij,mnj->mni', a, self.tsc)
        # elif len(self.shp) == 1:
        #     tsc_dop = np.einsum('ij,mj->mi', a, self.tsc)
        # else:
        #     tsc_dop = 0

        errm = (10**(self.fwdm.sigma_nrcs_db/10) - 1) * (np.random.rand(nsmp) - 0.5) / np.sqrt(2 * 0.5**3 / 3)
        delta_nrcs = self.__correlate_geonoise(tnrcs * errm.reshape(shp), obs_geo_a, correlation_model)
        delta_isv = self.__correlate_geonoise(np.random.randn(nsmp).reshape(shp) * self.fwdm.sigma_isv, obs_geo_a, correlation_model)
        delta_dca = self.__correlate_geonoise(np.random.randn(nsmp).reshape(shp) * self.fwdm.sigma_dca, obs_geo_a, correlation_model)
        return tnrcs + delta_nrcs, tsc_dop + tdca + delta_dca, imacs, cutoff  # , tisv + delta_isv

    def l1(self, obs_geo_a, obs_geo_b, correlation_model='cosine', pol=1):
        if self.cart:
            return self.l1_cart(obs_geo_a, obs_geo_b, correlation_model, pol=pol)
        else:
            return self.l1_polar(obs_geo_a, obs_geo_b, correlation_model, pol=pol)


if __name__ == '__main__':
    # %% Prepare....
    from stereoid.oceans import FwdModel, RetrievalModel, FwdModelMonostaticProxy
    datadir = '/Users/plopezdekker/Documents/WORK/STEREOID/DATA/Ocean'
    fname = "C_band_nrcs_dop_ocean_simulation.nc"
    fnameisv = "C_band_isv_ocean_simulation.nc"
    obsgeo = ObsGeo(35, 36, 40)
    # %% Forward model, this takes some time
    fwdm = FwdModel(datadir, os.path.join(datadir, fnameisv), dspd=2, duvec=0.5)
    # fwdm = FwdModelMonostaticProxy(os.path.join(datadir, fname), os.path.join(datadir, fnameisv), dspd=0.25)
    # %% Scene
    U = 8
    Udir = 90
    sgm = SceneGenerator(fwdm, (10, 10), wspd=U, wdir=Udir, cartesian=True)
    fwdm.inc_min
    fwdm.inc_step
    # %% Run scene generator
    snrcs, sdca = sgm.l1(obsgeo)
    snrcs.shape
