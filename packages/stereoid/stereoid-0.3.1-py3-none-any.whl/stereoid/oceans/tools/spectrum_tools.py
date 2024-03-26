import logging
from collections import namedtuple
from typing import Tuple, Optional

import numpy
from scipy.signal import convolve2d
import numpy.typing as npt
import stereoid.oceans.waves.wave_spectra as swave_spectra
import stereoid.oceans.waves.spectral_conversions as spectral_conv
import stereoid.oceans.waves.high_resolution_var as hr_var
import stereoid.utils.tools as tools
from stereoid.oceans.forward_models import SAR_spectra as SAR_model
from stereoid.oceans import ObsGeoAngles
import stereoid.oceans.tools.observation_tools as obs_tools
from stereoid.oceans.forward_models.wrappers import (
    interp_weights as griddata_step1,
    interpolate as griddata_step2,
)

# Define logger level for debug purposes
logger = logging.getLogger(__name__)
ObsGeoTrio = namedtuple("ObsGeoTrio", ["concordia", "discordia", "sentinel1"])
G = 9.81


def conv2(x, y, mode='same'):
    return numpy.rot90(convolve2d(numpy.rot90(x, 2), numpy.rot90(y, 2), mode=mode), 2)


def wave_number_grids_polar(lambda_min: float, lambda_max: float, n_k: int) -> dict:
    """Wavelengths and wave number on grids
    Parameters:
    -----------
    lambda_min: float
        Min wavelength value
    lambda_max: float
        Max wavelength value
    n_k: int
        Number of wavelength in the grid
    Returns
    -------
    dict
       Dictionaryy with k_x, k_y, k, omega, phi, dks
    """
    k_min = 2 * numpy.pi / lambda_max  # minimum wave number
    k_max = 2 * numpy.pi / lambda_min  # should at least pass the Bragg wave
    # number
    # k_x = k_min * np.arange(1, n_k + 1)
    # vector of wave numbers (single side)
    k = 10 ** numpy.linspace(numpy.log10(k_min),
                                           numpy.log10(k_max), n_k)


    # directions
    nphi = 72
    phi = numpy.linspace(-numpy.pi, numpy.pi, nphi)

    # angular velocity
    omega = numpy.where(k > 0, numpy.sqrt(G * k), 0)

    # resolution
    dk = numpy.gradient(k)
    dphi = 2 * numpy.pi / nphi * numpy.ones(len(phi))

    return {"k": k,
            "omega": omega, "phi": phi, "dk": dk, "dphi": dphi}


def wave_number_grids(lambda_min: float, lambda_max: float, n_k: int) -> dict:
    """Wavelengths and wave number on grids
    Parameters:
    -----------
    lambda_min: float
        Min wavelength value
    lambda_max: float
        Max wavelength value
    n_k: int
        Number of wavelength in the grid
    Returns
    -------
    dict
       Dictionaryy with k_x, k_y, k, omega, phi, dks
    """
    k_min = 2 * numpy.pi / lambda_max  # minimum wave number
    k_max = 2 * numpy.pi / lambda_min  # should at least pass the Bragg wave
    # number
    # k_x = k_min * np.arange(1, n_k + 1)
    # vector of wave numbers (single side)
    k_x = numpy.reshape(10 ** numpy.linspace(numpy.log10(k_min),
                                             numpy.log10(k_max), n_k), (1, n_k))
    # extend domain (distance increase higher wave noms)
    # k_x[20:] = k_x[20:] * 1.015 ** np.arange(2, n_k - 20)
    # double sided spectrum
    k_x = numpy.append(numpy.append(-numpy.flip(k_x), 0), k_x)
    dk = numpy.gradient(k_x, 1)
    # two-dimensionnal
    k_x = numpy.dot(numpy.ones((n_k * 2 + 1, 1)), k_x.reshape(1, n_k * 2 + 1))
    k_y = numpy.transpose(k_x)
    k = numpy.sqrt(k_x ** 2 + k_y ** 2)
    omega = numpy.where(k > 0, numpy.sqrt(G * k), 0)
    # 0 is cross-track direction waves, 90 along-trac
    phi = numpy.arctan2(k_y, k_x)
    # patch size matrix, Compute the outer product of two vectors.
    dks = numpy.outer(dk, dk)
    return {"k_x": k_x, "k_y": k_y, "k": k,
            "omega": omega, "phi": phi, "dks": dks}


