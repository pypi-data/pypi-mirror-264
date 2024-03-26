import os

import numpy as np
import matplotlib.pyplot as plt

from drama.io import cfg
from drama.performance.sar import calc_aasr, calc_nesz, RASR, RASRdata, pattern, AASRdata, NESZdata, SARModeFromCfg
from drama.performance.sar.azimuth_performance import mode_from_conf
import drama.geo as geo
from drama.geo.geo_history import GeoHistory
import stereoid.oceans as strocs
import stereoid.utils.config as st_config


def calc_sar_perf(conf, rxname, savedir, txname = 'sentinel', mode = "IWS",
                  is_bistatic = True, do_aasrs=True, do_neszs = True, do_rasrs = False):
    """Computes NESZ, AASR and (eventually) RASR.

    Parameters
    ----------
    conf : ConfigFile
        ConfigFile object with Harmony configuration.
    rxname : str
        Name of receiver (must be defined in config file).
    savedir : str
        Directory where results are put.
    txname : str
        Name of transmitter, defaults to 'sentinel'.
    mode : str
        Name of operating mode, defaults to 'IWS'.
        The code looks for the mode definition in conf.
    is_bistatic : bool
        Defaults to True, set to False for a monostatic configuration,
        which sets the along-track separation to zero
    do_aasrs : bool
        True (default) to calculate AASR.
    do_neszs : bool
        True (default) to calculate NESZ.
    do_rasrs : bool
        True to calculate RASR. Default is False because RASR is at time of
        writing prone to out of bounds interpolation errors.

    Returns
    -------
    type
        Description of returned object.

    """

    rxcnf = getattr(conf, rxname)
    txcnf = getattr(conf, txname)
    if is_bistatic:
        dau_km = int(conf.formation_primary.dau[0] / 1e3)
    else:
        dau_km = int(0)
    dau_str = f'{dau_km:03d}km' #("%ikm" % dau_km)
    indstr = rxname
    sysid = indstr # ("%s_%3.2fm" % (indstr, b_at))
    if rxcnf.DBF:
        sysid = sysid + "_DBF"

    if rxcnf.SCORE:
        sysid = sysid + "_SCORE"
    savedirr = os.path.join(savedir, sysid)
    savedirr = os.path.join(savedirr, dau_str)
    n_az_pts = 11
    inc_range=[10,48]
    (incs, PRFs, proc_bw,
     steering_rates,
     burst_lengths, short_name, proc_tap, tau_p, bw_p) = mode_from_conf(conf, mode)
    Nswth = incs.shape[0]

    # Azimuth ambiguities
    if do_aasrs:
        aasrs = []
        aasr_files = []
        for swth in range(Nswth):
            modeandswth = ("%s_sw%i" % (short_name, swth + 1))
            modedir = os.path.join(savedirr, modeandswth)
            aasr_files.append(os.path.join(modedir,'aasr.p'))
            aasr_ = calc_aasr(conf, mode, swth,
                              txname='sentinel',
                              rxname=rxname,
                              savedirr=savedirr,
                              t_in_bs=None,
                              n_az_pts=n_az_pts,
                              view_patterns=False,
                              Tanalysis=20,
                              # vmin=-25.0, vmax=-15.0,
                              az_sampling=200, Namb=3,
                              bistatic=is_bistatic)
            aasr_.save(os.path.join(modedir,'aasr.p'))
            aasrs.append(aasr_)

        aasr = AASRdata.from_filelist(aasr_files)
        aasr.save(os.path.join(savedirr, "%s_AASR.p" % short_name))

    # NESZ
    if do_neszs:
        neszs = []
        nesz_files = []
        for swth in range(Nswth):
            modeandswth = ("%s_sw%i" % (short_name, swth + 1))
            modedir = os.path.join(savedirr, modeandswth)
            nesz_files.append(os.path.join(modedir,'nesz.p'))
            nesz_ = calc_nesz(conf, mode, swth, txname='sentinel',
                              rxname=rxname,
                              savedirr=savedirr,
                              t_in_bs=None,
                              n_az_pts=n_az_pts,
                              extra_losses=rxcnf.L,
                              Tanalysis=10,
                              az_sampling=200, bistatic=is_bistatic)
            nesz_.save(os.path.join(modedir,'nesz.p'))
            neszs.append(nesz_)

        nesz = NESZdata.from_filelist(nesz_files)
        nesz.save(os.path.join(savedirr, "%s_NESZ.p" % short_name))
        #nesz = NESZdata.from_file(os.path.join(savedirr, "%s_NESZ.p" % short_name))

    # Range ambiguities
    if do_rasrs:
        rasrs = []
        rasr_files = []
        for swth in range(0, Nswth):
            modeandswth = ("%s_sw%i" % (short_name, swth + 1))
            modedir = os.path.join(savedirr, modeandswth)
            rasr_files.append(os.path.join(modedir,'rasr.p'))

            rasr_ = RASR(conf, mode, swth, txname='sentinel',
                         rxname=rxname,
                         savedirr=savedirr,
                         t_in_bs=None,
                         Namb=1,
                         n_az_pts=n_az_pts, n_amb_az=5, Tanalysis=10,
                         az_sampling=100, bistatic=is_bistatic, verbosity=2)
            rasr_.save(os.path.join(modedir,'rasr.p'))
            rasrs.append(rasr_)

        rasr = RASRdata.from_filelist(rasr_files)
        rasr.save(os.path.join(savedirr, "%s_RASR.p" % short_name))


#%%
if __name__ == '__main__':
    rx_ipc_name = 'hrmny_2021_tripple_ati'
    rx_cpc_name = 'hrmny_2021_tripple'
    parfile_name = 'Hrmny_2021_1.cfg'
    paths = st_config.parse(section="Paths")
    main_dir = paths["main"]
    datadir = paths["data"]
    runid = '2021_1'
    pardir = paths["par"]
    parfile = pardir / parfile_name
    conf = cfg.ConfigFile(parfile)
    savedirr = os.path.join(paths["results"], "SARPERF")
    daus = [350e3, 400e3, 450e3]
    #%%
    for dau in daus:
        conf.formation_primary.dau[:] = dau
        for rxname in [rx_ipc_name, rx_cpc_name]:
            calc_sar_perf(conf, rxname, savedirr, txname = 'sentinel', mode = "WM",
                          is_bistatic = True, do_aasrs=True, do_neszs = True, do_rasrs = False)
    #%%
    conf.formation_primary.dau[:] = 0  # To be sure
    calc_sar_perf(conf, 'sentinel', savedirr, txname = 'sentinel', mode = "IWS_S1",
                  is_bistatic = False, do_aasrs=True, do_neszs = True, do_rasrs = False)
