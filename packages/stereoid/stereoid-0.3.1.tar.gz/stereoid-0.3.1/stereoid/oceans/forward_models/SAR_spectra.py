__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import stereoid.oceans.GMF.cmod5n as cmod5n
import numpy as np
import math
import copy
from typing import Optional, Tuple
from scipy.optimize import curve_fit
from stereoid.oceans.waves.wave_spectra import tuning_param_wb
from stereoid.oceans.forward_models.RIM_constants import constants as co
from stereoid.oceans.forward_models.Doppler import tilt_transfer_func
from stereoid.oceans.waves.wave_spectra import elfouhaily
from stereoid.oceans.waves.wave_spectra import elfouhaily_spread
from stereoid.oceans.bistatic_pol import elfouhaily_coefficient
from stereoid.oceans.forward_models.wrappers import (
    interp_weights as griddata_step1,
    interpolate as griddata_step2,
)
from stereoid.oceans.radar_model import SpectralNoiseModel
import stereoid.oceans.forward_models.wrappers as wrappers
from stereoid.oceans import ObsGeoAngles
from stereoid.polarimetry import pol_rotations as polrot
import stereoid.oceans.tools.observation_tools as obs_tools
from stereoid.oceans.forward_models.backscatter import backscatter_Kudry2023
from stereoid.oceans.forward_models.backscatter import backscatter_Kudry2023_polar
import logging

logger = logging.getLogger(__name__)

# Radar Wave length
K_R = 2 * np.pi / co.la_r


# FIXME: only works for 'V' transmit now
# FIXME: The noise of kx,ky should be 'conjugately' replicated for the
# co-spectra (for SWB, we only use the cr_spectra)
# run multistatic SAR spectra for the Harmony scientific work bench
def run_spectra_SWB(obsgeo, inc_m: float, long_waves: dict, short_waves: dict,
                    u10: float, phi_w: float, num_looks: int,
                    cross: Optional[bool] = True,
                    noise: Optional[bool] = True,
                    polbase: Optional[list] = ['m', 'M'],
                    nord: Optional[int] = 5,
                    fetch: Optional[float] = 100E3,
                    short_wave_spec_type: Optional[str] = 'polar'):
    """

    Parameters
    ----------
    obsgeo: ObsGeo
    inc_m: float
        Incidence angle in rad
    long_waves: dict
        Long wave spectrum dictionnary with S, k_x, k_y
        S has the same size as the SAR spectrum
    short_waves: dict
        short-wave Kudryavtsev spectrum with S(2D), k_x(2D), k_y(2D) or S(1D), k(1D), phi(1D)
    u10: float
        this is a non-local mean wind direction
        (maybe a 20 km x 20 km average)
    phi_w: float
        this is a non-local mean wind direction
    num_looks: int
        number of looks
    cross = True: bool
        compute cross-spectra or not (1, 0)
    noise = True: bool
        add noise to the spectra or not (1, 0)
    polbase = ['m', 'M']: list[bool]
        polarisation label for companions
    nord = 5: int
        Number of order
    fetch = 100e3: float
        Fetch length in m

    Returns
    -------

    """
    SHP = long_waves["S"].shape

    # output SAR spectra
    SAR_cospectra = {"S1": {}, "HA": {}, "HB": {}}
    SAR_crspectra = {"S1": {}, "HA": {}, "HB": {}}
    for key in SAR_cospectra.keys():
        if key == "S1":
            # Here for now I chose to use H/V for S1, but we could also just
            # stay with I (=H) and O (=V)
            SAR_cospectra[key] = {"H": np.zeros(SHP), "V": np.zeros(SHP)}
            SAR_crspectra[key] = {"H": np.zeros(SHP), "V": np.zeros(SHP)}
        else:
            SAR_cospectra[key] = {polbase[0]: np.zeros(SHP),
                                  polbase[1]: np.zeros(SHP)}
            SAR_crspectra[key] = {polbase[0]: np.zeros(SHP),
                                  polbase[1]: np.zeros(SHP)}

    # observation geometries
    (obs_geo_concordia, obs_geo_discordia, obs_geo_sentinel1) = (
        obsgeo.concordia,
        obsgeo.discordia,
        obsgeo.sentinel1,
    )

    # grid resolution for the Cartesian short-wave spectrum
    if short_wave_spec_type != 'polar':
        dk_ku = np.gradient(short_waves["k_x"][0, :])
        dks_ku = np.outer(dk_ku, dk_ku)

    # ######### monostatic ##########
    # ranges for the monostatic and the transmit bistatic
    Rt = obs_geo_concordia.swth_geo.inc2r_t(inc_m)

    # get the spectral content (wave spectrum/wave numbers and direction)
    obsgeo_angles = ObsGeoAngles(inc_m, None, 0)
    # FIXME: this wrapper implicitely assumes 'V' as transmit pol
    if short_wave_spec_type == 'polar':
        S_ku = copy.deepcopy(short_waves["S"])
        k_ku = copy.deepcopy(short_waves["k"])
        phi_ku = copy.deepcopy(short_waves["phi"])
    else:
        S_ku = copy.deepcopy(short_waves["S"])
        kx_ku = copy.deepcopy(short_waves["k_x"])
        ky_ku = copy.deepcopy(short_waves["k_y"])
    S = copy.deepcopy(long_waves["S"])
    kx = copy.deepcopy(long_waves["k_x"])
    ky = copy.deepcopy(long_waves["k_y"])

    #nwnd = np.mean(u10)

    # compute monostatic transfer functions and the scattering components (I think we can do this in the bistatic way)
    # the scattering components are required to weight the RAR transfer functions
    if short_wave_spec_type == 'polar':
        # scattering coefficients (and Doppler, not required)
        s_mono, d_mono, q = wrappers.backscatter_Doppler_mono_polar(S_ku, k_ku, phi_ku,
                                                              phi_w,
                                                              obsgeo_angles, u10,
                                                              fetch, degrees=False)

        # compute RAR transfer functions
        T_sp, T_br_hh, T_br_vv, T_wb = transfer_func_RAR_bist_polar(kx, ky, inc_m, inc_m,
                                                              0., mtf='RIM2023',
                                                              S_ku=S_ku,
                                                              k_ku=k_ku,
                                                              phi_ku=phi_ku,
                                                              phi_w=phi_w, u10=u10)
    else:
        # scattering coefficients (and Doppler, not required)
        s_mono, d_mono, q = wrappers.backscatter_Doppler_mono(S_ku, kx_ku, ky_ku,
                                                          dks_ku, phi_w,
                                                          obsgeo_angles, u10,
                                                          fetch, degrees=False)

        # compute RAR transfer functions
        T_sp, T_br_hh, T_br_vv, T_wb = transfer_func_RAR_bist(kx, ky, inc_m, inc_m,
                                                              0, mtf='RIM2023',
                                                              S_ku=S_ku,
                                                              kx_ku=kx_ku,
                                                              ky_ku=ky_ku, dks_ku=dks_ku,
                                                              phi_w=phi_w, u10=u10)



    # monostatic scattering and scattering ratios
    nrcs_co = (s_mono["Bragg"] + s_mono["specular"]) * (1 - q) + s_mono["wave_breaking"] * q
    rat = np.array(
        [s_mono["specular"] * (1 - q), s_mono["Bragg"] * (1 - q), s_mono["wave_breaking"] * q]) / nrcs_co

    # compute monostatic co-col (VV) transfer functions and associated covariance (correlation) functions
    TV_I = rat[0] * T_sp + rat[1] * T_br_vv + rat[2] * T_wb
    _res = corr_func_bist(long_waves, TV_I, inc_m, inc_m, 0, Rt, Rt)
    II, yy, xx, Iy, yI, Ix, xI, xy, yx = _res

    # co-polar (VV) SAR spectrum
    MV = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)
    MV = np.absolute(MV)
    # probably some rounding issues, or problems at (kx,ky==0.5ks)
    MV[0, 0] = 0

    # compute monostatic cross-col (VH) transfer functions and covarianc functions
    TH_I = T_wb * 1.0
    _res = corr_func_bist(long_waves, TH_I, inc_m, inc_m, 0, Rt, Rt)
    II, yy, xx, Iy, yI, Ix, xI, xy, yx = _res

    # cross-polar (VH) SAR spectrum
    MH = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)
    MH = np.absolute(MH)
    MH[0, 0] = 0

    # add noise to the co-spectrum
    if noise is True:
        # spectral noise model
        shp = S.shape
        dy = long_waves["k_y"][1, 0] - long_waves["k_y"][0, 0]
        dx = long_waves["k_x"][0, 1] - long_waves["k_x"][0, 0]
        SNM = SpectralNoiseModel(obsgeo.sentinel1.swth_geo, az_res=dy,
                                 grg_res=dx)

        Sc, sigma_SV = SNM.add_noise_correlated(MV, kx, ky, num_looks, inc_m)
        MV = Sc + compute_noise(sigma_SV)
        Sc, sigma_SH = SNM.add_noise_correlated(MH, kx, ky, num_looks, inc_m)
        MH = Sc + compute_noise(sigma_SH)

    # two mono-static cospectra get stored
    SAR_cospectra["S1"]["V"] = MV
    SAR_cospectra["S1"]["H"] = MH

    # compute monostatic co-pol and cross-pol cross-spectra
    if cross is True:
        II, yy, xx, Iy, yI, Ix, xI, xy, yx = corr_func_bist(long_waves, TV_I, inc_m, inc_m, 0, Rt, Rt, dT=0.075)
        MV_cr = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)
        II, yy, xx, Iy, yI, Ix, xI, xy, yx = corr_func_bist(long_waves, TH_I, inc_m, inc_m, 0, Rt, Rt, dT=0.075)
        MH_cr = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)

        # add noise to the cross-spectra
        if noise is True:
            MV_cr = MV_cr + (compute_noise(sigma_SV)
                             + 1j * compute_noise(sigma_SV)) / np.sqrt(2)
            MH_cr = MH_cr + (compute_noise(sigma_SH)
                             + 1j * compute_noise(sigma_SH)) / np.sqrt(2)
        MV_cr[0, 0] = 0
        MH_cr[0, 0] = 0

        # two mono-static cross-spectra get stored
        SAR_crspectra["S1"]["V"] = MV_cr
        SAR_crspectra["S1"]["H"] = MH_cr

    # ######### bistatic heading Harmony ##########
    # two mono-static cospectra
    Cm, CM, Cm_cr, CM_cr = func_spectrum(obs_geo_concordia, inc_m,
                                         obsgeo_angles,
                                         long_waves, short_waves, u10, phi_w,
                                         num_looks, Rt,
                                         cross=cross, noise=noise, nord=nord,
                                         magic_num=100, fetch=fetch,
                                         pol='V', rxpol=polbase)
    SAR_cospectra["HA"][polbase[0]] = Cm
    SAR_cospectra["HA"][polbase[1]] = CM

    # compute cross-spectrum
    if cross is True:
        SAR_crspectra["HA"][polbase[0]] = Cm_cr
        SAR_crspectra["HA"][polbase[1]] = CM_cr

    # ######### bistatic trailing Harmony ##########
    Dm, DM, Dm_cr, DM_cr = func_spectrum(obs_geo_discordia, inc_m,
                                         # Dm, DM, Dm_cr, DM_cr = func_spectrum(obs_geo_concordia, inc_m,
                                         obsgeo_angles,
                                         long_waves, short_waves, u10, phi_w,
                                         num_looks, Rt,
                                         cross=cross, noise=noise, nord=nord,
                                         magic_num=100, fetch=fetch,
                                         pol='V', rxpol=polbase)
    SAR_cospectra["HB"][polbase[0]] = Dm
    SAR_cospectra["HB"][polbase[1]] = DM

    # compute cross-spectrum
    if cross is True:
        SAR_crspectra["HB"][polbase[0]] = Dm_cr
        SAR_crspectra["HB"][polbase[1]] = DM_cr

    if cross is True:
        return SAR_cospectra, SAR_crspectra
    else:
        return SAR_cospectra


