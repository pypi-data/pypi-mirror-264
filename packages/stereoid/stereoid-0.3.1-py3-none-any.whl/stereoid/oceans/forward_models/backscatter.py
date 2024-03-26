__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
from typing import Optional
from stereoid.oceans.waves.wave_spectra import tuning_param_wb
from stereoid.oceans.waves.wave_spectra import Kudry_spec
from stereoid.oceans.waves.wave_spectra import Kudry_spec_polar
from stereoid.oceans.waves.wave_spectra import spec_peak
from stereoid.oceans.forward_models.RIM_constants import constants as co


def backscatter_Kudry2023_polar(S, k, phi, phi_w=0, theta=np.deg2rad(35), u_10=10, k_r=0):
    """

    Parameters
    ----------
    S: wave spectrum
    k: wave number
    phi: direction with respect to cross-track
    phi_w: wind direction
    theta: incident angle
    u_10: wind speed
    k_r: wave number corrected for the bistatic geometry

    Returns
    -------

    """

    # gradients and grids
    dk = np.gradient(k)
    dphi = (phi[1] - phi[0]) * np.ones(len(phi))
    k, phi = np.meshgrid(k, phi)
    dk, dphi = np.meshgrid(dk, dphi)

    # wind stress
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)

    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number

    # angular frequency and some conversions
    k_inv = 1 / k
    k_inv[0, 0] = 0
    C = np.sqrt(co.g / k + co.gamma * k / co.rho_w)
    C[0, 0] = 0  # phase velocity

    k_d = co.d * k_r
    k_wb = 2 * np.pi / 0.3  # Kudry et al. 2005, above eq. 19
    k_wb_r = np.min((co.b_r * k_r, k_wb))

    # spectral conversions
    # we have to be careful, single sided B might be required
    B = k ** 4 * S  # saturation spectrum
    B[0, 0] = 0

    ### specular scattering
    # FIXME: not considered for now, do not use this script at low incident angles
    sigma_sp = 0

    #### Bragg scattering
    # set of slopes, incidence angles and a new set of wave numbers for Bragg scattering
    # the probability density function for n
    I = k < k_d
    s_br = np.sqrt(np.sum(np.cos(phi[I]) ** 2 * k[I] ** 3 * S[I] * dk[I] * dphi[I]))
    # print(s_br)
    nk = 400  # hardcoded
    n = np.linspace(-5 * s_br, 5 * s_br, nk, endpoint=True)
    dn = n[1] - n[0]
    P = 1 / (np.sqrt(2 * np.pi) * s_br) * np.exp(-0.5 * n ** 2 / s_br ** 2)

    # incidence angles and a new set of wave numbers for Bragg scattering
    dtheta = 1E-10
    theta_prime = theta - np.arctan(n)
    theta_prime2 = theta - np.arctan(n) + dtheta
    I2 = np.absolute(theta_prime2) < np.pi / 2
    P2 = P[I2]
    I = np.absolute(theta_prime) < np.pi / 2
    P = P[I]  # angles larger than 90 degree cannot exist
    theta_prime = theta_prime[I]
    theta_prime2 = theta_prime2[I2]
    k_b = 2 * k_r * np.sin(theta_prime)  # check this np.absolute()
    k_b2 = 2 * k_r * np.sin(theta_prime2)  # check this np.absolute()
    # print(k_b)

    # reflection coefficients (for each local incidence angle)
    G_VV = scattering_coeff(theta_prime, pol='V')
    G_HH = scattering_coeff(theta_prime, pol='H')

    # recompute the spectrum for the wave numbers k_b # this has to be fixed, it works with a double sided spectrum
    # FIXME: we assume the radar direction is 0, so we can simply interpolate at index 0
    I = np.argmin(np.absolute(phi[:, 0]))
    Ipi = 0
    Sr_temp = 0.5 * S[I, :] + 0.5 * S[Ipi, :]
    Sr_bragg = np.interp(k_b, k[I, :], Sr_temp)
    # Sr_bragg = 10 ** np.interp(np.log10(k_b), np.log10(k[I, :]), np.log10(Sr_temp))
    # k_b_temp=2 * k_r * np.sin(theta)

    # compute bragg scattering for each wave number k_b, eq. 3, Kudry et al. (2005)
    s_bragg_VV = 16 * np.pi * k_r ** 4 * np.absolute(G_VV) ** 2 * Sr_bragg
    s_bragg_HH = 16 * np.pi * k_r ** 4 * np.absolute(G_HH) ** 2 * Sr_bragg

    # Bragg scattering (integrate over certain limits to exclude specular reflections)
    I_lim = 2 * k_r * np.sin(np.absolute(theta_prime)) >= k_d  # eq. 4, Kudry et al. (2005)
    sigma_br_VV = np.sum(s_bragg_VV[I_lim] * P[I_lim] * dn)  # eq. 3, Kudry et al. (2005)
    sigma_br_HH = np.sum(s_bragg_HH[I_lim] * P[I_lim] * dn)  # eq. 3, Kudry et al. (2005)

    # derivative of Bragg scattering
    # FIXME: not fully consistent with the original DopRIM (in Doppler.py), where we use ds_0brdt for the derivative
    Sr2_bragg = np.interp(k_b2, k[I, :], Sr_temp)
    G2_VV = scattering_coeff(theta_prime2, pol='V')
    G2_HH = scattering_coeff(theta_prime2, pol='H')
    s2_bragg_VV = 16 * np.pi * k_r ** 4 * np.absolute(G2_VV) ** 2 * Sr2_bragg
    s2_bragg_HH = 16 * np.pi * k_r ** 4 * np.absolute(G2_HH) ** 2 * Sr2_bragg
    # I_lim = 2 * k_r * np.sin(np.absolute(theta_prime2)) >= k_d  # eq. 4, Kudry et al. (2005)
    dsigmadt_br_VV = 1 / sigma_br_VV * (np.sum(s2_bragg_VV[I_lim] * P2[I_lim] * dn) - sigma_br_VV) / dtheta
    dsigmadt_br_HH = 1 / sigma_br_HH * (np.sum(s2_bragg_HH[I_lim] * P2[I_lim] * dn) - sigma_br_HH) / dtheta
    # print(dsigmadt_br_VV,dsigmadt_br_HH)

    #### wave breaking
    # NRCS and tilting function
    dtheta = 1E-5  # equation 60, Kudry et al. (2003)
    # Note, below eq. 60 they make claims that the below is -3.4 an -8.8 at theta=40,45 deg, this is not exactly correct
    s_0wb = (1 / np.cos(theta)) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan(theta) ** 2 / co.s_wb ** 2) + co.eps_wb / co.s_wb ** 2
    s_0wb2 = (1 / np.cos(theta)) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan(theta + dtheta) ** 2 / co.s_wb ** 2) + co.eps_wb / co.s_wb ** 2
    ds_0wb = s_0wb2 - s_0wb
    M_wb = 1 / s_0wb * ds_0wb / dtheta

    # distribution of wave breakers
    # k_p = spec_peak( u_10, F )  # spectral peak
    alpha, n, C_b = tuning_param_wb(u_star, C, k)  # Yurovskaya et al. (2013)
    Lambda = k_inv / 2 * (B / alpha) ** (n + 1)

    # fraction of wave breakers
    # FIXME: check this, maybe the lowest k should be related to k_p (Lambda is only valid in the equilibrium range)
    I_lims = np.logical_and(k > 0, k < k_wb_r)
    Lambda_int = np.sum(Lambda[I_lims] * dphi[I_lims] * dk[I_lims])
    A_wb = np.sum(Lambda[I_lims] * dphi[I_lims] * dk[I_lims] * np.cos(-phi[I_lims])) / Lambda_int
    q = co.c_q * Lambda_int  # eq. 27 in Kudry et al. (2005) and eq. 56 in Kudry et al. (2003)

    # wave breaking backscatter
    sigma_wb = s_0wb * (1 + M_wb * co.theta_wb * A_wb)
    # FIXME: not fully consistent with the original DopRIM (in Doppler.py), where we use ds_0wbdt for the derivative
    dsigmadt_wb = 1 / sigma_wb * (s_0wb2 * (1 + M_wb * co.theta_wb * A_wb) - sigma_wb) / dtheta

    # save all NRCS
    # in radar los direction; downwind, upwind, crosswind; derivatives
    sigma_los = np.array([sigma_sp, sigma_br_VV, sigma_br_HH, sigma_wb])
    # sigma_duc=np.array([sigma_wb_do, sigma_wb_up, sigma_wb_cr1, sigma_wb_cr2])
    dsigmadth = np.array([0, dsigmadt_br_VV, dsigmadt_br_HH, dsigmadt_wb])

    return sigma_los, dsigmadth, q


