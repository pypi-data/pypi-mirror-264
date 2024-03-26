import netCDF4
import pickle
from typing import Optional
import os
import numpy as np


def get_model_data(model_file: str, norm0: float, dir0: float, size: list
                   ) -> dict:
    if model_file is not None:
        _, ext = os.path.splitext(model_file)
        if ext == '.nc':
            dic = read_netcdf(model_file)
        else:
            _dic = read_pickle(model_file)
            dic = _dic['model']
        if "wnd_norm" not in dic.keys():
            dic["wnd_norm"] = np.sqrt(dic["wnd_u"]**2 + dic["wnd_v"]**2)
        if "wnd_dir" not in dic.keys():
            dic["wnd_dir"] = np.arctan2(dic["wnd_v"], dic["wnd_u"])
    else:
        dic = {}
        if norm0 is not None:
            dic['wnd_norm'] = numpy.full(size, norm0)
        else:
            dic['wnd_norm'] = None
        if dir0 is not None:
            dic['wnd_dir'] = numpy.full(size, par.dir0)
        else:
            dic['wnd_dir'] = None
    return dic



def read_pickle(ifile: str) -> dict:
    with open(ifile, 'rb') as f:
        dic = pickle.load(f)
    return dic


def read_netcdf(ifile: str, list_var: Optional[list] = None) -> dict:
    dic = {}
    handler = netCDF4.Dataset(ifile, 'r')
    if list_var is not None:
        _list = list_var
    else:
        _list = list(handler.variables.keys())
    for key in _list:
        dic[key] = handler[key][:]
    handler.close()
    return dic


def read_netcdf_old(ifile: str, var: str) -> dict:
    dic = {}
    handler = netCDF4.Dataset(ifile, 'r')
    for key in handler.variables.keys():
        if var in key:
            _key = key.split('_')
            pol = _key[-1]
            sat = _key[-2]
            if var not in dic.keys():
                dic[var] = {}
            if sat not in dic[var].keys():
                dic[var][sat] = {}
            dic[var][sat][pol] = handler[key][:]
        else:
            dic[key] = handler[key][:]
    handler.close()
    return dic