def func_spectrum(obs_geo_x, inc_m: float, obsgeo_angles, long_waves: dict,
                  short_waves: dict, nwnd_local: float, phi_w: float, n: int,
                  Rt: float,
                  cross: Optional[bool] = True, noise: Optional[bool] = True,
                  nord: Optional[int] = 4, magic_num: Optional[float] = 100,
                  pol: Optional[str] = 'V', rxpol: Optional[list] = ['m', 'M'],
                  fetch: Optional[float] = 100E3, short_wave_spec_type: Optional[str] = 'polar'):
    S = copy.deepcopy(long_waves["S"])
    kx = copy.deepcopy(long_waves["k_x"])
    ky = copy.deepcopy(long_waves["k_y"])
    if short_wave_spec_type == 'polar':
        S_ku = copy.deepcopy(short_waves["S"])
        k_ku = copy.deepcopy(short_waves["k"])
        phi_ku = copy.deepcopy(short_waves["phi"])
    else:
        S_ku = copy.deepcopy(short_waves["S"])
        kx_ku = copy.deepcopy(short_waves["k_x"])
        ky_ku = copy.deepcopy(short_waves["k_y"])
        dks_ku = copy.deepcopy(short_waves["dks"])

    # angles and ranges
    Rr = obs_geo_x.swth_geo.inc2r_r(inc_m)
    inc_me_x = obs_geo_x.swth_geo.inc2me_inc(inc_m)
    inc_b_x = obs_geo_x.swth_geo.inc2slave_inc(inc_m)
    bist_ang_x = obs_geo_x.swth_geo.inc2bistatic_angle_az(inc_m)
    alpha_rot_x = np.arctan2(np.sin(bist_ang_x) * np.sin(inc_b_x),
                             (np.sin(inc_m) + np.cos(bist_ang_x) * np.sin(inc_b_x)))

    # Rotation of the short wave spectrum
    if short_wave_spec_type == 'polar':
        S_ku_rot=obs_tools.compute_rotation_polar(alpha_rot_x, short_waves)
    else:
        xy, uv = obs_tools.compute_rotation(alpha_rot_x, short_waves)
        vtx, wts = griddata_step1(xy, uv)
        S_ku_rot = griddata_step2(S_ku.flatten(), vtx, wts)
        S_ku_rot = S_ku_rot.reshape(S_ku.shape)
    obsgeo_me = ObsGeoAngles(inc_me_x, None, alpha_rot_x)
    k_rx = K_R * obs_geo_x.swth_geo.inc2me_k_scaling(inc_m)

    if short_wave_spec_type == 'polar':
        s_me, d_bi = wrappers.backscatter_Doppler_monoeq_polar(S_ku_rot, k_ku, phi_ku, phi_w, obsgeo_me, obsgeo_angles,
                                                         nwnd_local, fetch, pol, k_r=k_rx, degrees=False)
        _res = transfer_func_RAR_bist_polar(kx, ky, inc_m, inc_b_x, bist_ang_x,
                                      mtf='RIM2023', S_ku=S_ku_rot, k_ku=k_ku,
                                      phi_ku=phi_ku, phi_w=phi_w, u10=nwnd_local)
    else:
        s_me, d_bi = wrappers.backscatter_Doppler_monoeq(S_ku_rot, kx_ku, ky_ku, dks_ku, phi_w, obsgeo_me, obsgeo_angles,
                                                     nwnd_local, fetch, pol, k_r=k_rx, degrees=False)
        _res = transfer_func_RAR_bist(kx, ky, inc_m, inc_b_x, bist_ang_x,
                                      mtf='RIM2023', S_ku=S_ku_rot, kx_ku=kx_ku,
                                      ky_ku=ky_ku, dks_ku=dks_ku, phi_w=phi_w, u10=nwnd_local)

    # compute RAR transfer functions
    msg = f'angles inc {np.degrees(inc_m):.3f}, inc_b {np.degrees(inc_b_x):.3f}, bist_ang {np.degrees(bist_ang_x):.3f}'
    logger.debug(msg)
    logger.debug(f'wind dir {np.rad2deg(phi_w):.3f}, norm {nwnd_local:.3f}')

    T_sp, T_br_hh, T_br_vv, T_wb = _res

    # polarimetry (I think this will only work without any cross-terms,
    # which we do not use)
    T_r_MM = s_me['Bragg'] * np.exp(1j * np.absolute(T_br_vv) / magic_num)
    T_r_mm = s_me['Bragg'] * np.exp(1j * np.absolute(T_br_hh) / magic_num)
    T_s = (s_me["specular"] * np.exp(1j * np.absolute(T_sp) / magic_num)
           + s_me["wave_breaking"] * np.exp(1j * np.absolute(T_wb) / magic_num))
    T_cp = s_me["wave_breaking_cross"] * np.exp(1j * np.absolute(T_wb) / magic_num)
    xcov_bi2 = polrot.monoeq2bistatic(
        T_r_MM,
        T_s,
        T_cp,
        inc_m,
        obs_geo_x.swth_geo,
        sigma_hh_r=T_r_mm,  # PLD: This should work, buit it is evil.
        txpol=pol,
        rxpol=rxpol,
        method="fp",
    )
    # we haFIXME: at the Bragg transfer functions there is a line at kx=0,
    # we have to check what this is

    # compute co-spectra
    Tm_I = np.angle(xcov_bi2[:, :, 0, 0]) * magic_num
    _res = corr_func_bist(long_waves, Tm_I, inc_m, inc_b_x, bist_ang_x, Rt, Rr)
    II, yy, xx, Iy, yI, Ix, xI, xy, yx = _res
    Bm = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)
    Bm = np.absolute(Bm)
    # probably some rounding issues, or problems at (kx,ky==0.5ks)
    Bm[0, 0] = 0

    TM_I = np.angle(xcov_bi2[:, :, 1, 1]) * magic_num
    _res = corr_func_bist(long_waves, TM_I, inc_m, inc_b_x, bist_ang_x, Rt, Rr)
    II, yy, xx, Iy, yI, Ix, xI, xy, yx = _res
    BM = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)
    BM = np.absolute(BM)
    # probably some rounding issues, or problems at (kx,ky==0.5ks)
    BM[0, 0] = 0

    # add noise to the co-spectrum
    if noise is True:
        shp = S.shape
        dy = long_waves["k_y"][1, 0] - long_waves["k_y"][0, 0]
        dx = long_waves["k_x"][0, 1] - long_waves["k_x"][0, 0]
        SNM = SpectralNoiseModel(obs_geo_x.swth_geo, az_res=dy,
                                 grg_res=dx)

        Sc, sigma_Sm = SNM.add_noise_correlated(Bm, kx, ky, n, inc_m)
        Bm = Sc + compute_noise(sigma_Sm)
        Sc, sigma_SM = SNM.add_noise_correlated(BM, kx, ky, n, inc_m)
        BM = Sc + compute_noise(sigma_SM)

    # two mono-static cross-spectra
    # SAR_cospectra["HB"][polbase[0]] = Bm
    # SAR_cospectra["HB"][polbase[1]] = BM
    Bm_cr = Bm * 0
    BM_cr = BM * 0
    # compute cross-spectrum
    if cross is True:
        _res = corr_func_bist(long_waves, Tm_I, inc_m, inc_b_x, bist_ang_x, Rt,
                              Rr, dT=0.075)
        II, yy, xx, Iy, yI, Ix, xI, xy, yx = _res
        Bm_cr = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)
        _res = corr_func_bist(long_waves, TM_I, inc_m, inc_b_x, bist_ang_x, Rt,
                              Rr, dT=0.075)
        II, yy, xx, Iy, yI, Ix, xI, xy, yx = _res
        BM_cr = SAR_spec_bist(II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky, ord=nord, al=1)

        # add noise to the cross-spectrum
        if noise is True:
            Bm_cr = (Bm_cr + (compute_noise(sigma_Sm)
                              + 1j * compute_noise(sigma_Sm)) / np.sqrt(2))
            BM_cr = (BM_cr + (compute_noise(sigma_SM)
                              + 1j * compute_noise(sigma_SM)) / np.sqrt(2))
        Bm_cr[0, 0] = 0
        BM_cr[0, 0] = 0

        # two mono-static cross-spectra
        # SAR_crspectra["HB"][polbase[0]] = Bm_cr
        # SAR_crspectra["HB"][polbase[1]] = BM_cr
    return Bm, BM, Bm_cr, BM_cr

# ensures the noise is flipped and conjugated
def compute_noise(sigma_n):
    """

    Parameters
    ----------
    sigma_n:
    spectral grid of noise standard deviations from Spectral Noise Model

    Returns
    -------
    N:
    realization of noise to be added to the spectra
    for cross-spectra divide by sqrt(2) and add to both real and imaginary values
    """

    # realization of noise
    shp=sigma_n.shape
    N_temp=np.random.randn(shp[0], shp[1])

    # ensure complex conjugates have absolute values equal at kx,ky and -kx,-ky
    # first handled the four quadrants
    N=N_temp*1.0
    q1 = N_temp[1:int(shp[0] / 2), 1:int(shp[1] / 2)]
    q3 = np.conj(np.flipud(np.fliplr(q1)))
    q2 = N_temp[int(shp[0] / 2 + 1):, 1:int(shp[1] / 2)]
    q4 = np.conj(np.flipud(np.fliplr(q2)))
    N[-int(shp[0] / 2 - 1):, -int(shp[1] / 2 - 1):] = q3
    N[1:int(shp[0] / 2), -int(shp[1] / 2 - 1):] = q4

    # handle the 'zero axis' (kx=0 or ky=0)
    N[0, -int(shp[1] / 2 - 1):] = np.flip(N_temp[0, 1:int(shp[1] / 2)])
    N[-int(shp[0] / 2 - 1):, 0] = np.flip(N_temp[1:int(shp[0] / 2), 0])

    # handle the 'Nyquist axis' (kx=max(ky) or ky=max(ky))
    N[int(shp[0] / 2), -int(shp[1] / 2 - 1):] = np.flip(N_temp[int(shp[0] / 2), 1:int(shp[1] / 2)])
    N[-int(shp[0] / 2 - 1):, int(shp[1] / 2)] = np.flip(N_temp[1:int(shp[0] / 2), int(shp[1] / 2)])

    return N