def backscatter_Kudry2023(S, kx, ky, dks, phi_w=0, theta=35, u_10=10, k_r=0, degrees: Optional[bool] = True):
    """

    Parameters
    ----------
    S: wave spectrum
    kx: cross-track wave number
    ky: along-track wave number
    dks: two-dimensional spectral resolution
    phi_w: wind direction
    theta: incident angle
    u_10: wind speed
    k_r: wave number corrected for the bistatic geometry
    degrees: boolean

    Returns
    -------

    """

    # to radians
    if degrees:
        theta = np.deg2rad(theta)
        phi_w = np.deg2rad(phi_w)
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)

    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number

    # angular frequency and some conversions
    k = np.sqrt(kx ** 2 + ky ** 2)
    k_inv = 1 / k
    k_inv[0, 0] = 0
    C = np.sqrt(co.g / k + co.gamma * k / co.rho_w)
    C[0, 0] = 0  # phase velocity
    phi_k = np.arctan2(ky, kx)  # wave directions

    k_d = co.d * k_r
    k_wb = 2 * np.pi / 0.3  # Kudry et al. 2005, above eq. 19
    k_wb_r = np.min((co.b_r * k_r, k_wb))

    # spectral conversions
    # we have to be careful, single sided B might be required
    B = k ** 4 * S  # saturation spectrum
    B[0, 0] = 0

    ### specular scattering
    # FIXME: not considered for now, do not use this script at low incident angles
    sigma_sp = 0

    #### Bragg scattering
    # set of slopes, incidence angles and a new set of wave numbers for Bragg scattering
    # the probability density function for n
    s_br = np.sqrt(np.sum(np.cos(phi_k[k < k_d]) ** 2 * k[k < k_d] ** 2 * S[k < k_d] * dks[k < k_d]))
    # print(s_br)
    nk = 400  # hardcoded
    n = np.linspace(-5 * s_br, 5 * s_br, nk, endpoint=True)
    dn = n[1] - n[0]
    P = 1 / (np.sqrt(2 * np.pi) * s_br) * np.exp(-0.5 * n ** 2 / s_br ** 2)

    # incidence angles and a new set of wave numbers for Bragg scattering
    dtheta = 1E-10
    theta_prime = theta - np.arctan(n)
    theta_prime2 = theta - np.arctan(n) + dtheta
    I2 = np.absolute(theta_prime2) < np.pi / 2
    P2 = P[I2]
    I = np.absolute(theta_prime) < np.pi / 2
    P = P[I]  # angles larger than 90 degree cannot exist
    theta_prime = theta_prime[I]
    theta_prime2 = theta_prime2[I2]
    k_b = 2 * k_r * np.sin(theta_prime)  # check this np.absolute()
    k_b2 = 2 * k_r * np.sin(theta_prime2)  # check this np.absolute()

    # reflection coefficients (for each local incidence angle)
    G_VV = scattering_coeff(theta_prime, pol='V')
    G_HH = scattering_coeff(theta_prime, pol='H')

    # recompute the spectrum for the wave numbers k_b # this has to be fixed, it works with a double sided spectrum
    # FIXME: we assume the radar direction is 0, so we can simply interpolate at ky=0
    Sr_temp = 0.5 * S[int((len(ky) - 1) / 2), :] + 0.5 * np.flip(S[int((len(ky) - 1) / 2), :])
    kx_temp = kx[int((len(ky) - 1) / 2), :]
    Sr_bragg = np.interp(k_b, kx_temp[kx_temp > 0], Sr_temp[kx_temp > 0])
    # k_b_temp = 2 * k_r * np.sin(theta)

    # compute bragg scattering for each wave number k_b, eq. 3, Kudry et al. (2005)
    s_bragg_VV = 16 * np.pi * k_r ** 4 * np.absolute(G_VV) ** 2 * Sr_bragg
    s_bragg_HH = 16 * np.pi * k_r ** 4 * np.absolute(G_HH) ** 2 * Sr_bragg

    # Bragg scattering (integrate over certain limits to exclude specular reflections)
    I_lim = 2 * k_r * np.sin(np.absolute(theta_prime)) >= k_d  # eq. 4, Kudry et al. (2005)
    sigma_br_VV = np.sum(s_bragg_VV[I_lim] * P[I_lim] * dn)  # eq. 3, Kudry et al. (2005)
    sigma_br_HH = np.sum(s_bragg_HH[I_lim] * P[I_lim] * dn)  # eq. 3, Kudry et al. (2005)

    # derivative of Bragg scattering
    # FIXME: not fully consistent with the original DopRIM (in Doppler.py), where we use ds_0brdt for the derivative
    Sr2_bragg = np.interp(k_b2, kx_temp[kx_temp > 0], Sr_temp[kx_temp > 0])
    G2_VV = scattering_coeff(theta_prime2, pol='V')
    G2_HH = scattering_coeff(theta_prime2, pol='H')
    s2_bragg_VV = 16 * np.pi * k_r ** 4 * np.absolute(G2_VV) ** 2 * Sr2_bragg
    s2_bragg_HH = 16 * np.pi * k_r ** 4 * np.absolute(G2_HH) ** 2 * Sr2_bragg
    # I_lim = 2 * k_r * np.sin(np.absolute(theta_prime2)) >= k_d  # eq. 4, Kudry et al. (2005)
    dsigmadt_br_VV = 1 / sigma_br_VV * (np.sum(s2_bragg_VV[I_lim] * P2[I_lim] * dn) - sigma_br_VV) / dtheta
    dsigmadt_br_HH = 1 / sigma_br_HH * (np.sum(s2_bragg_HH[I_lim] * P2[I_lim] * dn) - sigma_br_HH) / dtheta
    # print(dsigmadt_br_VV,dsigmadt_br_HH)

    #### wave breaking
    # NRCS and tilting function
    dtheta = 1E-5  # equation 60, Kudry et al. (2003)
    # Note, below eq. 60 they make claims that the below is -3.4 an -8.8 at theta=40,45 deg, this is not exactly correct
    s_0wb = (1 / np.cos(theta)) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan(theta) ** 2 / co.s_wb ** 2) + co.eps_wb / co.s_wb ** 2
    s_0wb2 = (1 / np.cos(theta)) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan(theta + dtheta) ** 2 / co.s_wb ** 2) + co.eps_wb / co.s_wb ** 2
    ds_0wb = s_0wb2 - s_0wb
    M_wb = 1 / s_0wb * ds_0wb / dtheta

    # distribution of wave breakers
    # k_p = spec_peak( u_10, F )  # spectral peak
    alpha, n, C_b = tuning_param_wb(u_star, C, k)  # Yurovskaya et al. (2013)
    Lambda = k_inv / 2 * (B / alpha) ** (n + 1)

    # fraction of wave breakers
    # FIXME: check this, maybe the lowest k should be related to k_p (Lambda is only valid in the equilibrium range)
    I_lims = np.logical_and(k > 0, k < k_wb_r)
    Lambda_int = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims])
    A_wb = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims] * np.cos(-phi_k[I_lims])) / Lambda_int
    q = co.c_q * Lambda_int  # eq. 27 in Kudry et al. (2005) and eq. 56 in Kudry et al. (2003)

    # wave breaking backscatter
    sigma_wb = s_0wb * (1 + M_wb * co.theta_wb * A_wb)
    # FIXME: not fully consistent with the original DopRIM (in Doppler.py), where we use ds_0wbdt for the derivative
    dsigmadt_wb = 1 / sigma_wb * (s_0wb2 * (1 + M_wb * co.theta_wb * A_wb) - sigma_wb) / dtheta

    # downwind, upwind and crosswind wave breaking backscatter
    # FIXME: didn't really carefully check up- and downwind, but shouldn't matter
    # A_wb_up = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims] * np.cos(phi_w - phi_k[I_lims])) / Lambda_int
    # A_wb_do = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims] * np.cos(phi_w + np.pi - phi_k[I_lims])) / Lambda_int
    # A_wb_cr1 = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims] * np.cos(phi_w + np.pi/2 - phi_k[I_lims])) / Lambda_int
    # A_wb_cr2 = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims] * np.cos(phi_w - np.pi/2 - phi_k[I_lims])) / Lambda_int
    # sigma_wb_do = s_0wb * (1 + M_wb * co.theta_wb * A_wb_up)
    # sigma_wb_up = s_0wb * (1 + M_wb * co.theta_wb * A_wb_do)
    # sigma_wb_cr1 = s_0wb * (1 + M_wb * co.theta_wb * A_wb_cr1)
    # sigma_wb_cr2 = s_0wb * (1 + M_wb * co.theta_wb * A_wb_cr2)

    # save all NRCS
    # in radar los direction; downwind, upwind, crosswind; derivatives
    sigma_los = np.array([sigma_sp, sigma_br_VV, sigma_br_HH, sigma_wb])
    # sigma_duc=np.array([sigma_wb_do, sigma_wb_up, sigma_wb_cr1, sigma_wb_cr2])
    dsigmadth = np.array([0, dsigmadt_br_VV, dsigmadt_br_HH, dsigmadt_wb])

    return sigma_los, dsigmadth, q


