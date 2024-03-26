import os
from drama.io import cfg
from drama.performance.sar.azimuth_performance import mode_from_conf

__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"


def sarperf_files(main_dir, rxname, mode="IWS",
                  txname='sentinel', is_bistatic=True, runid='EUSAR',
                  parpath=None):
    ''' Construct path for SAR performance analyses
    Input: 
    - main_dir
    '''
    #patterdir = os.path.join(datadir, 'PATTERNS')
    # Next two lines are for Sentinel-1 performance
    # rxname = 'sentinel'
    # For companions, is_bistatic should be True
    if parpath is None:
        parpath = os.path.join(main_dir, 'PAR', f'Hrmny_{runid}.cfg')
    conf = cfg.ConfigFile(parpath)
    # extract relevant info from conf
    rxcnf = getattr(conf, rxname)
    txcnf = getattr(conf, txname)
    if is_bistatic:
        dau_km = int(conf.formation_primary.dau[0] / 1e3)
    else:
        dau_km = int(0)
    indstr = rxname
    sysid = indstr  # ("%s_%3.2fm" % (indstr, b_at))
    if rxcnf.DBF:
        sysid = f'{sysid}_DBF'

    if rxcnf.SCORE:
        sysid = f'{sysid}_SCORE'

    savedirr = os.path.join(main_dir, 'RESULTS', 'SARPERF', sysid)
    savedirr = os.path.join(savedirr, f'{dau_km:03d}km')
      #
    # mode = "stripmap"

    (incs, PRFs, proc_bw,
     steering_rates,
     burst_lengths, short_name, proc_tap, tau_p, bw_p) = mode_from_conf(conf, mode)
    n_swath = PRFs.size
    aasr_files = []
    rasr_files = []
    nesz_files = []
    mode_dirs = []
    for swth in range(n_swath):
        swth1 = swth + 1
        modeandswth = (f'{short_name}_sw{swth1:03d}')
        modedir = os.path.join(savedirr, modeandswth)
        mode_dirs.append(modedir)
        aasr_files.append(os.path.join(modedir, 'aasr.p'))
        nesz_files.append(os.path.join(modedir, 'nesz.p'))
        rasr_files.append(os.path.join(modedir, 'rasr.p'))
    nesz_file = os.path.join(savedirr, f'{short_name}_NESZ.p')
    aasr_file = os.path.join(savedirr, f'{short_name}_AASR.p')
    rasr_file = os.path.join(savedirr, f'{short_name}_RASR.p')

    filedict = {"root_dir": savedirr,
                "nesz": nesz_file,
                "aasr": aasr_file,
                "rasr": rasr_file,
                "neszs": nesz_files,
                "aasrs": aasr_files,
                "rasrs": rasr_files,
                "txname": txname,
                "rxname": rxname}
    return filedict
