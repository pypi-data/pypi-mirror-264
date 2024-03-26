import os
import logging
from typing import Sequence

import numpy
import scipy
from scipy.ndimage import rotate
import xarray as xr

# wavespectra is an optional package
try:
    import wavespectra
    has_wavespectra = True
except ModuleNotFoundError:
    has_pydap = False
    has_wavespectra = False

# Define logger level for debug purposes
logger = logging.getLogger(__name__)


def read_scene(scn_file: str, size_cut: list, read_function, rot_angle: float, l1_resolution: float = 1E3):
    """Read california data and SWAN data
    Image size, let us arbitrarily do (20,20)
    For now set the rotation angle to zero, so that the input grids can be
    aligned properly
    Otherwise, make sure that you run SWAN on the according, rotated gridi
    as well
    Parameters:
    ----------
    scn_file: str
        scn_file path
    size_cut: list
        min and max of the area to be processed
    read_function: function
        read function for the model
    rot_angle: float
        angle to rotate the grid (in degrees)

    Returns:
    --------
    dict
        model dictionnary (wnd_u, wnd_v, tsc_u, tsc_v, wnd_norm, wnd_dir
                           ic_u, ic_v, dx, dy, dudy, dudx, dvdy, dvdx,
                           dicudy, dicudx, dicvdy, dicvdx,...)
    dict
        model mean dictionnary with sst and wnd_norm mean
    """
    # TODO: we should refactor this, California cannot be hard coded as only option
    # AT: REVIEW
    model_all, dx = read_function(scn_file, smp_out=l1_resolution, rot_angle=rot_angle)
    # Cut model:
    # ToDo: Handle irregular grid
    model = cut_scene(model_all, dx, size_cut[0], size_cut[1])
    for key in list(model.keys()):
        _shp = len(numpy.shape(model[key]))
        if _shp == 3:
            model[f'{key}_u'] = model[key][:, :, 0]
            model[f'{key}_v'] = model[key][:, :, 1]
            del model[key]

    wnd_norm = numpy.sqrt(model["wnd_u"] ** 2 + model["wnd_v"] ** 2)
    I = wnd_norm < 1
    model["wnd_u"][I] = 4
    model["wnd_norm"] = numpy.sqrt(model["wnd_u"] ** 2 + model["wnd_v"] ** 2)
    model["wnd_dir"] = numpy.arctan2(model["wnd_v"], model["wnd_u"])

    # Project current to estimate roughly interior currents:
    model["ic_u"], model["ic_v"] = project_deep_currents(model["tsc_u"], model["tsc_v"])
    model["dx"] = dx
    model["dy"] = dx
    # mean values
    mean_model = {}
    for key in model.keys():
        mean_model[key] = numpy.mean(model[key])

    # compute divergence of currents
    # TODO: recompute accurate divergence and gradient
    # Here dx = dy
    model["dudy"], model["dudx"] = numpy.gradient(model["tsc_u"], dx, dx)
    model["dvdy"], model["dvdx"] = numpy.gradient(model["tsc_v"], dx, dx)

    model["dicudy"], model["dicudx"] = numpy.gradient(model["ic_u"], dx, dx)
    model["dicvdy"], model["dicvdx"] = numpy.gradient(model["ic_v"], dx, dx)
    model["longitude"] = model["lon"]
    model["latitude"] = model["lat"]

    # compute SST  and wind norm anomalies
    for key in ("sst", "wnd_norm"):
        # variations should not be too big and scene size also not too large
        model[f"{key}_anomaly"] = model[key] - mean_model[key]
    return model, mean_model


def cut_scene(dic_model: dict, dx: float, sizeaz: list, sizer: list):
    """Cut scene from Ocean dynamics model to IWS range
    Parameters:
    -----------
    dic_model: dict
        Model data dictionnary
    dx: float
        Resolution in x direction
    sizeaz: list(min, max)
        Cut domain in azimuthal direction
    sizer: list(min, max)
        Cut domain in range direction

    Returns:
        dict
        Input dictionnary on the new domain size
    """
    # Cut size to IWS range
    dy = dx * 1.0
    slicex = slice(int(sizeaz[0] / dy), int(sizeaz[1] / dy))
    slicey = slice(int(sizer[0] / dx), int(sizer[1] / dx))
    dic_out = {}
    for key, var in dic_model.items():
        _shp = len(numpy.shape(var))
        if _shp == 2:
            dic_out[key] = dic_model[key][slicex, slicey]
        elif _shp == 3:
            dic_out[key] = dic_model[key][slicex, slicey, :]
        else:
            logger.debug(f'{key} shape not handled by cut_scene function')
    # xs = dx * numpy.arange(tsc.shape[1])
    # ys = dy * numpy.arange(tsc.shape[0])
    return dic_out


