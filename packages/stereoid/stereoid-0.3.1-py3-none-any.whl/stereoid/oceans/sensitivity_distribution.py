import os

import numpy as np

import drama.geo as sargeo
from drama.io import cfg
from drama.performance.sar import NESZdata
import stereoid.sar_performance as strsarperf
from stereoid.oceans import ObsGeo, FwdModel, RadarModel, RetrievalModel


class SensitivityDistribution:
    """Class to computer wind and TSC retirieval performance."""

    def __init__(
        self,
        maindir,
        run_id,
        parfile,
        d_at=350e3,
        prod_res=2e3,
        mode="IWS",
        nesz_ati=None,
        nesz_full=None,
        nesz_s1=None,
        b_ati=6,
        inc_m=35,
        rx_ati_name="tud_2020_half",
        rx_dual_name="tud_2020_dual6m",
        fwd_model="SSAlin",
        fnameisv="C_band_isv_ocean_simulation.nc",
        min_max_speed=None,
        pol_ind=1,
    ):
        """Class initialization.

        Parameters
        ----------
        maindir: str
        run_id: str
        parfile: str
        rx_ati_name: str
                     name of ATI rx configuration section in parfile
        rx_ati_name: str
                     name of full antenna rx configuration section in parfile
        d_at: float
              along-track separation between S-1 and companions. Default value is 350e3 m
        prod_res: float
                  L2 product resolution
        b_ati: float
               short along-track baseline
        inc_m: float
               indicent angle (deg)
        mode: str
              operating mode, either IWS or WM
        fwd_model: str
                   forward model ('SSAlin' or "KAlin")
        fnameisv: str
                  isv parameter file (not really used)
        """
        # FIXME: We assume I directory structure. I don't like this
        self.data_dir = os.path.join(maindir, "DATA/ScatteringModels/Oceans")
        self.parfile = parfile
        self.conf = cfg.ConfigFile(parfile)
        self.__d_at = d_at
        self.swth_bst = sargeo.SingleSwathBistatic(par_file=parfile, dau=d_at)
        self.mode = mode
        self.rx_ati_name = rx_ati_name
        self.rx_dual_name = rx_dual_name
        self.__inc_v = np.linspace(20, 50)
        geo = sargeo.QuickRadarGeometry(693e3)
        self.__la_v = geo.inc_to_look(np.radians(self.__inc_v))
        if nesz_s1 is not None:
            nesz = np.zeros_like(self.__la_v).reshape((1, self.__la_v.size)) + nesz_s1
            self.s1_nesz = NESZdata(
                self.__la_v, self.__inc_v, nesz, nesz, [0], self.conf, self.mode, 0
            )
        else:
            self.s1_nesz = None
        self.nesz_ati = nesz_ati
        self.nesz_full = nesz_full
        self.b_ati = b_ati
        self.inc_m = inc_m
        self.fnameisv = fnameisv
        self.u_mag_min_max = min_max_speed
        self.fwd_model = fwd_model
        self.prod_res = prod_res
        self.u_mag = np.sqrt(self.u_v ** 2 + self.u_u ** 2)
        self.u_phi = np.arctan2(self.u_v, self.u_u)
        self.fstr_dual = strsarperf.sarperf_files(
            maindir, rx_dual_name, mode=mode, runid=run_id
        )
        self.fstr_ati = strsarperf.sarperf_files(
            maindir, rx_ati_name, mode=mode, runid=run_id
        )
        self.fstr_s1 = strsarperf.sarperf_files(
            maindir, "sentinel", is_bistatic=False, mode=mode, runid=run_id
        )
        self.pol_ind = pol_ind

    def cov_wind(self):
        """Calculate the wind covariance matrix"""
        radarm = RadarModel(
            self.obsgeo,
            self.fstr_s1,
            self.fstr_dual,
            self.fstr_ati,
            sentinel_nesz=self.s1_nesz,
            dual_nesz=self.full_nesz,
            ati_nesz=self.ati_nesz,
            b_ati=self.b_ati,
            prod_res=self.prod_res,
        )
        jac_n, jac_d = self.fwdm.fwd_jacobian(self.inc_m)
        j = jac_n[:, pol_ind]  # n_sat x 2-D space x n_wind_v x n_wind_u matrix
        # JˆH \cdot J
        # we also transpose while we are at it
        jhj = np.einsum("jimn,jkmn->mnik", j, j)
        # Now pseudo inverse
        jhi_i = np.linalg.inv(jhj)
        j_pi = np.einsum("mnik,jkmn->mnij", jhi_i, j)
        incind = np.abs(radarm.dual_nesz.inc_v - self.inc_m).argmin()
        nesz_hrmny = np.mean(10 ** (radarm.dual_nesz.nesz[:, incind] / 10))
        nesz_S1 = np.mean(10 ** (radarm.s1_nesz.nesz[:, incind] / 10))
        snrs = np.transpose(
            self.fwdm.nrcs_lut(pol_ind, cart=True), [1, 2, 0]
        ) / np.array([nesz_S1, nesz_hrmny, nesz_hrmny]).reshape((1, 1, 3))
        n_looks = self.prod_res ** 2 / self.az_res / 5
        alpha_p = np.sqrt(1 / n_looks * ((1 + 1 / snrs) ** 2 + 1 / snrs ** 2))
        cov_s = np.zeros((j.shape[2], j.shape[3], j.shape[0], j.shape[0]))
        for ind in range(3):
            cov_s[:, :, ind, ind] = (
                alpha_p[:, :, ind] ** 2
                * self.fwdm.nrcs_lut(pol_ind, cart=True)[ind] ** 2
            )
        cov_w = np.einsum("mnik,mnkj,mnlj->mnil", j_pi, cov_s, j_pi)
        alpha_a = np.radians(self.obsgeo.bist_ang / 2)
        cov_g = np.zeros((j.shape[2], j.shape[3], j.shape[0], j.shape[0]))
        k_g = 0.06 * np.exp(-self.u_mag / 12)
        for ind in range(3):
            cov_g[:, :, ind, ind] = self.fwdm.nrcs_lut(pol_ind, cart=True)[ind] ** 2
        cov_g[:, :, 0, 1] = (
            self.fwdm.nrcs_lut(pol_ind, cart=True)[0]
            * self.fwdm.nrcs_lut(pol_ind, cart=True)[1]
            * np.cos(alpha_a)
        )
        cov_g[:, :, 1, 0] = cov_g[:, :, 0, 1]
        cov_g[:, :, 0, 2] = (
            self.fwdm.nrcs_lut(pol_ind, cart=True)[0]
            * self.fwdm.nrcs_lut(pol_ind, cart=True)[2]
            * np.cos(alpha_a)
        )
        cov_g[:, :, 2, 0] = cov_g[:, :, 0, 2]
        cov_g[:, :, 1, 2] = (
            self.fwdm.nrcs_lut(pol_ind, cart=True)[1]
            * self.fwdm.nrcs_lut(pol_ind, cart=True)[2]
            * np.cos(2 * alpha_a)
        )
        cov_g[:, :, 2, 1] = cov_g[:, :, 1, 2]
        cov_g = k_g.reshape(self.u_mag.shape + (1, 1)) ** 2 * cov_g
        cov_wg = np.einsum("mnik,mnkj,mnlj->mnil", j_pi, cov_g, j_pi)
        return cov_w + cov_wg

    def cov_wind_polar(self):
        cov_wind_mg = self.cov_wind()
        j_p2c = np.zeros(self.u_mag.shape + (2, 2))
        j_p2c[:, :, 0, 0] = np.cos(self.u_phi)
        j_p2c[:, :, 0, 1] = -1 * self.u_mag * np.sin(self.u_phi)
        j_p2c[:, :, 1, 0] = np.sin(self.u_phi)
        j_p2c[:, :, 1, 1] = self.u_mag * np.cos(self.u_phi)
        j_c2p = np.linalg.inv(j_p2c)
        return np.einsum("mnik,mnkj,mnlj->mnil", self.j_c2p, cov_wind_mg, self.j_c2p)

    @property
    def fwd_model(self):
        """Get the current model type descriptor"""
        return self._fwd_model

    @fwd_model.setter
    def fwd_model(self, model):
        self._fwd_model = model
        self.fwdm = FwdModel(
            self.data_dir,
            os.path.join(self.data_dir, self.fnameisv),
            dspd=0.5,
            duvec=0.5,
            model=self._fwd_model,
            min_max_speed=self.u_mag_min_max,
            at_distance=self._d_at,
        )
        self.u_u = self.fwdm.w_u.reshape((1, self.fwdm.w_u.size))
        self.u_v = self.fwdm.w_v.reshape((self.fwdm.w_v.size, 1))

    @property
    def nesz_ati(self):
        return self.__nesz_ati

    @nesz_ati.setter
    def nesz_ati(self, nesz):
        self.__nesz_ati = nesz
        if nesz is None:
            self.ati_nesz = None
        else:
            nesz = np.zeros_like(self.__la_v).reshape((1, self.__la_v.size)) + nesz
            self.ati_nesz = NESZdata(self.__la_v, self.__inc_v, nesz, nesz,
                                     [0], self.conf, self.mode, 0)

    @property
    def nesz_full(self):
        return self.__nesz_full

    @nesz_full.setter
    def nesz_full(self, nesz):
        self.__nesz_full = nesz
        if nesz is None:
            self.full_nesz = None
        else:
            nesz = np.zeros_like(self.__la_v).reshape((1, self.__la_v.size)) + nesz
            self.full_nesz = NESZdata(self.__la_v, self.__inc_v, nesz, nesz,
                                      [0], self.conf, self.mode, 0)

    @property
    def inc_m(self):
        return self.__inc_m

    @inc_m.setter
    def inc_m(self, incm):
        self.__inc_m = incm
        self.obsgeo = ObsGeo.from_swath_geo(incm, self.swth_bst, ascending=True)

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode
        az_res_dct = {"WM":5, "IWS":20}
        self.az_res = az_res_dct[mode]
