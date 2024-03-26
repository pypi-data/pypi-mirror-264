__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

import numpy as np
import scipy.interpolate as interp
from matplotlib import pyplot as plt
import matplotlib
import drama.performance.doppler_centroid as doppler_centroid
import stereoid.oceans.cmod5n as cmod5
import drama.constants as cnst
# import drama.geo.geometry as sargeo
from drama.orbits import orbit_to_vel
import os
import drama.performance.insar as insar
from drama.performance import sar as sar


class ATIPerf(object):
    def __init__(self, nesz_data, b_ati, prod_res=2e3,
                 f0=5.4e9, sys_coh=0.99, az_res=20, grg_res=5,
                 tau_ati=None):
        """

        :param nesz_data: NESZData object
        :param b_ati: physical along-track baseline
        :param prod_res: product resolution
        :param f0: radar frequency
        :param sys_coh: maximum coherence
        """
        self.nesz_data = nesz_data
        self.b_ati = b_ati
        self.prod_res = prod_res
        self.f0 = f0
        self.sys_coh = sys_coh
        # TODO: here go to radians, nesz_data is in degree!
        self.inc2nesz = interp.interp1d(nesz_data.inc_v, nesz_data.nesz)
        self.naz = nesz_data.nesz.shape[0]
        self.caz = int(self.naz/2)
        self.az_res = az_res
        self.grg_res = grg_res
        if tau_ati is None:
            self.tau = self.b_ati / 2 / orbit_to_vel(self.nesz_data.conf.orbit.Horb)
        else:
            self.tau = tau_ati

    def sigma_phase(self, inc_0_in, sigma_0_in, coh_t=1, az=None):
        inc_0 = np.array(inc_0_in)
        if inc_0.ndim == 0:
            inc_0 = inc_0.reshape((1,))
        sigma_0 = np.array(sigma_0_in)
        if sigma_0.ndim == 0:
            sigma_0 = sigma_0.reshape((1,))
        if az is None:
            az = self.caz
        nesz = self.inc2nesz(inc_0)[az]
        snr = sigma_0 - nesz
        coh_snr = insar.coh_m(snr, decibel=True)
        nlk = self.prod_res ** 2 / (self.grg_res * self.az_res)
        # FIX-ME include RASR
        coh = coh_snr * self.sys_coh * coh_t
        stdv = np.sqrt((1. - coh ** 2.) / (2. * nlk * coh ** 2.))
        return stdv

    def sigma_dop(self, inc_0, sigma_0, coh_t=1, az=None, tau=None):
        if tau is None:
            tau = self.tau
        sigma_fd = self.sigma_phase(inc_0, sigma_0, coh_t=coh_t, az=az) / np.pi / 2 / tau
        return sigma_fd

    def sigma_vdop(self, inc_0, sigma_0, coh_t=1, az=None, tau=None):
        if tau is None:
            tau = self.tau
        wl = cnst.c / self.f0
        sigma_v = wl / 2 * self.sigma_dop(inc_0, sigma_0, coh_t=coh_t, az=az, tau=tau)
        return sigma_v


