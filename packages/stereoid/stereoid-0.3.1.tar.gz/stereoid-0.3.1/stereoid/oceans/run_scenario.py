import os
import logging
import pickle

import numpy
import xarray as xr
from scipy.signal import convolve2d
from scipy.ndimage import median_filter
#from scipy.interpolate import RBFInterpolator
import drama.utils.resample as dr_resample

import stereoid.oceans.read_scenario_California as read_scenario_California
import stereoid.oceans.read_scenarios as read_scenarios
import stereoid.oceans.tools.scene_tools as scene_tools
import stereoid.oceans.tools.spectrum_tools as spectrum_tools
import stereoid.oceans.tools.backscatter_doppler_tools as bkscatter_doppler
import stereoid.oceans.tools.observation_tools as obs_tools
import stereoid.oceans.tools.write_tools as write_tools
import stereoid.oceans.tools.read_tools as read_tools

# Define logger level for debug purposes
logger = logging.getLogger(__name__)
logging.getLogger('numba').setLevel(logging.WARNING)


def tolist(x):
    if isinstance(x, list):
        return x
    else:
        return [x]


def make_default(p):
    p.noise = getattr(p, 'noise', False)
    p.progress_bar = getattr(p, 'progress_bar', True)
    p.nprocessor = getattr(p, 'nprocessor', 18)

    # Geometry
    p.dau = getattr(p, 'dau', 400E3)
    p.incident_angle = getattr(p, 'incident_angle', 31)

    # Mode for SAR
    p.parfile = getattr(p, 'parfile', 'Hrmny_2021_1.cfg')
    p.rx_ipc_name = getattr(p, 'rx_ipc_name', "tud_2020_tripple_ati")
    p.rx_cpc_name = getattr(p, 'rx_cpc_name', "tud_2020_tripple")
    # az_res_dct = {"WM": 5, "IWS": 20}
    # mode =
    # az_res = az_res_dct[mode]
    # b_ati = 9

    # Polarization
    p.txpol = getattr(p, 'txpol', 'V')
    p.rxpolbase = getattr(p, 'rxpolbase', 'mM')

    # Wave spectral parameters
    p.lambda_range = getattr(p, 'lambda_range', None)
    if p.lambda_range is None:
        p.lambda_min = getattr(p, 'lambda_min', None)
        p.lambda_max = getattr(p, 'lambda_max', None)
        p.n_k = getattr(p, 'n_k', None)
        p.lambda_range = (p.lambda_min, p.lambda_max, p.n_k)
    if None in p.lambda_range:
        p.lambda_range = getattr(p, 'lambda_range', (0.01, 1000, 200))
    p.lambda_min, p.lambda_max, p.n_k = p.lambda_range

    # SAR spectrum parameters
    p.SAR_spectra_lambda_max = getattr(p, "SAR_spectra_lambda_max", 2000)
    p.spec_samp = tolist(getattr(p, 'spec_samp', [10, 10]))
    if len(p.spec_samp) < 2:
        p.spec_samp = [p.spec_samp[0], p.spec_samp[0]]
    p.SAR_spectra_looks = getattr(p, "SAR_spectra_looks", 25)

    # Output parameters
    p.main_out = getattr(p, 'main_out', './')
    p.obs_nonoise_file = getattr(p, 'obs_nonoise_file', 'default_harmony')
    p.obs_file = getattr(p, 'obs_file', 'default_harmony')
    lvariable = ["Doppler", "Backscatter", "imacs", "cut_off"]
    p.list_variable = getattr(p, 'list_variable', lvariable)
    p.model_reader = getattr(p, "model_reader", "California")
    p.l1_resolution = getattr(p, "l1_resolution", 1E3)


def make_default_lut(p):
    # LUT
    p.lut_wind_range = getattr(p, 'lut_wind_range', (4, 25, 1))
    p.lut_iwa_range = getattr(p, 'lut_iwa_range', (0.84, 2, 0.05))
    p.lut_incidence_range = getattr(p, 'lut_incidence_range', (250e3, 10))
    p.save_iwa = getattr(p, 'save_iwa', True)