# bistatic RAR transfer functions
def transfer_func_RAR_bist_polar(kx, ky, theta_t, theta_r, alpha, mtf='Schulz',
                           phi_w=0.0, u10=10.0, S_ku=0,
                           k_ku=0, phi_ku=0, fetch=100E3):
    """Transfer function for RAR bistatic
    kx: array
        Wave number in range
    ky: array
        Wave number in azimuth
    theta_t: float
        angle in rad
    theta_r: float
        angle in rad
    alpha: float
        rotation angle in rad
    mtf = 'Schulz': str
        MTF type choose between Schulz, RIM, Fresnel
    phi_w = 0: float
        Wind direction in rad
    u10 = 15: float
        Waves?
    S_ky = 0: float
    kx_ku = 0: float
    ky_ku = 0: float
    dks_ku = 0: float
    fetch = 100E3: float

    """
    # angular frequency and some conversions
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)
    phi = np.arctan2(ky, kx)

    # some relevant angles for the monostatic approximation
    rt_hat = np.array([np.sin(theta_t), 0, np.cos(theta_t)])  # unit vector for the transmitter
    rr_hat = np.array(
        [np.sin(theta_r) * np.cos(alpha), np.sin(theta_r) * np.sin(alpha), np.cos(theta_r)])  # for the receiver
    r2w_hat = rt_hat + rr_hat  # two-way vector
    theta_m = np.arccos(r2w_hat[2]/np.linalg.norm(r2w_hat))  # monostatic-equivalent incident angle
    alpha_m = np.arctan2(np.sin(alpha) * np.sin(theta_r),
                         np.sin(theta_t) + np.cos(alpha) * np.sin(theta_r))  # monostatic-equivalent range direction
    k_r = K_R * np.linalg.norm(r2w_hat) / 2  # scaled radar wavenumber FIXME: check this, it should be okay
    #print(alpha,alpha_m)

    k_l = (kx * np.cos(alpha_m) - ky * np.sin(alpha_m))
    T_I = np.zeros(k.shape)

    if np.logical_and(mtf != 'RIM',mtf != 'RIM2023'):
        print('Warning! Only RIM2023 implemented for polar!')
        return T_I

    if np.logical_or(mtf == 'RIM',mtf == 'RIM2023'):
        # this mtf is derived from Hansen et al. (2012) [consistency SWB]
        # radar wave number scaled to the monostatic equivalent

        # get tilt transfer functions
        if mtf == 'RIM':
            print('Warning! Only RIM2023 implemented for polar!')
        '''
            Mt_sp, Mt_br_vv, Mt_br_hh, Mt_wb = tilt_transfer_func(S_ku, kx_ku, ky_ku, dks_ku, theta_m, k_r, phi_w)

            # hydrodynamic transfer functions
            k_wb = k_r / 10
            C_wb = np.sqrt(co.g / k_wb + co.gamma * k_wb / co.rho_w)
            omega_wb = np.sqrt(g * k_wb + co.gamma * k_wb ** 3 / co.rho_w)
            k_br = 2 * k_r * np.sin(theta_m)
            C_br = np.sqrt(co.g / k_br + co.gamma * k_br / co.rho_w)
            omega_br = np.sqrt(g * k_br + co.gamma * k_br ** 3 / co.rho_w)
            u_star = u10 * np.sqrt((0.8 + 0.065 * u10) * 1e-3)  # drag velocity
            _, n_br, C_b_br = tuning_param_wb(u_star, C_br * np.ones(1), k_br * np.ones(1))
            # m_g = 2 / n_br  # Kudry et al. (2003)
            beta_br = C_b_br * (u_star / C_br) ** 2  # Kudry et al. (1997)
            tau_br = n_br * beta_br[0] * omega_br / omega
            _, n_wb, C_b_wb = tuning_param_wb(u_star, C_wb * np.ones(1), k_wb * np.ones(1))
            # m_g = 2 / n_wb
            beta_wb = C_b_wb * (u_star / C_wb) ** 2
            tau_wb = n_wb * beta_wb[0] * omega_wb / omega
            Mh_br = co.m_k * np.cos(phi) ** 2 * (1 - 1j * tau_br) / (1 + tau_br ** 2)
            Mh_wb = -1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * np.cos(phi) ** 2) * (1 - 1j * tau_wb) / (
                    1 + tau_wb ** 2)
        '''

        if mtf == 'RIM2023':
            sigma_los, dsigmadth, q_s = backscatter_Kudry2023_polar(S_ku, k_ku, phi_ku, phi_w=phi_w, theta=theta_m,
                                                              u_10=u10,
                                                              k_r=k_r)
            Mt_sp=dsigmadth[0] # is zero
            Mt_br_vv=dsigmadth[1]
            Mt_br_hh=dsigmadth[2]
            Mt_wb=dsigmadth[3]

            # hydrodynamic transfer functions
            k_wb = k_r / 10
            C_wb = np.sqrt(co.g / k_wb + co.gamma * k_wb / co.rho_w)
            omega_wb = np.sqrt(g * k_wb + co.gamma * k_wb ** 3 / co.rho_w)
            u_star = u10 * np.sqrt((0.8 + 0.065 * u10) * 1e-3)  # drag velocity
            beta_wb = co.c_beta * (u_star / C_wb) ** 2
            mu_wb = co.n_g * beta_wb * omega_wb / omega
            #Mh_wb = co.n_k / 2 * (co.n_g + 1) * (1 + 0.5 * np.cos(2 * phi)) / k_wb * (1 - 1j * tau_wb) / (1 + tau_wb ** 2)
            #Mh_wb = co.n_k / 2 * (co.n_g + 1) * (1 + 0.5 * np.cos(2 * phi)) * (1 - 1j * tau_wb) / (1 + tau_wb ** 2)
            # FIXME: we have to be careful with the sign here
            Mh_wb = np.where(k > 0, -1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * np.cos(phi) ** 2) * (1 - 1j * mu_wb) / (1 + mu_wb ** 2),0)
            Mh_br = np.zeros(Mh_wb.shape)
            Mh_sp = np.zeros(Mh_wb.shape)

        # specular variations can be ignored
        # I think that the hydro transfer functions are now consistent with Schulz-Stellenfleth and Hansen
        # I think there is an error in Kudry et al. (1997)
        # The tilt transfer functions are not in-line with Li et al. (2019)
        # FIXME: this should be rigorously checked
        k_l = (kx * np.cos(alpha_m) - ky * np.sin(alpha_m))
        T_sp = -1j * k_l * Mt_sp + k * Mh_sp #+ 1j * k_l / np.tan(theta_m)
        T_br_hh = -1j * k_l * Mt_br_hh + k * Mh_br #+ 1j * k_l / np.tan(theta_m)
        T_br_vv = -1j * k_l * Mt_br_vv + k * Mh_br #+ 1j * k_l / np.tan(theta_m)
        T_wb = -1j * k_l * Mt_wb + k * Mh_wb #+ 1j * k_l / np.tan(theta_m)

        return T_sp, T_br_hh, T_br_vv, T_wb