class DCAPerf(object):
    def __init__(self, nesz_data, b_ati, prod_res,
                 tx_name='sentinel', rx_name='airbus_dual_rx',
                 f0=5.4e9, sys_coh=0.99, az_res=20, grg_res=5,
                 tx_ant=None, rx_ant=None):
        """

        :param nesz_data: NESZData object
        :param b_ati: physical along-track baseline
        :param prod_res: product resolution
        :param f0: radar frequency
        :param sys_coh: maximum coherence
        :param tx_name: name of tx system, as un config file
        :param rx_name: name of rx system, as un config file
        :param az_res: ...
        :param grg_res: ...
        :param tx_ant: tx antenna object. If None then it is constructed (default)
        :param rx_ant: rx antenna object. If None then it is constructed (default)
        """
        self.nesz_data = nesz_data
        self.b_ati = b_ati
        self.prod_res = prod_res
        self.f0 = f0
        self.sys_coh = sys_coh
        self.inc2nesz = interp.interp1d(nesz_data.inc_v, nesz_data.nesz)
        self.naz = nesz_data.nesz.shape[0]
        self.caz = int(self.naz/2)
        self.az_res = az_res
        self.grg_res = grg_res
        # SAR modes
        self.sar_modes = sar.SARModeFromCfg(self.nesz_data.conf, self.nesz_data.modename)
        # Azimuth pattern
        txcnf = getattr(self.nesz_data.conf, tx_name)
        rxcnf = getattr(self.nesz_data.conf, rx_name)
        if hasattr(txcnf, 'wa_tx'):
            wa_tx = txcnf.wa_tx
        else:
            wa_tx = 1
        if hasattr(rxcnf, 'we_tx'):
            we_tx = rxcnf.we_tx
        else:
            we_tx = 1
        if tx_ant is None:
            tx_ant = sar.pattern(self.f0,
                                 type_a=txcnf.type_a, type_e=txcnf.type_e,
                                 La=txcnf.La, Le=txcnf.Le,
                                 el0=(np.degrees(np.mean(self.nesz_data.la_v)) - txcnf.tilt),
                                 Nel_a=txcnf.Na, Nel_e=txcnf.Ne,
                                 wa=wa_tx, we=we_tx)
        if rx_ant is None:
            if hasattr(rxcnf, 'wa_rx'):
                if type(rxcnf.wa_rx) is np.ndarray:
                    wa_rx = rxcnf.wa_rx
                else:
                    c0 = rxcnf.wa_rx
                    Na = rxcnf.Na
                    wa_rx = (c0 -
                             (1 - c0) * np.cos(2 * np.pi * np.arange(Na) / (Na - 1)))
            else:
                wa_rx = 1
            if hasattr(rxcnf, 'we_rx'):
                if type(rxcnf.we_rx) is np.ndarray:
                    we_rx = rxcnf.we_rx
                else:
                    c0 = rxcnf.we_rx
                    Ne = rxcnf.Ne
                    we_rx = (c0 -
                             (1 - c0) * np.cos(2 * np.pi * np.arange(Ne) / (Ne - 1)))
            else:
                we_rx = 1

            if hasattr(rxcnf, 'azimuth_spacing'):
                azimuth_spacing = rxcnf.azimuth_spacing
            else:
                azimuth_spacing = 1
            if hasattr(rxcnf, 'elevation_spacing'):
                elevation_spacing = rxcnf.elevation_spacing
            else:
                elevation_spacing = 1
            rx_ant = sar.pattern(self.f0,
                                 type_a=rxcnf.type_a, type_e=rxcnf.type_e,
                                 La=rxcnf.La, Le=rxcnf.Le,
                                 Nel_a=rxcnf.Na, Nel_e=rxcnf.Ne,
                                 wa=wa_rx, we=we_rx,
                                 spacing_a=azimuth_spacing, spacing_e=elevation_spacing)
            self.tx_pat = tx_ant   # .azimuth
            self.rx_pat = rx_ant   # .azimuth

    def tx_az_pat(self, ang, field=True, squint_rad=None, use_ne=False):
        """ Returns azimuth normalized pattern
            :param ang: angle in radians
            :param field: return field if True, intensity if False
            :param squint_rad: overides init squint. If it is a vector then
                               it will be combined with ang, following numpy
                               rules. So, this could be sued to calculate a
                               stack of patterns with different squints, or
                               to compute the pattern seen by a target in
                               TOPS or Spotlight mode
            :param use_ne:  use numexpr to speed up
        """
        # We return only the co-pol pattern
        return self.tx_pat.azimuth(ang, field=field, squint_rad=squint_rad, use_ne=use_ne)[0]

    def rx_az_pat(self, ang, field=True, squint_rad=None, use_ne=False):
        return self.rx_pat.azimuth(ang, field=field, squint_rad=squint_rad, use_ne=use_ne)[0]

    def sigma_dop(self, inc_0_in, sigma_0_in, az=None, degree=True):
        """

        :param inc_0_in: scalar or matrix with same dimensions as sigma_0_in
        :param sigma_0_in:
        :param az:
        :param degree:
        :return:
        """
        inc_0 = np.atleast_1d(inc_0_in)
        sigma_0 = np.atleast_1d(sigma_0_in)
        if az is None:
            az = self.caz
        nesz = self.inc2nesz(inc_0)[az]
        snr = sigma_0 - nesz
        # FIXME: treating ambiguity as white noise, ignoring spectrum
        # Need a better strategy for different values of PRF
        swths = self.sar_modes.inc2swath(inc_0, degree=degree)
        swths = np.broadcast_to(swths, snr.shape)
        unique_swaths = np.unique(swths)
        sigma_fd = np.zeros_like(sigma_0_in)
        for swth in unique_swaths:
            # print(swth)
            if swth > 0:
                prf = self.sar_modes.prfs[swth - 1]
                if swths.size > 1:
                    # We need to filter
                    selected = np.where(swths == swth)
                    snr_ = snr[selected]
                    sigma_fd_ = doppler_centroid.stripmap(12, self.grg_res, self.prod_res, numerical=True,
                                                          snr_db=snr_, La2=None,
                                                          v_ef=orbit_to_vel(698e3),
                                                          az_res=self.az_res,
                                                          rx_pat=self.rx_az_pat,
                                                          tx_pat=self.tx_az_pat,
                                                          f0=self.f0,
                                                          prf=prf)
                    sigma_fd[selected] = sigma_fd_
                else:
                    snr_ = snr
                    sigma_fd = doppler_centroid.stripmap(12, self.grg_res, self.prod_res, numerical=True,
                                                         snr_db=snr_, La2=None,
                                                         v_ef=orbit_to_vel(698e3),
                                                         az_res=self.az_res,
                                                         rx_pat=self.rx_az_pat,
                                                         tx_pat=self.tx_az_pat,
                                                         f0=self.f0,
                                                         prf=prf)

        return sigma_fd

    def sigma_vdop(self, inc_0, sigma_0, az=None, degree=True):
        wl = cnst.c / self.f0
        sigma_v = wl / 2 * self.sigma_dop(inc_0, sigma_0, az=az, degree=degree)
        return sigma_v


