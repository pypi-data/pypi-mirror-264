import os

import numpy as np
from matplotlib import pyplot as plt
# from matplotlib import rc
# rc('text', usetex=False)

import drama.geo as sargeo
from drama.io import cfg
from drama.performance.sar import NESZdata
import stereoid.sar_performance as strsarperf
from stereoid.oceans import ObsGeo, FwdModel, RadarModel, RetrievalModel,FwdModelRIM
from drama.geo.derived_geo import BistaticRadarGeometry

# %%
class RetrievalPerformance(object):
    """Class to compute wind and TSC retirieval performance."""

    def __init__(self, maindir, run_id, parfile, fwd_model, d_at=350e3, prod_res=2e3, mode="IWS",
                 nesz_ati=None, nesz_full=None, nesz_s1=None, b_ati=6, inc_m=35,
                 rx_ati_name='tud_2020_tripple_ati', rx_dual_name='tud_2020_tripple',
                 fnameisv="C_band_isv_ocean_simulation.nc", min_max_speed=None,
                 ascending=True,
                 umag_err_max=1, udir_err_max=15, tscmag_err_max=0.5, tscdir_err_max=25):
        """Class initialization.

        Parameters
        ----------
        maindir: str
        run_id: str
        parfile: str
        fwd_model: instance of FwdModel of FwdModelRIM
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
        fnameisv: str
                  isv parameter file (not really used)
        """
        self.update = False
        self.ascending = ascending
        self.umag_err_max = umag_err_max
        self.udir_err_max = udir_err_max
        self.tscmag_err_max = tscmag_err_max
        self.tscdir_err_max = tscdir_err_max
        # FIXME: We assume I directory structure. I don't like this
        self.data_dir = os.path.join(maindir, "DATA/ScatteringModels/Oceans")
        self.parfile = parfile
        self.conf = cfg.ConfigFile(parfile)
        self.__d_at = d_at
        # self.swth_bst = sargeo.SingleSwathBistatic(par_file=parfile, dau=d_at)
        self.companion_delay = d_at/7.4e3
        self.cmpgeo_a = BistaticRadarGeometry(par_file=parfile, companion_delay = -self.companion_delay)
        self.cmpgeo_b = BistaticRadarGeometry(par_file=parfile, companion_delay = self.companion_delay)
        self.mode = mode
        self.rx_ati_name = rx_ati_name
        self.rx_dual_name = rx_dual_name
        self.__inc_v = np.linspace(20, 50)
        geo = sargeo.QuickRadarGeometry(693e3)
        self.__la_v = geo.inc_to_look(np.radians(self.__inc_v))
        if nesz_s1 is not None:
            nesz = np.zeros_like(self.__la_v).reshape((1, self.__la_v.size)) + nesz_s1
            self.s1_nesz = NESZdata(self.__la_v, self.__inc_v, nesz, nesz,
                                    [0], self.conf, self.mode, 0)
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
        self.u_mag = np.sqrt(self.u_v**2 + self.u_u**2)
        self.u_phi = np.arctan2(self.u_v, self.u_u)
        self.j_p2c = np.zeros(self.u_mag.shape + (2, 2))
        self.j_p2c[:, :, 0, 0] = np.cos(self.u_phi)
        self.j_p2c[:, :, 0, 1] = -1 * self.u_mag * np.sin(self.u_phi)
        self.j_p2c[:, :, 1, 0] = np.sin(self.u_phi)
        self.j_p2c[:, :, 1, 1] = self.u_mag * np.cos(self.u_phi)
        self.j_c2p = np.linalg.inv(self.j_p2c)
        self.fstr_dual = strsarperf.sarperf_files(maindir, rx_dual_name, mode=mode, runid=run_id, parpath=parfile)
        self.fstr_ati = strsarperf.sarperf_files(maindir, rx_ati_name, mode=mode, runid=run_id, parpath=parfile)
        self.fstr_s1 = strsarperf.sarperf_files(maindir, 'sentinel', is_bistatic=False,
                                                mode=mode, runid=run_id, parpath=parfile)
        self.calc()
        self.update = True

    def calc(self, umag_err_max=1, udir_err_max=15, tscmag_err_max=0.5, tscdir_err_max=25):
        """Calculate sensitivity histograms."""
        #self.umag_err_max = self.umag_err_max
        #self.udir_err_max = self.udir_err_max
        #self.tscmag_err_max = self.tscmag_err_max
        radarm = RadarModel(self.obsgeo_a,
                            self.fstr_s1, self.fstr_dual, self.fstr_ati,
                            sentinel_nesz=self.s1_nesz,
                            dual_nesz=self.full_nesz,
                            ati_nesz=self.ati_nesz, b_ati=self.b_ati,
                            prod_res=self.prod_res)
        if not (self.fwdm.fwdm_type == "RIM"):
            self.fwdm.at_distance = self.__d_at
        self.fwdm.inc = self.inc_m
        jac_n, jac_d = self.fwdm.fwd_jacobian(self.inc_m)
        j = jac_n[:, 1]   # n_sat x 2-D space x n_wind_v x n_wind_u matrix
        # JˆH \cdot J
        # we also transpose while we are at it
        jhj = np.einsum("jimn,jkmn->mnik", j, j)
        # Now pseudo inverse
        jhi_i = np.linalg.inv(jhj)
        j_pi = np.einsum("mnik,jkmn->mnij", jhi_i, j)
        incind = np.abs(radarm.dual_nesz.inc_v - self.inc_m).argmin()
        nesz_hrmny = np.mean(10**(radarm.dual_nesz.nesz[:, incind] / 10))
        nesz_S1 = np.mean(10**(radarm.s1_nesz.nesz[:, incind]/10))
        snrs = (np.transpose(self.fwdm.nrcs_lut(1, cart=True), [1, 2, 0])
                / np.array([nesz_S1, nesz_hrmny, nesz_hrmny]).reshape((1, 1, 3)))
        n_looks = self.prod_res**2 / self.az_res / 5
        alpha_p = np.sqrt(1/n_looks * ((1+1 / snrs)**2 + 1 / snrs**2))
        cov_s = np.zeros((j.shape[2], j.shape[3], j.shape[0], j.shape[0]))
        for ind in range(3):
            cov_s[:, :, ind, ind] = alpha_p[:, :, ind]**2 * self.fwdm.nrcs_lut(1, cart=True)[ind]**2
        cov_w = np.einsum("mnik,mnkj,mnlj->mnil", j_pi, cov_s, j_pi)
        alpha_a = (self.obsgeo_a.bist_ang/2)
        cov_g = np.zeros((j.shape[2], j.shape[3], j.shape[0], j.shape[0]))
        k_g = 0.06 * np.exp(-self.u_mag/12)
        for ind in range(3):
            cov_g[:, :, ind, ind] = self.fwdm.nrcs_lut(0, cart=True)[ind]**2
        cov_g[:, :, 0, 1] = (self.fwdm.nrcs_lut(0, cart=True)[0]
                             * self.fwdm.nrcs_lut(0, cart=True)[1] * np.cos(alpha_a))
        cov_g[:, :, 1, 0] = cov_g[:, :, 0, 1]
        cov_g[:, :, 0, 2] = (self.fwdm.nrcs_lut(0, cart=True)[0]
                             * self.fwdm.nrcs_lut(0, cart=True)[2] * np.cos(alpha_a))
        cov_g[:, :, 2, 0] = cov_g[:, :, 0, 2]
        cov_g[:, :, 1, 2] = (self.fwdm.nrcs_lut(0, cart=True)[1]
                             * self.fwdm.nrcs_lut(0, cart=True)[2] * np.cos(2*alpha_a))
        cov_g[:, :, 2, 1] = cov_g[:, :, 1, 2]
        cov_g = k_g.reshape(self.u_mag.shape + (1, 1))**2 * cov_g
        cov_wg = np.einsum("mnik,mnkj,mnlj->mnil", j_pi, cov_g, j_pi)
        self.cov_wind_mg = cov_w + cov_wg

        cov_w_pol = np.einsum("mnik,mnkj,mnlj->mnil", self.j_c2p, cov_w, self.j_c2p)

        self.umag_err_hist = self.sigma_to_pdf(np.sqrt(cov_w_pol[:, :, 0, 0]), self.umag_err_max)
        self.udir_err_hist = self.sigma_to_pdf(np.degrees(np.sqrt(cov_w_pol[:, :, 1, 1])), self.udir_err_max)
        # Doppler and TSC
        # Wave Doppler
        j_wd = jac_d[:, 1, :, :, :]
        # covariance matrix of wave Doppler
        cov_wd = np.einsum("ikmn,mnkj,ljmn->mnil", j_wd, cov_w, j_wd)
        # Measurement errors
        nrcs = np.transpose(self.fwdm.nrcs_lut(1, cart=True),[1, 2, 0])
        sigma_dop = np.transpose(radarm.sigma_dop(nrcs), [2, 0, 1])
        # covariance matrix
        cov_md = np.zeros_like(cov_wd)
        for ind in range(3):
            cov_md[:, :, ind, ind] = sigma_dop[ind]**2
        # Large scale uncertainty
        cov_d = cov_wd + cov_md
        W = np.linalg.inv(cov_d)
        ret = RetrievalModel(self.fwdm, self.obsgeo_a, self.obsgeo_b, cartesian=True)
        A = ret.tscv2doppler()
        A_wpsi = self.__pseudo_weighted_inverse(A, W)
        cov_tsc = np.einsum("mnik,mnkj,mnlj->mnil", A_wpsi, cov_d, A_wpsi)
        self.t_u_err_hist = self.sigma_to_pdf(np.sqrt(cov_tsc[:, :, 0, 0]),
                                              self.tscmag_err_max)
        self.t_v_err_hist = self.sigma_to_pdf(np.sqrt(cov_tsc[:, :, 1, 1]),
                                              self.tscmag_err_max)
        # Relative uncertainty
        cov_d = cov_md
        W = np.linalg.inv(cov_d)
        A_wpsi = self.__pseudo_weighted_inverse(A, W)
        cov_rtsc = np.einsum("mnik,mnkj,mnlj->mnil", A_wpsi, cov_d, A_wpsi)
        self.rt_u_err_hist = self.sigma_to_pdf(np.sqrt(cov_rtsc[:, :, 0, 0]),
                                               self.tscmag_err_max)
        self.rt_v_err_hist = self.sigma_to_pdf(np.sqrt(cov_rtsc[:, :, 1, 1]),
                                               self.tscmag_err_max)


    def wind_pdf(self, p1=10, p2=2.2):
        un = self.u_mag
        f_v = p2/p1 * (un / p1)**(p2-1) * np.exp(-(un/p1)**p2)
        return f_v / (2*np.pi) / un

    def sigma_to_pdf(self, sigma, vmax, nbins=100):
        pdf_w = self.wind_pdf()
        bins = np.linspace(0, vmax, nbins + 1)
        index = ~np.isnan(sigma)
        hist, bins = np.histogram(sigma[index], density=True,
                                  weights=pdf_w[index],
                                  bins=bins)
        bins = (bins[1:] + bins[0:-1]) / 2
        dbin = bins[1] - bins[0]
        return bins, np.cumsum(hist) * dbin


    @property
    def fwd_model(self):
        """Get the current model type descriptor"""
        return self._fwd_model

    @fwd_model.setter
    def fwd_model(self, fwdmodel):
        self._fwd_model = fwdmodel.fwdm_type
        # self.fwdm = FwdModel(self.data_dir, os.path.join(self.data_dir, self.fnameisv),
        #                      dspd=2, duvec=0.25, model=self._fwd_model, min_max_speed=self.u_mag_min_max)
        self.fwdm = fwdmodel
        self.u_u = self.fwdm.w_u.reshape((1, self.fwdm.w_u.size))
        self.u_v = self.fwdm.w_v.reshape((self.fwdm.w_v.size, 1))
        if self.update:
            self.calc()

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
        if self.update:
            self.calc()

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
        if self.update:
            self.calc()

    @property
    def inc_m(self):
        return self.__inc_m

    @inc_m.setter
    def inc_m(self, incm):
        self.__inc_m = incm
        #self.obsgeo = ObsGeo.from_swath_geo(incm, self.swth_bst, ascending=True)
        self.obsgeo_a = ObsGeo.from_companion_polarizations(np.radians(incm), self.cmpgeo_a, ascending=self.ascending)
        self.obsgeo_b = ObsGeo.from_companion_polarizations(np.radians(incm), self.cmpgeo_b, ascending=self.ascending)
        if self.update:
            self.calc()

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode
        az_res_dct = {"WM":5, "IWS":20}
        self.az_res = az_res_dct[mode]
        if self.update:
            self.calc()

    def __pseudo_weighted_inverse(self, A, W):
        """ Returns weithed pseudo inverse matrix for a set of weights."""
        AtW = np.einsum('ji,mnjk->mnik', A, W)
        AtWA = np.einsum('mnij,jk->mnik', AtW, A)
        AtWA_inv = np.linalg.inv(AtWA)
        Awpseudoi = np.einsum('mnij,mnjk->mnik', AtWA_inv, AtW)
        return Awpseudoi