# bistatic RAR transfer functions
def transfer_func_RAR_bist(kx, ky, theta_t, theta_r, alpha, mtf='Schulz',
                           phi_w=0.0, u10=10.0, S_ku=0,
                           kx_ku=0, ky_ku=0, dks_ku=0, fetch=100E3, pol='V'):
    """Transfer function for RAR bistatic
    kx: array
        Wave number in range
    ky: array
        Wave number in azimuth
    theta_t: float
        angle in rad
    theta_r: float
        angle in rad
    alpha: float
        rotation angle in rad
    mtf = 'Schulz': str
        MTF type choose between Schulz, RIM, Fresnel
    phi_w = 0: float
        Wind direction in rad
    u10 = 15: float
        Waves?
    S_ky = 0: float
    kx_ku = 0: float
    ky_ku = 0: float
    dks_ku = 0: float
    fetch = 100E3: float
    pol = 'V': str
        Polarization (only for Kirchhoff)

    """
    # angular frequency and some conversions
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)
    phi = np.arctan2(ky, kx)

    # some relevant angles for the monostatic approximation
    rt_hat = np.array([np.sin(theta_t), 0, np.cos(theta_t)])  # unit vector for the transmitter
    rr_hat = np.array(
        [np.sin(theta_r) * np.cos(alpha), np.sin(theta_r) * np.sin(alpha), np.cos(theta_r)])  # for the receiver
    r2w_hat = rt_hat + rr_hat  # two-way vector
    theta_m = np.arccos(r2w_hat[2]/np.linalg.norm(r2w_hat))  # monostatic-equivalent incident angle
    alpha_m = np.arctan2(np.sin(alpha) * np.sin(theta_r),
                         np.sin(theta_t) + np.cos(alpha) * np.sin(theta_r))  # monostatic-equivalent range direction
    k_r = K_R * np.linalg.norm(r2w_hat) / 2  # scaled radar wavenumber FIXME: check this, it should be okay
    #print(alpha,alpha_m)

    k_l = (kx * np.cos(alpha_m) - ky * np.sin(alpha_m))
    T_I = np.zeros(k.shape)
    if mtf == 'Schulz':
        # this is based on Schulz-Stellenfleth et al. (2002/2005)
        # FIXME Be careful, this one should be rigorously checked, things changed
        mu = 0.5  # relaxation parameter
        T_I = -1j * 4 * k_l / (np.tan(theta_m) * (1 + np.sin(theta_m) ** 2)) - 1j * k_l / np.tan(
            theta_m) + 4.5 * omega * k_l ** 2 * (omega - 1j * mu) / (k * (omega ** 2 + mu ** 2))

    if mtf == 'S1':
        # this is based on the S1 ocean product ATBD
        # FIXME I guess this k_l should be like below, but this should be rigorously checked, things changed
        dth = 0.001
        sigma = cmod5n.cmod5n_forward(np.array([u10, u10]), np.rad2deg(np.array([phi_w, phi_w])),
                                      np.rad2deg(np.array([theta_m, theta_m + dth])))
        # use CMOD5n here
        dsigma = (sigma[1] - sigma[0]) / dth
        T_I = k_l * dsigma / sigma[0] / np.cos(theta_m) * (
                k_l / k * np.sin(theta_m) + 1j * np.cos(theta_m))
        # combination of both equations (37)

    if mtf == 'Kirchhoff':
        # (Elfouhaily et al. 2001) [for Fred]
        # FIXME  this should be rigorously checked
        # monostatic equivalent, so use scaled k_r
        psi=90
        if pol=='H':
            psi=0
        dtheta = 0.001
        G1 = elfouhaily_coefficient(psi, 0, np.degrees(theta_m), 0, np.degrees(theta_m), k_r)
        G2 = elfouhaily_coefficient(psi, 0, np.degrees(theta_m + dtheta), 0,
                                    np.degrees(theta_m + dtheta), k_r)
        #print(G1-G2)
        #print(theta_m,np.degrees(theta_m))

        # Elfouhaily wave spectrum
        k_br1 = 2 * k_r * np.sin(theta_m)
        k_br2 = 2 * k_r * np.sin(theta_m + dtheta)
        Sp1 = elfouhaily(k_br1, u10, fetch)  # fetch hardcoded here, but I guess it will not change much
        Sp2 = elfouhaily(k_br2, u10, fetch)  # fetch hardcoded here, but I guess it will not change much
        dphi = np.angle(np.exp(1j * (phi_w + alpha_m)))  # including unwrapping
        D1 = elfouhaily_spread(k_br1, dphi, u10, fetch)
        D2 = elfouhaily_spread(k_br2, dphi, u10, fetch)
        Sr1 = 0.5 * Sp1 * D1 / k_br1 * 2 # FIXME: check factor 2 (don't think it matters, it cancels)
        Sr2 = 0.5 * Sp2 * D2 / k_br2 * 2
        #print(Sr1)
        dphi = np.angle(np.exp(1j * (phi_w + alpha_m-np.pi)))  # including unwrapping
        D1 = elfouhaily_spread(k_br1, dphi, u10, fetch)
        D2 = elfouhaily_spread(k_br2, dphi, u10, fetch)
        Sr1 = Sr1 + 0.5 * Sp1 * D1 / k_br1 * 2 # FIXME: check factor 2
        Sr2 = Sr2 + 0.5 * Sp2 * D2 / k_br2 * 2
        #print(Sr1)

        # Delta sigma
        # FIXME: k_r or K_R?
        sigma = 16 * np.pi * k_r ** 2 * G1 * Sr1  # equation 17 Elfouhaily 2001
        dsigmadtheta = 16 * np.pi * k_r ** 2 * (G2 * Sr2 - G1 * Sr1) / dtheta
        #print(1 / sigma * dsigmadtheta)
        T_I = -1j * k_l * 1 / sigma * dsigmadtheta
    T_I[T_I != T_I] = 0

    if np.logical_and(mtf != 'RIM',mtf != 'RIM2023'):
        return T_I

    if np.logical_or(mtf == 'RIM',mtf == 'RIM2023'):
        # this mtf is derived from Hansen et al. (2012) [consistency SWB]
        # radar wave number scaled to the monostatic equivalent

        # get tilt transfer functions
        if mtf == 'RIM':
            Mt_sp, Mt_br_vv, Mt_br_hh, Mt_wb = tilt_transfer_func(S_ku, kx_ku, ky_ku, dks_ku, theta_m, k_r, phi_w)

            # hydrodynamic transfer functions
            k_wb = k_r / 10
            C_wb = np.sqrt(co.g / k_wb + co.gamma * k_wb / co.rho_w)
            omega_wb = np.sqrt(g * k_wb + co.gamma * k_wb ** 3 / co.rho_w)
            k_br = 2 * k_r * np.sin(theta_m)
            C_br = np.sqrt(co.g / k_br + co.gamma * k_br / co.rho_w)
            omega_br = np.sqrt(g * k_br + co.gamma * k_br ** 3 / co.rho_w)
            u_star = u10 * np.sqrt((0.8 + 0.065 * u10) * 1e-3)  # drag velocity
            _, n_br, C_b_br = tuning_param_wb(u_star, C_br * np.ones(1), k_br * np.ones(1))
            # m_g = 2 / n_br  # Kudry et al. (2003)
            beta_br = C_b_br * (u_star / C_br) ** 2  # Kudry et al. (1997)
            tau_br = n_br * beta_br * omega_br / omega
            _, n_wb, C_b_wb = tuning_param_wb(u_star, C_wb * np.ones(1), k_wb * np.ones(1))
            # m_g = 2 / n_wb
            beta_wb = C_b_wb * (u_star / C_wb) ** 2
            tau_wb = n_wb * beta_wb * omega_wb / omega
            Mh_br = co.m_k * np.cos(phi) ** 2 * (1 - 1j * tau_br) / (1 + tau_br ** 2)
            Mh_wb = -1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * np.cos(phi) ** 2) * (1 - 1j * tau_wb) / (
                    1 + tau_wb ** 2)

        if mtf == 'RIM2023':
            sigma_los, dsigmadth, q_s = backscatter_Kudry2023(S_ku, kx_ku, ky_ku, dks_ku, phi_w=phi_w, theta=theta_m,
                                                              u_10=u10,
                                                              k_r=k_r, degrees=False)
            Mt_sp=dsigmadth[0] # is zero
            Mt_br_vv=dsigmadth[1]
            Mt_br_hh=dsigmadth[2]
            Mt_wb=dsigmadth[3]

            # hydrodynamic transfer functions
            k_wb = k_r / 10
            C_wb = np.sqrt(co.g / k_wb + co.gamma * k_wb / co.rho_w)
            omega_wb = np.sqrt(g * k_wb + co.gamma * k_wb ** 3 / co.rho_w)
            u_star = u10 * np.sqrt((0.8 + 0.065 * u10) * 1e-3)  # drag velocity
            beta_wb = co.c_beta * (u_star / C_wb) ** 2
            mu_wb = co.n_g * beta_wb * omega_wb / omega
            #Mh_wb = co.n_k / 2 * (co.n_g + 1) * (1 + 0.5 * np.cos(2 * phi)) / k_wb * (1 - 1j * tau_wb) / (1 + tau_wb ** 2)
            #Mh_wb = co.n_k / 2 * (co.n_g + 1) * (1 + 0.5 * np.cos(2 * phi)) * (1 - 1j * tau_wb) / (1 + tau_wb ** 2)
            Mh_wb = np.where(k > 0, -1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * np.cos(phi) ** 2) * (1 - 1j * mu_wb) / (1 + mu_wb ** 2),0)
            Mh_br = np.zeros(Mh_wb.shape)
            Mh_sp = np.zeros(Mh_wb.shape)

        # specular variations can be ignored
        # I think that the hydro transfer functions are now consistent with Schulz-Stellenfleth and Hansen
        # I think there is an error in Kudry et al. (1997)
        # The tilt transfer functions are not in-line with Li et al. (2019)
        # FIXME: this should be rigorously checked
        k_l = (kx * np.cos(alpha_m) - ky * np.sin(alpha_m))
        T_sp = -1j * k_l * Mt_sp + k * Mh_sp #- 1j * k_l / np.tan(theta_m)
        T_br_hh = -1j * k_l * Mt_br_hh + k * Mh_br #- 1j * k_l / np.tan(theta_m)
        T_br_vv = -1j * k_l * Mt_br_vv + k * Mh_br #- 1j * k_l / np.tan(theta_m)
        T_wb = -1j * k_l * Mt_wb + k * Mh_wb #- 1j * k_l / np.tan(theta_m)

        return T_sp, T_br_hh, T_br_vv, T_wb


# this is the bistatic equivalent of corr_func (Kleinherenbrink et al. (2022))
# be aware the x- and y-axis are switched in the paper
def corr_func_bist(waves: dict, T_I, theta_t, theta_r, alpha, R_t, R_r,
                   V=7400, dT=0):
    """
    this is the bistatic equivalent of corr_func (Kleinherenbrink et al(2022))
    waves: dict["S", "k_x", "k_y"]
        two-dimensional directional wave spectrum (Krogstad 1992: it is not
        symmetrical, but directional)
    T_I: float
        RAR transfer function
    theta_t: float
        incidence angle
    theta_r: float
        incidence angle
    alpha: float
        angle
    R_t: float
        range
    R_r: float
        range
    V: float
        platform velocity
    dT: float
        effective time between looks
    """
    # Swell parameters
    S = copy.deepcopy(waves["S"])
    kx = copy.deepcopy(waves["k_x"])
    ky = copy.deepcopy(waves["k_y"])
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)

    # compute some additional angles
    # alpha_p = np.arccos(R_t / R_r)
    # if alpha < 0:
    #    alpha_p = -alpha_p

    # some relevant vectors
    U_t = np.array([0, V, 0])  # velocity vectors
    U_r = np.array([0, V, 0])
    xhat = np.array([1, 0, 0])  # x/y directions
    yhat = np.array([0, 1, 0])
    rhatt = np.array([np.sin(theta_t), 0, np.cos(theta_t)])
    rhatr = np.array([np.sin(theta_r) * np.cos(alpha), np.sin(theta_r) * np.sin(alpha), np.cos(theta_r)])

    # spatial derivatives of unit vectors
    drhattdx = (xhat - np.sum(rhatt * xhat) * rhatt) / R_t
    drhatrdx = (xhat - np.sum(rhatr * xhat) * rhatr) / R_r
    drhattdy = (yhat - np.sum(rhatt * yhat) * rhatt) / R_t
    drhatrdy = (yhat - np.sum(rhatr * yhat) * rhatr) / R_r

    # ######### Transfer functions ###########
    # auxiliary functions
    # since I reversed order this might become messy (check this)
    dxdy = np.sin(alpha) * np.sin(theta_r) / (np.sin(theta_t) + np.cos(alpha) * np.sin(theta_r))
    dydx = 1 / dxdy
    proj_x = kx / k * (np.sin(theta_t) + np.sin(theta_r) * np.cos(alpha))
    proj_y = - ky / k * np.sin(theta_r) * np.sin(alpha)
    proj_z = 1j * (np.cos(theta_t) + np.cos(theta_r))
    aux = - omega * (proj_x + proj_y + proj_z)
    aux_x = 1 / ((np.sum(U_t * drhattdx) + np.sum(U_r * drhatrdx)) + (np.sum(U_t * drhattdy) + np.sum(U_r * drhatrdy)) * dydx)
    aux_y = 1 / ((np.sum(U_t * drhattdx) + np.sum(U_r * drhatrdx)) * dxdy + (np.sum(U_t * drhattdy) + np.sum(U_r * drhatrdy)))

    # Deprecated
    # aux = -R_t / V * omega * (1 / np.cos(alpha_p)**2 * (
    #        (kx * np.cos(alpha_p) - ky * np.sin(alpha_p)) / k * np.sin(theta_r) + 1j * np.cos(theta_r))
    #                          + (kx / k * np.sin(theta_t) + 1j * np.cos(theta_t)))
    # aux_x = 1 / (dydx * (1 + np.cos(alpha_p)) + np.sin(alpha_p) * np.sin(theta_t))
    # aux_y = 1 / (1 + np.cos(alpha_p) + dxdy * np.sin(alpha_p) * np.sin(theta_t))
    #T_I=T_I*0

    # 'SAR' transfer functions
    T_x = aux * aux_x
    T_y = aux * aux_y
    T_x[T_x != T_x] = 0
    T_y[T_y != T_y] = 0

    # ######### Cross-spectral functions ###########
    # cross-spectral functions
    N_II_pos = 0.5 * T_I * np.conj(T_I) * np.exp(-1j * omega * dT)
    N_yy_pos = 0.5 * T_y * np.conj(T_y) * np.exp(-1j * omega * dT)
    N_xx_pos = 0.5 * T_x * np.conj(T_x) * np.exp(-1j * omega * dT)
    N_Iy_pos = 0.5 * T_I * np.conj(T_y) * np.exp(-1j * omega * dT)
    N_yI_pos = 0.5 * T_y * np.conj(T_I) * np.exp(-1j * omega * dT)
    N_Ix_pos = 0.5 * T_I * np.conj(T_x) * np.exp(-1j * omega * dT)
    N_xI_pos = 0.5 * T_x * np.conj(T_I) * np.exp(-1j * omega * dT)
    N_yx_pos = 0.5 * T_y * np.conj(T_x) * np.exp(-1j * omega * dT)
    N_xy_pos = 0.5 * T_x * np.conj(T_y) * np.exp(-1j * omega * dT)

    # we need conj(N_II(-k))*S(-k)
    # this is under the assumption that we have a even number of samples
    # the principle is as follows:
    # 1. an FFT has outputs for wave numbers stored as [0 to N/2-1 and -N/2 to -1]*k_f
    # 2. after the FFTSHIFT this is [-N/2 to N/2-1]*k_f
    # 3. by flipping the output you get [N/2-1 running downwards to -N/2]
    # 4. here we do the multiplication np.conj(N_xx(-k)) * S(-k)
    # 5. because of the 'odd beast' at N/2 we have to shift the whole set by 1 step using np.roll
    # 5. The IFFTSHIFT ensures for outputs as [0 downwards to -N/2 and N/2-1 downwards to 1]
    # we can speed this up, but this makes is easier to interpret
    # Nk = len(k[:, 0])
    S_neg = np.fft.fftshift(S)
    S_neg = np.flipud(np.fliplr(S_neg))
    N_II_neg = np.fft.fftshift(N_II_pos)
    N_yy_neg = np.fft.fftshift(N_yy_pos)
    N_xx_neg = np.fft.fftshift(N_xx_pos)
    N_Iy_neg = np.fft.fftshift(N_Iy_pos)
    N_yI_neg = np.fft.fftshift(N_yI_pos)
    N_Ix_neg = np.fft.fftshift(N_Ix_pos)
    N_xI_neg = np.fft.fftshift(N_xI_pos)
    N_yx_neg = np.fft.fftshift(N_yx_pos)
    N_xy_neg = np.fft.fftshift(N_xy_pos)
    N_II_neg = np.flipud(np.fliplr(N_II_neg))
    N_yy_neg = np.flipud(np.fliplr(N_yy_neg))
    N_xx_neg = np.flipud(np.fliplr(N_xx_neg))
    N_Iy_neg = np.flipud(np.fliplr(N_Iy_neg))
    N_yI_neg = np.flipud(np.fliplr(N_yI_neg))
    N_Ix_neg = np.flipud(np.fliplr(N_Ix_neg))
    N_xI_neg = np.flipud(np.fliplr(N_xI_neg))
    N_yx_neg = np.flipud(np.fliplr(N_yx_neg))
    N_xy_neg = np.flipud(np.fliplr(N_xy_neg))
    SN_II_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_II_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_xx_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_xx_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yI_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yI_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_Iy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_Iy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_xI_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_xI_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_Ix_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_Ix_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yx_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yx_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_xy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_xy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))

    # ######### Correlation functions ###########
    # correlation functions
    rho_II = np.real(np.fft.ifft2(N_II_pos * S + SN_II_neg))  # / (2*np.pi)**2
    rho_yy = np.real(np.fft.ifft2(N_yy_pos * S + SN_yy_neg))  # / (2*np.pi)**2
    rho_xx = np.real(np.fft.ifft2(N_xx_pos * S + SN_xx_neg))  # / (2*np.pi)**2
    rho_Iy = np.real(np.fft.ifft2(N_Iy_pos * S + SN_Iy_neg))  # / (2*np.pi)**2
    rho_yI = np.real(np.fft.ifft2(N_yI_pos * S + SN_yI_neg))  # / (2*np.pi)**2
    rho_Ix = np.real(np.fft.ifft2(N_Ix_pos * S + SN_Ix_neg))  # / (2*np.pi)**2
    rho_xI = np.real(np.fft.ifft2(N_xI_pos * S + SN_xI_neg))  # / (2*np.pi)**2
    rho_yx = np.real(np.fft.ifft2(N_yx_pos * S + SN_yx_neg))  # / (2*np.pi)**2
    rho_xy = np.real(np.fft.ifft2(N_xy_pos * S + SN_xy_neg))  # / (2*np.pi)**2

    # check scaling
    '''
    S_neg= np.fft.ifftshift( np.roll( np.roll( S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    rho_ee=np.real( np.fft.ifft2( 0.5*S + 0.5*S_neg) )
    print(np.sqrt(rho_ee[0,0])*4)

    dk=kx[0,1]-kx[0,0]
    shp=kx.shape
    S_unsc=S/dk/dk/shp[0]/shp[1]
    S_unsc_neg=S/dk/dk/shp[0]/shp[1]
    rho_ee_check=np.sum((0.5*S_unsc+0.5*S_unsc_neg)*dk*dk)
    print( np.sqrt( rho_ee_check ) * 4 )
    '''

    return rho_II, rho_yy, rho_xx, rho_Iy, rho_yI, rho_Ix, rho_xI, rho_xy, rho_yx