def ATI_perf(Ltx=12, Lrx=2, rg_res=5, B_at=4.5, prod_res=1e3, v=4, phi=90, theta_i_range=(20, 45), NESZ=-20,
             f0=5.4e9, overplot=False, fontsize=12, az_ovs=1.2, dtar=None, label=None,
             sys_coh=0.99, az_res=None, linestyle=None, do_plot=True, theta_i=None, figsize=(6, 4)):
    if theta_i is None:
        theta_i = np.linspace(theta_i_range[0], theta_i_range[1])
    zs = np.zeros_like(theta_i)
    nrcs = cmod5.cmod5n_forward(zs + v, zs + phi, theta_i)
    snr_db = 10 * np.log10(nrcs) - NESZ
    snr = 10**(snr_db/10)
    # Commenting out ambiguities, since they do not directly change the coherence
    if dtar is None:
        coh_snr = insar.coh_m(snr_db, decibel=True)
    else:
        snra = 1/(1/snr+10**(-dtar/10))
        snra_db = 10 * np.log10(snra)
        coh_snr = insar.coh_m(snra_db, decibel=True)
    # sigma_f = np.zeros_like(theta_i)
    coh = coh_snr * sys_coh
    print("Minimum and max coherences: (%f, %f)" % (coh.min(), coh.max()))
    if az_res is None:
        az_res = Ltx/2
    nlk = prod_res ** 2 / (rg_res * az_res)
    print(nlk)
    stdv = np.sqrt((1. - coh ** 2.) / (2. * nlk * coh ** 2.))
    print("Minimum and max phase std: (%f, %f)" % (stdv.min(), stdv.max()))
    tau = B_at/2/orbit_to_vel(698e3)
    sigma_fd = stdv / np.pi / 2 / tau
    print("Minimum and max fd err: (%f, %f)" % (sigma_fd.min(), sigma_fd.max()))
    wl = cnst.c / f0
    sigma_v = wl / 2 * sigma_fd
    if label is None:
        label = ("NESZ=%3.1f dB" % NESZ)
    if overplot:
        plt.plot(theta_i, sigma_v, linestyle=linestyle, label=label)
    elif do_plot:
        # Font configuration
        font = {'family': "Arial",
                'weight': 'normal',
                'size': fontsize}
        matplotlib.rc('font', **font)
        plt.figure(figsize=figsize)
        plt.plot(theta_i, sigma_v, linestyle=linestyle, label=label)
        ax = plt.gca()
        ax.grid(True)
        plt.xlabel("Incident angle [deg]")
        plt.ylabel("$\sigma_{v,r}$ [m/s]")
        plt.tight_layout()
        plt.xlim(theta_i_range)
    return sigma_fd, sigma_v


