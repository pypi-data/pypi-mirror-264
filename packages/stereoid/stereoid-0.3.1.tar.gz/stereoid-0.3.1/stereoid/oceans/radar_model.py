import os
import logging
from collections import namedtuple
from typing import Optional, Union, Tuple, TypeVar, Type

import numpy as np
import numpy.typing as npt
import scipy.interpolate as interp

import drama.utils as drtls
from drama.performance.sar import NESZdata
import drama.geo as geo
from drama.geo import QuickRadarGeometry
from drama.geo.derived_geo import BistaticRadarGeometry
from stereoid.oceans import ATIPerf, DCAPerf


__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"
# Define logger level for debug purposes
logger = logging.getLogger(__name__)
T = TypeVar("T")
ObsGeoAngles = namedtuple("ObsGeoAngles", ["inc_m", "inc_b", "bist_ang"])


class ObsGeo(object):
    def __init__(
        self,
        inc_m: float,
        inc_b: float,
        bist_ang: float,
        swth_geo: Optional[
            Union[geo.SingleSwathBistatic, BistaticRadarGeometry]
        ] = None,
        ascending: Optional[bool] = True,
        h_orb: Optional[float] = 693e3,
        degrees: Optional[bool] = False,
    ):
        """
        `ObsGeo` holds variables that relate to the observation geometry of a bistatic radar.

        It is typically initialised using a SingleSwath instance or a
        BistaticRadarGeometry instance. Altering the incidence angle of the
        observation geometry triggers recalculation and update of the bistatic
        angle and the incidence angle of the secondary radar.

        Parameters
        ----------
        inc_m: float
            Incident angle of the main satellite.
        inc_b: float
            Incident angle of the secondary satellite.
        bist_ang: float
            Bistatic angle between the two satellites.
        swth_geo: geo.SingleSwathBistatic or BistaticRadarGeometry (and subclasses)
            Object that describes the geometry of the swath (Default is None).
        ascending: boolean
            Whether the pass is ascending or descending (Default is True).
        h_orb: float
             Orbit height (Default value is 693e3 m).
        degrees: bool
            Sets whether the input arguments `inc_m`, `inc_b` and `bist_ang` are
            handled as angles in radians (default) or in degrees (Default value
            is False).
        """
        self.swth_geo = swth_geo
        self.ascending = ascending
        self.inc_b = inc_b
        self.bist_ang = bist_ang
        self._inc_m = inc_m
        self.h_orb = h_orb
        self.degrees = degrees

    def get_angles_at_index(self, key):
        # fields of ObsGeoAngles are: inc_m, inc_b, bist_ang
        angles = (self.inc_m, self.inc_b, self.bist_ang)
        indexed_angles = []
        for angle in angles:
            try:
                indexed_angles.append(angle[tuple(key)])
            except TypeError:  # object is not subscriptable
                indexed_angles.append(angle) # index only properties that are arrays
        return ObsGeoAngles(*indexed_angles)

    @classmethod
    def from_swath_geo(cls, inc_m, swath_geo, ascending=True, degrees=False):
        if degrees:
            inc_m_r = np.radians(inc_m)
            inc_b = np.degrees(swath_geo.inc2slave_inc(inc_m_r, ascending=ascending))
            bist_ang = np.degrees(
                swath_geo.inc2bistatic_angle_az(inc_m_r, ascending=ascending)
            )
        else:
            inc_m_r = inc_m
            inc_b = swath_geo.inc2slave_inc(inc_m_r, ascending=ascending)
            bist_ang = swath_geo.inc2bistatic_angle_az(inc_m_r, ascending=ascending)

        return cls(inc_m, inc_b, bist_ang, swath_geo, ascending, degrees=degrees)

    @classmethod
    def from_companion_polarizations(
        cls: Type[T],
        inc_m: Union[float, npt.ArrayLike],
        companion_pol: BistaticRadarGeometry,
        ascending: bool = True,
        degrees: bool = False,
    ) -> T:
        if degrees:
            inc_m_r = np.radians(inc_m)
            inc_b = np.degrees(
                companion_pol.inc2slave_inc(inc_m_r, ascending=ascending)
            )
            bist_ang = np.degrees(
                companion_pol.inc2bistatic_angle_az(inc_m_r, ascending)
            )
        else:
            inc_b = companion_pol.inc2slave_inc(inc_m, ascending=ascending)
            bist_ang = companion_pol.inc2bistatic_angle_az(inc_m, ascending)
        return cls(inc_m, inc_b, bist_ang, companion_pol, ascending, degrees=degrees)

    def radians(self, dd):
        """
        Checks if the class is instantiated with `degrees` set, potentially
        converts `dd` to radians and returns angle `dd`.
        The method only converts if we are working in degrees (`self.degrees` is
        set), in which case it is assumed that `dd` is passed in degrees.

        Parameters
        ----------
        dd : float or ndarray
            The angle that is to be converted to radians (could potentially
            already be in radians).

        Returns
        -------
        float or ndarray
            `dd` in radians.
        """
        if self.degrees:
            return np.radians(dd)
        else:
            return dd

    def opdegrees(self, dd):
        """
        Optionally converts `dd` to degrees, depending on whether `self.degrees`
        is set.

        Parameters
        ----------
        dd : float or ndarray
            The angle that is to be converted.

        Returns
        -------
        float or ndarray
            `dd` potentially converted to degrees.
        """
        if self.degrees:
            return np.degrees(dd)
        else:
            return dd

    @property
    def inc_m(self):
        return self._inc_m

    @inc_m.setter
    def inc_m(self, inc_m):
        self._inc_m = inc_m
        if self.swth_geo is not None:
            inc_m_r = self.radians(inc_m)
            self.inc_b = self.opdegrees(
                self.swth_geo.inc2slave_inc(inc_m_r, ascending=self.ascending)
            )
            self.bist_ang = self.opdegrees(
                self.swth_geo.inc2bistatic_angle_az(inc_m_r, ascending=self.ascending)
            )

    def set_swath(self, inc_near, gr_v):
        """
        Sets the observation geometry for a set of ground range points with
        respect to the swath's near-range incident angle.

        The method computes the array of incidence angles that is defined by
        `inc_near` and the ground range vector `gr_v` and sets `inc_m` to this
        array. Setting `inc_m` calls the property's setter which recomputes
        `inc_b` and `bist_ang` to match the new main incidence angle.

        Parameters
        ----------
        inc_near: float
            incident angle at begin of swath
        gr_v: ndarray
            matrix of ground ranges, with zero at `inc_near`
        """
        qgeo = QuickRadarGeometry(self.h_orb, degrees=self.degrees)
        gr0 = qgeo.inc_to_gr(inc_near)
        self.gr = gr_v + gr0
        inc = qgeo.gr_to_inc(self.gr)
        dinc = inc_near - qgeo.gr_to_inc(gr0)  # To fix numerical errors
        self.inc_m = inc + dinc


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
                np.radians(self.s1_nesz.inc_v),
                self.s1_nesz.nesz,
                bounds_error=False,
                fill_value=None,
            )
            self.inc2dual_nesz = interp.interp1d(
                np.radians(self.dual_nesz.inc_v),
                self.dual_nesz.nesz,
                bounds_error=False,
                fill_value=None,
            )
            self.inc2ati_nesz = interp.interp1d(
                np.radians(self.ati_nesz.inc_v),
                self.ati_nesz.nesz,
                bounds_error=False,
                fill_value=None,
            )
        else:
            self.inc2s1_nesz = interp.interp1d(
                self.s1_nesz.inc_v,
                self.s1_nesz.nesz,
                bounds_error=False,
                fill_value=None,
            )
            self.inc2dual_nesz = interp.interp1d(
                self.dual_nesz.inc_v,
                self.dual_nesz.nesz,
                bounds_error=False,
                fill_value=None,
            )
            self.inc2ati_nesz = interp.interp1d(
                self.ati_nesz.inc_v,
                self.ati_nesz.nesz,
                bounds_error=False,
                fill_value=None,
            )

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
        if (nrcs_v.shape[-1] == 2) and (nrcs_v.ndim == 4):
            # The nrcs has n_az x n_rg x n_sat x pol dimensions
            nshp = nrcs_v[..., 0, :].shape
        else:
            # Assume the nrcs has n_az x n_rg x s_sat dimensions
            nshp = nrcs_v[..., 0].shape
        shp = nrcs_v.shape
        n_sat = shp[2]
        dca_o = np.zeros_like(dca_v)

        if noise:
            t_inc_m_degrees = np.degrees(t_inc_m)
            if (nrcs_v.shape[-1] == 2) and (nrcs_v.ndim == 4):
                # Add a singleton dimension. When this is passed to
                # DCAPerf's sigma_dop it is fed to the NESZ 1D
                # interpolator. The interpolator respects the input
                # shape and returns an NESZ of shape n_az_lut x n_rg x
                # 1 but we select the middle of the aperture in
                # azimuth so it becomes n_rg x 1. Then, when the ratio
                # of NRCS to NESZ is used to find the SNR they
                # broadcast to n_az x n_rg x n_pol.
                t_inc_m_degrees = t_inc_m_degrees[..., np.newaxis]
            s_dop = self.s1_dca_perf.sigma_dop(t_inc_m_degrees, drtls.db(nrcs_v[:, :, 0]))
            dca_o[:, :, 0] = dca_v[:, :, 0] + s_dop * np.random.randn(*nshp)
            s_dop1 = self.ati_perf.sigma_dop(t_inc_m_degrees, drtls.db(nrcs_v[:, :, 1]), tau=tau_ati)
            s_dop2 = self.dca_perf.sigma_dop(t_inc_m_degrees, drtls.db(nrcs_v[:, :, 1]))
            if best:
                s_dop = np.stack([s_dop1, s_dop2]).min(axis=0)
            else:
                s_dop = s_dop1
            dca_o[:, :, 1] = dca_v[:, :, 1] + s_dop * np.random.randn(*nshp)
            if n_sat == 3:
                s_dop1 = self.ati_perf.sigma_dop(t_inc_m_degrees, drtls.db(nrcs_v[:, :, 2]), tau=tau_ati)
                s_dop2 = self.dca_perf.sigma_dop(t_inc_m_degrees, drtls.db(nrcs_v[:, :, 2]))
                if best:
                    s_dop = np.stack([s_dop1, s_dop2]).min(axis=0)
                else:
                    s_dop = s_dop1
                dca_o[:, :, 2] = dca_v[:, :, 2] + s_dop * np.random.randn(*nshp)
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