def make_default_fwd(p):
    # Dynamical model parameters
    p.model_run = getattr(p, 'model_run', 'California')
    p.scn_file = getattr(p, 'scn_file', 'ocean_lionel.mat')
    p.sizeaz = getattr(p, 'sizeaz', [200E3, 210E3])
    p.sizer = getattr(p, 'sizer', [300E3, 310E3])

    # Wave model parameters
    p.run = getattr(p, 'run', 'R13')
    _dirf = os.path.join('stereoid', 'assets', 'test',
                         f'specCal_{p.run}.xarray')
    p.swan_file = getattr(p, 'swan_file', _dirf)
    p.read_from_netcdf = getattr(p, 'read_from_netcdf', False)
    p.fetch = getattr(p, 'fetch', 100e3)
    p.k_l = getattr(p, 'k_l', None)


def make_default_inv(p):
    p.dx = getattr(p, 'dx', 1)
    p.spec_samp = tolist(getattr(p, 'spec_samp', [10, 10]))
    if len(p.spec_samp) < 2:
        p.spec_samp = [p.spec_samp[0], p.spec_samp[0]]
    p.sigma_imacs = getattr(p, 'sigma_imacs', [2E-6, 8E-6])
    p.sigma_dir0 = getattr(p, 'sigma_dir0', [1, 10])
    p.sigma_norm0 = getattr(p, 'sigma_norm0', [1.7, 0.8])
    p.pyramid_factor = getattr(p, 'pyramid_factor', [10, 1])
    p.fetch = getattr(p, 'fetch', 500E3)
    p.model_file = getattr(p, 'model_file', None)
    p.norm0 = getattr(p, 'norm0', None)
    p.dir0 = getattr(p, 'dir0', None)
    p.threshold_cost = getattr(p, 'threshold_cost', 40)
    p.threshold_nrcs = getattr(p, 'threshold_nrcs', 1)
    p.filter_nrcs_length = getattr(p, 'filter_nrcs_length', 5)
    p.weight_imacs = getattr(p, 'weight_imacs', [[0.5, 1., 1.], [1., 1., 1.]])
    p.weight_nrcs = getattr(p, 'weight_nrcs', [[0.5, 1., 1.], [1., 1., 1.]])


