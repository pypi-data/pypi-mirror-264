import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from drama.io import cfg
from drama.performance.sar import calc_aasr, calc_nesz, RASR, RASRdata
from drama.performance.sar.azimuth_performance import mode_from_conf
import drama.geo as geo
from drama.geo.geo_history import GeoHistory
from drama.utils.misc import (save_object, load_object)
from sesame.casa_patterns import casa_pattern, tasi_pattern

__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

if __name__ == '__main__':
    do_casa = False
    do_rasr = True
    do_nesz = True
    fontsize=14
    do_plot_rasr = True
    main_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
    datadir = os.path.join(main_dir, 'DATA')
    patterdir = os.path.join(datadir, 'PATTERNS')
    rxname = 'airbus_rx'
    txname= 'sentinel'
    runid = 'EUSAR'
    pardir = os.path.join(main_dir, 'PAR')

    pltdirr = os.path.join(os.path.join(os.path.join(main_dir, 'RESULTS'), 'Activation'), runid)
    parfile = os.path.join(pardir, ("STEREOID_%s.cfg" % runid))
    conf = cfg.ConfigFile(parfile)
    # extract relevant info from conf
    rxcnf = getattr(conf, rxname)
    txcnf = getattr(conf, txname)
    #rxcnf = getattr(conf, rxname)
    # b_at = rxcnf.b_at
    dau_km = int(conf.formation_primary.dau[0] / 1e3)
    dau_str = ("%ikm" % dau_km)
    indstr = 'Airbus'
    sysid = indstr # ("%s_%3.2fm" % (indstr, b_at))
    if rxcnf.DBF:
        sysid = sysid + "_DBF"

    savedirr = os.path.join(os.path.join(os.path.join(main_dir, 'RESULTS'), 'SARPERF'), sysid)
    savedirr = os.path.join(savedirr, dau_str)
    mode = "IWS"
    # mode = "stripmap"
    Nswth = 3
    n_az_pts = 3
    inc_range=[10,45]

    (incs, PRFs, proc_bw,
     steering_rates,
     burst_lengths, short_name, proc_tap, tau_p, bw_p) = mode_from_conf(conf, mode)

    ghist = GeoHistory(conf,
                       tilt=txcnf.tilt,
                       tilt_b=rxcnf.tilt,
                       latitude=0,
                       bistatic=True,
                       dau=conf.formation_primary.dau[0],
                       inc_range=inc_range + np.array([-10, 20]),
                       inc_swth=[30, 45])

    if do_rasr:
        for swth in range(Nswth):
            rasr_250 = RASR(conf, mode, swth, Namb=2, Namb_az=4,
                            txname='sentinel',
                            rxname=rxname,
                            savedirr=savedirr,
                            t_in_bs=None,
                            n_az_pts=n_az_pts,
                            view_patterns=False,
                            vmin=-18.25, vmax=-16.75, use_ne=True, az_sampling=1e3)

            modeandswth = ("%s_sw%i" % (short_name, swth + 1))
            modedir = os.path.join(savedirr, modeandswth)

            # savefile = os.path.join(modedir, name) + "_AASR.png"
            rasr_250.save(os.path.join(modedir, "RASR.pkl"))

    if do_plot_rasr:
        plt.figure()
        font = {'family': "Arial",
                'weight': 'normal',
                'size': fontsize}
        matplotlib.rc('font', **font)
        def nrcs_prof(inc):
            return np.exp(-inc/6)

        for swth in range(Nswth):
            modeandswth = ("%s_sw%i" % (short_name, swth + 1))
            modedir = os.path.join(savedirr, modeandswth)
            rasrd = RASRdata.from_file(os.path.join(modedir, "RASR.pkl"))
            rasrd.calc_rasr(scattering_profile_func=nrcs_prof)

            plt.plot(rasrd.inc_v, 10 * np.log10(rasrd.rasr_total[int(0*rasrd.rasr_total.shape[0]/2), :]), linewidth=2.0)
            # plt.plot(rasrd.inc_v, 10 * np.log10(np.sum(rasrd.rasr_parcial[int(rasrd.rasr_total.shape[0] / 2), 2, :], axis=0)), linewidth=2.0)
        plt.xlabel("Incident angle [deg]")
        plt.ylabel("RASR [dB]")
        plt.grid(True)
        plt.savefig(os.path.join(savedirr, "RASR.png"))
        plt.close()