def wave_number_grids_sar(scene_size: int, dx: Optional[float] = 5,
                          dy: Optional[float] = 5):
    """
    Wave numbers for SAR spectra in a Cartesian grids (kx=cross,ky=along)
    Parameters:
    -----------
    scene_size: int
        Number of points in the x and y direction
    dx = 5 : float
        Range resolution
    dy = 15: float
        Azimuthal resolution
    Returns
    -------
    dict
       Dictionary with k_x, k_y, k, omega, phi, dks
    """
    Nx = int(scene_size / dx)
    Ny = int(scene_size / dy)
    dkx = 2 * numpy.pi / scene_size  # (Nx*dx)  # deviates slightly from scene size
    dky = 2 * numpy.pi / scene_size  # (Ny*dy)
    kx = 2 * numpy.pi * numpy.fft.fftfreq(Nx, dx)
    # reshape kx for broadcasting
    kx = kx.reshape((1, Nx))
    # create a meshgrid from kx
    kx = numpy.dot(numpy.ones((Ny, 1)), kx)
    ky = 2 * numpy.pi * numpy.fft.fftfreq(Ny, dy)
    ky = ky.reshape((Ny, 1))
    ky = numpy.dot(ky, numpy.ones((1, Nx)))
    k = numpy.sqrt(kx ** 2 + ky ** 2)
    omega = numpy.sqrt(G * k)  # angular velocity

    # 0 is cross-track direction waves, 90 along-track
    phi = numpy.arctan2(ky, kx)

    # 0 is cross-track direction waves, 90 along-track
    dks = dkx * dky * numpy.ones(kx.shape)
    return {"k_x": kx, "k_y": ky, "k": k,
            "omega": omega, "phi": phi, "dks": dks}


def rotation_cutoff(HX_angles, wn_grid: dict
                    ) -> Tuple[numpy.ndarray, numpy.ndarray]:
    alpha_rot = numpy.arctan2(numpy.sin(HX_angles.bist_ang) * numpy.sin(HX_angles.inc_b),
                              numpy.sin(HX_angles.inc_m) + numpy.cos(HX_angles.bist_ang) * numpy.sin(HX_angles.inc_b))
    xy, uv = obs_tools.compute_rotation(alpha_rot, wn_grid)
    vtx, wts = griddata_step1(xy, uv)
    return vtx, wts


def compute_swh(grid_wn: dict) -> float:
    dkx = grid_wn["k_x"][0, 1] - grid_wn["k_x"][0, 0]
    dky = grid_wn["k_y"][1, 0] - grid_wn["k_x"][0, 0]
    Hs = numpy.sum(numpy.sum(grid_wn["S"] * dkx, axis=1) * dky, axis=0)
    return Hs