def run_stereoid_fwd(par):
    logger.info("Build observation and geometry")
    make_default(par)
    make_default_fwd(par)
    # Observation geometry
    incident = numpy.deg2rad(par.incident_angle)
    obs_geo = obs_tools.build_geometry(par.parfile, incident, dau=par.dau)

    # Observation Performance
    fstr_dual, fstr_ati, fstr_s1 = obs_tools.build_performance_file(par)

    # Read model Data and SWAN spectra
    logger.info("Read model Data")
    sizeaz = par.sizeaz
    sizer = par.sizer
    rot_angle = par.rot_angle
    model_readers = {"California" : read_scenario_California.read_scenario_California,
                     "DALES": read_scenarios.read_scenario_DALES_KNMI}
    model, _ = scene_tools.read_scene(par.scn_file, (sizeaz, sizer),
                                      model_readers[par.model_reader], rot_angle,
                                      l1_resolution=par.l1_resolution)
    model_shape = model["sst"].shape
    if par.read_from_netcdf:
        swan_nc_file = scene_tools.construct_swan_filepath(
            par.swan_file, par.swan_dir, sizeaz, sizer
        )
        logger.info(f"Read SWAN spectra from netCDF file at {par.swan_as_nc}")
        ws = xr.open_dataset(swan_nc_file)
    else:
        logger.info("Read SWAN spectra from SWAN model.")
        ws = scene_tools.read_swan_spectra(par.swan_file, sizeaz, sizer,
                                           par.swan_as_nc, rot_angle)
        ind = numpy.isnan(ws['efth'][0, :, 0, 0].values)
        ws['efth'][0, ind, :, :] = ws['efth'][0, 0, :, :]
        # find the index of the first element that is not nan
        not_nan_index = (~ind).nonzero()[0][0]
        # nonzero returns a tuple of an array so index twice
        ws['efth'][0, ind, :, :] = ws['efth'][0, not_nan_index, :, :]
    # adjust observation geometry to match the width of model's swath
    shp1 = model_shape[1]
    _spac = numpy.arange(shp1).reshape((1, shp1)) * model["dx"]
    # set_swath modifies the properties of obs_geo!
    obs_geo.concordia.set_swath(incident, _spac)
    obs_geo.discordia.set_swath(incident, _spac)

    # Spectrum for short waves
    logger.info("Spectrum for short waves")
    mod_transfer, wn = spectrum_tools.spectrum_short_waves_swan(
        model, par.lambda_min, par.lambda_max, par.n_k, fetch=par.fetch
    )

    # Polarimetric bistatics backscatter and Doppler
    dic_geometry = {"inc": numpy.stack((obs_geo.concordia.inc_m[0],
                                        obs_geo.concordia.inc_b[0],
                                        obs_geo.discordia.inc_b[0]), axis=-1),
                    "bist_ang": numpy.stack((numpy.zeros_like(obs_geo.concordia.bist_ang[0]),
                                             obs_geo.concordia.bist_ang[0],
                                             obs_geo.discordia.bist_ang[0]),
                                            axis=-1),
                    "grg": obs_geo.concordia.gr[0],
                    "az": numpy.arange(0, model_shape[0], 1) * model["dy"],
                    }
    if any(item in par.list_variable for item in ("Doppler", "Backscatter")):
        logger.info("Polarimetrics backscatter and Doppler")
        _res = bkscatter_doppler.backscatter_doppler(
            ws,
            model,
            obs_geo,
            mod_transfer,
            wn,
            spec_type=par.spec_type_doppler_backscatter,
            pol=par.txpol,
            rxpol=par.rxpolbase,
            progress_bar=par.progress_bar,
            fetch=par.fetch,
            k_l=par.k_l,
            add_current_Doppler=par.add_current_Doppler
        )
        nrcsd, covd, dopd, q = _res
        os.makedirs(par.main_out, exist_ok=True)
        # Co and cross backscatter and Doppler
        # TODO we ll use the monoeq2bistatic function to create the covariance
        # matrices with the correct correlation between the polarizations
        # We ll also have to think a bit how we treat the noise, which is now
        # implemented for the diagonal elements of the covariance but not for
        # the cross terms, where the expected value is zero but the variance
        # isn't.
        # A bit of thinking and validation required.

        dic_final = {"wn": wn, "model": model, "nrcs": nrcsd,
                     "dop": dopd, "cov": covd}
        dic_final |= dic_geometry
        nfile = f"{par.obs_nonoise_file}.pyo"
        with open(nfile, "wb") as pf:
            pickle.dump(dic_final, pf)
        nfile = f"{par.obs_nonoise_file}.nc"
        write_tools.save_scene(nfile, ("nrcs", "dop"), dic_final,
                               global_attr=par)
        _str = "\nSaved the NRCS and Doppler"
        logger.info(f"{_str} in:\n{os.path.dirname(nfile)}.\n")
        if par.noise is True:
            # REVIEW I'm only passing one of the two ObsGeos. Should we
            # consider both geometries for the noise?
            dgeom = {
                "obs_geo": obs_geo.concordia,
                "fstr_dual": fstr_dual,
                "fstr_ati": fstr_ati,
                "fstr_s1": fstr_s1,
            }
            nrcsd_o, dopd_o, isv_o, dgeom = bkscatter_doppler.add_noise(
                nrcsd, dopd, model["dx"], par, dic_geom=dgeom
            )

            dic_final["nrcs"] = nrcsd_o
            dic_final["dop"] = dopd_o

        nfile = f"{par.obs_file}.pyo"
        with open(nfile, "wb") as pf:
            pickle.dump(dic_final, pf)
        nfile = f"{par.obs_file}.nc"
        write_tools.save_scene(nfile, ("nrcs", "dop"), dic_final,
                               global_attr=par)
        _str = "\nSaved the NRCS and Doppler with noise"
        logger.info(f"{_str} in:\n{os.path.dirname(nfile)}.\n")
        # Save model data in netcdf
        nfile = f'{par.obs_file}_model.nc'
        par.description = "Model interpolated on swath"
        dicm = {}
        list_model_key = ("longitude", "latitude", "sst", "tsc_v", "tsc_u", "wnd_u",
                          "wnd_v")
        for key in list_model_key:
            dicm[key] = dic_final["model"][key]
            write_tools.save_L2(nfile, dicm, global_attr=par)
    dic_geometry_s = {}
    for key in dic_geometry.keys():
        dic_geometry_s[key] = dic_geometry[key][::par.spec_samp[1]]
    # Polarimetric SAR co-spectra, cross-spectra imacs and cut_off
    if any(item in par.list_variable for item in ("imacs", "cut_off")):
        logger.info("SAR co-spectra, cross-spectra, Emacs and Cut Off")
        _msar = spectrum_tools.make_SAR_spectra
        _specres = _msar(ws, model, obs_geo, mod_transfer, wn, par.spec_samp,
                         par.SAR_spectra_lambda_max, par.SAR_spectra_looks,
                         pol=par.txpol, rxpol=par.rxpolbase, swell=False,
                         spec_type=par.spec_type_imacs_cutoff,
                         fetch=par.fetch, k_l=par.k_l, progress_bar=True)
        for key in ("longitude", "latitude"):
            model[key] = _specres[5][key]
        dic_final = {"wn": wn, "model": model, "cospectrum": _specres[0],
                     "cross-spectrum": _specres[1],
                     "imacs": _specres[2], "cut_off": _specres[3]}
        dic_final |= dic_geometry_s
        nfile = f"{par.obs_file}_sar.pyo"
        with open(nfile, "wb") as pf:
            pickle.dump(dic_final, pf)
        nfile = f"{par.obs_file}.nc"
        write_tools.save_scene(nfile, ("imacs", "cut_off"), dic_final,
                               global_attr=par)
        _text = f"\nSaved imacs and cut_off in:\n{os.path.dirname(nfile)}.\n"
        logger.info(_text)

        # TODO return _specres


