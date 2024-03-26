__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

import glob
import os
import re

import numpy as np
import xarray as xr


# merge_luts definition
def merge_luts(datadir, pols=["HH", "VV"], model="KAlin", du=None):
    """Merge LUTs with ocean fwd model.

    Parameters
    ----------
    datadir : str
        Description of parameter `datadir`.
    pols : list
        Description of parameter `pols`.
    model : str
        Description of parameter `model`.
    du : list, ndarray or None
        By default the function will scan de directory for files and read them
        all. Pass a list of distances if only a subset of (known) satellite
        spacings is to be loaded

    Returns
    -------
    xarray.Dataset
        Merged dataset

    """
    if model == "WCAlin":
        print("Reading WCAlin fwmd model")
        datadir2 = os.path.join(datadir, "WCAlin")

    elif model == "SSAlin":
        print("Reading SSAlin fwmd model")
        datadir2 = os.path.join(datadir, "SSAlin")
    else:
        print("Reading KAlin fwmd model")
        model = "KAlin"  # to be sure!
        datadir2 = os.path.join(datadir, "KAlin")

    if du is None:
        fls = glob.glob(os.path.join(datadir2, "*cs*km.nc"))
        ds = []
        for fl in fls:
            ds.append(int(re.findall(r"([-]?\d+)km", fl)[0]))
        ds.append(0)
        du = np.unique(np.array(ds))
    # Read S1 data
    fs1 = xr.open_dataset(os.path.join(datadir2, "s1_%s.nc" % pols[0]))
    # incident angle
    incv = fs1.inc_Tx
    wspeedv = fs1.wind_sp
    wdirv = fs1.wind_dr
    waveagev = fs1.iwa
    nrcsm = []
    pol_cord = xr.DataArray(pols, coords=[("Pol", pols)])
    nrcsm = []
    inc_rx_m = []
    azi_rx_m = []
    dcam = []
    # dus = np.concatenate((-np.flip(np.array(du)),[0], np.array(du)))
    comp_sep = xr.DataArray(du, dims="Separation")
    for d_u in du:
        nrcsm_ = []
        dcam_ = []
        for pol in pols:
            if d_u < 0:
                satstr = "s1_cs2_%s_%ikm.nc" % (pol, int(d_u))
            elif d_u == 0:
                satstr = "s1_%s.nc" % pol
            else:
                satstr = "s1_cs1_%s_%ikm.nc" % (pol, int(d_u))
            fsn = xr.open_dataset(os.path.join(datadir2, satstr))
            # nrcsm_.append(fsn.nrcs_KAlin)
            nrcsm_.append(getattr(fsn, "nrcs_%s" % model))
            # dcam_.append(fsn.mean_doppler_KAlin)
            dcam_.append(getattr(fsn, "mean_doppler_%s" % model))
        inc_rx_m.append(fsn.inc_Rx)
        azi_rx_m.append(fsn.azi_Rx)
        nrcsm_ = xr.concat(nrcsm_, pol_cord)
        dcam_ = xr.concat(dcam_, pol_cord)
        nrcsm.append(nrcsm_)
        dcam.append(dcam_)
    nrcsm = xr.concat(nrcsm, comp_sep)
    dcam = xr.concat(dcam, comp_sep)
    inc_rx_m = xr.concat(inc_rx_m, comp_sep)
    azi_rx_m = xr.concat(azi_rx_m, comp_sep)
    # NRCS(waveages, polarizations, winddirections, windspeeds, incangles)
    nrcsm = nrcsm.transpose(
        "Separation",
        "IWaveAge",
        "Pol",
        "t",
        "WindDirection",
        "WindSpeed",
        transpose_coords=True,
    )
    dcam = dcam.transpose(
        "Separation",
        "IWaveAge",
        "Pol",
        "t",
        "WindDirection",
        "WindSpeed",
        transpose_coords=True,
    )
    merged_ds = xr.merge(
        [
            nrcsm,
            dcam,
            azi_rx_m,
            inc_rx_m,
            wspeedv,
            waveagev,
            wdirv,
            incv,
            {"at_distance": comp_sep},
        ]
    )
    return merged_ds


if __name__ == "__main__":
    main_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
    pardir = os.path.join(main_dir, "PAR")
    datadir = "/Users/plopezdekker/Documents/WORK/STEREOID/DATA/Ocean"
    fwd_lut = merge_luts(datadir, model="WCAlin")
    fwd_lut.at_distance
