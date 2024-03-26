import os
import re
import sys
import datetime
import logging

import netCDF4
import numpy as np

DIM_DIRECTION = 'wind_direction'
DIM_INCIDENCE = 'incidence'
DIM_1 = 'nc'
DIM_SAT = "sat"
DIM_POL = "pol"
DIM_GRG = 'grg'
DIM_AZ = 'az'
FILL_VALUE = 1.0e+36


# Define logger level for debug purposes
logger = logging.getLogger(__name__)

list_params_lut = ["incident_angle", "rx_ipc_name", "rx_cpc_name", "mode",
                   "az_res", "b_ati", "txpol", "rxpolbase",
                   "lambda_min", "lambda_max", "n_k"]

list_params_fwd = ["incident_angle", "rx_ipc_name", "rx_cpc_name", "mode",
                   "az_res", "b_ati", "txpol", "rxpolbase",
                   "lambda_min", "lambda_max", "n_k", "fetch", #"model",
                   "SAR_spectra_lambda_max", "SAR_spectra_looks"]


def set_global_attributes(fid: netCDF4.Dataset, list_params: list, par):
    for key in list_params:
        setattr(fid, key, getattr(par, key, None))


def write_params(params, pfile):
    """ Write parameters that have been selected to run swot_simulator. """
    with open(pfile, 'w') as f:
        for key in dir(params):
            if not key[0:2] == '__':
                f.write('{} = {}\n'.format(key, params.__dict__[key]))


def set_attributes():
    dic_attr = {}
    _tmp = 'Wind direction counter clockwise from the across track direction'
    dic_attr['wind_direction'] = {'long_name': _tmp,
                                  'unit': 'degree',
                                  'type': 'f4',
                                  'dimension': (DIM_DIRECTION,),
                                  'fill_value': FILL_VALUE}
    dic_attr['incidence'] = {'long_name': 'Incidence angle',
                             'unit': 'degree',
                             'type': 'f4',
                             'dimension': (DIM_INCIDENCE, ),
                             'fill_value': FILL_VALUE}
    dic_attr['wind_norm'] = {'long_name': 'Wind norm',
                             'unit': 'm/s',
                             'type': 'f4',
                             'dimension': (DIM_1,),
                             'fill_value': FILL_VALUE}
    dic_attr['fetch'] = {'long_name': 'Fetch distance',
                         'unit': 'degree',
                         'type': 'f4',
                         'dimension': (DIM_1,),
                         'fill_value': FILL_VALUE}

    dic_attr['wave_age'] = {'long_name': 'Inverse Wave age',
                            'unit': '',
                            'type': 'f4',
                            'dimension': (DIM_1,),
                            'fill_value': FILL_VALUE}
    dic_attr['longitude'] = {'long_name': 'Longitude',
                            'unit': 'degrees East',
                            'type': 'f4',
                            'dimension': (DIM_AZ, DIM_GRG),
                            'fill_value': FILL_VALUE}
    dic_attr['latitude'] = {'long_name': 'Latitude',
                            'unit': 'degrees North',
                            'type': 'f4',
                            'dimension': (DIM_AZ, DIM_GRG),
                            'fill_value': FILL_VALUE}
    dic_attr['inc'] = {'long_name': 'Incidence angle of transmitted signal.',
                            'unit': 'rad',
                            'type': 'f4',
                            'dimension': (DIM_GRG, DIM_SAT),
                            'fill_value': FILL_VALUE}
    dic_attr['bist_ang'] = {'long_name': 'Bistatic angle of companion.',
                            'unit': 'rad',
                            'type': 'f4',
                            'dimension': (DIM_GRG, DIM_SAT),
                            'fill_value': FILL_VALUE}
    dic_attr['wnd_u'] = {'long_name': 'Eastward wind componant',
                         'unit': 'm/s',
                         'type': 'f4',
                         'dimension': (DIM_AZ, DIM_GRG),
                         'fill_value': FILL_VALUE}

    dic_attr['wnd_v'] = {'long_name': 'Northward wind componant',
                         'unit': 'm/s',
                         'type': 'f4',
                         'dimension': (DIM_AZ, DIM_GRG),
                         'fill_value': FILL_VALUE}
    dic_attr['tsc_u'] = {'long_name': 'Eastward velocity componant',
                         'unit': 'm/s',
                         'type': 'f4',
                         'dimension': (DIM_AZ, DIM_GRG),
                         'fill_value': FILL_VALUE}
    dic_attr['tsc_v'] = {'long_name': 'Northward velocity componant',
                         'unit': 'm/s',
                         'type': 'f4',
                         'dimension': (DIM_AZ, DIM_GRG),
                         'fill_value': FILL_VALUE}
    dic_attr['sst'] = {'long_name': 'Sea Surface Temperature',
                         'unit': 'degC',
                         'type': 'f4',
                         'dimension': (DIM_AZ, DIM_GRG),
                         'fill_value': FILL_VALUE}
    dic_attr['dca'] = {'long_name': 'Doppler Centroid Anomaly',
                         'unit': 'Hz',
                         'type': 'f4',
                         'dimension': (DIM_AZ, DIM_GRG, DIM_SAT),
                         'fill_value': FILL_VALUE}
    return dic_attr