# this is the extended version of SAR_spec
def SAR_spec_bist(rho_II, rho_yy, rho_xx, rho_Iy, rho_yI, rho_Ix, rho_xI,
                  rho_xy, rho_yx, kx, ky, al=1, be=0,
                  we=1, ord=4):
    # rho_ab: (co)variance functions
    # kx, ky: 2D waveform grid (cross and along)
    # al: cut-off inflation parameter
    # be: cut-off inflation parameter
    # we: weight of RAR
    # ord: length of expansion

    # dx and dy
    dkx = kx[0, 1] - kx[0, 0]
    dx = 2 * np.pi / dkx / len(kx[0, :])
    dky = ky[1, 0] - ky[0, 0]
    dy = 2 * np.pi / dky / len(ky[:, 0])

    # faster version (using an expansion)
    S2 = np.zeros(kx.shape, dtype=complex)
    for m in range(0, ord):
        xfac = (kx ** 2) ** m / math.factorial(m)
        for n in range(0, ord):
            yfac = (ky ** 2) ** n / math.factorial(n)
            for o in range(0, ord):
                xy_fac = (ky * kx) ** o / math.factorial(o)

                if o + n + m < ord:
                    dS = xfac * yfac * xy_fac * np.fft.fft2(
                        rho_xx ** m * rho_yy ** n * (rho_yx + rho_xy) ** o * (1 + rho_II * we))
                    S2 = S2 + dS

    S2 = np.exp(-kx ** 2 * (rho_xx[0, 0] * al + be) - ky ** 2 * (rho_yy[0, 0] * al + be) - ky * kx * (
            rho_yx[0, 0] * al + rho_xy[0, 0] * al + 2 * be)) * S2 * dx * dy

    # normalization
    S2 = S2 / (2 * np.pi) ** 2

    # '''

    ## I will keep this part in for cross-checking!!
    # it is necessary to do a non-linear mapping, so for each ky
    # (if you include range bunching each kx also) compute
    # the Fourier transform of G and select the row belonging to ky for the
    # spectrum
    '''
    # auxiliary
    # mu_xx = rho_xx - rho_xx[ 0, 0 ] * al - be
    # mu_yy = rho_yy - rho_yy[ 0, 0 ] * al - be
    # mu_xy = rho_xy - rho_xy[ 0, 0 ] * al - be
    # mu_yx = rho_yx - rho_yx[ 0, 0 ] * al - be

    # scene size divided by the number of samples
    # x = np.arange( 0, len( kx ) * dx, dx )
    # x = x.reshape( 1, len( kx ) )
    # scene size divided by the number of samples
    # y = np.arange( 0, len( ky ) * dy, dy )
    # y = y.reshape( len( ky ), 1 )

    import time
    start=time.time()
    S = np.zeros( kx.shape, dtype = complex )
    for i in range( 0, len( ky[ :, 0 ] ) ):
        for j in range( 0, len( kx[ 0, : ] ) ):
            # this will be equation 9 in Krogstad et al. (1994) excl. the I0-term or equation 31 in Engen and Johnsen (1995)
            if np.absolute( kx[ i, j ] ) < max_k and np.absolute( ky[ i, j ] ) < max_k:
                G = np.exp(
                    ky[ i, j ] ** 2 * mu_yy + kx[ i, j ] ** 2 * mu_xx + ky[ i, j ] * kx[ i, j ] * (mu_xy + mu_yx) ) * \
                    (1 + we * rho_II)  # + \
                # 1j * ky[i, j] * (rho_Iy - rho_yI) + \
                # ky[i, j] ** 2 * (rho_Iy- rho_Iy[0, 0] ) * (rho_yI - rho_yI[0, 0] ) + \
                # 1j * kx[i, j] * (rho_Ix - rho_xI) +\
                # kx[i, j] ** 2 * (rho_Ix - rho_Ix[0, 0]) * (rho_xI - rho_xI[0, 0]) + \
                # kx[i, j] * ky[i, j] * (rho_Ix - rho_Ix[0, 0]) * (rho_yI - rho_yI[0, 0]) + \
                # kx[i, j] * ky[i, j] * (rho_Iy - rho_Iy[0, 0]) * (rho_xI - rho_xI[0, 0]) )
                # FIXME: if you take the full spectral description also take into account weight

                DFT = np.outer( np.exp( -1j * ky[ i, j ] * y ), np.exp( -1j * kx[ i, j ] * x ) )
                S[ i, j ] = np.sum( G * DFT ) * dx * dy

    print( time.time() - start )
    # faster version
    from matplotlib import pyplot as plt
    from matplotlib.colors import LogNorm
    '''

    return S2

# this is phase/height spectra transform
def SAR_spec_bist_phase(rho_zz, rho_yy, rho_xx,
                  rho_xy, rho_yx, kx, ky, al=1, be=0,
                  we=1, ord=4):
    """
    This transform is a fast implementation to get a height, phase or I/Q spectrum. It differes from 'SAR_spec_bist' by a
    term '1' in the RAR and rho_II is replaced by rho_zz. You can still use 'corr_func_bist', but replace T_I with
    T_z.


    Parameters
    ----------
    rho_zz:
    cross-correlation function of heights, phases or I/Q values
    rho_yy
    rho_xx
    rho_xy
    rho_yx
    kx
    ky
    al
    be
    we
    ord

    Returns
    -------

    """
    # dx and dy
    dkx = kx[0, 1] - kx[0, 0]
    dx = 2 * np.pi / dkx / len(kx[0, :])
    dky = ky[1, 0] - ky[0, 0]
    dy = 2 * np.pi / dky / len(ky[:, 0])

    # faster version (using an expansion)
    S2 = np.zeros(kx.shape, dtype=complex)
    for m in range(0, ord):
        xfac = (kx ** 2) ** m / math.factorial(m)
        for n in range(0, ord):
            yfac = (ky ** 2) ** n / math.factorial(n)
            for o in range(0, ord):
                xy_fac = (ky * kx) ** o / math.factorial(o)

                if o + n + m < ord:
                    dS = xfac * yfac * xy_fac * np.fft.fft2(
                        rho_xx ** m * rho_yy ** n * (rho_yx + rho_xy) ** o * (rho_zz * we))
                    S2 = S2 + dS

    S2 = np.exp(-kx ** 2 * (rho_xx[0, 0] * al + be) - ky ** 2 * (rho_yy[0, 0] * al + be) - ky * kx * (
            rho_yx[0, 0] * al + rho_xy[0, 0] * al + 2 * be)) * S2 * dx * dy

    # normalization
    S2 = S2 / (2 * np.pi) ** 2

    return S2