# Kudryavtsev et al. (2005) backscatter
# for a bistatic system, a polarization rotation is required for each scattering mechanism 'backscatter_Kudry2005'
# for bi-static variants, rotate the input spectrum and wind speed by -alpha/2 or alpha/2
def backscatter_Kudry2005(S, kx, ky, dks,
                          phi_w: Optional[float] = 0,
                          theta: Optional[float] = 35,
                          alpha: Optional[float] = 0,
                          pol: Optional[str] = 'V',
                          u_10: Optional[float] = 10,
                          k_r: Optional[float] = 0,
                          degrees: Optional[bool] = True):
    # S: long-wave two-dimensional spectrum
    # kx,ky: wave numbers
    # dks: two-dimensional wave number resolution of the spectrum
    # theta: incidence angle [deg]
    # pol: transmit polarization
    # u_10: wind speed
    # phi_w: wave direction with respect to the radar [deg]
    # k_r: radar wave length [m]
    # alpha: bistatic angle [deg]

    # to radians
    if degrees:
        theta = np.deg2rad(theta)
        phi_w = np.deg2rad(phi_w)
        alpha = np.deg2rad(alpha)
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)

    # angular frequency and some conversions
    k = np.sqrt(kx ** 2 + ky ** 2)
    k_inv = 1 / k
    k_inv[0, 0] = 0
    C = np.sqrt(co.g / k + co.gamma * k / co.rho_w)
    C[0, 0] = 0  # phase velocity
    phi_k = np.arctan2(ky, kx)  # wave directions

    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number
        # PLD: I moved the next inside the if clause, because we will pass
        # the correcty bistatically scalled k_r to the function instead
        # of computing it (wrongly)
        if alpha != 0:
            k_r = k_r * np.cos(alpha / 2)

    k_d = co.d * k_r
    k_wb = 2 * np.pi / 0.3  # Kudry et al. 2005, above eq. 19
    k_wb_r = np.min((co.b_r * k_r, k_wb))

    # spectral conversions
    # we have to be careful, single sided B might be required
    B = k ** 4 * S  # saturation spectrum
    B[0, 0] = 0

    #### specular reflection
    # large-scale wave mss  # limits for integration not needed if we input S(k < k_d)
    s_i = np.sqrt(
        np.sum(k[k < k_d] ** 2 * np.cos(phi_k[k < k_d]) ** 2 * S[k < k_d] * dks[k < k_d]))
    s_cr = np.sqrt(
        np.sum(k[k < k_d] ** 2 * np.sin(phi_k[k < k_d] - phi_w) ** 2 * S[k < k_d] * dks[k < k_d]))
    s_up = np.sqrt(
        np.sum(k[k < k_d] ** 2 * np.cos(phi_k[k < k_d] - phi_w) ** 2 * S[k < k_d] * dks[k < k_d]))

    # Fresnel coefficients at zero incidence angle (the exponential factor below eq. 5, Kudry2005)
    # FIXME: check if this is not double accounting
    h_s = np.sqrt(np.sum(S[k > k_d] * dks[k > k_d]))
    R = Fresnel_coeff_normal(pol=pol, eps_w=co.eps_w) * np.exp(-4 * k_r ** 2 * h_s ** 2)

    # specular reflection (factor 2 missing in Kudry et al. (2005), compare with Yan Yuan and Kudry et al. (2003)
    s_spec = np.absolute(R) ** 2 / (2 * np.cos(theta) ** 4 * s_up * s_cr) * np.exp(
        -np.tan(theta) ** 2 / (2 * s_i ** 2))

    #### Bragg scattering
    # set of slopes, incidence angles and a new set of wave numbers for Bragg scattering
    # the probability density function for n
    s_br = np.sqrt(np.sum(np.cos(phi_k[k < k_d]) ** 2 * k[k < k_d] ** 2 * S[k < k_d] * dks[k < k_d]))
    nk = 200  # hardcoded
    n = np.linspace(-5 * s_br, 5 * s_br, nk, endpoint=True)
    dn = n[1] - n[0]
    P = 1 / (np.sqrt(2 * np.pi) * s_br) * np.exp(-0.5 * n ** 2 / s_br ** 2)

    # incidence angles and a new set of wave numbers for Bragg scattering
    theta_prime = theta - np.arctan(n)
    P = P[np.absolute(theta_prime) < np.pi / 2]  # angles larger than 90 degree cannot exist
    theta_prime = theta_prime[np.absolute(theta_prime) < np.pi / 2]
    k_b = 2 * k_r * np.sin(theta_prime)  # check this np.absolute()

    # reflection coefficients (for each local incidence angle)
    G = scattering_coeff(theta_prime, pol=pol)

    # recompute the spectrum for the wave numbers k_b # this has to be fixed, it works with a double sided spectrum
    # FIXME: we assume the radar direction is 0, so we can simply interpolate at ky=0
    Sr_temp = 0.5 * S[int((len(ky) - 1) / 2), :] + 0.5 * np.flip(S[int((len(ky) - 1) / 2), :])
    kx_temp = kx[int((len(ky) - 1) / 2), :]
    Sr_bragg = np.interp(k_b, kx_temp[kx_temp > 0], Sr_temp[kx_temp > 0])

    # compute bragg scattering for each wave number k_b, eq. 3, Kudry et al. (2005)
    s_bragg = 16 * np.pi * k_r ** 4 * np.absolute(G) ** 2 * Sr_bragg

    # Bragg scattering (integrate over certain limits to exclude specular reflections)
    I_lim = 2 * k_r * np.sin(np.absolute(theta_prime)) >= k_d  # eq. 4, Kudry et al. (2005)
    s_bragg = np.sum(s_bragg[I_lim] * P[I_lim] * dn)  # eq. 3, Kudry et al. (2005)

    #### wave breaking
    # NRCS and tilting function
    dtheta = 1E-5  # equation 60, Kudry et al. (2003)
    # Note, below eq. 60 they make claims that the below is -3.4 an -8.8 at theta=40,45 deg, this is not exactly correct
    s_0wb = (1 / np.cos(theta)) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan(theta) ** 2 / co.s_wb ** 2) + co.eps_wb / co.s_wb ** 2
    ds_0wb = (1 / np.cos(theta)) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan(theta + dtheta) ** 2 / co.s_wb ** 2) + co.eps_wb / co.s_wb ** 2 - s_0wb
    M_wb = 1 / s_0wb * ds_0wb / dtheta

    # distribution of wave breakers
    # k_p = spec_peak( u_10, F )  # spectral peak
    alpha, n, C_b = tuning_param_wb(u_star, C, k)  # Yurovskaya et al. (2013)
    Lambda = k_inv / 2 * (B / alpha) ** (n + 1)

    # fraction of wave breakers
    # FIXME: check this, maybe the lowest k should be related to k_p (Lambda is only valid in the equilibrium range)
    I_lims = np.logical_and(k > 0, k < k_wb_r)
    Lambda_int = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims])
    A_wb = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims] * np.cos(-phi_k[I_lims])) / Lambda_int
    q = co.c_q * Lambda_int  # eq. 27 in Kudry et al. (2005) and eq. 56 in Kudry et al. (2003)

    # wave breaking backscatter
    s_break = s_0wb * (1 + M_wb * co.theta_wb * A_wb)

    return s_spec, s_bragg, s_break, q  # output: NRCS of specular reflection, Bragg scattering and wave breaking + fraction