# This function provides basically three options to construct the wave spectrum:
# 1) LUT type: local Elfouhaily long-wave spectrum with Kudry short-wave spectrum
# 2) Elf_noneq: local Elfouhaily long-wave spectrum with Kudry short-wave spectrum, short-wave alterations by currents
# 3) SWAN_noneq: SWAN long-wave spectrum with Kudry short-wave spectrum, short-wave alterations by currents
def compute_spec(ws, wn: dict, model: dict, SHP: list, spec_type: str,
                 mod_transfer: dict, ind: list, fetch: Optional[float] = 100e3,
                 swell: Optional[bool] = False,
                 short_wave_spec_type: Optional[str] = 'polar',
                 k_l: Optional[float] = None) -> Tuple[float, float]:
    """
    Compute spectrum
    Parameters:
    ----------
    ws: wavespectrum
        Wavespectrum from model or None 
    wn: dict
        Wave number grid for the SAR computation
    model: dict
        Input OGCM model (wnd_norm, wnd_dir, wnd_anomaly, dudx, dvdx, dudy,
                          dvdy)
    SHP: list
        model shape
    spec_type: str
       spec_type (SWAN_noneq or Elf_noneq or LUT)
    mod_transfer: dict
        Transfer function (ux, vx, uy, vy)
    ind: list
        indice i, j in the model 
    fetch = 100e3: float
        fetch distance in m
    swell = False: bool
        Set if Swell should be computed
    k_l = None: float
        Separating wave number for merging the long and short wave spectra.
    Returns:
    -------
    [float, float]
        B, S
    """
    # long-wave spectrum
    # I think this should work, but be careful
    # TO DO check
    i, j = ind
    Kudry = swave_spectra.Kudry_spec
    Kudry_polar = swave_spectra.Kudry_spec_polar
    if spec_type == "SWAN_noneq" or spec_type == "Elf_noneq":
        if ws is None:
            S_lw = 0  # this is going to screw us
            print("SWAN wave spectrum not found!")
        else:
            ws_dir = 90 - (ws.dir - 180)
            E = ws.efth[0, j + i * SHP[1], :, :]
            E = numpy.array(E.values)
            if short_wave_spec_type == 'polar':
                S_lw = spectral_conv.SWAN2Polar(
                    E, ws.freq.values, ws_dir.values, wn["k"], wn["phi"]
                )
            else:
                S_lw = spectral_conv.SWAN2Cartesian(
                    E, ws.freq.values, ws_dir.values, wn["k_x"], wn["k_y"], wn["dks"]
                )
        B_lw = wn["k"] ** 4 * S_lw
    # Local wind
    # nwnd_mean = numpy.mean(model["wnd_norm"])
    # wnd_dir_mean = numpy.mean(model["wnd_dir_mean"])
    nwnd_local = model["wnd_norm"][i, j]
    rwnd_dir = model["wnd_dir"][i, j]
    if swell is True:
        logger.info("Warning swell currently not added to wave " "spectrum!")

    # short-wave spectrum
    if spec_type == "SWAN_noneq":
        # here we create a local short-wave spectrum which is not altered by
        # currents
        # it requies local wind speed and direction
        # the non-equilibrium part for the energy balance comes from SWAN's
        # long waves
        if short_wave_spec_type == 'polar':
            Bm, B_neq, B_w, B_pc = Kudry_polar(
                wn["k"], wn["phi"], nwnd_local, 0, rwnd_dir, S=S_lw, k_cut=k_l
            )
        else:
            Bm, B_neq, B_eq, I_swpc = Kudry(
                wn["k_x"], wn["k_y"], nwnd_local, 0, rwnd_dir, wn["dks"], S=S_lw, k_cut=k_l
            )

        # FIXME: we simply override the transfer functions for now
        # the if-statement ensures the mod-transfers are not overriden for the wave spectra, which we forced to be zero
        Sm = numpy.where(wn["k"] > 0, Bm * wn["k"] ** -4, 0)
        if numpy.mean(mod_transfer["ux"]) != 0: # not sure why we needed this
            if short_wave_spec_type == 'polar':
                Tux, Tvx, Tuy, Tvy = hr_var.Rascle2014_currents(
                    Sm, wn["k"], wn["phi"], nwnd_local, fetch, m_star=0.9
                )
                # FIXME: wind transfer functions set to zero (not used anyway)
                Tw = 0

            else:
                Tux, Tvx, Tuy, Tvy = hr_var.Rascle2017_currents(
                Sm, wn["k_x"], wn["k_y"], nwnd_local, fetch, m_star = 0.9
                )
                Tw = hr_var.Johannessen2005_wind(
                wn["k_x"], wn["k_y"], nwnd_local, rwnd_dir, m_star = 0.9
                )

            mod_transfer = {"ux": Tux, "vx": Tvx, "uy": Tuy, "vy": Tvy, "wnd": Tw}

        # the effects of currents on the short waves are captured using
        # transfer functions
        # the transfer functions do not consider relaxation,
        # so only apply this to short waves
        Nm = numpy.where(wn["k"] > 0, wn["omega"] / wn["k"] * Sm, 0)
        dN = (
                mod_transfer["ux"] * model["dudx"][i, j]
                + mod_transfer["vx"] * model["dvdx"][i, j]
                + mod_transfer["uy"] * model["dudy"][i, j]
                + mod_transfer["vy"] * model["dvdy"][i, j]
        )
        # wave action after current
        N = Nm + dN
        # curvature after current
        B_sw = numpy.where(wn["k"] > 0, N / wn["omega"] * wn["k"] * wn["k"] ** 4, 0)
        B_sw[B_sw < 0] = 0

        # the long waves of SWAN are merged with the short waves
        # FIXME: these if-statements are a bit excessive, shorten
        I_kp = numpy.argmax(S_lw)
        if short_wave_spec_type == 'polar':
            # this is a bit ugly
            k_temp, phi_temp = numpy.meshgrid(wn["k"], wn["phi"])
            k_p=k_temp.ravel()[I_kp]
            k_p=numpy.min((k_p, 2*numpy.pi/10 )) # do not allow peak wavelength to drop below 10 m
            if k_l == None:
                k_l = 10 * k_p
            else:
                k_l = numpy.max((10 * k_p, k_l))
            B = swave_spectra.merge_spectra_polar(B_lw, B_sw, wn["k"], wn["phi"],k_l)
        else:
            # not really sure why we are still computing this, 'k' is available
            k_p = numpy.sqrt(
                wn["k_x"].ravel()[I_kp] ** 2 + wn["k_y"].ravel()[I_kp] ** 2
            )
            k_p=numpy.min((k_p, 2*numpy.pi/10 )) # do not allow peak wavelength to drop below 10 m
            if k_l == None:
                k_l = 10 * k_p
            else:
                k_l = numpy.max((10 * k_p, k_l))
            B = swave_spectra.merge_spectra(B_lw, B_sw, wn["k_x"], wn["k_y"],k_l)

    elif spec_type == 'Elf_noneq':
        # FIXME we don't need these two variables if we are not going to use dB
        # wnd_anomaly = model["wnd_anomaly"][i, j]
        # wnd_transfer = mod_transfer["wnd"]

        # this creates a mean Kudry spectrum using local wind speed
        # and direction
        # the non-equilibrium part of the spectrum comes from a mean
        # Elfouhaily spectrum
        if short_wave_spec_type == 'polar':
            Bm, B_neq, B_w, B_pc = Kudry_polar(
                wn["k"], wn["phi"], nwnd_local, fetch, rwnd_dir, k_cut=k_l
            )
        else:
            Bm, B_neq, B_eq, I_swpc = Kudry(
                wn["k_x"], wn["k_y"], nwnd_local, fetch, rwnd_dir, wn["dks"], k_cut=k_l
            )

        # FIXME: we simply override the transfer functions for now
        # the if-statement ensures the mod-transfers are not overriden for the wave spectra, which we forced to be zero
        Sm = numpy.where(wn["k"] > 0, Bm * wn["k"] ** -4, 0)
        if numpy.mean(mod_transfer["ux"]) != 0:
            if short_wave_spec_type == 'polar':
                Tux, Tvx, Tuy, Tvy = hr_var.Rascle2014_currents(
                    Sm, wn["k"], wn["phi"], nwnd_local, fetch, m_star=0.9
                )
                # FIXME: wind transfer functions set to zero (not used anyway)
                Tw = 0

            else:
                Tux, Tvx, Tuy, Tvy = hr_var.Rascle2017_currents(
                    Sm, wn["k_x"], wn["k_y"], nwnd_local, fetch, m_star=0.9
                )
                Tw = hr_var.Johannessen2005_wind(
                    wn["k_x"], wn["k_y"], nwnd_local, rwnd_dir, m_star=0.9
                )
            mod_transfer = {"ux": Tux, "vx": Tvx, "uy": Tuy, "vy": Tvy, "wnd": Tw}

        # the effects of currents and wind anomalies on the short waves
        # are captured using transfer functions
        # the transfer functions do not consider relaxation,
        # so only apply this to short waves
        Nm = numpy.where(wn["k"] > 0, wn["omega"] / wn["k"] * Sm, 0)
        dN = (
                mod_transfer["ux"] * model["dudx"][i, j]
                + mod_transfer["vx"] * model["dvdx"][i, j]
                + mod_transfer["uy"] * model["dudy"][i, j]
                + mod_transfer["vy"] * model["dvdy"][i, j]
        )
        # alternations from the wind
        # this is a strange, because it has no direction,
        # but it appears to work (Kudry2005)
        # FIXME currently we have dB off
        # dB = wnd_transfer * wnd_anomaly / nwnd_mean * Bm
        N = Nm + dN  # wave action after current
        # curvature after current + wind
        # FIXME Wind transfer function off. To be consistent use 20km * 20km
        # average wind speed and direction in line 225 and turn wind transfer
        # function on.
        B_sw = numpy.where(wn["k"] > 0, N / wn["omega"] * wn["k"] * wn["k"] ** 4, 0)  # + dB
        B_sw[B_sw < 0] = 0

        # the long waves of SWAN are merged with the short waves
        I_kp = numpy.argmax(S_lw)
        if short_wave_spec_type == 'polar':
            # this is a bit ugly
            k_temp, phi_temp = numpy.meshgrid(wn["k"], wn["phi"])
            k_p = k_temp.ravel()[I_kp]
            k_p=numpy.min((k_p, 2*numpy.pi/10 )) # do not allow peak wavelength to drop below 10 m
            if k_l == None:
                k_l = 10 * k_p
            else:
                k_l = numpy.max((10 * k_p, k_l))
            B = swave_spectra.merge_spectra_polar(B_lw, B_sw, wn["k"], wn["phi"], k_l)
        else:
            # not really sure why we are still computing this, 'k' is available
            k_p = numpy.sqrt(
                wn["k_x"].ravel()[I_kp] ** 2 + wn["k_y"].ravel()[I_kp] ** 2
            )
            k_p=numpy.min((k_p, 2*numpy.pi/10 )) # do not allow peak wavelength to drop below 10 m
            if k_l == None:
                k_l = 10 * k_p
            else:
                k_l = numpy.max((10 * k_p, k_l))
            B = swave_spectra.merge_spectra(B_lw, B_sw, wn["k_x"], wn["k_y"], k_l)
    else:
        # this creates a Kudry spectrum using LUT wind speed, direction
        # and fetch
        # the non-equilibrium part of the spectrum comes from an Elfouhaily
        # spectrum

        if short_wave_spec_type == 'polar':
            Bm, B_neq, B_w, B_pc = Kudry_polar(
                wn["k"], wn["phi"], nwnd_local, fetch, rwnd_dir, k_cut=k_l
            )
        else:
            Bm, B_neq, B_eq, I_swpc = Kudry(
                wn["k_x"], wn["k_y"], nwnd_local, fetch, rwnd_dir, wn["dks"], k_cut=k_l
            )
        B = Bm * 1.0

    S = numpy.where(B > 0, wn["k"] ** -4 * B, 0)
    return B, S