# this is a version of SAR_spec_bist to estimate the wind-wave signal
# + the "cut-off of wind+swell"
# FIXME: this appears to work, but be cautious
def SAR_spec_bist_windwaves(wrho_II, wrho_yy, wrho_xx, wrho_xy, wrho_yx,
                            lambda_c, kx, ky, theta_t=35, theta_r=35,
                            alpha=0, al=1, be=0,
                            we=1, ord=4):  # ,rho_a,T_0,t_s):
    """
    # wrho_ab: (co)variance functions of wind wave system only
    # lambda_c: cut-off parameter
    # kx, ky: 2D waveform grid (cross and along)
    # theta_t: incident angle transmitter [degrees]
    # theta_r: incident angle receiver [degrees]
    # alpha: bistatic angle [degrees]
    # al: cut-off inflation parameter
    # be: cut-off inflation parameter
    # we: weight of RAR
    # ord: length of expansion
    """

    # convert to radians
    theta_t = np.deg2rad(theta_t)
    theta_r = np.deg2rad(theta_r)
    alpha = np.deg2rad(alpha)

    # get the effective range direction
    alpha_range = np.arctan(
        np.sin(alpha) * np.sin(theta_r) / (np.sin(theta_t) + np.cos(alpha) * np.sin(theta_r)))

    # compute some relevant parameters
    # k = kx ** 2 + ky ** 2
    d_k = (ky + kx * np.tan(alpha_range)) * np.cos(alpha_range)
    # wave-number distance to 'range direction'

    # estimate the variance functions
    if alpha != 0:
        rho = (lambda_c / np.pi) ** 2

    if alpha == 0:
        rho_yy0 = (lambda_c / np.pi) ** 2

    # dx and dy
    dkx = kx[0, 1] - kx[0, 0]
    dx = 2 * np.pi / dkx / len(kx[0, :])
    # scene size divided by the number of samples
    dky = ky[1, 0] - ky[0, 0]
    dy = 2 * np.pi / dky / len(ky[:, 0])
    # scene size divided by the number of samples

    # faster version (using an expansion)
    if alpha != 0:
        S2 = np.zeros(kx.shape, dtype=complex)
        for m in range(0, ord):
            xfac = (kx ** 2) ** m / math.factorial(m)
            for n in range(0, ord):
                yfac = (ky ** 2) ** n / math.factorial(n)
                for o in range(0, ord):
                    xy_fac = (ky * kx) ** o / math.factorial(o)

                    if o + n + m < ord:
                        dS = xfac * yfac * xy_fac * np.fft.fft2(
                            wrho_xx ** m * wrho_yy ** n * (wrho_yx + wrho_xy) ** o * (1 + wrho_II * we))
                        S2 = S2 + dS

        S2 = np.exp(-d_k ** 2 * (rho * al + be)) * S2 * dx * dy

    if alpha == 0:
        S2 = np.zeros(kx.shape, dtype=complex)
        for i in range(0, ord):
            S2 = S2 + 1 / math.factorial(i) * ky ** (2 * i) * np.fft.fft2(wrho_yy ** i * (1 + wrho_II))
        S2 = np.exp(-ky ** 2 * (rho_yy0 * al + be)) * S2 * dx * dy

    # normalization
    S2 = S2 / (2 * np.pi) ** 2

    return S2

def cutoff_and_macs(waves: dict, obsgeo,
                    compute_macs: Optional[bool] = True,
                    compute_cutoff: Optional[bool] = True,
                    vtx: Optional[np.ndarray] = np.zeros((3, 3)),
                    wts: Optional[np.ndarray] = np.zeros((3, 3))):
    """
    Parameters
    ----------
    waves: long waves dictionnary, contains key S, k_x, k_y
    obsgeo
    compute_macs
    compute_cutoff

    Returns
    -------
    cutoff
    macs

    """
    macs = 0
    cutoff = 0
    S = copy.deepcopy(waves["S"])
    kx = copy.deepcopy(waves["k_x"])
    ky = copy.deepcopy(waves["k_y"])
    # shape of ky and some spectrum properties
    shp = ky.shape
    dky = ky[1, 0] - ky[0, 0]
    dkx = kx[0, 1] - kx[0, 0]
    y_max = 2 * np.pi / dky
    y = np.linspace(-y_max / 2, y_max / 2, shp[0])

    # effective range direction
    u = np.sin(obsgeo.inc_m) + np.cos(obsgeo.bist_ang) * np.sin(obsgeo.inc_b)
    alpha_rot = np.arctan2(np.sin(obsgeo.bist_ang) * np.sin(obsgeo.inc_b), u)

    # this is for the monostatic case
    S_rot = S * 1.0
    kx_h = kx * 1.0
    ky_h = ky * 1.0

    # rotate grid for the bistatic forms
    if obsgeo.bist_ang != 0:
        kx_h = kx * np.cos(alpha_rot) - ky * np.sin(alpha_rot)
        ky_h = ky * np.cos(alpha_rot) + kx * np.sin(alpha_rot)
        if vtx.shape[0] == 3:
            xy = np.column_stack((kx.flatten(), ky.flatten()))
            uv = np.column_stack((kx_h.flatten(), ky_h.flatten()))
            vtx, wts = griddata_step1(uv, xy)
        S_rot = griddata_step2(S.flatten(), vtx, wts)
        S_rot = S_rot.reshape(S.shape)
        S_rot[np.absolute(ky_h) > np.max(ky)] = 0
        S_rot[np.absolute(kx_h) > np.max(kx)] = 0

    if compute_cutoff is True:
        # get one-dimensional cross-correlation
        rho = np.fft.ifft2(S_rot)
        rho = np.fft.ifftshift(np.real(rho))
        rho_y = np.sum(rho, axis=1)
        rho_y = rho_y / np.max(rho_y)

        # compute cut-off
        p0 = [0., 100.]  # initial settings
        try:
            Fcoeff, var_matrix = curve_fit(fit_cut_off, y, rho_y, p0=p0)
        except RuntimeError:
            Fcoeff = [0, 0]
        cutoff = np.real(Fcoeff[1])
        # from matplotlib import pyplot as plt
        # plt.plot(y,rho_y)
        # plt.show()

    if compute_macs is True:
        # MACS region
        # kx_lim1 = 2 * np.pi / 20
        # kx_lim2 = 2 * np.pi / 15
        # ky_lim = 2 * np.pi / 600
        # I_macs = np.logical_and( np.absolute( ky ) < ky_lim,
        # np.logical_and( kx > kx_lim1, kx < kx_lim2 ) )

        # compute MACS
        # macs = np.sum( S[ I_macs ] ) * dkx * dky

        # Gaussian weighting for MACS
        kx_0 = 2 * np.pi / 17.5
        sigma_kx = 0.05
        sigma_ky = 2 * np.pi / 600
        macs_filt = (np.exp(-(ky_h) ** 2 / sigma_ky ** 2)
                     * np.exp(-(kx_h - kx_0) ** 2 / sigma_kx ** 2))
        macs_filt = macs_filt / np.sum(macs_filt)
        # from matplotlib import pyplot as plt
        # plt.imshow( np.fft.fftshift( macs_filt ), origin = 'lower' )
        # plt.show()
        # compute MACS
        macs = np.sum(S * macs_filt * dky * dkx)

    return cutoff, macs


def fit_cut_off(y, *p):
    y0, la = p
    return np.exp(-np.pi ** 2 * (y - y0) ** 2 / (la ** 2))


# SEASTAR RAR transfer functions
def transfer_func_RAR_SEASTAR(kx, ky, theta, alpha, mtf='Kirchhoff',
                           phi_w=0.0, u10=10.0, fetch=100E3, pol='V'):
    """Transfer function for RAR bistatic
    kx: array
        Wave number in range
    ky: array
        Wave number in azimuth
    theta_t: float
        angle in rad
    theta_r: float
        angle in rad
    alpha: float
        rotation angle in rad
    mtf = 'Schulz': str
        MTF type choose between Schulz, RIM, Fresnel
    phi_w = 0: float
        Wind direction in rad
    u10 = 15: float
        Waves?
    S_ky = 0: float
    kx_ku = 0: float
    ky_ku = 0: float
    dks_ku = 0: float
    fetch = 100E3: float
    pol = 'V': str
        Polarization (only for Kirchhoff)

    """
    # angular frequency and some conversions
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    k_l = (kx * np.cos(alpha) - ky * np.sin(alpha))

    T_I = np.zeros(k.shape)
    if mtf == 'Kirchhoff':
        # (Elfouhaily et al. 2001) [for Fred]
        # FIXME  this should be rigorously checked
        # monostatic equivalent, so use scaled k_r
        psi=90
        if pol=='H':
            psi=0
        dtheta = 0.001
        G1 = elfouhaily_coefficient(psi, 0, np.degrees(theta), 0, np.degrees(theta), K_R)
        G2 = elfouhaily_coefficient(psi, 0, np.degrees(theta + dtheta), 0,
                                    np.degrees(theta + dtheta), K_R)
        #print(G1-G2)
        #print(theta_m,np.degrees(theta_m))

        # Elfouhaily wave spectrum
        k_br1 = 2 * K_R * np.sin(theta)
        k_br2 = 2 * K_R * np.sin(theta + dtheta)
        Sp1 = elfouhaily(k_br1, u10, fetch)  # fetch hardcoded here, but I guess it will not change much
        Sp2 = elfouhaily(k_br2, u10, fetch)  # fetch hardcoded here, but I guess it will not change much
        dphi = np.angle(np.exp(1j * (phi_w + alpha)))  # including unwrapping
        D1 = elfouhaily_spread(k_br1, dphi, u10, fetch)
        D2 = elfouhaily_spread(k_br2, dphi, u10, fetch)
        Sr1 = 0.5 * Sp1 * D1 / k_br1 * 2 # FIXME: check factor 2 (don't think it matters, it cancels)
        Sr2 = 0.5 * Sp2 * D2 / k_br2 * 2
        #print(Sr1)
        dphi = np.angle(np.exp(1j * (phi_w + alpha-np.pi)))  # including unwrapping
        D1 = elfouhaily_spread(k_br1, dphi, u10, fetch)
        D2 = elfouhaily_spread(k_br2, dphi, u10, fetch)
        Sr1 = Sr1 + 0.5 * Sp1 * D1 / k_br1 * 2 # FIXME: check factor 2
        Sr2 = Sr2 + 0.5 * Sp2 * D2 / k_br2 * 2
        #print(Sr1)

        # Delta sigma
        sigma = 16 * np.pi * K_R ** 2 * G1 * Sr1  # equation 17 Elfouhaily 2001
        dsigmadtheta = 16 * np.pi * K_R ** 2 * (G2 * Sr2 - G1 * Sr1) / dtheta
        #print(1 / sigma * dsigmadtheta)
        T_I = -1j * k_l * 1 / sigma * dsigmadtheta
    T_I[T_I != T_I] = 0

    return T_I