def run_partition_swan(par, partition: bool):
    if partition:
        logger.debug('Partitioning the SWAN dataset.')
        sizeaz = par.sizeaz
        sizer = par.sizer
        ws = scene_tools.partition_swan_spectra(par.swan_file, par.swan_dir,
                                                sizeaz, sizer)
    else:
        import wavespectra
        logger.debug('Converting the entire SWAN dataset to netCDF.')
        ws = wavespectra.read_swan(par.swan_file, dirorder=True, as_site=True)
        out_file = scene_tools.construct_swan_filepath(par.swan_file,
                                                       par.swan_dir,
                                                       None, None)
        logger.debug(f'Saving output to netcdf at {out_file}')
        ws.to_netcdf(out_file)
        logger.info('Finished reading SWAN spectra')


def compute_lut(par):
    import multiprocessing
    make_default(par)
    make_default_lut(par)
    THREADS = par.nprocessor
    pool = multiprocessing.Pool(THREADS)

    logger.info("Build observation and geometry")
    # Observation geometry
    incident = numpy.deg2rad(par.incident_angle)
    obs_geo = obs_tools.build_geometry(par.parfile, incident,
                                       dau=par.dau)

    logger.debug("Prepare jobs")

    # Specification for the case of the LUT:
    range_length, nb_points = par.lut_incidence_range
    list_key_param = ["lambda_min", "lambda_max", "n_k", "txpol", "rxpolbase",
                      "progress_bar", "obs_nonoise_file", "main_out",
                      "save_iwa", "spec_samp", "list_variable",
                      "SAR_spectra_lambda_max", "SAR_spectra_looks", "k_l"]
    from_param = {}
    for key in list_key_param:
        from_param[key] = getattr(par, key)
    # inverses wave age
    iwa = numpy.arange(par.lut_iwa_range[0], par.lut_iwa_range[1],
                       par.lut_iwa_range[2])

    _spac = numpy.linspace(0, range_length,
                           num=nb_points).reshape((1, nb_points))
    # set_swath modifies the properties of obs_geo!
    obs_geo.concordia.set_swath(incident, _spac)
    obs_geo.discordia.set_swath(incident, _spac)
    jobs = []
    wi = par.lut_wind_range
    logger.debug("Launch jobs")
    for _wnd_norm in range(wi[0], wi[1], wi[2]):
        for _iwa in iwa:
            job = (_wnd_norm, _iwa, nb_points, from_param, obs_geo)
            jobs.append(job)
    pool.map(worker_lut, jobs)
    pool.close()
    _path,  _file = os.path.split(par.obs_file)
    if par.save_iwa is False:
        pattern = "wind_(?P<wind>\d{2})_fetch_(?P<fetch>\d{6}).nc"
        if "Doppler" in par.list_variable:
            _pat = f"dop_{_file}"
            write_tools.aggregate_luts_fetch(_pat, pattern, par.main_out)
        if "Backscatter" in par.list_variable:
            _pat = f"nrcs_{_file}"
            write_tools.aggregate_luts_fetch(_pat, pattern, par.main_out)
        if "imacs" in par.list_variable:
            _pat = f"imacs_{_file}"
            write_tools.aggregate_luts_fetch(_pat, pattern, par.main_out)
        if "cut_off" in par.list_variable:
            _pat = f"cut_off_{_file}"
            write_tools.aggregate_luts_fetch(_pat, pattern, par.main_out)

    else:
        pattern = "wind_(?P<wind>\d{2})_iwa_(?P<iwa>\d{3}).nc"
        if "Doppler" in par.list_variable:
            _pat = f"dop_{_file}"
            write_tools.aggregate_luts_iwa(_pat, pattern, par.main_out)
        if "Backscatter" in par.list_variable:
            _pat = f"nrcs_{_file}"
            write_tools.aggregate_luts_iwa(_pat, pattern, par.main_out)
        if "imacs" in par.list_variable:
            _pat = f"imacs_{_file}"
            write_tools.aggregate_luts_iwa(_pat, pattern, par.main_out)
        if "cut_off" in par.list_variable:
            _pat = f"cut_off_{_file}"
            write_tools.aggregate_luts_iwa(_pat, pattern, par.main_out)