def save_lut(filename: str, dic: dict, dic_dim: dict, list_var: list):
    # : fetch: float, incidence: np.array):
    _path, _bn = os.path.split(filename)
    for phyvar in list_var:
        _filename = os.path.join(_path, f"{phyvar}_{_bn}")
        try:
            os.remove(_filename)
        except OSError:
            pass
        if phyvar == 'nrcs':
            _shp = dic['nrcs']['HB']['M'].shape
            unit = 'Linear'
            long_name = 'Backscatter for satellite'
        elif phyvar == 'dop':
            _shp = dic['dop']['HB']['M'].shape
            unit = 'Hz'
            long_name = 'Doppler for satellite'
        elif phyvar == 'imacs':
            _shp = dic['imacs']['HB']['M'].shape
            unit = ''
            long_name = 'imacs'
        elif phyvar == 'cut_off':
            _shp = dic['cut_off']['HB']['M'].shape
            unit = ''
            long_name = 'Cut-Off'
        else:
            unit = ''
            long_name = phyvar
        handler = netCDF4.Dataset(_filename, 'w')
        handler.createDimension(DIM_INCIDENCE, _shp[1])
        handler.createDimension(DIM_DIRECTION, _shp[0])
        handler.createDimension(DIM_1, 1)

        for sat in dic[phyvar].keys():
            if sat == "incidence":
                continue
            for pol in dic[phyvar][sat].keys():
                _name = f"{phyvar}_{sat}_{pol}"
                if phyvar == 'imacs':
                    _tmp = handler.createVariable(f'real_{_name[1:]}', 'f4',
                                                  (DIM_DIRECTION, DIM_INCIDENCE))
                    _tmp.unit = unit
                    _tmp.long_name = f"Real {long_name} {sat} with polarization {pol}"
                    _tmp[:] = np.real(dic[phyvar][sat][pol])
                    _tmp = handler.createVariable(f'imag_{_name[1:]}', 'f4',
                                                  (DIM_DIRECTION, DIM_INCIDENCE))
                    _tmp.unit = unit
                    _tmp.long_name = f"Imaginary {long_name} {sat} with polarization {pol}"
                    _tmp[:] = np.imag(dic[phyvar][sat][pol])
                else:

                    _tmp = handler.createVariable(_name, 'f4',
                                                  (DIM_DIRECTION, DIM_INCIDENCE))
                    _tmp.unit = unit
                    _tmp.long_name = f"{long_name} {sat} with polarization {pol}"
                    _tmp[:] = dic[phyvar][sat][pol]
        list_dim = ['incidence', 'wind_direction', 'wind_norm', 'fetch',
                    'wave_age']
        dicattr = set_attributes()
        for key in list_dim:
            _tmp = handler.createVariable(key, dicattr[key]['type'],
                                          dicattr[key]['dimension'])
            _tmp.unit = dicattr[key]['unit']
            _tmp.long_name = dicattr[key]['unit']
            try:
                _tmp[:] = dic_dim[key]
            except:
                msg = f'Wrong dimension with {key}, {len(dic_dim[key]):03d}'
                logger.debug(msg)
        handler.created_time = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
        handler.description = "Look up tables for Harmony project build using stereoid tools"

        handler.close()