def make_SAR_spectra(
        ws,
        model: dict,
        obs_geo_trio: ObsGeoTrio,
        mod_transfer: dict,
        wn: dict,
        spec_samp: list,
        lambda_max: float,
        n: int,
        pol: Optional[str] = "V",
        rxpol: Optional[str] = "mM",
        swell: Optional[bool] = False,
        spec_type: Optional[str] = "SWAN_noneq",
        short_wave_spec_type: Optional[str] = "polar",
        fetch: Optional[float] = 100e3,
        noise: Optional[bool] = True,
        k_l: Optional[float] = None,
        progress_bar: Optional[bool] = True,
) -> tuple[npt.ArrayLike]:
    # override (maybe not necessary, check this)
    # obs_geo.set_swath(
    # incm, np.arange(tsc.shape[1]).reshape((1, tsc.shape[1])) * grid_spacing
    # )
    """
    Compute co-spectrum and cross spectrum, imacs and cut-off
    Parameters:
    ----------
    ws: wavespectrum
        Wavespectrum from model or None 
    model: dict
        Input OGCM model (wnd_norm, wnd_dir, wnd_anomaly, dudx, dvdx, dudy,
                          dvdy)
    obs_geo_trio: ObsGeoTrio
        Geometry angles
    mod_transfer: dict
        Transfer function (ux, vx, uy, vy)
    wn: dict
        Wave number grid for the SAR computation
    spec_samp: list
        Sub sampling for spectrum computation (int, int)
    lambda_max: float
        Max wavelength for SAR spectrum computation
    n: int
        Number of wavelength for the SAr spectrum
    pol = 'V': str
        Polarization labeling for Sentinel
    rxpol = "mM": str
        Polarization for companion
    spec_type = "SWAN_noneq": str
       spec_type (SWAN_noneq or LUT)
    fetch = 100e3: float
        fetch distance in m
    noise = True: bool
        Computation of noise
    k_l = None: float
        Separating wave number for merging the long and short wave spectra.
    swell = False: bool
        Set if Swell should be computed
    progress_bar = True: bool
        Activate or deactivate progress bar
    Returns:
    -------
    [dict, dict, dict, dict, array]
        Cospectra, Cross-spectra, imacs, cut-off, incidence
    """
    model_shp = model["wnd_norm"].shape
    mshp = (int(numpy.ceil(model_shp[0] / spec_samp[0])),
            int(numpy.ceil(model_shp[1] / spec_samp[1])))

    # we will take low-pass filtered input grids to compute the spectra
    # FIXME: we assume that for real scenes spec_samp is never 1, but for the LUT it is. You do not want any filtering applied for the LUT.
    if spec_samp[0] != 1: # this lives under the assumption that both directions it is not 1
        # FIXME: if spec_samp is even, we have 1 row/column overlap between successive spectra
        L0=spec_samp[0]
        L1 = spec_samp[1]
        if numpy.mod(spec_samp[0],2) == 0:
            L0=L0+1
        if numpy.mod(spec_samp[1],2) == 0:
            L1=L1+1
        fi = numpy.ones((L0, L1)) / L0 / L1
        w_x = numpy.cos(model["wnd_dir"]) * model["wnd_norm"]
        w_y = numpy.sin(model["wnd_dir"]) * model["wnd_norm"]
        w_x = conv2(w_x, fi, 'same')
        w_y = conv2(w_y, fi, 'same')

        # filter wind
        model["wnd_norm"] = numpy.sqrt(w_x ** 2 + w_y ** 2)
        model["wnd_dir"] = numpy.arctan2(w_y, w_x)

        # filter current gradients
        model["dudy"]=conv2(model["dudy"], fi, 'same')
        model["dudx"]=conv2(model["dudx"], fi, 'same')
        model["dvdy"]=conv2(model["dvdy"], fi, 'same')
        model["dvdx"]=conv2(model["dvdx"], fi, 'same')

    # set modulation transfer functions to zero
    # effectively we ignore the effect of currents on the transfer functions
    #mod_transfer['ux'] = numpy.zeros(mod_transfer['ux'].shape)
    #mod_transfer['uy'] = numpy.zeros(mod_transfer['ux'].shape)
    #mod_transfer['vx'] = numpy.zeros(mod_transfer['ux'].shape)
    #mod_transfer['vy'] = numpy.zeros(mod_transfer['ux'].shape)

    # Polarimetry for rotations
    rxpol, polbase = obs_tools.set_polarization(rxpol)
    # compute one SAR spectrum per [spec_samp] km x [spec_samp] km
    wn_grid = wave_number_grids_sar(lambda_max)
    kshp = wn_grid["k"].shape
    pg = progress_bar

    # co-spectra and cross=spectra
    listsat = ("S1", "HA", "HB")
    co_spec = {}
    cr_spec = {}
    macs = {}
    cutoff = {}
    swh = {}

    for key in listsat:
        co_spec[key] = {}
        cr_spec[key] = {}
        macs[key] = {}
        cutoff[key] = {}

    # some dictionaries for the output of spectra and derived parameters
    # shp = kx.shape
    SHPshp = (mshp[0], mshp[1], kshp[0], kshp[1])
    incidence = numpy.zeros((mshp[1]))
    swh = numpy.zeros(mshp)
    lon = numpy.zeros(mshp)
    lat = numpy.zeros(mshp)
    for key in listsat:
        if key == "S1":
            # Here for now I chose to use H/V for S1, but we could also just stay with I (=H) and O (=V)
            co_spec[key] = {"H": numpy.zeros(SHPshp), "V": numpy.zeros(SHPshp)}
            cr_spec[key] = {"H": numpy.zeros(SHPshp, dtype='complex'),
                            "V": numpy.zeros(SHPshp, dtype='complex')}
            macs[key] = {"H": numpy.zeros(mshp, dtype='complex'),
                         "V": numpy.zeros(mshp, dtype='complex')}
            cutoff[key] = {"H": numpy.zeros(mshp), "V": numpy.zeros(mshp)}
        else:
            co_spec[key] = {polbase[0]: numpy.zeros(SHPshp),
                            polbase[1]: numpy.zeros(SHPshp)}
            cr_spec[key] = {polbase[0]: numpy.zeros(SHPshp, dtype='complex'),
                            polbase[1]: numpy.zeros(SHPshp, dtype='complex')}
            macs[key] = {polbase[0]: numpy.zeros(mshp, dtype='complex'),
                         polbase[1]: numpy.zeros(mshp, dtype='complex')}
            cutoff[key] = {polbase[0]: numpy.zeros(mshp),
                           polbase[1]: numpy.zeros(mshp)}

    tools.print_info_spec(spec_type)
    # look in two directions through the scene
    for j in tools.progress(0, model_shp[1], step=spec_samp[1], progress_bar=pg): # this goes through the 'x-direction'

        # observations geometry
        (obs_geo_c_angles_j, obs_geo_d_angles_j,
         ) = obs_geo_trio.concordia.get_angles_at_index(
            [0, j]
        ), obs_geo_trio.discordia.get_angles_at_index(
            [0, j]
        )
        inc_tx = obs_geo_c_angles_j.inc_m
        inc_rxc = obs_geo_c_angles_j.inc_b
        inc_rxd = obs_geo_d_angles_j.inc_b
        bist_c = obs_geo_c_angles_j.bist_ang
        bist_d = obs_geo_d_angles_j.bist_ang
        S1_angles = ObsGeoAngles(inc_tx, inc_tx, 0)
        HA_angles = ObsGeoAngles(inc_tx, inc_rxc, bist_c)
        HB_angles = ObsGeoAngles(inc_tx, inc_rxd, bist_d)

        # rotations for cutoff computations (heading satellite)
        vtx_h, wts_h = rotation_cutoff(HA_angles, wn_grid)

        # rotations for cutoff computations (trailing satellite)
        vtx_t, wts_t = rotation_cutoff(HB_angles, wn_grid)

        for i in range(0, model_shp[0], spec_samp[0]):  # this goes through the 'y-direction'


            # This computes a local wind-wave spectrum for SAR transfer function
            # The wind-wave spectrum S_ku is computed on a logaritmic wave number grid
            B, S_ku = compute_spec(ws, wn, model, model_shp, spec_type,
                                   mod_transfer, (i, j), fetch=fetch, swell=swell, short_wave_spec_type=short_wave_spec_type, k_l=k_l)
            rwnd_dir = model["wnd_dir"][i, j]
            nwnd_local = model["wnd_norm"][i, j]

            # This computes the 'resolved' wave spectrum on a Cartesian grid
            # To this wave spectrum the SAR spectral transfer functions will be applied
            if spec_type == "SWAN_noneq" or spec_type == "Elf_noneq":
                ws_dir = 90 - (ws.dir - 180)
                # # on this grid the SAR spectrum is computed
                # get long-wave spectrum as the average of
                spec_count = 0
                E = numpy.zeros(ws.efth[0, j + i * model_shp[1], :, :].shape)
                # FIXME: we make the odd/even spec_samp to odd filter length (so creates overlap)
                for jj in range(j - int(spec_samp[1] / 2), j + int(spec_samp[1] / 2) + 1):
                    for ii in range(i - int(spec_samp[0] / 2), i + int(spec_samp[0] / 2) + 1):
                        if numpy.logical_and(jj > -1, jj < model_shp[1]):
                            if numpy.logical_and(ii > -1, ii < model_shp[0]):
                                E_temp = ws.efth[0, j + i * model_shp[1], :, :]
                                E_temp = numpy.array(E_temp.values)
                                E = E + E_temp
                                spec_count = spec_count + 1
                E = E / spec_count
                S = spectral_conv.SWAN2Cartesian(
                    E, ws.freq.values, ws_dir.values, wn_grid["k_x"],
                    wn_grid["k_y"], wn_grid["dks"])
                S[0, 0] = 0
            else:
                # S = numpy.zeros(numpy.shape(wn_grid["dks"]))
                dphi = numpy.angle(numpy.exp(1j * (wn_grid["phi"] - rwnd_dir)))
                k = wn_grid["k"]
                # FIXME: replaced with a different spreading function
                # elf = (swave_spectra.elfouhaily_spread(k, dphi, nwnd_local, fetch)
                #       * swave_spectra.elfouhaily(k, nwnd_local, fetch) / k)
                elf = (swave_spectra.DandP_spread(k, dphi, nwnd_local, fetch)
                       * swave_spectra.elfouhaily(k, nwnd_local, fetch) / k)
                S = numpy.where(k > 0, elf, 0)


            # scaling to work with Fourier transforms
            # S = S * dks * dks * numberofk * numberofk
            S = S * wn_grid["dks"] * kshp[0] * kshp[1]
            # dks is already the two-dimensional cell size

            ii = int(i / spec_samp[0])
            jj = int(j / spec_samp[1])
            incidence[jj] = inc_tx

            # Resolved wave spectrum
            wn_grid["S"] = S
            # Wind-wave spectrum for transfer functions
            wn["S"] = S_ku
            # This function computes the polarimetric transfer functions, the cross-covariance functions and eventually the spectra
            cospec_tmp, crspec_tmp = SAR_model.run_spectra_SWB(obs_geo_trio,
                                                               inc_tx, wn_grid,
                                                               wn, nwnd_local,
                                                               rwnd_dir, n,
                                                               cross=True,
                                                               noise=noise,
                                                               nord=4,
                                                               polbase=rxpol,
                                                               fetch=fetch,
                                                               short_wave_spec_type='polar')

            # store co-spectra and cross-spectra
            for sat in cospec_tmp.keys():
                for pol in cospec_tmp[sat].keys():
                    # co-spectra
                    co_spec[sat][pol][ii, jj, :, :] = cospec_tmp[sat][pol][:, :]
                    # cr-spectra
                    cr_spec[sat][pol][ii, jj, :, :] = crspec_tmp[sat][pol][:, :]

            # cut-off and macs
            dic_angles = {"S1": S1_angles, "HA": HA_angles, "HB": HB_angles}
            for sat in listsat:
                if sat == 'S1':
                    _vtx = numpy.zeros((3, 3))
                    _wts = numpy.zeros((3, 3))
                elif sat == 'HA':
                    _vtx = vtx_h
                    _wts = wts_h
                elif sat == 'HB':
                    _vtx = vtx_t
                    _wts = wts_t
                else:
                    logger.error(f"Unknown satellite name {sat}")
                for pol in crspec_tmp[sat].keys():
                    wn_grid["S"] = crspec_tmp[sat][pol][:, :]
                    _res = SAR_model.cutoff_and_macs(wn_grid, dic_angles[sat],
                                                     compute_macs=True,
                                                     compute_cutoff=True,
                                                     vtx=_vtx, wts=_wts)
                    cutoff[sat][pol][ii, jj], macs[sat][pol][ii, jj] = _res

            if 'longitude' in model.keys():
                lon[ii, jj] = model['longitude'][i, j]
            if 'latitude' in model.keys():
                lat[ii, jj] = model['latitude'][i, j]
            swh[ii, jj] = compute_swh(wn_grid)

    coord = {'longitude': lon, 'latitude': lat}
    return co_spec, cr_spec, macs, cutoff, incidence, coord