# this is the SEASTAR equivalent of corr_func (Kleinherenbrink et al. (2022))
# be aware the x- and y-axis are switched in the paper
def corr_func_SEASTAR(waves: dict, T_I, theta, alpha, R_t, V=7400, dT=0):
    """
    this is the bistatic equivalent of corr_func (Kleinherenbrink et al(2022))
    waves: dict["S", "k_x", "k_y"]
        two-dimensional directional wave spectrum (Krogstad 1992: it is not
        symmetrical, but directional)
    T_I: float
        hydrodynamic relaxation rate
    theta_t: float
        incidence angle
    theta_r: float
        incidence angle
    alpha: float
        angle
    R_t: float
        range
    R_r: float
        range
    V: float
        platform velocity
    dT: float
        effective time between looks
    """
    # Swell parameters
    S = copy.deepcopy(waves["S"])
    kx = copy.deepcopy(waves["k_x"])
    ky = copy.deepcopy(waves["k_y"])
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)

    # compute some additional angles
    # alpha_p = np.arccos(R_t / R_r)
    # if alpha < 0:
    #    alpha_p = -alpha_p

    # some relevant vectors
    U_t = np.array([0, V, 0])  # velocity vectors
    U_r = np.array([0, V, 0])
    xhat = np.array([1, 0, 0])  # x/y directions
    yhat = np.array([0, 1, 0])
    rhatt = np.array([np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), np.cos(theta)])
    rhatr = np.array([np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), np.cos(theta)])

    # spatial derivatives of unit vectors
    drhattdx = (xhat - np.sum(rhatt * xhat) * rhatt) / R_t
    drhatrdx = (xhat - np.sum(rhatr * xhat) * rhatr) / R_t
    drhattdy = (yhat - np.sum(rhatt * yhat) * rhatt) / R_t
    drhatrdy = (yhat - np.sum(rhatr * yhat) * rhatr) / R_t

    # ######### Transfer functions ###########
    # auxiliary functions
    # since I reversed order this might become messy (check this)
    dxdy = np.sin(alpha) * np.sin(theta) / (np.cos(alpha) * np.sin(theta))
    dydx = 1 / dxdy
    proj_x = kx / k * np.sin(theta) * np.cos(alpha) * 2
    proj_y = - ky / k * np.sin(theta) * np.sin(alpha) * 2
    proj_z = 1j * (np.cos(theta) + np.cos(theta))
    aux = - omega * (proj_x + proj_y + proj_z)
    aux_x = 1 / ((np.sum(U_t * drhattdx) + np.sum(U_r * drhatrdx)) + (np.sum(U_t * drhattdy) + np.sum(U_r * drhatrdy)) * dydx)
    aux_y = 1 / ((np.sum(U_t * drhattdx) + np.sum(U_r * drhatrdx)) * dxdy + (np.sum(U_t * drhattdy) + np.sum(U_r * drhatrdy)))

    # Deprecated
    # aux = -R_t / V * omega * (1 / np.cos(alpha_p)**2 * (
    #        (kx * np.cos(alpha_p) - ky * np.sin(alpha_p)) / k * np.sin(theta_r) + 1j * np.cos(theta_r))
    #                          + (kx / k * np.sin(theta_t) + 1j * np.cos(theta_t)))
    # aux_x = 1 / (dydx * (1 + np.cos(alpha_p)) + np.sin(alpha_p) * np.sin(theta_t))
    # aux_y = 1 / (1 + np.cos(alpha_p) + dxdy * np.sin(alpha_p) * np.sin(theta_t))
    #T_I=T_I*0

    # 'SAR' transfer functions
    T_x = aux * aux_x
    T_y = aux * aux_y
    T_x[T_x != T_x] = 0
    T_y[T_y != T_y] = 0

    # ######### Cross-spectral functions ###########
    # cross-spectral functions
    N_II_pos = 0.5 * T_I * np.conj(T_I) * np.exp(-1j * omega * dT)
    N_yy_pos = 0.5 * T_y * np.conj(T_y) * np.exp(-1j * omega * dT)
    N_xx_pos = 0.5 * T_x * np.conj(T_x) * np.exp(-1j * omega * dT)
    N_Iy_pos = 0.5 * T_I * np.conj(T_y) * np.exp(-1j * omega * dT)
    N_yI_pos = 0.5 * T_y * np.conj(T_I) * np.exp(-1j * omega * dT)
    N_Ix_pos = 0.5 * T_I * np.conj(T_x) * np.exp(-1j * omega * dT)
    N_xI_pos = 0.5 * T_x * np.conj(T_I) * np.exp(-1j * omega * dT)
    N_yx_pos = 0.5 * T_y * np.conj(T_x) * np.exp(-1j * omega * dT)
    N_xy_pos = 0.5 * T_x * np.conj(T_y) * np.exp(-1j * omega * dT)

    # we need conj(N_II(-k))*S(-k)
    # this is under the assumption that we have a even number of samples
    # the principle is as follows:
    # 1. an FFT has outputs for wave numbers stored as [0 to N/2-1 and -N/2 to -1]*k_f
    # 2. after the FFTSHIFT this is [-N/2 to N/2-1]*k_f
    # 3. by flipping the output you get [N/2-1 running downwards to -N/2]
    # 4. here we do the multiplication np.conj(N_xx(-k)) * S(-k)
    # 5. because of the 'odd beast' at N/2 we have to shift the whole set by 1 step using np.roll
    # 5. The IFFTSHIFT ensures for outputs as [0 downwards to -N/2 and N/2-1 downwards to 1]
    # we can speed this up, but this makes is easier to interpret
    # Nk = len(k[:, 0])
    S_neg = np.fft.fftshift(S)
    S_neg = np.flipud(np.fliplr(S_neg))
    N_II_neg = np.fft.fftshift(N_II_pos)
    N_yy_neg = np.fft.fftshift(N_yy_pos)
    N_xx_neg = np.fft.fftshift(N_xx_pos)
    N_Iy_neg = np.fft.fftshift(N_Iy_pos)
    N_yI_neg = np.fft.fftshift(N_yI_pos)
    N_Ix_neg = np.fft.fftshift(N_Ix_pos)
    N_xI_neg = np.fft.fftshift(N_xI_pos)
    N_yx_neg = np.fft.fftshift(N_yx_pos)
    N_xy_neg = np.fft.fftshift(N_xy_pos)
    N_II_neg = np.flipud(np.fliplr(N_II_neg))
    N_yy_neg = np.flipud(np.fliplr(N_yy_neg))
    N_xx_neg = np.flipud(np.fliplr(N_xx_neg))
    N_Iy_neg = np.flipud(np.fliplr(N_Iy_neg))
    N_yI_neg = np.flipud(np.fliplr(N_yI_neg))
    N_Ix_neg = np.flipud(np.fliplr(N_Ix_neg))
    N_xI_neg = np.flipud(np.fliplr(N_xI_neg))
    N_yx_neg = np.flipud(np.fliplr(N_yx_neg))
    N_xy_neg = np.flipud(np.fliplr(N_xy_neg))
    SN_II_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_II_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_xx_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_xx_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yI_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yI_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_Iy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_Iy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_xI_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_xI_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_Ix_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_Ix_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yx_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yx_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_xy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_xy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))

    # ######### Correlation functions ###########
    # correlation functions
    rho_II = np.real(np.fft.ifft2(N_II_pos * S + SN_II_neg))  # / (2*np.pi)**2
    rho_yy = np.real(np.fft.ifft2(N_yy_pos * S + SN_yy_neg))  # / (2*np.pi)**2
    rho_xx = np.real(np.fft.ifft2(N_xx_pos * S + SN_xx_neg))  # / (2*np.pi)**2
    rho_Iy = np.real(np.fft.ifft2(N_Iy_pos * S + SN_Iy_neg))  # / (2*np.pi)**2
    rho_yI = np.real(np.fft.ifft2(N_yI_pos * S + SN_yI_neg))  # / (2*np.pi)**2
    rho_Ix = np.real(np.fft.ifft2(N_Ix_pos * S + SN_Ix_neg))  # / (2*np.pi)**2
    rho_xI = np.real(np.fft.ifft2(N_xI_pos * S + SN_xI_neg))  # / (2*np.pi)**2
    rho_yx = np.real(np.fft.ifft2(N_yx_pos * S + SN_yx_neg))  # / (2*np.pi)**2
    rho_xy = np.real(np.fft.ifft2(N_xy_pos * S + SN_xy_neg))  # / (2*np.pi)**2

    # check scaling
    '''
    S_neg= np.fft.ifftshift( np.roll( np.roll( S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    rho_ee=np.real( np.fft.ifft2( 0.5*S + 0.5*S_neg) )
    print(np.sqrt(rho_ee[0,0])*4)

    dk=kx[0,1]-kx[0,0]
    shp=kx.shape
    S_unsc=S/dk/dk/shp[0]/shp[1]
    S_unsc_neg=S/dk/dk/shp[0]/shp[1]
    rho_ee_check=np.sum((0.5*S_unsc+0.5*S_unsc_neg)*dk*dk)
    print( np.sqrt( rho_ee_check ) * 4 )
    '''

    return rho_II, rho_yy, rho_xx, rho_Iy, rho_yI, rho_Ix, rho_xI, rho_xy, rho_yx





## This function is for the monostatic case, but is not rigorously checked anymore. Use the bistatic one!!!
# monostatic RAR transfer functions
def transfer_func_RAR(kx, ky, theta, mtf='Schulz', phi_w=0.0, u10=15.0,
                      S_ku=0, kx_ku=0, ky_ku=0,
                      dks_ku=0, fetch=100E3):
    """

    Parameters
    ----------
    kx
    ky
    theta
    mtf
    phi_w
    u10
    mu
    S_ku
    kx_ku
    ky_ku

    Returns
    -------

    """
    # angular frequency
    theta = np.deg2rad(theta)
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)
    phi = np.arctan2(ky, kx)

    T_I = np.zeros(k.shape)
    if mtf == 'Schulz':
        # this mtf is based on Schulz-Stellenfleth et al. (2002/2005)
        mu = 0.5  # relaxation parameter
        T_I = (-1j * 4 * kx / (np.tan(theta) * (1 + np.sin(theta) ** 2))
               - 1j * kx / np.tan(theta) + 4.5 * omega * kx ** 2
               * (omega - 1j * mu) / (k * (omega ** 2 + mu ** 2)))

    if mtf == 'S1':
        # this mtf is based on the ATBD of the ocean product of S1
        dth = 0.001
        # use CMOD5n here
        sigma = cmod5n.cmod5n_forward(np.array([u10, u10]),
                                      np.array([phi_w, phi_w]),
                                      np.rad2deg(np.array([theta, theta + dth])))
        dsigma = (sigma[1] - sigma[0]) / dth
        T_I = kx * dsigma / sigma[0] / np.cos(theta) * (
                kx / k * np.sin(theta) + 1j * np.cos(theta))
        # combination of both equations (37)

    if mtf == 'Fresnel':
        # this mtf uses the slope of Fresnel scattering
        # (Elfouhaily et al. 2001) [for Fred]

        # assumption is 'V' transmit
        dtheta = 0.001
        # equation 36/18, Elfouhaily et al. (1999/2001)
        G1 = elfouhaily_coefficient(90, 0, theta, 0, theta, K_R)
        G2 = elfouhaily_coefficient(90, 0, theta + dtheta, 0, theta + dtheta, K_R)

        # Elfouhaily wave spectrum
        k_br1 = 2 * K_R * np.sin(theta)
        k_br2 = 2 * K_R * np.sin(theta + dtheta)
        Sp1 = elfouhaily(k_br1, u10, fetch)
        Sp2 = elfouhaily(k_br2, u10, fetch)
        # including unwrapping
        dphi = (phi_w - 0 + np.pi) % (2 * np.pi) - np.pi
        D1 = elfouhaily_spread(k_br1, dphi, u10, fetch)
        D2 = elfouhaily_spread(k_br2, dphi, u10, fetch)
        Sr1 = 0.5 * Sp1 * D1 / k_br1
        Sr2 = 0.5 * Sp2 * D2 / k_br2
        # including unwrapping
        dphi = (phi_w - np.pi - 0 + np.pi) % (2 * np.pi) - np.pi
        D1 = elfouhaily_spread(k_br1, dphi, u10, fetch)
        D2 = elfouhaily_spread(k_br2, dphi, u10, fetch)
        Sr1 = Sr1 + 0.5 * Sp1 * D1 / k_br1
        Sr2 = Sr2 + 0.5 * Sp2 * D2 / k_br2

        # Delta sigma
        sigma = 16 * np.pi * K_R ** 2 * G1 * Sr1
        dsigmadtheta = 16 * np.pi * K_R ** 2 * (G2 * Sr2 - G1 * Sr1) / dtheta
        T_I = -1j * kx * 1 / sigma * dsigmadtheta
    T_I[T_I != T_I] = 0

    if mtf != 'RIM':
        return T_I

    if mtf == 'RIM':
        # this mtf is derived from Hansen et al. (2012) [consistency SWB]

        # get tilt transfer functions
        Mt_sp, Mt_br_vv, Mt_br_hh, Mt_wb = tilt_transfer_func(S_ku, kx_ku,
                                                              ky_ku, dks_ku, theta, K_R, phi_w)

        # hydrodynamic transfer functions
        # FIXME: the tau's need to be updated like in the bistatic function
        Mh_br = co.m_k * np.cos(phi) ** 2 * (1 - 1j * co.tau_br) / (1 + co.tau_br ** 2)
        Mh_wb = (-1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * np.cos(phi) ** 2)
                 * (1 - 1j * co.tau_wb) / (1 + co.tau_wb ** 2))

        # specular variations can be ignored
        # I think that the hydro transfer functions are now consistent
        # with Schulz-Stellenfleth and Hansen
        # I think there is an error in Kudry et al. (1997)
        # The tilt transfer functions are not in-line with Li et al. (2019)
        # FIXME: this should be rigorously checked
        T_sp = -1j * kx * Mt_sp + 0 - 1j * kx / np.tan(theta)
        T_br_hh = -1j * kx * Mt_br_hh + k * Mh_br - 1j * kx / np.tan(theta)
        T_br_vv = -1j * kx * Mt_br_vv + k * Mh_br - 1j * kx / np.tan(theta)
        T_wb = -1j * kx * Mt_wb + k * Mh_wb - 1j * kx / np.tan(theta)

        return T_sp, T_br_hh, T_br_vv, T_wb