def search_file(pattern: str, path: str, key: str):
    regex = re.compile(pattern).search
    listfile = []
    listwind = []
    listkey = []

    for dir_path, _, filenames in os.walk(path):
        for filename in filenames:
            match = regex(filename)
            if match:
                listfile.append(filename)
                listwind.append(int(match.group("wind")))
                listkey.append(int(match.group(key)))

    _ind = np.argsort(listfile)
    listfile = np.array(listfile)[_ind]
    listwind = np.array(listwind)[_ind]
    listkey = np.array(listkey)[_ind]
    return listfile, listwind, listkey


def aggregate_luts_fetch(_pat: str, _pattern: str, path: str):

    ofile = os.path.join(path, f'{_pat}.nc')
    try:
        os.remove(ofile)
    except OSError:
        pass

    pattern = _pattern
    listfile, listwind, listfetch = search_file(pattern, path, "fetch")

    _tmpdic = {}
    first = True
    if not listfile.size:
        logger.error(f'no file {pattern} found in {path}')
        sys.exit(1)
    for filename in listfile:
        handler = netCDF4.Dataset(os.path.join(path, filename), 'r')
        for key in handler.variables.keys():
            if first:
                _tmpdic[key] = {}
                _tmpdic[key]['array'] = []
                _tmpdic[key]['mask'] = []
            _var = np.ma.array(handler[key][:])
            if "dop" in key or "nrcs" in key:
                _shape = np.shape(_var)
            _mask = np.ma.getmaskarray(_var)
            _var = np.ma.masked_where((_mask | np.isnan(_var)), _var)
            _tmpdic[key]['array'].append(_var)
            _tmpdic[key]['mask'].append(_mask)
        if first:
            for attrname in handler[key].ncattrs():
                _tmpdic[key][attrname] = getattr(handler[key], attrname)
            metadata = {}
            for attrname in handler.ncattrs():
                metadata[attrname] = getattr(handler, attrname)
            listkey = list(handler.variables.keys())
        handler.close()
        first = False
    ddict = {}
    for key in listkey:
        ddict[key] = {}
        ddict[key]['_FillValue'] = FILL_VALUE
        ddict[key]['array'] = np.stack(_tmpdic[key]["array"])
        ddict[key]['array'][np.isnan(ddict[key]['array'])] = FILL_VALUE
        for attrname in _tmpdic[key].keys():
            if attrname == 'array' or attrname == 'mask':
                continue
            ddict[key][attrname] = _tmpdic[key][attrname]
    for key in ("incidence", "wind_direction"):
        ddict[key]["array"] = _tmpdic[key]["array"][0]
    ofid = netCDF4.Dataset(ofile, 'w')
    for key, value in metadata.items():
        setattr(ofid, key, value)
    for key in ddict.keys():
        _var = ddict[key]['array']
        if len(_var.shape) == 1 or _var.shape[1] == 1:
            if _var.shape[0] == _shape[1]:
                odim = ('incidence',)
            elif _var.shape[0] == _shape[0]:
                odim = ('direction',)
            elif _var.shape[0] == len(listfile):
                odim = ('wind_fetch')
        else:
            odim = ('wind_fetch', 'direction', 'incidence')
        if '_FillValue' in ddict[key].keys():
            fv = ddict[key]['_FillValue']
        else:
            fv = False
        _tmp = ofid.createVariable(key, _var.dtype, odim, fill_value=fv)
        for k, v in ddict[key].items():
            if k != 'array' and k != '_FillValue':
                setattr(_tmp, k, v)
        if _shape[1] == 1:
            _tmp[:] = _var[:, 0]
        else:
            _tmp[:] = _var
    ofid.close()