def performance_vs_inc(retr_perf, ninc=20):
    """Compute performace vs incident angle.

    Parameters
    ----------
    retr_perf : RetrievalPerformance
        The retrieval performance instance for whcih to compute the performance as a function of the incidence angle.

    ninc: int
        number of angles of incidence.

    Returns
    -------
    a tuple with histograms of standard deviation of errors of wind magnitude,
    wind direction, the cross-track and along-tack component of the TSC, and
    the cross-track and along-tack component of the relative TSC
    """
    modecfg = getattr(retr_perf.conf, retr_perf.mode)
    incv = np.linspace(np.ceil(modecfg.inc_near[0]), np.floor(modecfg.inc_far[-1]), ninc)
    umag_hists = np.zeros((ninc, 100))
    udir_hists = np.zeros_like(umag_hists)
    tsc_u_hists = np.zeros_like(umag_hists)
    tsc_v_hists = np.zeros_like(umag_hists)
    rtsc_u_hists = np.zeros_like(umag_hists)
    rtsc_v_hists = np.zeros_like(umag_hists)
    for incind in range(ninc):
        #print(incv[incind])
        retr_perf.inc_m = incv[incind]
        umag_hists[incind] = retr_perf.umag_err_hist[1]
        udir_hists[incind] = retr_perf.udir_err_hist[1]
        tsc_u_hists[incind] = retr_perf.t_u_err_hist[1]
        tsc_v_hists[incind] = retr_perf.t_v_err_hist[1]
        rtsc_u_hists[incind] = retr_perf.rt_u_err_hist[1]
        rtsc_v_hists[incind] = retr_perf.rt_v_err_hist[1]

    return incv, umag_hists, udir_hists, tsc_u_hists, tsc_v_hists, rtsc_u_hists, rtsc_v_hists


