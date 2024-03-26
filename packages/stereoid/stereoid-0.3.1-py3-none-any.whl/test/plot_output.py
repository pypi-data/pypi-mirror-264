import pickle
import argparse
import os
import sys
import numpy
import netCDF4
from typing import Optional

from matplotlib import pyplot


LPLOT = ["nrcs", "dop"]  # , 'cov']
LSAT = ["S1", "HA", "HB"]
VMIN = {"nrcs": 0, "dop": -80, "cov": 5}
VMAX = {"nrcs": 0.003, "dop": 80, "cov": -5}
MPLOT = ["tsc_u", "tsc_v", "wnd_u", "wnd_v", "sst"]
LISTDIM = ["wind_norm", "wind_direction", "incidence", "wave_age"]


def load_data(sfile: str, listdim: Optional[list] = LISTDIM,
              listvar: Optional[list] = []):
    path, basename = os.path.split(sfile)
    bname, ext = os.path.splitext(basename)
    print(path, bname, ext)
    if ext == ".nc":
        dic = {}
        for nlplot in LPLOT:
            _file = os.path.join(path, f"{nlplot}_{basename}")
            print(_file)
            handler = netCDF4.Dataset(_file, 'r')
            if "lon" in listdim:
                dic["model"] = {"lon": handler["lon"][:],
                                "lat": handler["lat"][:]}
            dic["dim"] = {}
            listvar = list(handler.variables.keys())
            for key in listdim:
                if key in listvar:
                    listvar.remove(key)
                dic["dim"][key] = handler[key][:]
            for vkey in listvar:
                nvar, nsat, npol = vkey.split('_')
                if nvar not in dic.keys():
                    dic[nvar] = {}
                if nsat not in dic[nvar].keys():
                    dic[nvar][nsat] = {}
                dic[nvar][nsat][npol] = handler[vkey][:]
            handler.close()
    else:
        with open(sfile, "rb") as f:
            dic = pickle.load(f)
    dic["bname"] = bname
    return dic


def plot_subplot(key: str, dic: dict, lon: numpy.ndarray, lat: numpy.ndarray,
                 indi: Optional[int] = 0, indj: Optional[int] = 0,
                 dmin: Optional[dict] = None, dmax: Optional[dict] = None):
    fig, ax = pyplot.subplots(2, 3, figsize=(20, 10))
    fig.suptitle(f"{key}")
    _min = None
    _max = None
    if dmin is not None:
        _min = dmin[key]
    if dmax is not None:
        _max = dmax[key]
    for i, isat in enumerate(LSAT):
        if isat == "incidence":
            continue
        pol = list(dic[key][isat].keys())
        if "incidence" in pol:
            pol.remove("incidence")
        for j, ipol in enumerate(pol):
            _var = dic[key][isat][ipol]
            if len(_var.shape) > 2:
                _var = _var[indi, :, :, indj]
            C = ax[j][i].pcolormesh(
                lon, lat, _var, vmin=_min, vmax=_max
            )
            ax[j][i].set_title(f"{isat} {ipol}")
            pyplot.colorbar(C, ax=ax[j][i])
    return fig


def plot_lut(sfile: str, output_dir: str, list_plot: list,
             dmin: Optional[dict] = None, dmax: Optional[dict] = None):
    dic = load_data(sfile)
    _shape = (len(dic["dim"]["wind_norm"]), len(dic["dim"]["wind_direction"]),
              len(dic["dim"]["incidence"]), len(dic["dim"]["wave_age"]))
    lat = dic["dim"]["wind_direction"]
    lon = dic["dim"]["incidence"]
    for i in range(_shape[0]):
        for j in range(_shape[-1]):
            for key in list_plot:
                fig = plot_subplot(key, dic, lon, lat, indi=i, indj=j,
                                  dmin=dmin, dmax=dmax)
                wn = dic["dim"]["wind_norm"][i]
                wa = dic["dim"]["wave_age"][j]
                fig.suptitle(f"{key} {wn:.1f} m/s wind, {wa:.3f} wave age")
                wn = int(wn)
                wa = int(wa*100)
                _name = f'{key}_{dic["bname"]}_wind_{wn:02d}_wave_{wa:03d}.png'
                pyplot.savefig(os.path.join(output_dir, _name))


def plot_output(
    sfile: str,
    output_dir: str,
    list_plot: list,
    dmin: Optional[dict] = None,
    dmax: Optional[dict] = None,
):
    dic = load_data(sfile)
    lon = dic["model"]["lon"]
    lat = dic["model"]["lat"]
    for key in list_plot:
        fig = plot_subplot(key, dic, lon, lat, indi=0, indj=0,
                          dmin=dmin, dmax=dmax)
        pyplot.savefig(os.path.join(output_dir, f'{key}_{dic["bname"]}.png'))


def plot_model(
    sfile: str,
    output_dir: str,
    list_plot: list,
    dmin: Optional[dict] = None,
    dmax: Optional[dict] = None,
):
    dic = load_data(sfile)
    lon = dic["model"]["lon"]
    lat = dic["model"]["lat"]
    ni = 2
    nj = 3
    fig, ax = pyplot.subplots(ni, nj, figsize=(20, 10))
    for count, key in enumerate(list_plot):
        fig.suptitle("Model")
        _min = None
        _max = None
        if dmin is not None:
            _min = dmin[key]
        if dmax is not None:
            _max = dmax[key]
        i = count % nj
        j = int(count / nj)
        C = ax[j][i].pcolormesh(lon, lat, dic["model"][key], vmin=_min, vmax=_max)
        ax[j][i].set_title(key)
        pyplot.colorbar(C, ax=ax[j][i])

    pyplot.savefig(os.path.join(output_dir, f'model_{dic["bname"]}.png'))


if __name__ == "__main__":
    import stereoid.utils.tools as tools

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "params_file",
        nargs="?",
        type=str,
        default=None,
        help="Path of the parameters file",
    )
    args = parser.parse_args()
    if args.params_file is None:
        print("Please specify a parameter file")
        sys.exit(1)
    p = tools.load_python_file(args.params_file)
    test_dir = p.resdir / "swb_tests"
    test_dir.mkdir(exist_ok=True)
    #test_dir = "/tmp"
    print(f"Saving figures in {test_dir}.")
    if "lut" in args.params_file:
        print("Compute Plots for lut")
        #plot_lut(f"{p.obs_file}.nc", test_dir, ["nrcs", ], dmin=VMIN, dmax=VMAX)
        plot_lut(f"{p.obs_file}.nc", test_dir, ["dop", ], dmin=VMIN, dmax=VMAX)
    else:
        plot_output(f"{p.obs_file}.pyo", test_dir, LPLOT)
        #sarplot = ["emacs", "cut_off"]  # , 'cov']
        #plot_output(f"{p.obs_file}_sar.pyo", test_dir, sarplot)
        plot_model(f"{p.obs_file}.pyo", test_dir, MPLOT)