def aggregate_luts_iwa(_pat: str, pattern, path: str, global_attr = None):
    _file = _pat.rstrip('_')
    ofile = os.path.join(path, f'{_file}.nc')
    try:
        os.remove(ofile)
    except OSError:
        pass
    pattern = _pat + pattern
    listfile, listwind, listiwa = search_file(pattern, path, "iwa")
    print(ofile, listfile)
    _tmpdic = {}
    dicdim = {}
    listdim = ['incidence', 'wind_direction', 'wind_norm', 'wave_age']
    setlistwind = sorted(list(set(listwind)))
    setlistiwa = sorted(list(set(listiwa)))

    for i, wind in enumerate(setlistwind):
        for j, iwa in enumerate(setlistiwa):
            _ind = np.where((listwind == wind) & (listiwa == iwa))
            filename = listfile[_ind][0]
            handler = netCDF4.Dataset(os.path.join(path, filename), 'r')
            if i == 0 and j == 0:
                metadata = {}
                listkey = list(handler.variables.keys())
                for attrname in handler.ncattrs():
                    metadata[attrname] = getattr(handler, attrname)
                for ndim in listdim:
                    _var = np.ma.array(handler[ndim][:])
                    dicdim[ndim] = _var
                _shape = ((len(setlistwind), len(dicdim['wind_direction']),
                           len(dicdim['incidence']), len(setlistiwa)))
            for key in handler.variables.keys():
                _var = np.ma.array(handler[key][:])
                if i == 0 and j == 0:
                    _tmpdic[key] = {}
                    if key in listdim:
                        if _var.shape[0] > 1:
                            _tmpdic[key]['array'] = _var
                            _tmpdic[key]['mask'] = np.full(_var.shape, False)
                        else:
                            _tmpdic[key]['array'] = []
                            _tmpdic[key]['mask'] = []
                    if len(_var.shape) == 2:
                        _tmpdic[key]['array'] = np.full(_shape, np.nan)
                        _tmpdic[key]['mask'] = np.full(_shape, False)

                    for attrname in handler[key].ncattrs():
                        _tmpdic[key][attrname] = getattr(handler[key], attrname)
                _mask = np.ma.getmaskarray(_var)
                _var = np.ma.masked_where((_mask | np.isnan(_var)), _var)
                if any(item in key for item in ("dop", "nrcs", "macs", "cut_off")):
                    _tmpdic[key]['array'][i, :, :, j] = _var
                    _tmpdic[key]['mask'][i, :, :, j] = _mask
                else:
                    if (key == 'wind_norm' and j == 0) or (key == 'wave_age' and i == 0):
                        _tmpdic[key]['array'].append(_var)
                        _tmpdic[key]['mask'].append(_mask)
            handler.close()
    # _tmpdic['wind_norm']['array'] = np.array(setlistwind, dtype='float')
    # _tmpdic['wave_age']['array'] = np.array(setlistiwa, dtype='float')
    ddict = {}
    for key in listkey:
        if key == 'fetch':
            continue
        ddict[key] = {}
        ddict[key]['_FillValue'] = FILL_VALUE
        if key in listdim:
            if key in ('incidence', 'wind_direction'):
                ddict[key]['array'] = _tmpdic[key]["array"]
            else:
                ddict[key]['array'] = np.stack(_tmpdic[key]["array"])
        else:
            ddict[key]['array'] = _tmpdic[key]["array"]
            ddict[key]['array'][np.isnan(ddict[key]['array'])] = FILL_VALUE
        for attrname in _tmpdic[key].keys():
            if attrname == 'array' or attrname == 'mask':
                continue
            ddict[key][attrname] = _tmpdic[key][attrname]
    ofid = netCDF4.Dataset(ofile, 'w')
    for key in listdim:
        _tmp = ofid.createDimension(key, len(ddict[key]['array']))
    for key, value in metadata.items():
        setattr(ofid, key, value)
    for key in ddict.keys():
        _var = ddict[key]['array']
        _shape = _var.shape
        if key in listdim:
            odim = (key, )
        else:
            odim = ('wind_norm', 'wind_direction', 'incidence', 'wave_age')
        if '_FillValue' in ddict[key].keys():
            fv = ddict[key]['_FillValue']
        else:
            fv = False
        _tmp = ofid.createVariable(key, _var.dtype, odim, fill_value=fv)
        for k, v in ddict[key].items():
            if k != 'array' and k != '_FillValue':
                setattr(_tmp, k, v)
        _tmp[:] = _var
    if global_attr is not None:
        set_global_attributes(ofid, list_params_lut, global_attr)
    ofid.close()