def worker_lut(*args):
    _wnd_norm, _iwa, nb_points, par, obs_geo = args[0]
    # dimensionless fetch scalar
    X_0 = 22E3
    g = 9.81
    # compute fetch from iwa
    X = numpy.arctanh((_iwa / 0.84) ** (-1/0.75)) ** (1 / 0.4) * X_0
    k_0 = g / _wnd_norm ** 2
    fetch = X / k_0
    ws = None
    if ~numpy.isfinite(fetch):
        return None

    # model dict should contain wnd_u, wnd_v, wnd_norm, wnd_anomaly
    model = scene_tools.generate_wind(nb_points, _wnd_norm)
    # Spectrum for short waves
    logger.info("Spectrum for short waves")
    mod_transfer, wn = spectrum_tools.spectrum_short_waves_swan(
        model, par["lambda_min"], par["lambda_max"], par["n_k"], fetch=fetch
    )
    # override model transfer functions
    # FIXME: I do not think this is really necessary, but it is a precaution
    mod_transfer['ux'] = numpy.zeros(mod_transfer['ux'].shape)
    mod_transfer['uy'] = numpy.zeros(mod_transfer['ux'].shape)
    mod_transfer['vx'] = numpy.zeros(mod_transfer['ux'].shape)
    mod_transfer['vy'] = numpy.zeros(mod_transfer['ux'].shape)



    iwn = int(_wnd_norm)
    fm = int(fetch)
    wan = int(_iwa*100)
    _obsf = par["obs_nonoise_file"]

    # Polarimetric bistatics backscatter and Doppler
    if any(ite in par["list_variable"] for ite in ("Doppler", "Backscatter")):
        logger.info("Polarimetrics backscatter and Doppler")
        _res = bkscatter_doppler.backscatter_doppler(
            ws,
            model,
            obs_geo,
            mod_transfer,
            wn,
            pol=par["txpol"],
            spec_type="LUT",
            rxpol=par["rxpolbase"],
            progress_bar=par["progress_bar"],
            fetch=fetch,
            k_l=par["k_l"]
        )
        # nrcs_mono, dop_mono, q, nrcs_bi1, dop_bi1, nrcs_bi2, dop_bi2 = _res
        nrcsd, covd, dopd, q = _res

        os.makedirs(par["main_out"], exist_ok=True)
        # Co and cross backscatter and Doppler
        # TODO we will use the monoeq2bistatic function to create the
        # covariance matrices with the correct correlation between the
        # polarizations
        # We will also have to think a bit how we treat the noise, which is now
        # implemented for the diagonal elements of the covariance but not for
        # the cross terms, where the expected value is zero but the variance
        # isn't.
        # A bit of thinking and validation required.
        incidence = numpy.rad2deg(nrcsd["incidence"])
        nrcsd.pop("incidence", None)

        dic_final = {"wn": wn, "model": model, "nrcs": nrcsd, "dop": dopd,
                     "cov": covd}
        wnd_dir = numpy.rad2deg(dic_final['model']['wnd_dir'][:, 0])
        dic_dim = {'wind_direction': wnd_dir,
                   'incidence': incidence,
                   'wind_norm': dic_final['model']['wnd_norm'][0, 0],
                   'fetch': fetch,
                   'wave_age': _iwa,
                   }
        if par["save_iwa"]:
            _pat = f"{_obsf}wind_{iwn:02d}_iwa_{wan:03d}"
        else:
            _pat = f"{_obsf}wind_{iwn:02d}_fetch_{fm:06d}"
        # nfile = f"{_pat}.pyo"
        # with open(nfile, "wb") as pf:
        #    pickle.dump(dic_final, pf)
        nfile = f"{_pat}.nc"
        write_tools.save_lut(nfile, dic_final, dic_dim, ["nrcs", "dop"])
    if any(item in par["list_variable"] for item in ("imacs", "cut_off")):
        logger.info("SAR co-spectra, cross-spectra, Emacs and Cut Off")
        _msar = spectrum_tools.make_SAR_spectra
        _specres = _msar(ws, model, obs_geo, mod_transfer, wn,
                         par["spec_samp"], par["SAR_spectra_lambda_max"],
                         par["SAR_spectra_looks"], pol=par["txpol"],
                         rxpol=par["rxpolbase"], swell=False,
                         spec_type="LUT", fetch=fetch, k_l=par["k_l"],
                         noise=False, progress_bar=True)
        dic_final = {"wn": wn, "model": model, "cospectrum": _specres[0],
                     "cross-spectrum": _specres[1],
                     "imacs": _specres[2], "cut_off": _specres[3]}
        wnd_dir = numpy.rad2deg(dic_final['model']['wnd_dir'][:, 0])
        dic_dim = {'wind_direction': wnd_dir,
                   'incidence': numpy.rad2deg(_specres[4]),
                   'wind_norm': dic_final['model']['wnd_norm'][0, 0],
                   'fetch': fetch,
                   'wave_age': _iwa,
                   }
        if par["save_iwa"]:
            _pat = f"{_obsf}wind_{iwn:02d}_iwa_{wan:03d}"
        else:
            _pat = f"{_obsf}wind_{iwn:02d}_fetch_{fm:06d}"
        nfile = f"{_pat}.nc"
        write_tools.save_lut(nfile, dic_final, dic_dim, ["imacs", "cut_off"])