# this is based on Kudryavtsev et al. (2019)
def backscatter_crosspol_polar(S, k, phi, theta=35, u_10=20, k_r=0, fetch=500E3):
    # S: long-wave two-dimensional spectrum
    # kx,ky: wave numbers
    # dks: two-dimensional wave number resolution of the spectrum
    # theta: incidence angle [deg]
    # pol: transmit polarization
    # u_10: wind speed
    # k_r: radar wave length [m]
    # alpha: bistatic angle [deg]
    # fetch: fetch [m]

    # gradients and grids
    #dk = np.gradient(k)
    #dphi = (phi[1] - phi[0]) * np.ones(len(phi))
    k, phi = np.meshgrid(k, phi)
    #dk, dphi = np.meshgrid(dk, dphi)

    # angular frequency and some conversions
    k_inv = 1 / k
    k_inv[0, 0] = 0
    C = np.sqrt(co.g / k + co.gamma * k / co.rho_w)
    C[0, 0] = 0  # phase velocity

    #### Bragg scattering
    # we have to check the 'absolute of Gpp-Gqq', in our function we already take G already absolute
    k_b = 2 * k_r * np.sin(theta)
    k_d = co.d * k_b  # this is for the Kudryavtsev 2019 equation for s_n
    # FIXME: I use the scattering coefficients from Kudry et al. (2019) here, this gives different results as 2003 or Plant
    Gvv = scattering_coeff_Kudry2019(theta, 'V')
    Ghh = scattering_coeff_Kudry2019(theta, 'H')
    k_p = spec_peak(u_10, fetch)
    Omega = u_10 * np.sqrt(k_p / co.g)
    s_n = np.sqrt(0.5 * co.c_sn * np.log(Omega ** -2 * k_d * u_10 ** 2 / co.g))  # take half of A4
    # FIXME: check this, in Kudry et al. (2005) double sided in (2019) not?
    I = np.argmin(np.absolute(phi[:, 0]))
    Ipi = 0
    Sr_temp = 0.5 * S[I, :] + 0.5 * S[Ipi, :]
    Sr_bragg = np.interp(k_b, k[I, :], Sr_temp)
    B_r = Sr_bragg * k_r ** 4
    # eq. A1c, Kudry et al. (2019)
    s_bragg = np.pi * np.tan(theta) ** -4 * np.absolute(Gvv - Ghh) ** 2 * s_n ** 2 / np.sin(theta) ** 2 * B_r
    #### wave breaking
    # eq. 11, Kudry et al. (2019)
    s_break = np.pi * np.absolute(Gvv - Ghh) ** 2 / np.tan(theta) ** 4 * co.s_wb ** 2 / (
            2 * np.sin(theta) ** 2) * co.B_wb

    return s_bragg, s_break