def save_scene(filename: str, list_var: list, dic: dict, global_attr = None):
    try:
        os.remove(filename)
    except OSError:
        pass
    _path, _bn = os.path.split(filename)
    secondary_variables = ('longitude', 'latitude', 'inc', 'bist_ang')
    dicattr = set_attributes()
    for phyvar in list_var:
        _filename = os.path.join(_path, f"{phyvar}_L1_{_bn}")
        if phyvar == 'nrcs':
            _shp = dic['nrcs']['HB']['M'].shape
            unit = 'Linear'
            long_name = 'Backscatter for satellite'
        elif phyvar == 'dop':
            _shp = dic['dop']['HB']['M'].shape
            unit = 'Hz'
            long_name = 'Doppler for satellite'
        elif phyvar == 'imacs':
            _shp = dic['imacs']['HB']['M'].shape
            unit = ''
            long_name = 'imacs'
        elif phyvar == 'cut_off':
            _shp = dic['cut_off']['HB']['M'].shape
            unit = ''
            long_name = 'Cut-Off'
        else:
            unit = ''
            long_name = phyvar
        handler = netCDF4.Dataset(_filename, 'w')
        # Create the dimensions
        handler.createDimension(DIM_AZ, _shp[0])
        handler.createDimension(DIM_GRG, _shp[1])
        handler.createDimension(DIM_1, 1)
        handler.createDimension(DIM_SAT, 3)
        handler.createDimension(DIM_POL, 2)
        # Create the corresponding coordinate variables
        az = handler.createVariable(DIM_AZ, "f4", DIM_AZ)
        az[:] = dic[DIM_AZ]
        grg = handler.createVariable(DIM_GRG, "f4", DIM_GRG)
        grg[:] = dic[DIM_GRG]
        sat = handler.createVariable(DIM_SAT, np.dtype("U2"), DIM_SAT)
        phyvar_keys = list(dic[phyvar].keys())
        if "incidence" in phyvar_keys:
            phyvar_keys.remove("incidence")
        sat[:] = np.array(phyvar_keys, np.dtype("U2"))
        pol = handler.createVariable(DIM_POL, np.dtype("U1"), DIM_POL)
        pol[:] = np.array(tuple(dic[phyvar][phyvar_keys[1]]), np.dtype("U1"))
        current_ncvar = handler.createVariable(phyvar, 'f4', (DIM_AZ, DIM_GRG, DIM_SAT, DIM_POL))
        current_ncvar.unit = unit
        current_ncvar.long_name = long_name
        # FIXME: this is a dirty way to store the real part of the macs also
        if phyvar == "imacs":
            phyvar2="rmacs"
            current_ncvar2 = handler.createVariable(phyvar2, 'f4', (DIM_AZ, DIM_GRG, DIM_SAT, DIM_POL))
            current_ncvar2.unit = unit
            current_ncvar2.long_name = long_name
        for (i_sat, sat) in enumerate(dic[phyvar].keys()):
            if sat == "incidence":
                continue
            for (i_pol, pol) in enumerate(dic[phyvar][sat].keys()):
                if phyvar == "imacs":
                    current_ncvar[..., i_sat, i_pol] = np.imag(dic[phyvar][sat][pol])
                    current_ncvar2[..., i_sat, i_pol] = np.real(dic[phyvar][sat][pol])
                else:
                    current_ncvar[..., i_sat, i_pol] = dic[phyvar][sat][pol]
        for key in secondary_variables:
            _tmp = handler.createVariable(key, dicattr[key]['type'],
                                          dicattr[key]['dimension'])
            _tmp.unit = dicattr[key]['unit']
            _tmp.long_name = dicattr[key]['long_name']
            if key in ('longitude', 'latitude'):
                _tmp[:] = dic['model'][key]
            else:
                _tmp[:] = dic[key]

        handler.created_time = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
        handler.description = "L1 for Harmony project build using stereoid tools"
        if global_attr is not None:
            set_global_attributes(handler, list_params_fwd, global_attr)
        logger.info(f"Saved {phyvar} in {_filename}\n")
        handler.close()


def save_L2(filename: str, dic:dict, global_attr = None):
    try:
        os.remove(filename)
    except OSError:
        pass
    _path, _bn = os.path.split(filename)
    dicattr = set_attributes()
    handler = netCDF4.Dataset(filename, 'w')
    # Create the dimensions
    _shp = np.shape(dic['longitude'])
    handler.createDimension(DIM_AZ, _shp[0])
    handler.createDimension(DIM_GRG, _shp[1])
    for key in dic.keys():
        current_ncvar = handler.createVariable(key, 'f4', dicattr[key]['dimension'])
        current_ncvar[:] = dic[key][:]
        if key in dicattr.keys():
            current_ncvar.unit = dicattr[key]['unit']
            current_ncvar.long_name = dicattr[key]['long_name']
    handler.created_time = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    handler.description = "L2 for Harmony mission build using stereoid tools"
    if global_attr is not None:
        set_global_attributes(handler, list_params_fwd, global_attr)
    handler.close()