def conv2(x, y, mode='same'):
    return numpy.rot90(convolve2d(numpy.rot90(x, 2), numpy.rot90(y, 2), mode=mode), 2)

def run_inversion(par):
    ''' reconstruct wind and current using inversion algorithm '''
    import stereoid.oceans.tools.retrieval_tools as retrieval_tools
    make_default_inv(par)

    # # -- Read Lut
    logger.info('Read LUT')
    list_lut = {}
    for key in ('nrcs', 'dop', 'imacs', 'cut_off'):
        slut = f'{key}_{par.lut_pattern}'
        list_lut[key] = {'file': os.path.join(par.lut_directory, slut)}
    _lut = retrieval_tools.read_lut(list_lut)

    # # -- Read data
    logger.info('Read Data')
    dic_l1 = {}
    for key in ('nrcs', 'imacs', 'dop', 'cut_off'):
        _pat = os.path.join(par.data_directory, f'{par.data_pattern[key]}')
        dic_l1[key], lon, lat, inc = retrieval_tools.read_L1(_pat, key, normalise_imacs=par.normalise_imacs)
        if key == 'nrcs':
            longitude = + lon
            latitude = + lat
            incident = + numpy.array(inc)
    for key, value in dic_l1.items():
        # the imacs and cutoff have to be resampled as they are generated on a lower resolution than the NRCS
        if key == 'cut_off' or key == 'imacs':
            resampled_array = numpy.zeros_like(dic_l1["nrcs"])

            for i_sat in range(value.shape[2]):
                for i_pol in range(value.shape[3]):

                    # this gives the opportunity to filter the imacs and cutoff before resampling
                    if par.filt_imacs != None and key == 'imacs':

                        if par.filt_type == 'median':
                            dic_l1[key][..., i_sat, i_pol] = median_filter(dic_l1[key][..., i_sat, i_pol],
                                                                           (par.filt_imacs, par.filt_imacs))
                        else:
                            sig = par.filt_imacs*1.
                            n = numpy.arange(-3 * sig, 3 * sig + 1)
                            filt = numpy.outer(numpy.exp(-0.5 * n ** 2 / sig ** 2), numpy.exp(-0.5 * n ** 2 / sig ** 2))
                            filt = filt / numpy.sum(filt)
                            dic_l1[key][..., i_sat, i_pol]=conv2(dic_l1[key][..., i_sat, i_pol],filt,'same')

                    if par.filt_cutoff != None and key == 'cut_off':
                        if par.filt_type == 'median':
                            dic_l1[key][..., i_sat, i_pol] = median_filter(dic_l1[key][..., i_sat, i_pol],
                                                                       (par.filt_cutoff, par.filt_cutoff))
                        else:
                            sig = par.filt_cutoff*1.
                            n = numpy.arange(-3 * sig, 3 * sig + 1)
                            filt = numpy.outer(numpy.exp(-0.5 * n ** 2 / sig ** 2), numpy.exp(-0.5 * n ** 2 / sig ** 2))
                            filt = filt / numpy.sum(filt)
                            dic_l1[key][..., i_sat, i_pol]=conv2(dic_l1[key][..., i_sat, i_pol],filt,'same')

                    # this removes the iwa dependence, so that cut_off is not used in the minimization
                    if par.no_iwa == 1 and key == 'cut_off':
                        dic_l1[key][..., i_sat, i_pol]=0
                        print('Warning! No iwa considered. Only for retrieval type 2.')



                    # resampling of the imacs and cutoff
                    resampled_array[..., i_sat, i_pol] = dr_resample.lincongrid2d(dic_l1[key][..., i_sat, i_pol], dic_l1["nrcs"].shape[0:2])
            dic_l1[key] = resampled_array

    # # -- Read Model
    logger.info('Read Model')
    dic_model = read_tools.get_model_data(par.model_file, par.norm0, par.dir0,
                                          longitude.shape)

    # # -- Compute Geometry
    logger.info('Compute Geometry')
    obs_geo = obs_tools.build_geometry(par.parfile, incident, dau=par.dau)

    # # -- Initialize retrieval
    logger.info('Retrieve wind and currents')
    fwdm, retm = retrieval_tools.fwd_model_rim(_lut, obs_geo, par.dx, par.normalise_imacs)

    # # -- Retrieve wind
    _retrieve = retrieval_tools.retrieve_wind
    wind_u, wind_v, dca = _retrieve(dic_l1, retm, par.fetch,
                                    norm0=dic_model['wnd_norm'],
                                    dir0=dic_model['wnd_dir'],
                                    sigma_imacs=tolist(par.sigma_imacs),
                                    sigma_dir0=tolist(par.sigma_dir0),
                                    sigma_norm0=tolist(par.sigma_norm0),
                                    rfac=tolist(par.pyramid_factor),
                                    threshold_j=par.threshold_cost,
                                    threshold_nrcs=par.threshold_nrcs,
                                    filter_nrcs_length=par.filter_nrcs_length,
                                    weight_imacs=tolist(par.weight_imacs),
                                    weight_nrcs=tolist(par.weight_nrcs),
                                    )

    # # -- Retrieve current
    tsc_u, tsc_v = retrieval_tools.retrieve_tsc(dic_l1, retm, dca)

    # # -- Save output
    logger.info('Save outputs')
    odic = {'wnd_u': wind_u, 'wnd_v': wind_v, 'dca': dca, 'tsc_u': tsc_u,
            'tsc_v': tsc_v, 'longitude': longitude, 'latitude': latitude}
    ofile = os.path.join(par.out_directory, f'{par.out_file}.nc')
    os.makedirs(par.out_directory, exist_ok=True)
    with open(ofile, 'wb') as f:
        pickle.dump(odic, f)
    _ = odic.pop('dca')
    write_tools.save_L2(ofile, odic)
    _text = f"\nSaved L2 as {ofile}.\n"
    logger.info(_text)