class SpectralNoiseModel(object):
    def __init__(
        self,
        obs_geo_bist,
        az_res=20,
        grg_res=5,
        degrees=False,
    ):
        """
        Parameters
        ----------
        obs_geo:
        az_res:
        grg_res:
        degrees:
        """
        self.obs_geo_bist = obs_geo_bist
        self.az_res = az_res
        self.grg_res = grg_res
        self.degrees = degrees

    # Goldfinger 1982
    # assumption is that neighbouring intensities are uncorrelated, which is not true
    def add_noise_Goldfinger(self, S, kx, ky, n ):
        """
        # S: SAR spectrum
        # kx,ky: across-track and along-track wave numbers
        # n: number of independent looks
        """

        # some values
        dkx = kx[ 0, 1 ] - kx[ 0, 0 ]
        dky = ky[ 1, 0 ] - ky[ 0, 0 ]
        A = 2 * np.pi / dkx * 2 * np.pi / dky  # surface area
        shp = S.shape

        # DC is removed, but would be by definition 1 * surface area
        I2 = 1 ** 2
        DC = I2 * A

        # first mean, then the biased spectrum
        S_bar = (np.sum( S ) + DC) / shp[ 0 ] / shp[ 1 ]
        Sc = S + S_bar / n

        # the uncertainty on the co-spectra (for I and Q of the cross-spectra use sqrt(2)*sigma_Sc)
        sigma_Sc = Sc / np.sqrt( n )

        return Sc, sigma_Sc

    # Correlated noise
    # assumption is that neighbouring intensities are uncorrelated, which is not true
    def add_noise_correlated(self, S, kx, ky, n, inc_m ):
        """
        # S: SAR spectrum
        # kx,ky: across-track and along-track wave numbers
        # n: number of independent looks
        # inc_m: radians
        """

        # some values
        dkx = kx[ 0, 1 ] - kx[ 0, 0 ]
        dky = ky[ 1, 0 ] - ky[ 0, 0 ]
        A = 2 * np.pi / dkx * 2 * np.pi / dky  # surface area
        shp = S.shape

        # DC is removed, but would be by definition 1 * surface area
        I2 = 1 ** 2
        DC = I2 * A / (2 * np.pi) ** 2

        # we add back DC to the spectrum
        S[ 0, 0 ] = DC

        # spectral mask
        bsgeo = self.obs_geo_bist
        specmask = bsgeo.spectral_mask(inc_m, self.az_res, drg=self.grg_res,
                                       baseband=False, ascending=True,
                                       Nx=shp[1], Ny=shp[0])

        # the pyramid should be convoluted with the spectrum S
        # FIXME: carefully check this normalization and the ifft vs fft order
        # in case of uncorrelated samples the pyramid becomes flat and has the value 1
        pyramid = np.real(np.fft.fft2(np.fft.ifft2(specmask["mask"])**2)) / shp[1] / shp[0]
        #from matplotlib import pyplot as plt
        #plt.imshow(np.fft.fftshift(pyramid))
        #plt.colorbar()
        #plt.show()

        # to scale it properly for uncorrelated samples, as in Goldfinger, we need again the division '/ shp[1] / shp[0]'
        # we have to take the convolution of the pyramid with the spectrum (can actually be done in one step)
        S_bar = np.fft.fft2(np.fft.ifft2(S)*np.fft.ifft2(pyramid)) / shp[ 0 ] / shp[ 1 ]
        Sc = S + S_bar / n
        Sc[0,0]=0

        # the uncertainty on the co-spectra (for I and Q of the cross-spectra use sqrt(2)*sigma_Sc)
        sigma_Sc = Sc / np.sqrt( n )

        return Sc, sigma_Sc

    # add system noise (as a constant)
    #FIXME: I do not think it works like this
    def add_noise_additive(self,sigma0,NESZ,S,n=25):
        """

        Parameters
        ----------
        sigma0: backscatter
        NESZ: noise equivalent sigma zero
        S: two-dimensional cross-spectrum

        Returns
        -------
        Sn: spectrum with additive noise
        """

        # normalized NESZ
        sigma_n=NESZ/(sigma0+NESZ)

        # add noise
        shp=S.shape
        S=S+sigma_n/np.sqrt(2)/n* (np.random.rand(shp[0],shp[1]) + 1j*np.real(S)+np.random.rand(shp[0],shp[1]))

        return S

