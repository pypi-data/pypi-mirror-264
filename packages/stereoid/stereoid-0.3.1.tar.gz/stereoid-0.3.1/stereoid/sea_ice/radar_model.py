__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

import os
import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
import scipy.interpolate as interp

import drama.utils as drtls
from drama.performance.sar import calc_aasr, calc_nesz, RASR, pattern, AASRdata, NESZdata, SARModeFromCfg
from stereoid.sea_ice import ATIPerf, DCAPerf
from typing import Optional, Union, Tuple, TypeVar, Type

class RadarModel(object):
    def __init__(
        self,
        obs_geo,
        sentinel_fls=None,
        dual_fls=None,
        ati_fls=None,
        sentinel_nesz=None,
        dual_nesz=None,
        ati_nesz=None,
        az_res=20,
        grg_res=5,
        b_ati=10,
        prod_res=2e3,
        dual_name="tud_2020_dual6m",
        ati_name="tud_2020_half",
        degrees=False,
    ):
        """
        Implements the STEREOID/Harmomy multistatic radar model.

        Parameters
        ----------
        obs_geo : ObsGeo
            Obseration geometry.
        sentinel_fls : dict or None, optional
            Dictionary of files with calculated Sentinel-1 performances.
        dual_fls : dict or None, optional
            Dictionary of files with calculated companion full antenna performances.
        ati_fls : dict or None, optional
            Dictionary of files with calculated companion ATI (single phase center) performances.
        sentinel_nesz : NESZdata or None, optional
            Supersedes NESZ in sentinel_fls.
        dual_nesz : NESZdata or None, optional.
            Supersedes NESZ in dual_fls.
        ati_nesz : NESZdata or None, optional
            Supersedes NESZ in ati_fls.
        az_res : float
            Azimuth resolution, (Defaults to 20 m (IWS)).
        grg_res : float
            Ground range resolution, (Defaults to 5 m).
        b_ati : float
            Along-track short baseline, (Defaults to 10 m).
        prod_res : float
            Product resolution, (Defaults to 2e3 m).
        dual_name : str
            name of dual antenna configuration in case dual_nesz is given.
        ati_name : str
            name of single antenna configuration in case ati_nesz is given.
        degrees : bool
            True if we want to input degrees (defaults to False).
        """
        self.obs_geo = obs_geo
        self.b_ati = b_ati
        self.degrees = degrees
        # if provided, read NESZs from corresponding files
        if isinstance(sentinel_fls, dict):
            self.s1_nesz = NESZdata.from_file(sentinel_fls["nesz"])
            self.txname = sentinel_fls["txname"]
        else:
            self.txname = "sentinel"

        if isinstance(dual_fls, dict):
            self.dual_nesz = NESZdata.from_file(dual_fls["nesz"])
            self.rx_dual_name = dual_fls["rxname"]
        else:
            self.rx_dual_name = dual_name

        if isinstance(ati_fls, dict):
            self.ati_nesz = NESZdata.from_file(ati_fls["nesz"])
            self.rx_ati_name = ati_fls["rxname"]
        else:
            self.rx_ati_name = ati_name
        # TODO read ambiguities, etc.

        # if provided use provided NESZ data
        if isinstance(sentinel_nesz, NESZdata):
            self.s1_nesz = sentinel_nesz

        if isinstance(dual_nesz, NESZdata):
            self.dual_nesz = dual_nesz

        if isinstance(ati_nesz, NESZdata):
            self.ati_nesz = ati_nesz
        if not self.degrees:
            self.inc2s1_nesz = interp.interp1d(
                np.radians(self.s1_nesz.inc_v), self.s1_nesz.nesz
            )
            self.inc2dual_nesz = interp.interp1d(
                np.radians(self.dual_nesz.inc_v), self.dual_nesz.nesz
            )
            self.inc2ati_nesz = interp.interp1d(
                np.radians(self.ati_nesz.inc_v), self.ati_nesz.nesz
            )
        else:
            self.inc2s1_nesz = interp.interp1d(self.s1_nesz.inc_v, self.s1_nesz.nesz)
            self.inc2dual_nesz = interp.interp1d(
                self.dual_nesz.inc_v, self.dual_nesz.nesz
            )
            self.inc2ati_nesz = interp.interp1d(self.ati_nesz.inc_v, self.ati_nesz.nesz)

        self.ati_perf = None
        self.dca_perf = None
        self.s1_dca_perf = None
        self.az_res = az_res
        self.grg_res = grg_res
        # Get ATI baseline

        # This calls some code...
        self.prod_res = prod_res

    @property
    def prod_res(self):
        return self.__prod_res

    @prod_res.setter
    def prod_res(self, prod_res):
        self.__prod_res = prod_res
        self.ati_perf = ATIPerf(
            self.ati_nesz,
            self.b_ati,
            prod_res=prod_res,
            az_res=self.az_res,
            grg_res=self.grg_res,
        )
        self.dca_perf = DCAPerf(
            self.dual_nesz,
            self.b_ati,
            prod_res,
            az_res=self.az_res,
            grg_res=self.grg_res,
            tx_name=self.txname,
            rx_name=self.rx_dual_name,
        )
        self.s1_dca_perf = DCAPerf(
            self.s1_nesz,
            self.b_ati,
            prod_res,
            az_res=self.az_res,
            grg_res=self.grg_res,
            tx_name=self.txname,
            rx_name=self.txname,
        )

    def add_errors(self, nrcs_v, dca_v, isv_im_v, noise=True, best=True):
        if self.obs_geo.degrees:
            t_inc_m = np.radians(self.obs_geo.inc_m)
        else:
            t_inc_m = self.obs_geo.inc_m
        # ati baseline
        try:
            atipar = self.obs_geo.swth_geo.bati2insarpar(t_inc_m, f0=5.4e9, ascending=self.obs_geo.ascending)
            tau_ati = self.b_ati * atipar["dtdb"]
        except:
            tau_ati = None
        if isinstance(nrcs_v, dict):
            return self.add_errors_dict(
                nrcs_v, dca_v, isv_im_v, t_inc_m, tau_ati, noise=noise, best=best
            )
        else:
            return self.add_errors_arr(
                nrcs_v, dca_v, isv_im_v, t_inc_m, tau_ati, noise=noise, best=best
            )

    def add_errors_arr(self, nrcs_v, dca_v, isv_im_v, t_inc_m, tau_ati, noise=True, best=True):
        """
        Add instrument errors to input data.
        """
        shp = nrcs_v.shape
        nshp = nrcs_v[..., 0].shape
        # dca_f = dca_v.reshape((int(dca_v.size / shp[-1]), shp[-1]))
        # nrcs_f = nrcs_v.reshape((int(dca_v.size / shp[-1]), shp[-1]))
        dca_o = np.zeros_like(dca_v)

        if noise:
            s_dop = self.s1_dca_perf.sigma_dop(np.degrees(t_inc_m), drtls.db(nrcs_v[..., 0]))
            dca_o[..., 0] = dca_v[..., 0] + s_dop * np.random.randn(*nshp)
            s_dop1 = self.ati_perf.sigma_dop(np.degrees(t_inc_m), drtls.db(nrcs_v[..., 1]), tau=tau_ati)
            s_dop2 = self.dca_perf.sigma_dop(np.degrees(t_inc_m), drtls.db(nrcs_v[..., 1]))
            if best:
                s_dop = np.stack([s_dop1, s_dop2]).min(axis=0)
            else:
                s_dop = s_dop1
            dca_o[..., 1] = dca_v[..., 1] + s_dop * np.random.randn(*nshp)
            if shp[-1] == 3:
                s_dop1 = self.ati_perf.sigma_dop(np.degrees(t_inc_m), drtls.db(nrcs_v[..., 2]), tau=tau_ati)
                s_dop2 = self.dca_perf.sigma_dop(np.degrees(t_inc_m), drtls.db(nrcs_v[..., 2]))
                if best:
                    s_dop = np.stack([s_dop1, s_dop2]).min(axis=0)
                else:
                    s_dop = s_dop1
                # print("Debug...")
                # print(s_dop.shape)
                dca_o[..., 2] = dca_v[..., 2] + s_dop * np.random.randn(*nshp)
            nrcs_o = nrcs_v + np.random.randn(*nrcs_v.shape) * self.sigma_nrcs(nrcs_v)
        else:
            nrcs_o = nrcs_v
        return nrcs_o, dca_o, isv_im_v

    def add_errors_dict(
        self,
        nrcs_v: dict,
        dca_v: dict,
        isv_im_v: dict,
        t_inc_m: np.ndarray,
        tau_ati: np.ndarray,
        noise: Optional[bool] = True,
        best: Optional[bool] = True,
    ) -> Tuple[dict, dict, dict]:
        """
        Add instrument errors to input data.
        """
        # listkey = list(nrcs_v.keys())
        # nshp = nrcs_v[listkey[0]].shape
        # dca_f = dca_v.reshape((int(dca_v.size / shp[-1]), shp[-1]))
        # nrcs_f = nrcs_v.reshape((int(dca_v.size / shp[-1]), shp[-1]))
        nrcsd_o = {}  # {"S1": {}, "HA": {}, "HB": {}}
        dopd_o = {}  # {"S1": {}, "HA": {}, "HB": {}}
        covd_o = (
            {}
        )  # {"S1": numpy.zeros(SHP, dtype=complex), "HA": numpy.zeros(SHP, dtype=complex), "HB": numpy.zeros(SHP, dtype=complex)}
        # for key in nrcsd.keys():
        #     if key == "S1":
        #         # Here for now I chose to use H/V for S1, but we could also just stay with I (=H) and O (=V)
        #         nrcsd[key] = {"H" : numpy.zeros(SHP), "V" : numpy.zeros(SHP)}
        #         dopd[key] = {"H" : numpy.zeros(SHP), "V" : numpy.zeros(SHP)}
        #     else:
        #         nrcsd[key] = {"I" : numpy.zeros(SHP), "O" : numpy.zeros(SHP)}
        #         dopd[key] = {"I" : numpy.zeros(SHP), "O" : numpy.zeros(SHP)}
        if noise:
            for satkey in nrcs_v.keys():
                dopd_o[satkey] = {}
                nrcsd_o[satkey] = {}
                if satkey == "S1":
                    for polkey in nrcs_v["S1"].keys():
                        nshp = nrcs_v[satkey][polkey].shape
                        s_dop = self.s1_dca_perf.sigma_dop(
                            np.degrees(t_inc_m), drtls.db(nrcs_v["S1"][polkey])
                        )
                        dopd_o["S1"][polkey] = dca_v["S1"][
                            polkey
                        ] + s_dop * np.random.randn(*nshp)
                        s_nrcs = self.sigma_nrcs_single(
                            nrcs_v["S1"][polkey], satkey, polkey
                        )
                        nrcsd_o["S1"][polkey] = nrcs_v["S1"][
                            polkey
                        ] + s_nrcs * np.random.randn(*nshp)
                else:
                    for polkey in nrcs_v[satkey].keys():
                        nshp = nrcs_v[satkey][polkey].shape
                        s_dop1 = self.ati_perf.sigma_dop(
                            np.degrees(t_inc_m), drtls.db(nrcs_v[satkey][polkey]), tau=tau_ati
                        )
                        s_dop2 = self.dca_perf.sigma_dop(
                            np.degrees(t_inc_m), drtls.db(nrcs_v[satkey][polkey])
                        )
                        if best:
                            s_dop = np.stack([s_dop1, s_dop2]).min(axis=0)
                        else:
                            s_dop = s_dop1
                        dopd_o[satkey][polkey] = dca_v[satkey][
                            polkey
                        ] + s_dop * np.random.randn(*nshp)
                        s_nrcs = self.sigma_nrcs_single(
                            nrcs_v[satkey][polkey], satkey, polkey
                        )
                        nrcsd_o[satkey][polkey] = nrcs_v[satkey][
                            polkey
                        ] + s_nrcs * np.random.randn(*nshp)
        else:
            nrcsd_o = nrcs_v
            dopd_o = dca_v
        return nrcsd_o, dopd_o, isv_im_v

    def sigma_nrcs(self, nrcs_v):
        """
        Compute SNR driven NRCS uncertainty.

        Parameters
        ----------
        nrcs_v : ndarray
            NRCS values, last dimension should have two or three elements,
            corresonding to the Sentinel-1 and one or two companions.

        Returns
        -------
        ndarray
            NRCS measurement uncertainties, with same dimensions as nrcs_v.
        """
        # if self.obs_geo.degrees:
        #     t_inc_m = self.obs_geo.inc_m
        # else:
        #     t_inc_m = np.degrees(self.obs_geo.inc_m)
        shp = nrcs_v.shape
        rshp = (int(nrcs_v.size / shp[-1]), shp[-1])
        cind = int(self.dual_nesz.nesz.shape[0] / 2)
        nesz_hrmny = 10 ** (self.inc2dual_nesz(self.obs_geo.inc_m)[cind] / 10)
        # incind = np.abs(self.dual_nesz.inc_v - self.obs_geo.inc_m).argmin()
        # nesz_hrmny = np.mean(10**(self.dual_nesz.nesz[:, incind] / 10))
        # nesz_S1 = np.mean(10**(self.s1_nesz.nesz[:, incind]/10))
        nesz_S1 = 10 ** (self.inc2s1_nesz(self.obs_geo.inc_m)[cind] / 10)
        if isinstance(nesz_hrmny, np.ndarray):
            if nrcs_v.shape[-1] == 2:
                neszs = np.stack((nesz_S1, nesz_hrmny), axis=-1)
            else:
                neszs = np.stack((nesz_S1, nesz_hrmny, nesz_hrmny), axis=-1)
            nrcs_ = nrcs_v
        else:
            nrcs_ = nrcs_v.reshape(rshp)
            neszs = np.zeros(nesz_S1.shape + (nrcs_v.shape[-1],))
            if nrcs_v.shape[-1] == 2:
                neszs = np.array([nesz_S1, nesz_hrmny]).reshape((1, 2))
            else:
                neszs = np.array([nesz_S1, nesz_hrmny, nesz_hrmny]).reshape((1, 3))
        snrs = nrcs_ / neszs
        n_looks = self.prod_res**2 / self.az_res / self.grg_res
        alpha_p = np.sqrt(1 / n_looks * ((1 + 1 / snrs) ** 2 + 1 / snrs**2))
        sigma_nrcs = alpha_p * nrcs_
        return sigma_nrcs.reshape(nrcs_v.shape)

    def sigma_nrcs_single(
        self, nrcs_v: np.ndarray, satkey: str, polkey: str
    ) -> np.ndarray:
        """Compute SNR driven NRCS uncertainty.

        Parameters
        ----------
        nrcs_v : ndarray
            NRCS values

        Returns
        -------
        ndarray
            NRCS measurement uncertainties, with same dimensions as nrcs_v.
        """
        shp = nrcs_v.shape

        cind = int(self.dual_nesz.nesz.shape[0] / 2)
        n_looks = self.prod_res**2 / self.az_res / self.grg_res
        if satkey == "S1":
            nesz = 10 ** (self.inc2s1_nesz(self.obs_geo.inc_m)[cind] / 10)
        else:
            nesz = 10 ** (self.inc2dual_nesz(self.obs_geo.inc_m)[cind] / 10)

        snrs = nrcs_v / nesz
        alpha_p = np.sqrt(1 / n_looks * ((1 + 1 / snrs) ** 2 + 1 / snrs**2))
        sigma_nrcs = alpha_p * nrcs_v  # .reshape(shp)
        return sigma_nrcs

    def sigma_dop(self, nrcs_v):
        """Compute SNR driven Doppler uncertaity.

        Parameters
        ----------
        nrcs_v : ndarray
            NRCS values, last dimension should have two or three elements,
            corresonding to the Sentinel-1 and one or two companions.

        Returns
        -------
        ndarray
            Doppler measurement uncertainties, with same dimensions as nrcs_v.

        """
        if isinstance(nrcs_v, dict):
            return self.sigma_dop_dict(nrcs_v)
        # Otherwise we run the rest of the np.ndarray based code
        if self.obs_geo.degrees:
            t_inc_m = self.obs_geo.inc_m
        else:
            t_inc_m = np.degrees(self.obs_geo.inc_m)
        try:
            atipar = self.obs_geo.swth_geo.bati2insarpar(np.radians(t_inc_m), f0=5.4e9, ascending=self.obs_geo.ascending)
            tau_ati = np.abs(self.b_ati * atipar["dtdb"])
        except:
            tau_ati = None
        shp = nrcs_v.shape
        rshp = (int(nrcs_v.size / shp[-1]), shp[-1])
        if len(shp) == 2:
            mshp = shp[0]
        else:
            mshp = (shp[0], shp[1])
        nrcs_f = nrcs_v.reshape(rshp)
        sigma_dca = np.zeros_like(nrcs_f)
        sigma_dca[:, 0] = self.s1_dca_perf.sigma_dop(
            t_inc_m, drtls.db(nrcs_f[:, 0]).reshape(mshp)
        ).flatten()
        sigma_dca[:, 1] = self.ati_perf.sigma_dop(
            t_inc_m, drtls.db(nrcs_f[:, 1]).reshape(mshp), tau=tau_ati
        ).flatten()
        if shp[-1] == 3:
            sigma_dca[:, 2] = self.ati_perf.sigma_dop(
                t_inc_m, drtls.db(nrcs_f[:, 2]).reshape(mshp), tau=tau_ati
            ).flatten()
        return sigma_dca.reshape(shp)

    def sigma_dop_dict(self, nrcs_v: dict) -> dict:
        """Compute SNR driven Doppler uncertaity.

        Parameters
        ----------
        nrcs_v : ndarray
            NRCS values, last dimension should have two or three elements,
            corresonding to the Sentinel-1 and one or two companions.

        Returns
        -------
        ndarray
            Doppler measurement uncertainties, with same dimensions as nrcs_v.

        """
        if self.obs_geo.degrees:
            t_inc_m = self.obs_geo.inc_m
        else:
            t_inc_m = np.degrees(self.obs_geo.inc_m)
        try:
            atipar = self.obs_geo.swth_geo.bati2insarpar(np.radians(t_inc_m), f0=5.4e9, ascending=self.obs_geo.ascending)
            tau_ati = np.abs(self.b_ati * atipar["dtdb"])
        except:
            tau_ati = None
        listkey = list(nrcs_v.keys())
        shp = nrcs_v[listkey[0]].shape
        rshp = nrcs_v[listkey[0]].size
        sigma_dca = {}
        for key in nrcs_v.keys():
            nrcs_f = nrcs_v[key].reshape(rshp)
            _ncrs = drtls.db(nrcs_f).reshape(shp)
            if "mono" in key:
                sigma_dca[key] = self.s1_dca_perf.sigma_dop(t_inc_m, _ncrs).flatten()

            else:
                sigma_dca[key] = self.ati_perf.sigma_dop(t_inc_m, _ncrs, tau=tau_ati).flatten()
            sigma_dca[key] = sigma_dca[key].reshape(shp)
        return sigma_dca