## This function is for the monostatic case, but is not rigorously checked anymore. Use the bistatic one!!!
# Implementation of Engen and Johnsen (1995)
# This works with linear spacing in kx and ky, maybe we have to change this
# I will make another function for a log-scale spacing
def corr_func(S, kx, ky, T_I, theta, R, V=7400, dT=0):
    """
    corr_func: Implementation of Engen and Johnsen (1995)
    S: two-dimensional directional wave spectrum (Krogstad 1992:
    it is not symmetrical, but directional)
    kx: wave numbers in the cross-direction (as in an FFT)
    ky: wave numbers in the along-direction (as in an FFT)
    mu: hydrodynamic relaxation rate (necessary for Schulz RAR mtf)
    theta: incidenet angle
    R: range
    V: platform velocity
    phi_w: wind direction (necessary for GMF based mtf)
    u10: wind speed (necessary for GMF based mtf)
    dT: effective time between looks
    """
    # angular frequency
    theta = np.deg2rad(theta)
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)

    # ######### Transfer functions ###########
    # 'SAR' transfer functions
    T_y = -R / V * omega * (kx / k * np.sin(theta) + 1j * np.cos(theta))
    T_y[T_y != T_y] = 0

    # ######### Cross-spectral functions ###########
    # positive cross-spectral functions
    N_II_pos = 0.5 * T_I * np.conj(T_I) * np.exp(-1j * omega * dT)
    N_yy_pos = 0.5 * T_y * np.conj(T_y) * np.exp(-1j * omega * dT)
    N_Iy_pos = 0.5 * T_I * np.conj(T_y) * np.exp(-1j * omega * dT)
    N_yI_pos = 0.5 * T_y * np.conj(T_I) * np.exp(-1j * omega * dT)

    # we need conj(N_II(-k))*S(-k)
    # this is under the assumption that we have a even number of samples
    # the principle is as follows:
    # 1. an FFT has outputs for wave numbers stored as
    # [0 to N/2-1 and -N/2 to -1]*k_f
    # 2. after the FFTSHIFT this is [-N/2 to N/2-1]*k_f
    # 3. by flipping the output you get [N/2-1 running downwards to -N/2]
    # 4. here we do the multiplication np.conj(N_xx(-k)) * S(-k)
    # 5. because of the 'odd beast' at N/2 we have to shift the whole set by 1
    # step using np.roll
    # 5. The IFFTSHIFT ensures for outputs as [0 downwards to -N/2 and N/2-1
    # downwards to 1]
    # we can speed this up, but this makes is easier to interpret
    # Nk = len(k[:, 0])
    S_neg = np.fft.fftshift(S)
    # watch out this stays in the fft-shifted system
    S_neg = np.flipud(np.fliplr(S_neg))
    N_II_neg = np.fft.fftshift(N_II_pos)
    N_yy_neg = np.fft.fftshift(N_yy_pos)
    N_Iy_neg = np.fft.fftshift(N_Iy_pos)
    N_yI_neg = np.fft.fftshift(N_yI_pos)
    N_II_neg = np.flipud(np.fliplr(N_II_neg))
    N_yy_neg = np.flipud(np.fliplr(N_yy_neg))
    N_Iy_neg = np.flipud(np.fliplr(N_Iy_neg))
    N_yI_neg = np.flipud(np.fliplr(N_yI_neg))
    SN_II_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_II_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_yI_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_yI_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))
    SN_Iy_neg = np.fft.ifftshift(np.roll(np.roll(np.conj(N_Iy_neg) * S_neg, 1,
                                                 axis=0), 1, axis=1))

    # ######### Correlation functions ###########
    # correlation functions
    rho_II = np.real(np.fft.ifft2(N_II_pos * S + SN_II_neg))  # / (2*np.pi)**2
    rho_yy = np.real(np.fft.ifft2(N_yy_pos * S + SN_yy_neg))  # / (2*np.pi)**2
    rho_Iy = np.real(np.fft.ifft2(N_Iy_pos * S + SN_Iy_neg))  # / (2*np.pi)**2
    rho_yI = np.real(np.fft.ifft2(N_yI_pos * S + SN_yI_neg))  # / (2*np.pi)**2

    return rho_II, rho_yy, rho_Iy, rho_yI

## This function is for the monostatic case, but is not rigorously checked anymore. Use the bistatic one!!!
# now based on Engen and Johnsen (1995) / Krogstad et al. (1994)
def SAR_spec(rho_II, rho_yy, rho_Iy, rho_yI, kx, ky, al=1, be=0, we=1, ord=4):
    '''
    # rho_ab: (co)variance functions of the
    # kx, ky: 2D waveform grid (cross and along)
    # al: cut-off inflation parameter
    # be: cut-off inflation parameter
    # we: weight of RAR
    # ord: order of expansion
    '''

    # dx and dy
    dkx = kx[0, 1] - kx[0, 0]
    dx = 2 * np.pi / dkx / len(kx[0, :])
    # scene size divided by the number of samples
    # x = np.arange( 0, len( kx ) * dx, dx )
    # x = x.reshape( 1, len( kx ) )
    dky = ky[1, 0] - ky[0, 0]
    dy = 2 * np.pi / dky / len(ky[:, 0])
    # scene size divided by the number of samples
    # y = np.arange( 0, len( ky ) * dy, dy )
    # y = y.reshape( len( ky ), 1 )

    # it is necessary to do a non-linear mapping, so for each ky
    # (if you include range bunching each kx also) compute
    # the Fourier transform of G and select the row belonging to ky for the
    # spectrum
    '''
    S = np.zeros( kx.shape, dtype = complex )
    for i in range( 0, len( ky[ :, 0 ] ) ):
        for j in range( 0, len( kx[ 0, : ] ) ):
            # this will be equation 9 in Krogstad et al. (1994) excl. the I0-term or equation 31 in Engen and Johnsen (1995)
            if np.absolute( kx[ i, j ] ) < max_k and np.absolute( ky[ i, j ] ) < max_k:
                G = np.exp( ky[ i, j ] ** 2 * rho_yy ) * \
                    (1 + we * rho_II)  # +
                # 1j * ky[i, j] * (rho_Iy - rho_yI) +
                # ky[i, j] ** 2 * (rho_Iy[i, j] - rho_Iy) * (rho_yI[i, j] - rho_yI))
                # FIXME: if you take the full spectral description also take into account weight

                # take the 'dft of G' (for one frequency)
                DFT = np.exp( ky[ i, j ] ** 2 * -(rho_yy[ 0, 0 ] * al + be) ) * np.outer(
                    np.exp( -1j * ky[ i, j ] * y ),
                    np.exp( -1j * kx[ i, j ] * x ) )
                S[ i, j ] = np.sum( G * DFT ) * dx * dy
    '''

    # faster version (using an expansion)
    S2 = np.zeros(kx.shape, dtype=complex)
    for i in range(0, ord):
        S2 = S2 + 1 / math.factorial(i) * ky ** (2 * i) * np.fft.fft2(rho_yy ** i * (1 + rho_II))
    S2 = np.exp(-ky ** 2 * (rho_yy[0, 0] * al + be)) * S2 * dx * dy

    # normalization
    S2 = S2 / (2 * np.pi) ** 2

    return S2

#
#
# ########################### \Deprecated ##########################

# Goldfinger 1982
# assumption is that neighbouring intensities are uncorrelated,
# which is not true
def remove_bias_Goldfinger(Sc, kx, ky, n):
    """
    # S: SAR spectrum
    # kx,ky: across-track and along-track wave numbers
    # n: number of independent looks
    """

    # some values
    dkx = kx[0, 1] - kx[0, 0]
    dky = ky[1, 0] - ky[0, 0]
    A = 2 * np.pi / dkx * 2 * np.pi / dky  # surface area
    shp = Sc.shape

    # DC is removed, but would be by definition 1 * surface area
    Idc = 1
    DC = Idc * A

    # first mean, then the biased spectrum
    Sc_bar = (np.sum(Sc) + DC) / shp[0] / shp[1]
    S = Sc - Sc_bar / (n + 1)

    return S

# ########################### Deprecated ##########################
#
#
# I will keep this here for Fred for now, but it will be moved
# Goldfinger 1982
# assumption is that neighbouring intensities are uncorrelated,
# which is not true
def add_noise_Goldfinger(S, kx, ky, n):
    """
    # S: SAR spectrum
    # kx,ky: across-track and along-track wave numbers
    # n: number of independent looks
    """

    # some values
    dkx = kx[0, 1] - kx[0, 0]
    dky = ky[1, 0] - ky[0, 0]
    A = 2 * np.pi / dkx * 2 * np.pi / dky  # surface area
    shp = S.shape

    # DC is removed, but would be by definition 1 * surface area
    Idc = 1
    DC = Idc * A

    # first mean, then the biased spectrum
    S_bar = (np.sum(S) + DC) / shp[0] / shp[1]
    Sc = S + S_bar / n

    # the uncertainty on the co-spectra (for I and Q of the cross-spectra
    # use sqrt(2)*sigma_Sc)
    sigma_Sc = Sc / np.sqrt(n)

    return Sc, sigma_Sc



if __name__ == '__main__':
    import numpy as np

    # wave numbers in a Cartesian grids (kx=cross,ky=along)
    g = 9.81
    Nk = 128
    lambda_max = 5000  # maximum wavelength (size of image)
    kx = np.ones((1, Nk))
    dk = 2 * np.pi / lambda_max  # fundamental frequency
    fs = lambda_max / Nk  # sampling rate
    kx[0, 0:int(Nk / 2)] = dk * np.arange(0, Nk / 2)
    kx[0, int(Nk / 2):] = dk * np.arange(-Nk / 2, 0)
    kx = np.dot(np.ones((Nk, 1)), kx)
    ky = np.transpose(kx)
    lambda_y = 2 * np.pi / ky
    lambda_x = 2 * np.pi / kx
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)  # angular velocity
    phi = np.arctan2(ky, kx)  # 0 is cross-track direction waves, 90along-track

    phi_s = np.deg2rad(45)  # swell direction
    f_p = 0.068  # peak frequency
    sigma_f = 0.007  # spread in frequency
    sigma_phi = np.deg2rad(8)  # spreadk in direction
    Hs = 1  # significant wave height
    k_p = (f_p * 2 * np.pi) ** 2 / g
    lambda_p = (2 * np.pi) / k_p