def construct_swan_filepath(
    swan_path: str, swan_dir: str, sizeaz: Sequence = None, sizer: Sequence = None
) -> str:
    """
    Constructs the path to the SWAN netCDF file.

    The file name includes the boundaries of the azimuth and range coordinates
    if those are passed to the function as arguments. The file name constructed
    has the format:
    {swan_ascii_filename}_x_{min_range}_{max_range}_y_{min_azimuth}_{max_azimuth}

    Parameters
    ----------
    swan_path : str
        The path to the SWAN ASCII file.
    swan_dir : str
        Path to the directory to store the output as a netCDF file.
    sizeaz : Sequence
        Sequence where the first element is the minimum azimuth coordinate and the
        second is the maximum azimuth coordinate (Default Value is None).
    sizer : Sequence
        Sequence where the first element is the minimum range coordinate and the
        second is the maximum range coordinate (Default value is None).

    Returns
    -------
    str
        The path to the netCDF file where the partitioned dataset was saved.
    """
    input_file_name, _ = os.path.splitext(os.path.basename(swan_path))
    if (sizer is None) or (sizeaz is None):
        filename = os.path.join(swan_dir, input_file_name + ".nc")
    else:
        xmin, xmax = sizer
        ymin, ymax = sizeaz
        xy = f"x_{int(xmin // 1000):03}_{int(xmax // 1000):03}_y_{int(ymin // 1000):03}_{int(ymax // 1000):03}"
        filename = os.path.join(swan_dir, input_file_name + "_" + xy + ".nc")
    return filename


def partition_swan_spectra(
    swan_path: str, swan_dir: str, sizeaz: Sequence, sizer: Sequence
) -> str:
    """
    Reads the output of the SWAN model, partitions it into a smaller dataset and
    stores the result as netCDF.

    The output of swan can be large, in the order of GB. Partitioning it, and
    saving the smaller partitioned dataset into netCDF format can be useful as
    it allows the creation of smaller test cases.

    Parameters
    ----------
    swan_path : str
        The path to the SWAN ASCII file.
    swan_dir : str
        Path to the directory to store the output as a netCDF file.
    sizeaz : Sequence
        Sequence where the first element is the minimum azimuth coordinate and the
        second is the maximum azimuth coordinate.
    sizer : Sequence
        Sequence where the first element is the minimum range coordinate and the
        second is the maximum range coordinate.

    Returns
    -------
    str
        The path to the netCDF file where the partitioned dataset was saved.
    """
    if not has_wavespectra:
        logger.error(
            "Reading the output of SWAN in ASCII requires the wavespectra package"
        )
        raise ImportError
    logger.debug("Read swan dataset.")
    ws = wavespectra.read_swan(swan_path, dirorder=True, as_site=True)
    logger.debug("End read swan.")
    ymin, ymax = sizeaz
    xmin, xmax = sizer
    Iy = (ws.lat >= ymin) & (ws.lat < ymax)
    Ix = (ws.lon >= xmin) & (ws.lon < xmax)
    logger.debug("Partioning data.")
    ws = ws.where(Ix & Iy, drop=True)
    out_file = construct_swan_filepath(swan_path, swan_dir, sizeaz, sizer)
    logger.debug(f"Saving output to netcdf at {out_file}")
    ws.to_netcdf(out_file)
    return out_file


def read_swan_spectra(
        swan_path: str, sizeaz: list, sizer: list, netcdf: bool = True, rot_angle: float = 0
):  # -> wavespectra.specdataset.SpecDataset:
    """Read the SWAN data and crop we read it in a one-dimensional way, because
    alpha=-obsgeo.bist_ang[0][j] wavespectra does weird things.
    Parameters:
    ----------
    swan_path: str
        swan data path
    size_az: list(min, max)
        Azimutal size of the scene (lat_min, lat_max)
    sizer: list(min, max) 
        Range size of the scene (lon_min, lon_max)
    rot_angle: float
        Angle to rotate the scene (degrees) (Default value = 0)

    Returns
    -------
    ws wavespectra object
    """
    if netcdf:
        logger.debug(f"Reading SWAN model from netcdf at {swan_path}.")
        ws = xr.open_dataset(swan_path)
    else:
        if not has_wavespectra:
            logger.error(
                "Reading the output of SWAN in ASCII requires the wavespectra package"
            )
            raise ImportError
        logger.debug(f"Reading SWAN model in ASCII format at {swan_path}.")
        ws = wavespectra.read_swan(swan_path, dirorder=True, as_site=True)
        logger.debug("Finished reading SWAN model.")
    if numpy.isclose(rot_angle, 0):
        Iy = (ws.lat >= sizeaz[0]) & (ws.lat < sizeaz[1])
        Ix = (ws.lon >= sizer[0]) & (ws.lon < sizer[1])
        ws = ws.where(Ix & Iy, drop=True)
    else:
# indices for interpolation/rotation of wave spectra
        x_loc = numpy.array(ws.lon.values)
        y_loc = numpy.array(ws.lat.values)
        shp = (numpy.unique(y_loc).shape[0], numpy.unique(x_loc).shape[0])
        ix_loc = numpy.arange(0, shp[1])
        iy_loc = numpy.arange(0, shp[0])
        ix_temp = numpy.outer(ix_loc, numpy.ones(shp[0])).T
        iy_temp = numpy.outer(iy_loc, numpy.ones(shp[1]))
        ix_rot = rotate(ix_temp, rot_angle)
        iy_rot = rotate(iy_temp, rot_angle)
        i_rot = numpy.round(iy_rot) * shp[1] + numpy.round(ix_rot)
        i_rot = i_rot.astype(dtype='int')
        dx = x_loc[1]-x_loc[0]
        # new x and y radar coordinates
        SHP=i_rot.shape
        x_rad = numpy.arange(SHP[1]) * dx
        y_rad = numpy.arange(SHP[0]) * dx
        Ix = (x_rad >= sizer[0]) & (x_rad < sizer[1])
        Iy = (y_rad >= sizeaz[0]) & (y_rad < sizeaz[1])
        x_rad = numpy.outer(x_rad, numpy.ones(SHP[0])).T
        y_rad = numpy.outer(y_rad, numpy.ones(SHP[1]))
        x_rad = x_rad[Iy, :]
        y_rad = y_rad[Iy, :]
        i_rad = i_rot[Iy, :]
        x_rad = x_rad[:, Ix]
        y_rad = y_rad[:, Ix]
        i_rad = i_rad[:, Ix]
        X_vec=x_rad.ravel()
        Y_vec=y_rad.ravel()
        I_vec=i_rad.ravel()
        # create a new dataset
        # FIXME: whether to add or subtract the rotation angle from the directions is very tricky, check this
        ws = xr.Dataset({"efth": (("time", "site", "freq", "dir"), ws["efth"].values[:, I_vec, :, :]),
                        "lon": (("site"), X_vec),
                        "lat": (("site"), Y_vec)},
                        coords={"time": numpy.ones(1),
                                "site": range(1, len(X_vec) + 1),
                                "freq": ws["freq"].values,
                                "dir": numpy.mod(ws["dir"].copy() + rot_angle, 360)})
    return ws


def project_deep_currents(tsc_u: numpy.ndarray, tsc_v: numpy.ndarray):
    """
    currents at a bit of depth (a ratio of 1/100 depth vs horizontal scales
    is assumed)

    Parameters:
    -----------
    tsc_u: array
        Eastward current
    tsc_v: array
        Northward current

    Returns:
    -----------
    array
        eastward internal current
    array
        northward internal current
    """
    ic_u = numpy.zeros(tsc_u.shape)
    ic_v = numpy.zeros(tsc_v.shape)
    # interior currents
    ic_u = scipy.signal.convolve2d(tsc_u, numpy.ones((3, 3)) / 3 / 3, "same")
    ic_v = scipy.signal.convolve2d(tsc_v, numpy.ones((3, 3)) / 3 / 3, "same")
    return ic_u, ic_v


def generate_wind(nb_points: int, wnd_norm: float) -> dict:
    """ Fake wind scene to compute LUT 
    Parameters:
    -----------
    nb_points: int
        number of points in range
    wnd_norm: float
        Norm of wind in m/s
    Returns
    -----------
    dict
        model dictionnary (wnd_dir, wnd_norm, wnd_u, wnd_v, wnd_anomaly)
    """
    model = {}
    # model["wnd_norm"] = numpy.array([numpy.arange(0, 30, 2),] * nb_points).T
    model["wnd_dir"] = numpy.array([numpy.arange(0, 361, 10), ] * nb_points).T
    model["wnd_dir"] = numpy.deg2rad(model["wnd_dir"])
    model["wnd_norm"] = numpy.full(model["wnd_dir"].shape, wnd_norm)
    model["wnd_u"] = wnd_norm * numpy.cos(model["wnd_dir"])
    model["wnd_v"] = wnd_norm * numpy.sin(model["wnd_dir"])
    model["wnd_anomaly"] = model["wnd_norm"] - numpy.mean(model["wnd_norm"])
    return model