#%% End of class
if __name__ == '__main__':
    import stereoid.utils.config as st_config
    import xarray as xr
    paths = st_config.parse(section="Paths")
    main_dir = paths["main"]
    datadirr = paths["data"]
    pardir = paths["par"]
    datadir = datadirr / 'ScatteringModels/Oceans'
    #fname = "C_band_nrcs_dop_ocean_simulation.nc"
    #fnameisv = "C_band_isv_ocean_simulation.nc"
    plotdir = os.path.join(main_dir,'RESULTS/OceanE2E/Analytic')
    os.makedirs(plotdir, exist_ok=True)
    modelstr = 'SSAlin'
    parfile = os.path.join(pardir, "Hrmny_2021_1.cfg")
    run_id = "2021_1"
    prod_res = 2e3
    along_track_separation_km = 350
    rimdir = '/Users/plopezdekker/Documents/WORK/STEREOID/DATA/ScatteringModels/Oceans/RIM'
    dopdir = '/Users/plopezdekker/Documents/WORK/STEREOID/DATA/ScatteringModels/Oceans/RIM'
    rimnrcs = {350:'nrcs_lut_20220409_dau350km_.nc', 450: 'nrcs_lut_20220425_dau450km_.nc'}
    rimdop = {350:'dop_lut_20220409_dau350km_.nc', 450: 'dop_lut_20220425_dau450km_.nc'}
    nrcsdata = xr.open_dataset(os.path.join(rimdir, rimnrcs[along_track_separation_km]))
    dopdata = xr.open_dataset(os.path.join(rimdir,rimdop[along_track_separation_km]))
    fwdm = FwdModelRIM(nrcsdata, dopdata, None, dspd=2, duvec=0.25, model=modelstr)
    fwdm.inc