def spectrum_short_waves_swan(
        model: dict,
        lambda_min: float,
        lambda_max: float,
        n_k: int,
        fetch: Optional[float] = 100e3,
        short_wave_spec_type: Optional[str] = 'polar',
):
    """Get reference spectrum from SWAN or other implemented model
    Parameters:
    -----------
    model: dict
        model dictionary ('wnd_v', 'wnd_u', 'wnd_norm', 'wnd_dir')
    lambda_min: float
        minimal wavelength value
    lambda_max: float
        maximal wavelength value
    n_k: int
        Number of wavelength for the spectrum
    fetch: float
        Length of fetch in m


    """
    # neq_spec = 'SWAN'

    # mean wind direction
    # scene size cannot be too big
    if short_wave_spec_type == 'polar':
        wave_number = wave_number_grids_polar(lambda_min, lambda_max, n_k)
    else:
        wave_number = wave_number_grids(lambda_min, lambda_max, n_k)
    phi_w = (numpy.mean(numpy.arctan2(model["wnd_v"], model["wnd_u"])))

    wave_number["phi_w"] = phi_w
    # (short-wave) spectrum from Kudry1999, Kudry2003, Kudry2005 based on
    # appendices from Yuroyskaya2013, KCM2014
    # we use one reference spectrum here for short waves, maybe it is better
    # to directly put the long waves into Kudry_spec to get right equilibrium
    U_mean = numpy.nanmean(model["wnd_norm"])
    if short_wave_spec_type == 'polar':
        Bm, B_neq, B_eq, I_swpc = swave_spectra.Kudry_spec_polar(
            wave_number["k"], wave_number["phi"], U_mean, fetch, phi_w
        )
    else:
        Bm, B_neq, B_eq, I_swpc = swave_spectra.Kudry_spec(
            wave_number["k_x"], wave_number["k_y"], U_mean, fetch, phi_w, wave_number["dks"]
        )
    Sm = numpy.where(wave_number["k"] > 0, Bm * wave_number["k"] ** -4, 0)
    # Nm = numpy.where(wave_number['k'] > 0,
    #                  wave_number['omega'] / wave_number['k'] * Bm, 0)

    # significant wave height (just for checking)
    #Hs = 4 * numpy.sqrt(numpy.sum(Sm * wave_number['dks']))

    # - Compute spatial transfer function for short-wave variations
    # These current modulation transfer functions should be applied to the
    # action spectrum 'Nm'
    if short_wave_spec_type == 'polar':
        Tux, Tvx, Tuy, Tvy = hr_var.Rascle2014_currents(
            Sm, wave_number["k"], wave_number["phi"], U_mean, fetch, m_star=0.9
        )
        # FIXME: wind transfer function set to zero (not used anyway)
        Tw=0
    else:
        Tux, Tvx, Tuy, Tvy = hr_var.Rascle2017_currents(
            Sm, wave_number["k_x"], wave_number["k_y"], U_mean, fetch, m_star=0.9
        )
        # This wind modulation transfer function should be applied to the
        # curvature spectrum 'Bm'
        Tw = hr_var.Johannessen2005_wind(
            wave_number["k_x"], wave_number["k_y"], U_mean, phi_w, m_star=0.9
        )

    mod_transfer = {"ux": Tux, "vx": Tvx, "uy": Tuy, "vy": Tvy, "wnd": Tw}
    return mod_transfer, wave_number