# %%

if __name__ == "__main__":
    from stereoid.oceans import FwdModel
    import drama.geo as geo
    from drama.io import cfg
    import stereoid.utils.config as st_config
    from drama.geo.bistatic_pol import CompanionPolarizations

    paths = st_config.parse(section="Paths")

    # %% Prepare....
    datadir = "/Users/plopezdekker/Documents/WORK/STEREOID/DATA/Ocean"
    fname = "C_band_nrcs_dop_ocean_simulation.nc"
    fnameisv = "C_band_isv_ocean_simulation.nc"
    main_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
    pardir = paths["par"]
    parfile = os.path.join(pardir, "Hrmny_2021_1.cfg")
    conf = cfg.ConfigFile(parfile)
    along_track_separation = 350e3
    # swth_bst = geo.SingleSwathBistatic(par_file=parfile, dau=along_track_separation)
    swth_bst = CompanionPolarizations(
        par_file=parfile, companion_delay=along_track_separation / 7.4e3
    )
    #%%
    incm = np.radians(35)
    obsgeo = ObsGeo.from_companion_polarizations(incm, swth_bst, ascending=True)
    obsgeo.inc_m = np.array(np.radians([34, 35, 36]))  # .reshape((1,3))
    obsgeo.set_swath(incm, np.array([0, 10e3, 20e3]))  # .reshape((1,3)))
    obsgeo.degrees
    obsgeo.bist_ang
    np.degrees(obsgeo.inc_m)
    obsgeo.h_orb
    # %%
    inc_v = np.linspace(20, 50)
    la_v = geo.inc_to_look(np.radians(inc_v), 693e3)
    nesz = np.zeros_like(la_v).reshape((1, la_v.size)) - 26
    nesz = np.linspace(-23, -26, la_v.size).reshape((1, la_v.size))
    s1_nesz = NESZdata(la_v, inc_v, nesz, nesz, [0], conf, "IWS", 0)
    dual_nesz = NESZdata(la_v, inc_v, nesz + 3, nesz + 3, [0], conf, "IWS", 0)
    ati_nesz = NESZdata(la_v, inc_v, nesz + 6, nesz + 6, [0], conf, "IWS", 0)
    radar = RadarModel(
        obsgeo, sentinel_nesz=s1_nesz, dual_nesz=dual_nesz, ati_nesz=ati_nesz, b_ati=6
    )
    nrcs = np.array([[0.1, 0.1, 0.1], [0.01, 0.01, 0.05], [0.01, 0.01, 0.05]])
    print(radar.sigma_dop(nrcs) * 0.054 / 2)
    print(radar.sigma_nrcs(nrcs))
    radar.add_errors(nrcs, np.zeros_like(nrcs), 0)
