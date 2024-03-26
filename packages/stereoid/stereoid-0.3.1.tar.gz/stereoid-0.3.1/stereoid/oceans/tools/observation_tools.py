import logging
import numpy
from scipy import interpolate
from collections import namedtuple
from typing import Tuple, Optional

from drama.geo.bistatic_pol import CompanionPolarizations
import stereoid.sar_performance as sar_perf
from stereoid.oceans import ObsGeo
from stereoid.oceans.waves.wave_spectra import Kudry_spec_polar


# Define logger level for debug purposes
logger = logging.getLogger(__name__)
ObsGeoTrio = namedtuple("ObsGeoTrio", ["concordia", "discordia", "sentinel1"])


def build_geometry(par_geometry: str, incident: float,
                   dau: Optional[float] = 300e3):
    """
    Compute geometry and performance.
    Input:
    par_geometry: Option file 
    incident: incident angle (rad)
    dau = 300e3 : distance between satellite (m)
    """

    # Geometry and Performance
    # TODO: see notes in ObsGeo, this needs to be
    # initialized with CompanionPolarizations, and we need two instances
    # since the geometry for the two Harmonies is not symmetric
    # AT: REVIEW
    cp_concordia = CompanionPolarizations(
        par_file=par_geometry, companion_delay=-dau / 7.4e3
    )
    cp_discordia = CompanionPolarizations(
        par_file=par_geometry, companion_delay=dau / 7.4e3
    )
    # a hack to get the spectral support for S1
    cp_sentinel1 = CompanionPolarizations(
        par_file=par_geometry, companion_delay=None
    )

    # Observation geometry calculated from orbit
    obs_geo_concordia = ObsGeo.from_companion_polarizations(
        incident, cp_concordia, degrees=False
    )
    obs_geo_discordia = ObsGeo.from_companion_polarizations(
        incident, cp_discordia, degrees=False
    )
    # a hack to get the spectral support for S1
    obs_geo_sentinel1 = ObsGeo.from_companion_polarizations(
        incident, cp_sentinel1, degrees=False
    )
    return ObsGeoTrio(obs_geo_concordia, obs_geo_discordia, obs_geo_sentinel1)


def build_performance_file(par):
    fstr_dual = sar_perf.sarperf_files(
        par.path, par.rx_cpc_name, mode=par.mode, runid=par.run_id, parpath=par.parfile
    )
    fstr_ati = sar_perf.sarperf_files(
        par.path, par.rx_ipc_name, mode=par.mode, runid=par.run_id, parpath=par.parfile
    )
    fstr_s1 = sar_perf.sarperf_files(
        par.path,
        "sentinel",
        is_bistatic=False,
        mode=par.mode,
        runid=par.run_id,
        parpath=par.parfile,
    )
    return fstr_dual, fstr_ati, fstr_s1


def set_polarization(rxpol: str) -> Tuple[str, list]:
    if rxpol == 'mM':
        polbase = ['m', 'M']
    elif rxpol == 'IO':
        polbase = ['I', 'O']
    else:
        logger.info("Unknown rxpol, defaulting to mM")
        rxpol = 'mM'
        polbase = ['m', 'M']
    return rxpol, polbase

# this function provides the input and output (kx,ky) to be used in wrappers.griddata_step1
# it does not do the actual rotation
# the interpolation algorithm for rotations is split up, because all spectra at the same incident angle require
# (more-or-less) the same rotation and it is rather slow
def compute_rotation(alpha_rot: float, ws: dict
                     ) -> Tuple[numpy.ndarray, numpy.ndarray]:
    # rotations with alpha_rot in radians
    kx_h = ws["k_x"] * numpy.cos(alpha_rot) + ws["k_y"] * numpy.sin(alpha_rot)
    ky_h = ws["k_y"] * numpy.cos(alpha_rot) - ws["k_x"] * numpy.sin(alpha_rot)
    xy = numpy.column_stack((ws["k_x"].flatten(), ws["k_y"].flatten()))
    uv = numpy.column_stack((kx_h.flatten(), ky_h.flatten()))
    return xy, uv

# this function does an actual rotation
def compute_rotation_polar(alpha_rot: float, ws: dict):
    # angles
    S=ws['S']
    phi=ws['phi']
    phi_int=phi-alpha_rot
    S_int = numpy.zeros(S.shape)

    # interpolation in polar coordinates is tricky due to wrapping, we will do this copying the spectrum a few times
    # it is a bit excessive, so we can speed it up
    phi=numpy.append(numpy.append(phi-2*numpy.pi,phi),phi+2*numpy.pi)
    S=numpy.vstack((S,S,S))

    # interpolate line-by-line
    for i in range(0,S.shape[1]):
        f = interpolate.interp1d(phi,S[:,i])
        S_int[:,i]=f(phi_int)

    return S_int

if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    from pylab import *
    #import stereoid.oceans.forward_models.backscatter as backscatter

    g = 9.81
    n_k=100
    lambda_min=0.005
    lambda_max=1000
    k_min = 2 * np.pi / lambda_max  # minimum wave number
    k_max = 2 * np.pi / lambda_min  # should at least pass the Bragg wave
    k = 10 ** np.linspace(np.log10(k_min),np.log10(k_max), n_k)
    nphi = 72
    phi = np.linspace(-np.pi, np.pi, nphi)
    omega = np.where(k > 0, np.sqrt(g * k), 0)
    dk = np.gradient(k)
    dphi = 2 * np.pi / nphi * np.ones(len(phi))

    # wave spectrum using Elfouhaily et al. (1997)
    u_10 = 10
    fetch = 500E3
    phi_w = 0
    B, B_neq, B_w, B_pc = Kudry_spec_polar(k, phi, u_10, fetch, phi_w, S=0)
    kv,phiv=np.meshgrid(k,phi)
    #dk, dphi = np.meshgrid(dk, dphi)
    S = np.where(kv > 0, B * kv ** -4, 0)
    cmap = cm.get_cmap('gist_ncar_r', 15)
    fig, ax = plt.subplots(subplot_kw=dict(projection= 'polar'))
    con=ax.pcolormesh(phiv, kv, np.log10(S),cmap=cmap,vmin=-15,vmax=0)
    ax.set_rscale('log')
    fig.colorbar(con,ax=ax)
    plt.show()

    ws = {"S": S, "k": k, "phi": phi}
    S_int=compute_rotation_polar(np.deg2rad(21), ws)

    cmap = cm.get_cmap('gist_ncar_r', 15)
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    con = ax.pcolormesh(phiv, kv, np.log10(S_int), cmap=cmap, vmin=-15, vmax=0)
    ax.set_rscale('log')
    fig.colorbar(con, ax=ax)
    plt.show()