def DCA_perf(Ltx=12, Lrx=12, rg_res=5, prod_res=1e3, v=4, phi=90, theta_i_range=(20, 45), NESZ=-20,
             f0 = 5.4e9, overplot=False, fontsize=12, az_ovs=1.2, dtar=15, label=None,
             az_res=None, rx_pat=None, linestyle=None, do_plot=True, theta_i=None, figsize=(6, 4)):
    # L = np.sqrt(Ltx * Lrx)//
    if theta_i is None:
        theta_i = np.linspace(theta_i_range[0], theta_i_range[1])
    zs = np.zeros_like(theta_i)
    NRCS = cmod5.cmod5n_forward(zs + v, zs + phi, theta_i)
    SNRdB = 10 * np.log10(NRCS) - NESZ
    SNR = 10**(SNRdB/10)
    SNRA = 1/(1/SNR+10**(-dtar/10))
    SNRAdB = 10 * np.log10(SNRA)
    #print("SNR:")
    #print(SNRdB)
    #print(SNRAdB)
    # sigma_f = doppler_centroid.stripmap(Ltx, rg_res, prod_res, Numerical=False, SNRdB=SNRdB)
    sigma_f = np.zeros_like(theta_i)
    # FIXME: treating ambiguity as white noise, ignoring spectrum
    for ind in range(sigma_f.size):
        sigma_f[ind] = doppler_centroid.stripmap(Ltx, rg_res, prod_res, numerical=True, SNRdB=SNRAdB[ind], La2=Lrx,
                                                 v_ef=orbit_to_vel(698e3), az_ovs=az_ovs,
                                                 az_res=az_res, rx_pat=rx_pat, f0=f0)
    wl = cnst.c / f0
    # df = 2 * v / wl
    sigma_v = wl / 2 * sigma_f
    sigma_v_h = sigma_v / np.sin(np.radians(theta_i))
    if label is None:
        label = ("NESZ=%3.1f dB" % NESZ)
    if overplot:
        plt.plot(theta_i, sigma_v, linestyle=linestyle, label=label)
    elif do_plot:
        # Font configuration
        font = {'family': "Arial",
                'weight': 'normal',
                'size': fontsize}
        matplotlib.rc('font', **font)
        plt.figure(figsize=figsize)
        plt.plot(theta_i, sigma_v, linestyle=linestyle, label=label)
        ax = plt.gca()
        ax.grid(True)
        plt.xlabel("Incident angle [deg]")
        plt.ylabel("$\sigma_{v,r}$ [m/s]")
        plt.tight_layout()
        plt.xlim(theta_i_range)

    return sigma_f, sigma_v, sigma_v_h