# this is based on Kudryavtsev et al. (2019)
def backscatter_crosspol(S, kx, ky, dks, theta=35, alpha=0, u_10=20, k_r=0, fetch=500E3, degrees=True):
    # S: long-wave two-dimensional spectrum
    # kx,ky: wave numbers
    # dks: two-dimensional wave number resolution of the spectrum
    # theta: incidence angle [deg]
    # pol: transmit polarization
    # u_10: wind speed
    # k_r: radar wave length [m]
    # alpha: bistatic angle [deg]
    # fetch: fetch [m]

    # to radians
    if degrees:
        theta = np.deg2rad(theta)
        alpha = np.deg2rad(alpha)

    # angular frequency and some conversions
    k = np.sqrt(kx ** 2 + ky ** 2)
    k_inv = 1 / k
    k_inv[0, 0] = 0
    C = np.sqrt(co.g / k + co.gamma * k / co.rho_w)
    C[0, 0] = 0  # phase velocity
    phi_k = np.arctan2(ky, kx)  # wave directions

    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length
        k_r = 2 * np.pi / la_r  # radar wave number
        # PLD see comment in previous function. We will pass bistatic-corrected k_r
        if alpha != 0:
            k_r = k_r * np.cos(alpha / 2)

    #### Bragg scattering
    # we have to check the 'absolute of Gpp-Gqq', in our function we already take G already absolute
    k_b = 2 * k_r * np.sin(theta)
    k_d = co.d * k_b  # this is for the Kudryavtsev 2019 equation for s_n
    # FIXME: I use the scattering coefficients from Kudry et al. (2019) here, this gives different results as 2003 or Plant
    Gvv = scattering_coeff_Kudry2019(theta, 'V')
    Ghh = scattering_coeff_Kudry2019(theta, 'H')
    k_p = spec_peak(u_10, fetch)
    Omega = u_10 * np.sqrt(k_p / co.g)
    s_n = np.sqrt(0.5 * co.c_sn * np.log(Omega ** -2 * k_d * u_10 ** 2 / co.g))  # take half of A4
    # print(s_n)
    # print('check')
    # k_d = co.d * k_r # this is for the Kudryavtser 2005 equation for s_n
    # s_n = np.sqrt( np.sum( np.cos( phi_k[ k < k_d ] ) ** 2 * k[ k < k_d ] ** 2 * S[ k < k_d ] * dks[ k < k_d ] ) )
    # print( s_n )
    # FIXME: check this, in Kudry et al. (2005) double sided in (2019) not?
    Sr_temp = 0.5 * S[int((len(ky) - 1) / 2), :] + 0.5 * np.flip(S[int((len(ky) - 1) / 2), :])
    S_r = np.interp(k_b, kx[int((len(ky) - 1) / 2), :], Sr_temp)
    B_r = S_r * k_r ** 4
    # eq. A1c, Kudry et al. (2019)
    s_bragg = np.pi * np.tan(theta) ** -4 * np.absolute(Gvv - Ghh) ** 2 * s_n ** 2 / np.sin(theta) ** 2 * B_r
    #### wave breaking
    # eq. 11, Kudry et al. (2019)
    s_break = np.pi * np.absolute(Gvv - Ghh) ** 2 / np.tan(theta) ** 4 * co.s_wb ** 2 / (
            2 * np.sin(theta) ** 2) * co.B_wb

    return s_bragg, s_break


