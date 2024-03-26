# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from drama.io import cfg
from drama.performance.sar import calc_aasr, calc_nesz, RASR, pattern
from drama.performance.sar.azimuth_performance import mode_from_conf, AASRdata
import drama.geo as geo
from drama.geo.geo_history import GeoHistory
from drama.utils.misc import (save_object, load_object)
# from sesame.casa_patterns import casa_pattern, tasi_pattern


__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"


if __name__ == '__main__':
    do_casa = False
    main_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
    datadir = os.path.join(main_dir, 'DATA')
    patterdir = os.path.join(datadir, 'PATTERNS')
    rxname = 'airbus_dual_rx'
    # rxname = 'airbus_ati_rx'
    txname = 'sentinel'
    runid = 'EUSAR'
    pardir = os.path.join(main_dir, 'PAR')

    pltdirr = os.path.join(os.path.join(os.path.join(main_dir, 'RESULTS'), 'Activation'), runid)
    parfile = os.path.join(pardir, ("STEREOID_%s.cfg" % runid))
    conf = cfg.ConfigFile(parfile)
    # extract relevant info from conf
    rxcnf = getattr(conf, rxname)
    txcnf = getattr(conf, txname)
    # tx_ant = pattern(conf.sar.f0,
    #                  type_a=txcnf.type_a,
    #                  type_e=txcnf.type_e,
    #                  La=txcnf.La,
    #                  Le=txcnf.Le,
    #                  Nel_a=txcnf.Na,
    #                  Nel_e=txcnf.Ne,
    #                  wa=txcnf.wa_tx,
    #                  we=txcnf.we)
    #rxcnf = getattr(conf, rxname)
    # b_at = rxcnf.b_at
    dau_km = int(conf.formation_primary.dau[0] / 1e3)
    dau_str = ("%ikm" % dau_km)
    indstr = 'airbus_dual'
    sysid = indstr # ("%s_%3.2fm" % (indstr, b_at))
    if rxcnf.DBF:
        sysid = sysid + "_DBF"

    savedirr = os.path.join(os.path.join(os.path.join(main_dir, 'RESULTS'), 'SARPERF'), sysid)
    savedirr = os.path.join(savedirr, dau_str)
    mode = "IWS" #
    #mode = "stripmap"
    Nswth = 3
    n_az_pts = 11
    inc_range = [10,45]

    (incs, PRFs, proc_bw,
     steering_rates,
     burst_lengths, short_name, proc_tap, tau_p, bw_p) = mode_from_conf(conf, mode)
    # modeandswth = ("%s_sw%i" % (short_name, swth + 1))
    # modedir = os.path.join(savedirr, modeandswth)
    # savefile = os.path.join(modedir, name) + "_AASR.png"
    # save_object(rasr_250, os.path.join(modedir, "RASR.pkl"))
    Nswth=1
    for swth in range(Nswth):
        aasr_ = calc_aasr(conf, mode, swth,
                          txname='sentinel',
                          rxname=rxname,
                          savedirr=savedirr, az_sampling=200,
                          t_in_bs=None,
                          n_az_pts=n_az_pts,
                          view_patterns=False,
                          vmin=-20.0, vmax=-13.0)
        plt.close('all')
    for swth in range(Nswth):
        la_v, inc_v, NESZ_out, NESZ_tap_out = calc_nesz(conf, mode, swth,
                                                        txname='sentinel',
                                                        rxname=rxname,
                                                        savedirr=savedirr,
                                                        t_in_bs=None,
                                                        n_az_pts=n_az_pts,
                                                        extra_losses=rxcnf.L,
                                                        vmin=-25, vmax=-18)
        plt.close('all')