if __name__ == '__main__':
    main_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
    #s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, np.sqrt(1e3*1.5e3), v=4, phi=90, fontsize=16, az_ovs=1.5, NESZ=-20)
    phi = 180
    DTAR = 17
    NESZ = -25
    az_res = 20
    f0 = 5.4e9
    fontsize = 16
    prod_res_km = 4
    prod_res = prod_res_km * 1e3
    er_range = (0, 0.15)
    b_at = 4.5

    s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, prod_res, fontsize=fontsize,
                               v=4, phi=phi, NESZ=NESZ, overplot=False, az_ovs=1.5,
                               label="$U_{10}$ = 4 m/s", dtar=DTAR, az_res=az_res)
    #plt.ylim((0, 0.2))
    s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, prod_res, fontsize=fontsize,
                               v=6, phi=phi, NESZ=NESZ, overplot=True, az_ovs=1.5,
                               label="$U_{10}$ = 6 m/s", dtar=DTAR, az_res=az_res)
    s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, prod_res, fontsize=fontsize,
                               v=8, phi=phi, NESZ=NESZ, overplot=True, az_ovs=1.5,
                               label="$U_{10}$ = 8 m/s", dtar=DTAR, az_res=az_res)
    # s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, np.sqrt(1e3 * 1.5e3), v=6, phi=90, NESZ=-23, overplot=True, az_ovs=1.5)
    plt.legend(loc=2)
    ax = plt.gca()
    ax.set_ylim(er_range)
    plt.title("DCA 4 m Antenna")
    plt.tight_layout()
    os.makedirs(os.path.join(main_dir,'RESULTS/DCA'), exist_ok=True)
    fout = os.path.join(main_dir,('RESULTS/DCA/dca_noiseandamb_upwind_%ikm_DTAR15_ant4m.png' % prod_res_km))
    plt.savefig(fout)

    # DCA, split antenna
    def rex_pat(sin_angle):
        return sar.phased_spacedarray(sin_angle, 1.3, f0, 2, 1, b_at)

    def rex_pat3(sin_angle):
        return sar.phased_spacedarray(sin_angle, 1.3, f0, 3, 1, b_at)

    DTAR = 18
    def dca_plots(Ltx=12.3, Lrx=4, rg_res=5, prod_res_km=prod_res_km, U=[4,6,8], phi=phi, NESZ=NESZ, dtar=DTAR,
                   rx_pattern=None, az_res=20, title="DCA 2 x 1.3 m Antenna", fontsize=16, er_range=er_range):
        prod_res = 1e3 * prod_res_km
        Us = np.array(U)
        ovplt = np.zeros_like(Us, dtype=np.bool)
        ovplt[:] = True
        ovplt[0] = False
        for ind in range(Us.size):
            label = ("$U_{10}$ = %i m/s" % (int(Us[ind])))
            s_f, s_v, s_v_h = DCA_perf(Ltx, Lrx, rg_res, prod_res, fontsize=fontsize,
                                       v=Us[ind], phi=phi, NESZ=NESZ, overplot=ovplt[ind], az_ovs=1.5,
                                       label=label, dtar=dtar, az_res=az_res,
                                       rx_pat=rx_pattern)

        # s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, np.sqrt(1e3 * 1.5e3), v=6, phi=90, NESZ=-23, overplot=True, az_ovs=1.5)
        plt.legend(loc=2)
        plt.title(title)
        ax = plt.gca()
        ax.set_ylim(er_range)
        plt.tight_layout()

    def ati_plots(Ltx=12.3, Lrx=4, rg_res=5, prod_res_km=prod_res_km, U=[4,6,8], phi=phi, NESZ=NESZ, dtar=DTAR,
                  rx_pattern=None, az_res=20, title="DCA 2 x 1.3 m Antenna", fontsize=16, er_range=er_range,
                  b_ati=4.5):
        prod_res = 1e3 * prod_res_km
        Us = np.array(U)
        ovplt = np.zeros_like(Us, dtype=np.bool)
        ovplt[:] = True
        ovplt[0] = False
        for ind in range(Us.size):
            label = ("$U_{10}$ = %i m/s" % (int(Us[ind])))
            s_f, s_v = ATI_perf(Ltx, Lrx, rg_res, B_at=b_ati, prod_res=prod_res, fontsize=fontsize,
                                       v=Us[ind], phi=phi, NESZ=NESZ, overplot=ovplt[ind], az_ovs=1.5,
                                       label=label, dtar=dtar, az_res=az_res)

        # s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, np.sqrt(1e3 * 1.5e3), v=6, phi=90, NESZ=-23, overplot=True, az_ovs=1.5)
        plt.legend(loc=2)
        plt.title(title)
        ax = plt.gca()
        ax.set_ylim(er_range)
        plt.tight_layout()

    prod_res_km = 2

    dca_plots(prod_res_km=prod_res_km, phi=phi, NESZ=NESZ + 1.8, title="DCA 2 x 1.3 m Antenna",
              rx_pattern=rex_pat, fontsize=fontsize)
    fout = os.path.join(main_dir, ('RESULTS/DCA/dca_sa_noiseandamb_upwind_%ikm_DTAR18_ant2x2.png' % prod_res_km))
    plt.savefig(fout)

    dca_plots(prod_res_km=prod_res_km, phi=phi, NESZ=NESZ + 1.8, title="DCA 3 x 1.3 m Antenna",
              rx_pattern=rex_pat3, fontsize=fontsize)
    fout = os.path.join(main_dir, ('RESULTS/DCA/dca_sa_noiseandamb_upwind_%ikm_DTAR18_ant3x2.png' % prod_res_km))
    plt.savefig(fout)

    ati_plots(prod_res_km=prod_res_km, phi=phi, NESZ=NESZ + 3, title="ATI $B_{ATI}=4.5$",
              b_ati=b_at, fontsize=fontsize)
    fout = os.path.join(main_dir, ('RESULTS/DCA/ATI_noiseandamb_upwind_%ikm_DTAR18_b_ati4_5.png' % prod_res_km))
    plt.savefig(fout)

    ati_plots(prod_res_km=prod_res_km, phi=phi, NESZ=NESZ + 3, title="ATI $B_{ATI}=9$",
              b_ati=2 * b_at, fontsize=fontsize)
    fout = os.path.join(main_dir, ('RESULTS/DCA/ATI_noiseandamb_upwind_%ikm_DTAR18_b_ati9.png' % prod_res_km))
    plt.savefig(fout)


    DTAR = 18
    fontsize = 16
    NESZ = -25 + 1.8
    s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, prod_res, fontsize=fontsize,
                               v=4, phi=phi, NESZ=NESZ, overplot=False, az_ovs=1.5,
                               label="$U_{10}$ = 4 m/s (DCA)", dtar=DTAR, az_res=az_res,
                               rx_pat=rex_pat, linestyle='-')
    # plt.ylim((0, 0.2))

    s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, prod_res, fontsize=fontsize,
                               v=8, phi=phi, NESZ=NESZ, overplot=True, az_ovs=1.5,
                               label="$U_{10}$ = 8 m/s (DCA)", dtar=DTAR, az_res=az_res,
                               rx_pat=rex_pat, linestyle='-')
    DTAR = 18
    s_f, s_v = ATI_perf(12.3, 4, 5, b_at, prod_res, fontsize=fontsize,
                        v=4, phi=phi, NESZ=NESZ + 3, overplot=True, az_ovs=1.5,
                        label="$U_{10}$ = 4 m/s (ATI)", dtar=DTAR, az_res=az_res, linestyle='-')
    # plt.ylim((0, 0.2))

    s_f, s_v = ATI_perf(12.3, 4, 5, b_at, prod_res, fontsize=fontsize,
                        v=8, phi=phi, NESZ=NESZ + 3, overplot=True, az_ovs=1.5,
                        label="$U_{10}$ = 8 m/s (ATI)", dtar=DTAR, az_res=az_res, linestyle='-')

    plt.legend(loc=0, frameon=True)
    #plt.legend(frameon=False)
    ax = plt.gca()
    #ax.set_yscale('log')
    #ax.set_ylim((0.005, 0.5))
    #ax = plt.gca()
    ax.set_ylim(er_range)
    plt.title("DCA vs ATI")
    plt.tight_layout()
    fout = os.path.join(main_dir, ('RESULTS/DCA/dca_vs_ATI_noiseandamb_upwind_%ikm_DTAR13-17_ant2x2.png' % prod_res_km))

    plt.savefig(fout)

    DTAR=18
    s_f, s_v = ATI_perf(12.3, 4, 5, b_at, prod_res, fontsize=fontsize,
                        v=4, phi=phi, NESZ=NESZ + 3, overplot=False, az_ovs=1.5,
                        label="$U_{10}$ = 4 m/s", dtar=DTAR, az_res=az_res)
    #plt.ylim((0, 0.2))
    s_f, s_v = ATI_perf(12.3, 4, 5, b_at, prod_res, fontsize=fontsize,
                        v=6, phi=phi, NESZ=NESZ + 3, overplot=True, az_ovs=1.5,
                        label="$U_{10}$ = 6 m/s", dtar=DTAR, az_res=az_res)
    s_f, s_v = ATI_perf(12.3, 4, 5, b_at, prod_res, fontsize=fontsize,
                        v=8, phi=phi, NESZ=NESZ + 3, overplot=True, az_ovs=1.5,
                        label="$U_{10}$ = 8 m/s", dtar=DTAR, az_res=az_res)
    # s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, np.sqrt(1e3 * 1.5e3), v=6, phi=90, NESZ=-23, overplot=True, az_ovs=1.5)
    plt.legend(loc=2)
    plt.title("ATI 2 x 1.3 m Antenna")
    ax = plt.gca()
    ax.set_ylim(er_range)
    plt.tight_layout()
    fout = os.path.join(main_dir, ('RESULTS/DCA/ATI_noiseandamb_upwind_%ikm_DTAR18.png' % prod_res_km))
    plt.savefig(fout)

    DTAR=18
    prod_res_km = 5
    prod_res = prod_res_km * 1e3
    s_f, s_v = ATI_perf(12.3, 4, 5, b_at, prod_res, fontsize=fontsize,
                        v=4, phi=phi, NESZ=NESZ + 3, overplot=False, az_ovs=1.5,
                        label="$U_{10}$ = 4 m/s", dtar=DTAR, az_res=az_res)
    #plt.ylim((0, 0.2))
    s_f, s_v = ATI_perf(12.3, 2, 5, b_at, prod_res, fontsize=fontsize,
                        v=6, phi=phi, NESZ=NESZ + 3, overplot=True, az_ovs=1.5,
                        label="$U_{10}$ = 6 m/s", dtar=DTAR, az_res=az_res)
    s_f, s_v = ATI_perf(12.3, 2, 5, b_at, prod_res, fontsize=fontsize,
                        v=8, phi=phi, NESZ=NESZ + 3, overplot=True, az_ovs=1.5,
                        label="$U_{10}$ = 8 m/s", dtar=DTAR, az_res=az_res)
    # s_f, s_v, s_v_h = DCA_perf(12.3, 4, 5, np.sqrt(1e3 * 1.5e3), v=6, phi=90, NESZ=-23, overplot=True, az_ovs=1.5)
    plt.legend(loc=2)
    plt.title("ATI 2 x 1 m Antenna")
    ax = plt.gca()
    ax.set_ylim(er_range)
    plt.tight_layout()
    fout = os.path.join(main_dir, ('RESULTS/DCA/ATI_noiseandamb_upwind_%ikm_DTAR18.png' % prod_res_km))
    plt.savefig(fout)