# this is the one of plant (basically Kudry et al. (2019), but multiplied by cos(theta)**2
def scattering_coeff(theta, pol='V', eps_w=73 + 1j * 18):
    # theta: incident angle [rad]
    # pol: polarization (H,V)
    if pol == 'V':  # scattering coefficients from Kudry et al. (2019), eq. A2 (cos(theta)**2 missing I think)
        Gpp = np.absolute(
            (eps_w - 1) * (eps_w * (1 + np.sin(theta) ** 2) - np.sin(theta) ** 2) * np.cos(theta) ** 2 / \
            (eps_w * np.cos(theta) + (eps_w - np.sin(theta) ** 2) ** 0.5) ** 2)
    if pol == 'H':
        Gpp = np.absolute(
            (eps_w - 1) * np.cos(theta) ** 2 / (np.cos(theta) + (eps_w - np.sin(theta) ** 2) ** 0.5) ** 2)
    return (Gpp)


# this is the one of  Kudry et al. (2019), which differs from Plant by cos(theta)**2 and we do not take the absolute value
def scattering_coeff_Kudry2019(theta, pol='V', eps_w=73 + 1j * 18):
    # theta: incident angle [rad]
    # pol: polarization (H,V)
    if pol == 'V':  # scattering coefficients from Kudry et al. (2019), eq. A2 (cos(theta)**2 missing I think)
        Gpp = (eps_w - 1) * (eps_w * (1 + np.sin(theta) ** 2) - np.sin(theta) ** 2) / \
              (eps_w * np.cos(theta) + (eps_w - np.sin(theta) ** 2) ** 0.5) ** 2
    if pol == 'H':
        Gpp = (eps_w - 1) / (np.cos(theta) + (eps_w - np.sin(theta) ** 2) ** 0.5) ** 2
    return (Gpp)