#%%
    ret_perf = RetrievalPerformance(main_dir, run_id, parfile, fwdm,
                                    d_at=along_track_separation_km*1e3,
                                    prod_res=1e3, b_ati=10)

#%%
    ret_perf.umag_err_max = 0.5
    ret_perf.udir_err_max = 5
    ret_perf.tscmag_err_max = 0.25
    ret_perf.inc_m = 35
    plt.figure()
    plt.plot(ret_perf.umag_err_hist[0], ret_perf.umag_err_hist[1])
    plt.grid(True)
    plt.figure()
    plt.plot(ret_perf.udir_err_hist[0], ret_perf.udir_err_hist[1])
    plt.grid(True)
    plt.figure()
    plt.plot(ret_perf.rt_u_err_hist[0], ret_perf.rt_u_err_hist[1])
    plt.plot(ret_perf.rt_v_err_hist[0], ret_perf.rt_v_err_hist[1])
    plt.grid(True)
    ret_perf.prod_res
    #ret_perf.rt_u_err_hist
#%%
    (incv,
     umag_hists, udir_hists,
     tsc_u_hists, tsc_v_hists,
     rtsc_u_hists, rtsc_v_hists) = performance_vs_inc(ret_perf, ninc=20)

#%%
    plt.figure()
    # plt.imshow(np.transpose(umag_hists), extent=[incv[0], incv[-1], 0, ret_perf.umag_err_max],
    #            origin='lower', aspect='auto')
    plt.contourf(incv, np.linspace(0, ret_perf.umag_err_max, 100), np.transpose(umag_hists),
                 levels=10, cmap='viridis', vmin=0, vmax=1, extend='max')
    plt.xlabel('Incident angle [deg]')
    plt.ylabel("$\sigma_{|U|} [m/s]$")
    plt.title("CDF($\sigma_{|U|}$)")
    plt.colorbar()
    plt.figure()
    # plt.imshow(np.transpose(umag_hists), extent=[incv[0], incv[-1], 0, ret_perf.umag_err_max],
    #            origin='lower', aspect='auto')
    plt.contourf(incv, np.linspace(0, ret_perf.udir_err_max, 100), np.transpose(udir_hists),
                 levels=10, vmin=0, vmax=1, extend='max')
    plt.xlabel('Incident angle [deg]')
    plt.ylabel(r"$\sigma_{\angle U} [deg]$")
    plt.title(r"CDF($\sigma_{\angle U}$)")
    plt.colorbar()

    # Relative TSC
    plt.figure()
    # plt.imshow(np.transpose(umag_hists), extent=[incv[0], incv[-1], 0, ret_perf.umag_err_max],
    #            origin='lower', aspect='auto')
    plt.contourf(incv, np.linspace(0, ret_perf.tscmag_err_max, 100), np.transpose(tsc_u_hists),
                 levels=10, cmap='viridis', vmin=0, vmax=1, extend='max')
    plt.xlabel('Incident angle [deg]')
    plt.ylabel("$\sigma_{TSC_u} [m/s]$")
    plt.title("CDF($\sigma_{TSC_u}$)")
    plt.colorbar()
    plt.figure()
    # plt.imshow(np.transpose(umag_hists), extent=[incv[0], incv[-1], 0, ret_perf.umag_err_max],
    #            origin='lower', aspect='auto')
    plt.contourf(incv, np.linspace(0, ret_perf.tscmag_err_max, 100), np.transpose(tsc_v_hists),
                 levels=10, vmin=0, vmax=1, extend='max')
    plt.xlabel('Incident angle [deg]')
    plt.ylabel("$\sigma_{TSC_v} [m/s]$")
    plt.title("CDF($\sigma_{TSC_v}$)")
    plt.colorbar()
    # tsc_v_hists[:,-5]