def scattering_coeff_Kudry2003(theta, pol='V'):
    # theta: incident angle [rad]
    # pol: polarization (H,V)
    if pol == 'V':  # scattering coefficients from Kudry et al. (2003), eq. 3/4
        Gp0 = np.sqrt(
            np.absolute(np.cos(theta) ** 4 * (1 + np.sin(theta) ** 2) ** 2 / (np.cos(theta) + 0.111) ** 4))
    if pol == 'H':
        Gp0 = np.sqrt(np.absolute(np.cos(theta) ** 4 / (0.111 * np.cos(theta) + 1) ** 4))
    return (Gp0)


def Fresnel_coeff_normal(pol='V', eps_w=73 + 1j * 18):
    # pol: polarization (H,V)
    # eps_w: dielectric constant of water
    if pol == 'H':
        R = np.absolute((np.cos(0) - np.sqrt(eps_w - np.sin(0) ** 2)) / (
                np.cos(0) + np.sqrt(eps_w - np.sin(0) ** 2)))
    if pol == 'V':
        R = np.absolute((np.cos(0) - np.sqrt(eps_w - np.sin(0) ** 2)) / (
                np.cos(0) + np.sqrt(eps_w - np.sin(0) ** 2)))
    return (R)


if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    from pylab import *

    # import stereoid.oceans.forward_models.backscatter as backscatter

    g = 9.81
    n_k = 100
    lambda_min = 0.005
    lambda_max = 1000
    k_min = 2 * np.pi / lambda_max  # minimum wave number
    k_max = 2 * np.pi / lambda_min  # should at least pass the Bragg wave
    k = 10 ** np.linspace(np.log10(k_min), np.log10(k_max), n_k)
    nphi = 72
    phi = np.linspace(-np.pi, np.pi, nphi)
    omega = np.where(k > 0, np.sqrt(g * k), 0)
    dk = np.gradient(k)
    dphi = 2 * np.pi / nphi * np.ones(len(phi))
    # wave spectrum using Elfouhaily et al. (1997)
    u_10 = 15
    fetch = 500E3
    phi_w = 0
    B, B_neq, B_w, B_pc = Kudry_spec_polar(k, phi, u_10, fetch, phi_w, S=0)
    kv, phiv = np.meshgrid(k, phi)
    # dk, dphi = np.meshgrid(dk, dphi)
    S = np.where(kv > 0, B * kv ** -4, 0)
    cmap = cm.get_cmap('gist_ncar_r', 15)
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    con = ax.pcolormesh(phiv, kv, np.log10(S), cmap=cmap, vmin=-15, vmax=0)
    ax.set_rscale('log')
    fig.colorbar(con, ax=ax)
    plt.show()
    # plt.figure()
    # plt.plot(k,np.sum(B*dphi[0],axis=0))
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.ylim(5E-4,2E-2)
    # plt.xlim(1E-2, 1E4)
    # plt.grid('on')
    # plt.show()

    # RIM
    # '''
    plt.figure(figsize=(15, 5))
    for j in range(0, 3):
        phi_w = j * 90.0

        # wave spectrum using Elfouhaily et al. (1997)
        u_10 = 17
        fetch = 500E3
        B, B_neq, B_w, B_pc = Kudry_spec_polar(k, phi, u_10, fetch, np.deg2rad(phi_w), S=0)
        S = np.where(kv > 0, B * kv ** -4, 0)

        plt.subplot(1, 3, j + 1)
        plt.grid('on')
        theta_i = np.arange(31, 46, 1)
        for i in range(0, len(theta_i)):
            sigma_los, dsigmadth, q = backscatter_Kudry2023_polar(S, k, phi, phi_w=np.deg2rad(phi_w),
                                                                  theta=np.deg2rad(theta_i[i]), u_10=u_10, k_r=0)
            s_spec = sigma_los[0]
            s_bragg_vv = sigma_los[1]
            s_bragg_hh = sigma_los[2]
            s_break = sigma_los[3]
            print(s_bragg_vv, s_break)

            if i == 0:
                plt.plot(theta_i[i], 10 * np.log10(s_spec * (1 - q)), 'b*', label='$\sigma_{sp}$')
                plt.plot(theta_i[i], 10 * np.log10(s_bragg_vv * (1 - q)), 'g*', label='$\sigma_{br,vv}$')
                plt.plot(theta_i[i], 10 * np.log10(s_bragg_hh * (1 - q)), 'y*', label='$\sigma_{br,hh}$')
                # plt.plot( theta_i[ i ], 10 * np.log10( s_bragg * (1 - q) ), 'y*', label='$\sigma_{br,vv}$' )
                plt.plot(theta_i[i], 10 * np.log10(s_break * q), 'r*', label='$\sigma_{wb}$')

            if i != 0:
                plt.plot(theta_i[i], 10 * np.log10(s_spec * (1 - q)), 'b*')
                plt.plot(theta_i[i], 10 * np.log10(s_bragg_vv * (1 - q)), 'g*')
                plt.plot(theta_i[i], 10 * np.log10(s_bragg_hh * (1 - q)), 'y*')
                # plt.plot( theta_i[i], 10 * np.log10( s_bragg * (1 - q)), 'y*')
                plt.plot(theta_i[i], 10 * np.log10(s_break * q), 'r*')

        plt.ylim(-40, 20)
        plt.legend()
    plt.show()
    # '''

    # '''
    # wavelengths and wave numbers
    g = 9.81
    n_k = 100  # number of frequencies single side (total 2*n_k - 1)
    lambda_min = 0.005  # minimum wave length
    lambda_max = 1000  # maximum wave length
    k_min = 2 * np.pi / lambda_max  # minimum wave number
    k_max = 2 * np.pi / lambda_min  # should at least pass the Bragg wave number
    # k_x = k_min * np.arange( 1, n_k + 1 )  # vector of wave numbers (single side)
    k_x = np.reshape(10 ** np.linspace(np.log10(k_min), np.log10(k_max), n_k), (1, n_k))
    # k_x[ 20: ] = k_x[ 20: ] * 1.015 ** np.arange( 1, n_k - 20 )  # extend domain (distance increase higher wave noms)
    k_x = np.append(np.append(-np.flip(k_x), 0), k_x)  # double sided spectrum
    dk = np.gradient(k_x, 1)
    k_x = np.dot(np.ones((n_k * 2 + 1, 1)), k_x.reshape(1, n_k * 2 + 1))  # two dimensional
    k_y = np.transpose(k_x)
    k = np.sqrt(k_x ** 2 + k_y ** 2)
    omega = np.where(k > 0, np.sqrt(g * k), 0)
    phi = np.arctan2(k_y, k_x)  # 0 is cross-track direction waves, 90 along-track
    dks = np.outer(dk, dk)  # patch size

    # wave spectrum using Elfouhaily et al. (1997)
    u_10 = 10
    fetch = 500E3
    phi_w = 0
    B, _, _, _ = Kudry_spec(k_x, k_y, u_10, fetch, phi_w, dks)
    S = np.where(k > 0, B * k ** -4, 0)
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    cmap = cm.get_cmap('gist_ncar_r', 15)
    con = ax.scatter(phi, k, c=np.log10(S), cmap=cmap, vmin=-15, vmax=0)
    ax.set_rscale('log')
    fig.colorbar(con, ax=ax)
    plt.show()

    # RIM
    '''
    plt.figure(figsize=(15,5))
    for j in range( 0, 3 ):
        phi_w=j*90.0

        # wave spectrum using Elfouhaily et al. (1997)
        u_10 = 10
        fetch = 500E3
        B, _, _, _ = Kudry_spec( k_x, k_y, u_10, fetch, np.deg2rad(phi_w), dks )
        S = np.where( k > 0, B * k ** -4, 0 )

        plt.subplot( 1, 3, j + 1 )
        plt.grid('on')
        theta_i = np.arange( 1, 80, 2 )
        for i in range( 0, len( theta_i ) ):
            s_spec, s_bragg, s_break, q = backscatter_Kudry2005( S, k_x, k_y, dks, phi_w, theta = theta_i[ i ], pol = 'V', u_10 = u_10, k_r = 0 )
            sigma_los, dsigmadth, q=backscatter_Kudry2023(S, k_x, k_y, dks,phi_w=phi_w,theta=theta_i[i], u_10=u_10, k_r=0, degrees = True)
            #s_spec=sigma_los[0]
            s_bragg_vv=sigma_los[1]
            s_bragg_hh = sigma_los[2]
            #s_break=sigma_los[3]

            if i == 0:
                plt.plot( theta_i[ i ], 10 * np.log10( s_spec * (1 - q) ), 'b*', label='$\sigma_{sp}$' )
                plt.plot( theta_i[ i ], 10 * np.log10( s_bragg_vv * (1 - q) ), 'g*', label='$\sigma_{br,vv}$' )
                plt.plot( theta_i[i], 10 * np.log10(s_bragg_hh * (1 - q)), 'y*', label='$\sigma_{br,hh}$')
                #plt.plot( theta_i[ i ], 10 * np.log10( s_bragg * (1 - q) ), 'y*', label='$\sigma_{br,vv}$' )
                plt.plot( theta_i[ i ], 10 * np.log10( s_break * q ), 'r*', label='$\sigma_{wb}$' )

            if i != 0:
                plt.plot( theta_i[ i ], 10 * np.log10( s_spec * (1 - q) ), 'b*' )
                plt.plot( theta_i[ i ], 10 * np.log10( s_bragg_vv * (1 - q) ), 'g*' )
                plt.plot( theta_i[i], 10 * np.log10( s_bragg_hh * (1 - q)), 'y*')
                #plt.plot( theta_i[i], 10 * np.log10( s_bragg * (1 - q)), 'y*')
                plt.plot( theta_i[ i ], 10 * np.log10( s_break * q ), 'r*' )



        plt.ylim( -40, 20 )
        plt.legend()
    plt.show()
    '''
    # '''
