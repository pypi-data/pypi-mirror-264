__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
from stereoid.oceans.waves.wave_spectra import tuning_param_wb
from stereoid.oceans.waves.wave_spectra import Kudry_spec
from stereoid.oceans.forward_models.backscatter import Fresnel_coeff_normal
from stereoid.oceans.forward_models.backscatter import scattering_coeff
from stereoid.oceans.forward_models.RIM_constants import constants as co
from stereoid.oceans.forward_models.backscatter import backscatter_Kudry2023
from stereoid.oceans.forward_models.backscatter import backscatter_Kudry2023_polar
from stereoid.oceans.waves.wave_spectra import Kudry_spec_polar


# this is the dual-pol polar version (used in backscatter_doppler_tools for bistatic polarimetry) of the Kudry2023' DopRIM
# it is a simplified version of the DopRIM and excludes specular scattering from regular surfaces
# note, to be consistent with Hansen2012, c_B and c_np in eq. 30 are used here as c_br_bar and c_wb_bar
# the latter makes it a bit confusing, but they are treated consistently later on
def DopRIM2023_DP_polar(S, k, phi, theta, u_10, phi_w, k_r=0, u_10_local=0):
    """

    Parameters
    ----------
    S
    k
    phi
    theta
    u_10
    phi_w
    k_r
    u_10_local

    Returns
    -------

    """

    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number

    # call backscatter
    sigma_los, dsigmadth, q = backscatter_Kudry2023_polar(S, k, phi, phi_w=phi_w, theta=theta, u_10=u_10, k_r=k_r)

    # gradients and grids
    dk = np.gradient(k)
    dphi = (phi[1] - phi[0]) * np.ones(len(phi))
    k, phi = np.meshgrid(k, phi)
    dk, dphi = np.meshgrid(dk, dphi)

    # some preparatory calculations
    k_inv = np.where(k > 0, 1 / k, 0)
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)  # drag velocity
    B = k ** 4 * S

    # wavelength of the shortest breaking waves providing radar returns
    d = 1 / 4
    k_np = k_r / 10
    k_wc = k_r / 10
    k_d = d * k_wc
    k_br = 2 * k_r * np.sin(theta)
    c_np = np.sqrt(co.g / k_np + co.gamma * k_np / co.rho_w)
    c_br = np.sqrt(co.g / k_br + co.gamma * k_br / co.rho_w)
    c = np.where(k > 0, np.sqrt(co.g / k + co.gamma * k / co.rho_w), 0)
    omega = np.where(k > 0, np.sqrt(co.g * k + co.gamma * k ** 3 / co.rho_w), 0)
    omega_np = np.sqrt(co.g * k_np + co.gamma * k_np ** 3 / co.rho_w)

    # wave breaking function
    alpha, n, C_b = tuning_param_wb(u_star, c, k)  # Yurovskaya et al. (2013)
    Lambda = k_inv / 2 * (B / alpha) ** (n + 1)
    # I_lims = np.logical_and( k > 0, k < k_wc )
    # print(Lambda_int)

    # directional distribution of facets
    # delta_np=(sigma_duc[0]+sigma_duc[1]-sigma_duc[2]-sigma_duc[3])/(sigma_duc[0]+sigma_duc[1]+sigma_duc[2]+sigma_duc[3])
    # A_wb = 2 * (1 + delta_np) * np.exp(-np.log(2 * (1 + delta_np) / (1 - delta_np)) * (2 * 0 / np.pi) ** 2)
    # A_wb_pi = 2 * (1 + delta_np) * np.exp(-np.log(2 * (1 + delta_np) / (1 - delta_np)) * (2 * np.pi / np.pi) ** 2)
    # from Kudryavtsev et al. (2003/2005) for wave breaking, split into breakers moving towards and away from you
    I_lims = k < k_wc
    Lambda_int = np.sum(Lambda[I_lims] * dphi[I_lims] * dk[I_lims])
    A_wb = np.sum(Lambda[I_lims] * dphi[I_lims] * dk[I_lims] * np.cos(-phi[I_lims]))
    I = np.argmin(np.absolute(phi[:, 0]))
    Sr_temp = 0.5 * S[I, :]
    # S_br = np.interp(k_br, k[I,:], Sr_temp)
    S_br = 10 ** np.interp(np.log10(k_br), np.log10(k[I, :]), np.log10(Sr_temp))
    Ipi = 0
    Sr_temp = 0.5 * S[Ipi, :]
    # S_br_pi = np.interp(k_br, k[Ipi,:], Sr_temp)
    S_br_pi = 10 ** np.interp(np.log10(k_br), np.log10(k[Ipi, :]), np.log10(Sr_temp))

    # facet velocities
    c_wb = 2 * c_np  # is c_wb_ar in equation 13
    eps_wb = 1 - 0.5 * np.exp(-(np.degrees(theta) - 20) / 20)
    c_wb_bar = eps_wb * c_wb * A_wb/Lambda_int  # this is partially from Hansen et al. (2012) + equation 12
    c_br_bar = c_br * (S_br - S_br_pi) / (S_br + S_br_pi)  # is c_B in equation 9

    # mtf's for tilt and hydro
    Mt_br_vv = dsigmadth[1]  # scalar
    Mt_br_hh = dsigmadth[2]  # scalar
    Mt_wb = dsigmadth[3]  # scalar

    # Mh_br = 0 # can be ingored, below equation 24
    beta_wc = co.c_beta * (
                u_star / c_np) ** 2  # below equation 23, note c_np=c_wc FIXME: not sure if this is exactly correct
    mu_wc = co.n_g * beta_wc * omega_np / omega  # note omega_np=omega_wc#
    # FIXME: check if 'k_np' is supposed to be there. Seems like a normalization for the integral in equation 27
    #Mh_wb = co.n_k / 2 * (co.n_g + 1) * (1 + 0.5 * np.cos(2 * phi)) / k_np * (1 - 1j * mu_wc) / (1 + mu_wc ** 2)
    Mh_wb = 1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * np.cos(phi) ** 2) * (1 - 1j * mu_wc) / (1 + mu_wc ** 2)

    # long-wave Doppler
    I_lim = np.logical_and(k > 0, k < k_br * d)
    c_br_vv = np.sum(
        -Mt_br_vv / np.tan(theta) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 3 * S[I_lim] * dk[I_lim] * dphi[
            I_lim])
    c_br_hh = np.sum(
        -Mt_br_hh / np.tan(theta) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 3 * S[I_lim] * dk[I_lim] * dphi[
            I_lim])

    I_lim = np.logical_and(k > 0, k < k_np / 10)
    c_wb1 = np.sum(-Mt_wb / np.tan(theta) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 3 * S[I_lim] * dk[I_lim] * dphi[I_lim])
    c_wb2 = np.sum(-np.real(Mh_wb[I_lim]) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 3 * S[I_lim] * dk[I_lim] * dphi[I_lim])
    c_wb3 = np.sum(np.imag(Mh_wb[I_lim])/np.tan(theta) * c[I_lim] * k[I_lim] ** 3 * S[I_lim] * dk[I_lim] * dphi[I_lim])
    c_wb = c_wb1 + c_wb2 + c_wb3
    #print(c_wb1,c_wb2, c_wb3)

    # specular set to zero
    c_sp_bar = 0
    c_sp = 0

    return c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh


# this is the dual-pol version (used in backscatter_doppler_tools for bistatic polarimetry) of the Kudry2023' DopRIM
# it is a simplified version of the DopRIM and excludes specular scattering from regular surfaces
# note, to be consistent with Hansen2012, c_B and c_np in eq. 30 are used here as c_br_bar and c_wb_bar
# the latter makes it a bit confusing, but they are treated consistently later on
def DopRIM2023_DP(S, kx, ky, dks, theta, u_10, phi_w, k_r, u_10_local=0):
    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number

    # call backscatter
    sigma_los, dsigmadth, q = backscatter_Kudry2023(S, kx, ky, dks, phi_w=phi_w, theta=theta, u_10=u_10, k_r=k_r,
                                                    degrees=False)

    # some preparatory calculations
    k = np.sqrt(kx ** 2 + ky ** 2)
    phi = np.arctan2(ky, kx)
    k_inv = np.where(k > 0, 1 / k, 0)
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)  # drag velocity
    B = k ** 4 * S

    # wavelength of the shortest breaking waves providing radar returns
    d = 1 / 4
    k_np = k_r / 10
    k_wc = k_r / 10
    k_d = d * k_wc
    k_br = 2 * k_r * np.sin(theta)
    c_np = np.sqrt(co.g / k_np + co.gamma * k_np / co.rho_w)
    c_br = np.sqrt(co.g / k_br + co.gamma * k_br / co.rho_w)
    c = np.where(k > 0, np.sqrt(co.g / k + co.gamma * k / co.rho_w), 0)
    omega = np.where(k > 0, np.sqrt(co.g * k + co.gamma * k ** 3 / co.rho_w), 0)
    omega_np = np.sqrt(co.g * k_np + co.gamma * k_np ** 3 / co.rho_w)

    # wave breaking function
    alpha, n, C_b = tuning_param_wb(u_star, c, k)  # Yurovskaya et al. (2013)
    Lambda = k_inv / 2 * (B / alpha) ** (n + 1)
    # I_lims = np.logical_and( k > 0, k < k_wc )
    # Lambda_int = np.sum( Lambda[ I_lims ] * k_inv[ I_lims ] * dks[ I_lims ] )
    # print(Lambda_int)

    # directional distribution of facets
    # delta_np=(sigma_duc[0]+sigma_duc[1]-sigma_duc[2]-sigma_duc[3])/(sigma_duc[0]+sigma_duc[1]+sigma_duc[2]+sigma_duc[3])
    # A_wb = 2 * (1 + delta_np) * np.exp(-np.log(2 * (1 + delta_np) / (1 - delta_np)) * (2 * 0 / np.pi) ** 2)
    # A_wb_pi = 2 * (1 + delta_np) * np.exp(-np.log(2 * (1 + delta_np) / (1 - delta_np)) * (2 * np.pi / np.pi) ** 2)
    # from Kudryavtsev et al. (2003/2005) for wave breaking, split into breakers moving towards and away from you
    I_lims = np.logical_and(k > 0, k < k_wc)
    Lambda_int = np.sum(Lambda[I_lims] * k_inv[I_lims] * dks[I_lims])
    A_wb = np.sum(Lambda[I_lims] * k_inv[I_lims] * np.cos(-phi[I_lims]) * dks[I_lims])
    Sr_temp = S[int((len(ky) - 1) / 2), :]
    kx_temp = kx[int((len(ky) - 1) / 2), :]  # go to logaritmic domain for better interpolation
    S_br = 10 ** np.interp(np.log10(k_br), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))
    Sr_temp = np.flip(S[int((len(ky) - 1) / 2), :])
    S_br_pi = 10 ** np.interp(np.log10(k_br), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))

    # facet velocities
    c_wb = 2 * c_np  # is c_wb_ar in equation 13
    eps_wb = 1 - 0.5 * np.exp(-(np.degrees(theta) - 20) / 20)
    c_wb_bar = eps_wb * c_wb * A_wb / Lambda_int   # is partially from Hansen et al. 2012
    c_br_bar = c_br * (S_br - S_br_pi) / (S_br + S_br_pi)  # is c_B in equation 9

    # mtf's for tilt and hydro
    Mt_br_vv = dsigmadth[1]  # scalar
    Mt_br_hh = dsigmadth[2]  # scalar
    Mt_wb = dsigmadth[3]  # scalar

    # Mh_br = 0 # can be ingored, below equation 24
    beta_wc = co.c_beta * (
                u_star / c_np) ** 2  # below equation 23, note c_np=c_wc FIXME: not sure if this is exactly correct
    mu_wc = co.n_g * beta_wc * omega_np / omega  # note omega_np=omega_wc#
    # FIXME: check if 'k_np' is supposed to be there. Seems like a normalization for the integral in equation 27
    #Mh_wb = co.n_k / 2 * (co.n_g + 1) * (1 + 0.5 * np.cos(2 * phi)) / k_np * (1 - 1j * mu_wc) / (1 + mu_wc ** 2)
    Mh_wb = 1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * np.cos(phi) ** 2) * (1 - 1j * mu_wc) / (1 + mu_wc ** 2)

    # long-wave Doppler
    I_lim = np.logical_and(k > 0, k < k_br * d)
    c_br_vv = np.sum(
        -Mt_br_vv / np.tan(theta) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])
    c_br_hh = np.sum(
        -Mt_br_hh / np.tan(theta) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])

    I_lim = np.logical_and(k > 0, k < k_np / 10)
    c_wb1 = np.sum(-Mt_wb / np.tan(theta) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])
    c_wb2 = np.sum(-np.real(Mh_wb[I_lim]) * np.cos(0 - phi[I_lim]) * c[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])
    c_wb3 = np.sum(np.imag(Mh_wb[I_lim])/np.tan(theta) * c[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])
    c_wb=c_wb1+c_wb2+c_wb3
    #print(c_wb1, c_wb2, c_wb3)

    # specular set to zero
    c_sp_bar = 0
    c_sp = 0

    return c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh

# FIXME: be very careful with the signs of the MTF's (not sure if they are fully correction in the 'old DopRIM's'
# this is the implementation for a multi-wave system as defined in Hansen et al. (2012), equations refer to this paper
# for bi-static variants, rotate the input spectrum, wind direction, current direction and swell direction towards the range direction
def DopRIM(S, kx, ky, dks, theta, alpha_p, v_c, phi_c, k_sw, phi_sw, A_sw, phi_w, u_10, pol='V', k_r=0,
           rat=np.array([0.1, 0.8, 0.1]), degrees=False, u_10_local=0):
    # S: wave spectrum (only wind waves up to 1/4 of the radar wave number)
    # kx,ky: wavenumbers
    # dks: wavenumber sample spacing dk*dk (can vary if the distance between kx and ky varies)
    # theta[deg]: radar incident angle
    # alpha_p[deg]: bistatic angle
    # rat: ratio of specular, Bragg and breaking reflections
    # v_c[m/s]: current velocity (current properties is one thing we want to get)
    # phi_c[deg]: current direction
    # k_sw[m/s]: swell phase velocity velocity
    # phi_sw[deg]: swell direction direction (we can get swell properties from SAR spectra)
    # A_sw[m]: swell amplitude
    # pol: incident polarization
    # phi_w[deg]: local wind direction (we can get a first estimate of wind-speed/direction from three lines-of-sight backscatter)
    # u_10[deg]:  wind speed
    # fetch[deg]: local wind fetch

    # convert to radians
    if degrees:
        alpha = np.deg2rad(alpha_p)
        phi_c = np.deg2rad(phi_c)
        theta = np.deg2rad(theta)
        phi_sw = np.deg2rad(phi_sw)
        phi_w = np.deg2rad(phi_w)
    else:
        alpha = alpha_p
    # radar wavelength
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number
        # PLD: I moved the next inside the if clause, because we will pass
        # the correcty bistatically scalled k_r to the function instead
        # of computing it (wrongly)
        if alpha != 0:
            k_r = k_r * np.cos(alpha / 2)

    # some computations
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)  # drag velocity
    k_br = 2 * k_r * np.sin(theta)  # Bragg wave number

    # angular frequency and some conversions
    k = np.sqrt(kx ** 2 + ky ** 2)
    k_inv = np.where(k > 0, 1 / k, 0)
    C = np.sqrt(co.g * k_inv + co.gamma * k / co.rho_w)
    C[0, 0] = 0  # phase velocity
    C_sw = np.sqrt(co.g / k_sw + co.gamma * k_sw / co.rho_w)
    C_br = np.sqrt(co.g / k_br + co.gamma * k_br / co.rho_w)
    phi_k = np.arctan2(ky, kx)  # wave directions
    omega = np.where(k > 0, np.sqrt(co.g * k + co.gamma * k ** 3 / co.rho_w), 0)

    # integration limits
    k_wb = k_r / 10  # wave number of the shortest breaking waves
    k_d = co.d * k_r
    k_p = k[np.unravel_index(np.argmax(S), S.shape)]  # peak wavenumber
    C_wb = np.sqrt(co.g / k_wb + co.gamma * k_wb / co.rho_w)

    # spectral conversions
    B = k ** 4 * S  # saturation spectrum

    # large-scale wave mss (the assumption is that phi_r=0, the radar direction is 0 degrees)
    # based on eq. 16 in Hansen et al. (2012) and eq. 13 in Kudry et al. (2005)
    I_lim = np.logical_and(k > 0, k < k_d)
    sL_i = np.sqrt(np.sum(k[I_lim] ** 2 * np.cos(phi_k[I_lim]) ** 2 * S[I_lim] * dks[I_lim]))
    sL_ci = np.sqrt(np.sum(k[I_lim] ** 2 * np.sin(phi_k[I_lim]) ** 2 * S[I_lim] * dks[I_lim]))
    sL_cr = np.sqrt(np.sum(k[I_lim] ** 2 * np.sin(phi_k[I_lim] - phi_w) ** 2 * S[I_lim] * dks[I_lim]))
    sL_up = np.sqrt(np.sum(k[I_lim] ** 2 * np.cos(phi_k[I_lim] - phi_w) ** 2 * S[I_lim] * dks[I_lim]))

    # swell wave mss (only in case there is swell)
    sL_sw = np.sqrt(A_sw ** 2 * k_sw ** 2 / 2)

    # eq. 21 in Kudry et al. (2005), eq. 28 from Kudry et al. (2003) for derivation
    alpha, n, C_b = tuning_param_wb(u_star, C, k)
    Lambda = np.where(k > 0, k_inv / 2 * (B / alpha) ** (n + 1), 0)

    # relaxation parameters
    omega_wb = np.sqrt(co.g * k_wb + co.gamma * k_wb ** 3 / co.rho_w)
    omega_br = np.sqrt(co.g * k_br + co.gamma * k_br ** 3 / co.rho_w)
    tau_sp = n * C_b * (u_10 / C) ** 2 * np.sqrt(co.g * k_sw) / np.sqrt(co.g * k)
    _, n_br, C_b_br = tuning_param_wb(u_star, C_br * np.ones(1), k_br * np.ones(1))
    # m_g = 2 / n_br  # Kudry et al. (2003)
    beta_br = C_b_br * (u_star / C_br) ** 2  # Kudry et al. (1997)
    tau_br = n_br * beta_br[0] * omega_br / omega
    _, n_wb, C_b_wb = tuning_param_wb(u_star, C_wb * np.ones(1), k_wb * np.ones(1))
    # m_g = 2 / n_wb
    beta_wb = C_b_wb * (u_star / C_wb) ** 2
    tau_wb = n_wb * beta_wb[0] * omega_wb / omega

    ###### RIM: backscatter derivatives ######
    dtheta = 1E-5
    ## specular (eq. 8, Kudry et al, 2003)
    I_lim = k > k_d
    h_s = np.sqrt(np.sum(S[I_lim] * dks[I_lim]))  # below eq. 5 Kudry et al. (2005)
    tmp = np.exp(-k_r ** 2 * h_s ** 2)
    R = Fresnel_coeff_normal(pol=pol, eps_w=co.eps_w) * tmp  # Fresnel coefficients
    sigma_0sp = R ** 2 / (np.cos(theta) ** 4 * 2 * sL_cr * sL_up) * np.exp(-np.tan(theta) ** 2 / (2 * sL_i ** 2))
    dsigma_0sp = R ** 2 / (np.cos(theta + dtheta) ** 4 * 2 * sL_cr * sL_up) * np.exp(
        -np.tan(theta + dtheta) ** 2 / (2 * sL_i ** 2)) - sigma_0sp

    ## Bragg scattering (eq. A5, Kudry et al, 2003)
    Sr_temp = 0.5 * S[int((len(ky) - 1) / 2), :] + 0.5 * np.flip(S[int((len(ky) - 1) / 2), :])
    k_b0 = 1.0 * k_br  # radar Bragg number
    kx_temp = kx[int((len(ky) - 1) / 2), :]  # go to logaritmic domain for better interpolation
    Sr0 = 10 ** np.interp(np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))
    Gp0 = scattering_coeff(theta, pol=pol)  # scattering coefficients
    sigma_0br = 16 * np.pi * k_r ** 4 * Gp0 ** 2 * Sr0
    k_b0 = 2 * k_r * np.sin(theta + dtheta)
    Sr0 = 10 ** np.interp(np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))
    Gp0 = scattering_coeff(theta + dtheta, pol=pol)
    dsigma_0br = 16 * np.pi * k_r ** 4 * Gp0 ** 2 * Sr0 - sigma_0br

    ## wave breaking (eq. 60, Kudry et al, 2003)
    sigma_0wb = (1 / np.cos(theta) ** 4 * np.exp(-np.tan(theta) ** 2 / co.s_wb ** 2) + co.eps_wb) / co.s_wb ** 2
    dsigma_0wb = (1 / np.cos(theta + dtheta) ** 4 * np.exp(
        -np.tan(theta + dtheta) ** 2 / co.s_wb ** 2) + co.eps_wb) / co.s_wb ** 2 - sigma_0wb

    ###### Dopp: Doppler ######
    ## transfer functions
    # complex hydrodynamic modulation functions (Hansen2012, eq. 10, 11, 12, 17 and 21)
    Mh_br = co.m_k * np.cos(phi_k) ** 2 * (1 - 1j * tau_br) / (1 + tau_br ** 2)
    Mh_wb = 1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * (kx * k_inv) ** 2) * (1 - 1j * tau_wb) / (1 + tau_wb ** 2)
    Mh = (1 - 1j * tau_sp) / (1 + tau_sp ** 2) * co.m_k * np.cos(phi_k - phi_sw) ** 2  # eq. 10/11
    I_lim = np.logical_and(k > k_p, k < k_d)
    sL = np.sum(S[I_lim] * k[I_lim] ** 2 * dks[I_lim])
    Mh_sp = (np.tan(theta) ** 2 / sL ** 2 - 1) * np.sum(
        Mh[I_lim] * S[I_lim] * k[I_lim] ** 2 * dks[I_lim]) / sL ** 2  # eq. 17

    # these tilt functions are k-independent
    Mt_sp = 1 / sigma_0sp * dsigma_0sp / dtheta  # scalar
    Mt_br = 1 / sigma_0br * dsigma_0br / dtheta  # scalar
    Mt_wb = 1 / sigma_0wb * dsigma_0wb / dtheta  # scalar
    print(Mt_br)
    # from matplotlib import pyplot as plt
    # plt.imshow(np.real(Mh_br))
    # plt.colorbar()
    # plt.show()
    # print(np.sum(-Mt_br / np.tan(theta) * np.cos(
    #    0 - phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]), np.sum(np.real(-Mh_br[I_lim]) * np.cos(
    #    0 - phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]), np.sum(np.imag(Mh_br[I_lim]) / np.tan(
    #    theta) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]))

    # print(np.sum(-Mt_wb / np.tan(theta) * np.cos(
    #    0 - phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]), np.sum(-np.real(Mh_wb[I_lim]) * np.cos(
    #    0 - phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]), np.sum(np.imag(Mh_wb[I_lim]) / np.tan(
    #    theta) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]))

    ## modulated contributions to Doppler
    # be aware c_br and c_wb are actually multiplied by sL**2, which is compensated in the last equation for Doppler velocity
    # we apply the same thing for c_sp
    # equation 5 for br and wb and equation 18 for sp
    I_lim = np.logical_and(k > 0, k < k_d)
    c_br = np.sum(((-Mt_br / np.tan(theta) - np.real(Mh_br[I_lim])) * np.cos(
        0 - phi_k[I_lim]) + np.imag(Mh_br[I_lim]) / np.tan(
        theta)) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])

    I_lim = np.logical_and(k > 0, k < k_wb / 10)
    c_wb = np.sum(((-Mt_wb / np.tan(theta) - np.real(Mh_wb[I_lim])) * np.cos(
        0 - phi_k[I_lim]) + np.imag(Mh_wb[I_lim]) / np.tan(theta)) * C[I_lim] *
                  k[I_lim] ** 2 * S[I_lim] * dks[I_lim])  # k_wb/10 is the limit

    c_sp = C_sw * (np.cos(0 - phi_sw) * (-Mt_sp / np.tan(theta) + np.real(Mh_sp)) + np.imag(Mh_sp) / np.tan(
        theta)) * sL_sw ** 2  # this one is currently turned off

    ## mean doppler contributions from scattering facets
    # equation 15 for sp, equation 19 for wb and phase velocity for br (see between equation 8-9)
    # FIXME: this should be scaled for the bistatic case
    c_br_bar = (co.drift_vel_offset + co.u10_to_driftvel * u_10_local) * np.cos(phi_w)

    I_lim = np.logical_and(k > 0, k < k_wb)
    c_wb_bar = np.sum(np.cos(phi_k[I_lim] - 0) * C[I_lim] * k_inv[I_lim] * Lambda[I_lim] * dks[I_lim]) / \
               np.sum(k_inv[I_lim] * Lambda[I_lim] * dks[I_lim])

    I_lim = np.logical_and(k > 0, k < k_d)
    # FIXME: check if this is correct, they like to use cross-wind and along-wind first and then correct for the radar direction
    c_sp_bar = np.cos(0) / sL_i ** 2 * \
               np.sum(np.cos(phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]) + \
               np.sin(0) / sL_ci ** 2 * \
               np.sum(np.sin(phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])

    #### Doppler velocity in the direction of the mono-static receiver (equivalent) ####
    V = v_c * np.sin(theta) * np.cos(phi_c) + \
        rat[0] * (c_sp_bar + c_sp) + \
        rat[1] * (c_br_bar + c_br) + \
        rat[2] * (c_wb_bar + c_wb)

    return V, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br


# Dual-pol version of DopRIM
def DopRIM_DP(S, kx, ky, dks, theta, alpha_p, v_c, phi_c, k_sw, phi_sw, A_sw, phi_w, u_10, k_r=0,
              rat=np.array([0.1, 0.8, 0.1]), degrees=False, u_10_local=0):
    # S: wave spectrum (only wind waves up to 1/4 of the radar wave number)
    # kx,ky: wavenumbers
    # dks: wavenumber sample spacing dk*dk (can vary if the distance between kx and ky varies)
    # theta[rad]: radar incident angle
    # alpha_p[rad]: bistatic angle
    # rat: ratio of specular, Bragg and breaking reflections
    # v_c[m/s]: current velocity (current properties is one thing we want to get)
    # phi_c[rad]: current direction
    # k_sw[m/s]: swell phase velocity velocity
    # phi_sw[rad]: swell direction direction (we can get swell properties from SAR spectra)
    # A_sw[m]: swell amplitude
    # phi_w[rad]: local wind direction (we can get a first estimate of wind-speed/direction from three lines-of-sight backscatter)
    # u_10[m/s]: local wind speed
    # fetch[m]: local wind fetch

    # convert to radians
    if degrees:
        alpha = np.deg2rad(alpha_p)
        phi_c = np.deg2rad(phi_c)
        theta = np.deg2rad(theta)
        phi_sw = np.deg2rad(phi_sw)
        phi_w = np.deg2rad(phi_w)
    else:
        alpha = alpha_p
    # radar wavelength
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number
        # PLD: I moved the next inside the if clause, because we will pass
        # the correcty bistatically scalled k_r to the function instead
        # of computing it (wrongly)
        if alpha != 0:
            k_r = k_r * np.cos(alpha / 2)

    # some computations
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)  # drag velocity
    k_br = 2 * k_r * np.sin(theta)  # Bragg wave number

    # angular frequency and some conversions
    k = np.sqrt(kx ** 2 + ky ** 2)
    k_inv = np.where(k > 0, 1 / k, 0)
    C = np.sqrt(co.g * k_inv + co.gamma * k / co.rho_w)
    C[0, 0] = 0  # phase velocity
    C_sw = np.sqrt(co.g / k_sw + co.gamma * k_sw / co.rho_w)
    C_br = np.sqrt(co.g / k_br + co.gamma * k_br / co.rho_w)
    phi_k = np.arctan2(ky, kx)  # wave directions
    omega = np.where(k > 0, np.sqrt(co.g * k + co.gamma * k ** 3 / co.rho_w), 0)

    # integration limits
    k_wb = k_r / 10  # wave number of the shortest breaking waves
    k_d = co.d * k_r
    # FIXME: this is dangerous if a swell system is included
    k_p = k[np.unravel_index(np.argmax(S), S.shape)]  # peak wavenumber
    C_wb = np.sqrt(co.g / k_wb + co.gamma * k_wb / co.rho_w)

    # spectral conversions
    B = k ** 4 * S  # saturation spectrum

    # large-scale wave mss (the assumption is that phi_r=0, the radar direction is 0 degrees)
    # based on eq. 16 in Hansen et al. (2012) and eq. 13 in Kudry et al. (2005)
    I_lim = np.logical_and(k > 0, k < k_d)
    sL_i = np.sqrt(np.sum(k[I_lim] ** 2 * np.cos(phi_k[I_lim]) ** 2 * S[I_lim] * dks[I_lim]))
    sL_ci = np.sqrt(np.sum(k[I_lim] ** 2 * np.sin(phi_k[I_lim]) ** 2 * S[I_lim] * dks[I_lim]))
    sL_cr = np.sqrt(np.sum(k[I_lim] ** 2 * np.sin(phi_k[I_lim] - phi_w) ** 2 * S[I_lim] * dks[I_lim]))
    sL_up = np.sqrt(np.sum(k[I_lim] ** 2 * np.cos(phi_k[I_lim] - phi_w) ** 2 * S[I_lim] * dks[I_lim]))

    # swell wave mss (only in case there is swell)
    sL_sw = np.sqrt(A_sw ** 2 * k_sw ** 2 / 2)

    # eq. 21 in Kudry et al. (2005), eq. 28 from Kudry et al. (2003) for derivation
    alpha, n, C_b = tuning_param_wb(u_star, C, k)
    Lambda = np.where(k > 0, k_inv / 2 * (B / alpha) ** (n + 1), 0)

    # relaxation parameters
    omega_wb = np.sqrt(co.g * k_wb + co.gamma * k_wb ** 3 / co.rho_w)
    omega_br = np.sqrt(co.g * k_br + co.gamma * k_br ** 3 / co.rho_w)
    tau_sp = n * C_b * (u_10 / C) ** 2 * np.sqrt(co.g * k_sw) / omega
    _, n_br, C_b_br = tuning_param_wb(u_star, C_br * np.ones(1), k_br * np.ones(1))
    # m_g = 2 / n_br  # Kudry et al. (2003)
    beta_br = C_b_br * (u_star / C_br) ** 2  # Kudry et al. (1997)
    tau_br = n_br * beta_br[0] * omega_br / omega
    _, n_wb, C_b_wb = tuning_param_wb(u_star, C_wb * np.ones(1), k_wb * np.ones(1))
    # m_g = 2 / n_wb
    beta_wb = C_b_wb * (u_star / C_wb) ** 2
    tau_wb = n_wb * beta_wb[0] * omega_wb / omega

    ###### RIM: backscatter derivatives ######
    dtheta = 1E-5
    ## specular (eq. 8, Kudry et al, 2003)
    I_lim = k > k_d
    h_s = np.sqrt(np.sum(S[I_lim] * dks[I_lim]))  # below eq. 5 Kudry et al. (2005)
    tmp = np.exp(-k_r ** 2 * h_s ** 2)
    Rvv2 = (Fresnel_coeff_normal(pol='V', eps_w=co.eps_w) * tmp) ** 2  # Fresnel coefficients
    # Rhh2 = (Fresnel_coeff_normal( pol = 'H', eps_w = co.eps_w ) * tmp)**2
    sL_cr_sL_up_2 = 2 * sL_cr * sL_up
    tmp = np.exp(-np.tan(theta) ** 2 / (2 * sL_i ** 2)) / (np.cos(theta) ** 4 * sL_cr_sL_up_2)
    sigma_0sp_vv = Rvv2 * tmp
    # sigma_0sp_hh = Rhh2 * tmp
    tmp = np.exp(-np.tan(theta + dtheta) ** 2 / (2 * sL_i ** 2)) / (np.cos(theta + dtheta) ** 4 * sL_cr_sL_up_2)
    dsigma_0sp_vv = Rvv2 * tmp - sigma_0sp_vv
    # dsigma_0sp_hh = Rhh2 * tmp - sigma_0sp_hh
    ## Bragg scattering (eq. A5, Kudry et al, 2003)
    Sr_temp = 0.5 * S[int((len(ky) - 1) / 2), :] + 0.5 * np.flip(S[int((len(ky) - 1) / 2), :])
    k_b0 = 1.0 * k_br  # radar Bragg number
    kx_temp = kx[int((len(ky) - 1) / 2), :]  # go to logaritmic domain for better interpolation
    Sr0 = 10 ** np.interp(np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))
    # scattering coefficients
    Gp0_vv = scattering_coeff(theta, pol="V")
    Gp0_hh = scattering_coeff(theta, pol="H")
    tmp = 16 * np.pi * k_r ** 4 * Sr0
    sigma_0br_vv = Gp0_vv ** 2 * tmp
    sigma_0br_hh = Gp0_hh ** 2 * tmp
    k_b0 = 2 * k_r * np.sin(theta + dtheta)
    Sr0 = 10 ** np.interp(np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))
    Gp0_vv = scattering_coeff(theta + dtheta, pol="V")
    Gp0_hh = scattering_coeff(theta + dtheta, pol="H")
    tmp = 16 * np.pi * k_r ** 4 * Sr0
    dsigma_0br_vv = Gp0_vv ** 2 * tmp - sigma_0br_vv
    dsigma_0br_hh = Gp0_hh ** 2 * tmp - sigma_0br_hh
    ## wave breaking (eq. 60, Kudry et al, 2003)
    sigma_0wb = (1 / np.cos(theta) ** 4 * np.exp(-np.tan(theta) ** 2 / co.s_wb ** 2) + co.eps_wb) / co.s_wb ** 2
    dsigma_0wb = (1 / np.cos(theta + dtheta) ** 4 * np.exp(
        -np.tan(theta + dtheta) ** 2 / co.s_wb ** 2) + co.eps_wb) / co.s_wb ** 2 - sigma_0wb

    ###### Dopp: Doppler ######
    ## transfer functions
    # complex hydrodynamic modulation functions (Hansen2012, eq. 10, 11, 12, 17 and 21)
    Mh_br = co.m_k * np.cos(phi_k) ** 2 * (1 - 1j * tau_br) / (1 + tau_br ** 2)
    Mh_wb = 1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * (kx * k_inv) ** 2) * (1 - 1j * tau_wb) / (1 + tau_wb ** 2)
    Mh = (1 - 1j * tau_sp) / (1 + tau_sp ** 2) * co.m_k * np.cos(phi_k - phi_sw) ** 2  # eq. 10/11
    I_lim = np.logical_and(k > k_p, k < k_d)
    sL = np.sum(S[I_lim] * k[I_lim] ** 2 * dks[I_lim])
    Mh_sp = (np.tan(theta) ** 2 / sL ** 2 - 1) * np.sum(
        Mh[I_lim] * S[I_lim] * k[I_lim] ** 2 * dks[I_lim]) / sL ** 2  # eq. 17

    # these tilt functions are k-independent
    Mt_sp = 1 / sigma_0sp_vv * dsigma_0sp_vv / dtheta  # scalar
    Mt_br_vv = 1 / sigma_0br_vv * dsigma_0br_vv / dtheta
    Mt_br_hh = 1 / sigma_0br_hh * dsigma_0br_hh / dtheta  # scalar
    Mt_wb = 1 / sigma_0wb * dsigma_0wb / dtheta  # scalar

    ## modulated contributions to Doppler
    # be aware c_br and c_wb are actually multiplied by sL**2, which is compensated in the last equation for Doppler velocity
    # we apply the same thing for c_sp
    # equation 5 for br and wb and equation 18 for sp
    I_lim = np.logical_and(k > 0, k < k_d)
    c_br_vv = np.sum(((-Mt_br_vv / np.tan(theta) - np.real(Mh_br[I_lim])) * np.cos(
        0 - phi_k[I_lim]) + np.imag(Mh_br[I_lim]) / np.tan(
        theta)) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])
    c_br_hh = np.sum(((-Mt_br_hh / np.tan(theta) - np.real(Mh_br[I_lim])) * np.cos(
        0 - phi_k[I_lim]) + np.imag(Mh_br[I_lim]) / np.tan(
        theta)) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])
    I_lim = np.logical_and(k > 0, k < k_wb / 10)
    c_wb = np.sum(((-Mt_wb / np.tan(theta) - np.real(Mh_wb[I_lim])) * np.cos(
        0 - phi_k[I_lim]) + np.imag(Mh_wb[I_lim]) / np.tan(theta)) * C[I_lim] *
                  k[I_lim] ** 2 * S[I_lim] * dks[I_lim])  # k_wb/10 is the limit

    c_sp = C_sw * (np.cos(0 - phi_sw) * (-Mt_sp / np.tan(theta) + np.real(Mh_sp)) + np.imag(Mh_sp) / np.tan(
        theta)) * sL_sw ** 2

    ## mean doppler contributions from scattering facets
    # FIXME: this should be scaled for the bistatic case
    c_br_bar = (co.drift_vel_offset + co.u10_to_driftvel * u_10_local) * np.cos(phi_w)

    I_lim = np.logical_and(k > 0, k < k_wb)
    c_wb_bar = np.sum(np.cos(phi_k[I_lim] - 0) * C[I_lim] * k_inv[I_lim] * Lambda[I_lim] * dks[I_lim]) / \
               np.sum(k_inv[I_lim] * Lambda[I_lim] * dks[I_lim])

    I_lim = np.logical_and(k > 0, k < k_d)
    # FIXME: check if this is correct, they like to use cross-wind and along-wind first and then correct for the radar direction
    c_sp_bar = np.cos(0) / sL_i ** 2 * \
               np.sum(np.cos(phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim]) + \
               np.sin(0) / sL_ci ** 2 * \
               np.sum(np.sin(phi_k[I_lim]) * C[I_lim] * k[I_lim] ** 2 * S[I_lim] * dks[I_lim])

    return c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_hh, c_br_vv


# for bi-static variants, rotate the input spectrum, wind direction, current direction and swell direction by -alpha_p/2 or alpha_p/2
def tilt_transfer_func(S, kx, ky, dks, theta, k_r, phi_w):
    """

    Parameters
    ----------
    S: Kudryavtsev two-dimensional Cartesian wave spectrum
    kx: cross-track wave number
    ky: along-track wave number
    theta: incident angle of monostatic equivalent
    k_r: radar wave number of monostatic equivalent
    phi_w: wind speed [rad]

    Returns
    -------
    Mt:
        tilt modulation transfer functions
    """

    # angular frequency and some conversions
    k = np.sqrt(kx ** 2 + ky ** 2)
    phi_k = np.arctan2(ky, kx)  # wave directions

    # limits, peak and Bragg wave number
    k_d = co.d * k_r
    k_br = 2 * k_r * np.sin(theta)

    # large-scale wave mss (the assumption is that phi_r=0, the radar direction is 0 degrees)
    # based on eq. 16 in Hansen et al. (2012) and eq. 13 in Kudry et al. (2005)
    I_lim = np.logical_and(k > 0, k < k_d)
    sL_i = np.sqrt(np.sum(k[I_lim] ** 2 * np.cos(phi_k[I_lim]) ** 2 * S[I_lim] * dks[I_lim]))
    sL_ci = np.sqrt(np.sum(k[I_lim] ** 2 * np.sin(phi_k[I_lim]) ** 2 * S[I_lim] * dks[I_lim]))
    sL_cr = np.sqrt(np.sum(k[I_lim] ** 2 * np.sin(phi_k[I_lim] - phi_w) ** 2 * S[I_lim] * dks[I_lim]))
    sL_up = np.sqrt(np.sum(k[I_lim] ** 2 * np.cos(phi_k[I_lim] - phi_w) ** 2 * S[I_lim] * dks[I_lim]))

    # dtheta
    dtheta = 1E-5

    ## specular (eq. 8, Kudry et al, 2003)
    I_lim = k > k_d
    h_s = np.sqrt(np.sum(S[I_lim] * dks[I_lim]))  # below eq. 5 Kudry et al. (2005)
    tmp = np.exp(-k_r ** 2 * h_s ** 2)
    Rvv2 = (Fresnel_coeff_normal(pol='V', eps_w=co.eps_w) * tmp) ** 2  # Fresnel coefficients
    # Rhh2 = (Fresnel_coeff_normal( pol = 'H', eps_w = co.eps_w ) * tmp)**2
    sL_cr_sL_up_2 = 2 * sL_cr * sL_up
    tmp = np.exp(-np.tan(theta) ** 2 / (2 * sL_i ** 2)) / (np.cos(theta) ** 4 * sL_cr_sL_up_2)
    sigma_0sp_vv = Rvv2 * tmp
    # sigma_0sp_hh = Rhh2 * tmp
    tmp = np.exp(-np.tan(theta + dtheta) ** 2 / (2 * sL_i ** 2)) / (np.cos(theta + dtheta) ** 4 * sL_cr_sL_up_2)
    dsigma_0sp_vv = Rvv2 * tmp - sigma_0sp_vv
    # dsigma_0sp_hh = Rhh2 * tmp - sigma_0sp_hh

    ## Bragg scattering (eq. A5, Kudry et al, 2003)
    Sr_temp = 0.5 * S[int((len(ky) - 1) / 2), :] + 0.5 * np.flip(S[int((len(ky) - 1) / 2), :])
    k_b0 = 1.0 * k_br  # radar Bragg number
    kx_temp = kx[int((len(ky) - 1) / 2), :]  # go to logaritmic domain for better interpolation
    Sr0 = 10 ** np.interp(np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))
    # scattering coefficients
    Gp0_vv = scattering_coeff(theta, pol="V")
    Gp0_hh = scattering_coeff(theta, pol="H")
    tmp = 16 * np.pi * k_r ** 4 * Sr0
    sigma_0br_vv = Gp0_vv ** 2 * tmp
    sigma_0br_hh = Gp0_hh ** 2 * tmp
    k_b0 = 2 * k_r * np.sin(theta + dtheta)
    Sr0 = 10 ** np.interp(np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]))
    Gp0_vv = scattering_coeff(theta + dtheta, pol="V")
    Gp0_hh = scattering_coeff(theta + dtheta, pol="H")
    tmp = 16 * np.pi * k_r ** 4 * Sr0
    dsigma_0br_vv = Gp0_vv ** 2 * tmp - sigma_0br_vv
    dsigma_0br_hh = Gp0_hh ** 2 * tmp - sigma_0br_hh

    ## wave breaking (eq. 60, Kudry et al, 2003)
    sigma_0wb = (1 / np.cos(theta) ** 4 * np.exp(-np.tan(theta) ** 2 / co.s_wb ** 2) + co.eps_wb) / co.s_wb ** 2
    dsigma_0wb = (1 / np.cos(theta + dtheta) ** 4 * np.exp(
        -np.tan(theta + dtheta) ** 2 / co.s_wb ** 2) + co.eps_wb) / co.s_wb ** 2 - sigma_0wb

    # these tilt functions are k-independent
    Mt_sp = 1 / sigma_0sp_vv * dsigma_0sp_vv / dtheta  # scalar
    Mt_br_vv = 1 / sigma_0br_vv * dsigma_0br_vv / dtheta
    Mt_br_hh = 1 / sigma_0br_hh * dsigma_0br_hh / dtheta  # scalar
    Mt_wb = 1 / sigma_0wb * dsigma_0wb / dtheta  # scalar

    return Mt_sp, Mt_br_vv, Mt_br_hh, Mt_wb


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
    u_10 = 10
    fetch = 500E3
    phi_w = 0
    B, B_neq, B_w, B_pc = Kudry_spec_polar(k, phi, u_10, fetch, phi_w, S=0)
    kv, phiv = np.meshgrid(k, phi)
    # dk, dphi = np.meshgrid(dk, dphi)
    S = np.where(kv > 0, B * kv ** -4, 0)
    '''
    cmap = cm.get_cmap('gist_ncar_r', 15)
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    con = ax.pcolormesh(phiv, kv, np.log10(S), cmap=cmap, vmin=-15, vmax=0)
    ax.set_rscale('log')
    fig.colorbar(con, ax=ax)
    plt.show()
    plt.figure()
    plt.plot(k, np.sum(B * dphi[0], axis=0))
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(5E-4, 2E-2)
    plt.xlim(1E-2, 1E4)
    plt.grid('on')
    plt.show()
    '''

    # RIM
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
            rat = np.array([s_spec * (1 - q), s_bragg_vv * (1 - q), s_break * q]) / (
                    s_spec * (1 - q) + s_bragg_vv * (1 - q) + s_break * q)

            c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh = DopRIM2023_DP_polar(S, k, phi,
                                                                                             np.deg2rad(theta_i[i]),
                                                                                             u_10, np.deg2rad(phi_w),
                                                                                             k_r=0)
            #print(c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh)
            print(s_bragg_vv,s_break)
            if i == 0:
                # plt.plot( theta_i[ i ], rat[ 0 ],'.b', label='specular' )
                # plt.plot( theta_i[ i ], rat[ 2 ],'.r', label='wave breaking' )
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp_bar, 'b*', label = 'bar{c}_{sp}' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb_bar, 'r*', label = 'bar{c}_{wb}' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br_bar, 'g*', label = 'bar{c}_{br}' )
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp, 'b.', label = 'c_{sp}' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb, 'r.', label = 'c_{wb}' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br, 'g.', label = 'c_{br}' )
                # plt.plot( theta_i[ i ], V, 'k.', label = 'total' )
                plt.plot(theta_i[i], rat[0] * (c_sp + c_sp_bar), 'b.', label='specular')
                plt.plot(theta_i[i], rat[2] * (c_wb + c_wb_bar), 'g.', label='breakers')
                plt.plot(theta_i[i], rat[1] * (c_br_bar + c_br_vv), 'r.', label='Bragg')
            if i != 0:
                # plt.plot( theta_i[i], rat[ 0 ],'.b')
                # plt.plot( theta_i[ i ], rat[ 2 ],'.r')
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp_bar, 'b*' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb_bar, 'r*' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br_bar, 'g*' )
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp, 'b.' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb, 'r.' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br, 'g.' )
                # plt.plot(theta_i[i], V, 'k.')
                plt.plot(theta_i[i], rat[0] * (c_sp + c_sp_bar), 'b.')
                plt.plot(theta_i[i], rat[2] * (c_wb + c_wb_bar), 'g.')
                plt.plot(theta_i[i], rat[1] * (c_br_bar + c_br_vv), 'r.')

        plt.ylim(-2, 2)
        plt.legend()
    plt.show()

    #'''
    # wavelengths and wave numbers
    g = 9.81
    n_k = 200  # number of frequencies single side (total 2*n_k - 1)
    lambda_min = 0.01  # minimum wave length
    lambda_max = 2000  # maximum wave length
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

    # DopRIM
    theta_i = np.arange(31, 46, 1)
    alpha = 0
    v_c = 0
    phi_c = 0
    k_sw = 0.02
    phi_sw = 0
    A_sw = 0.01
    plt.figure(figsize=(15, 5))
    print('Cartesian')
    for j in range(0, 3):
        phi_w = j * 90.0

        # wave spectrum using Elfouhaily et al. (1997)
        u_10 = 10
        fetch = 500E3
        B, _, _, _ = Kudry_spec(k_x, k_y, u_10, fetch, np.deg2rad(phi_w), dks)
        S = np.where(k > 0, B * k ** -4, 0)
        # print(phi_w)

        plt.subplot(1, 3, j + 1)
        for i in range(0, len(theta_i)):

            # s_spec, s_bragg_vv, s_break, q = backscatter.backscatter_Kudry2005(S, k_x, k_y, dks, phi_w, theta=theta_i[i],
            #                                                                pol='V',
            #                                                                u_10=u_10, k_r=0)
            sigma_los, dsigmadth, q = backscatter_Kudry2023(S, k_x, k_y, dks, phi_w=phi_w, theta=theta_i[i],
                                                            u_10=u_10, k_r=0, degrees=True)
            s_spec = sigma_los[0]
            s_bragg_vv = sigma_los[1]
            s_bragg_hh = sigma_los[2]
            s_break = sigma_los[3]
            rat = np.array([s_spec * (1 - q), s_bragg_vv * (1 - q), s_break * q]) / (
                    s_spec * (1 - q) + s_bragg_vv * (1 - q) + s_break * q)
            #print(rat)

            # V, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br = DopRIM(S, k_x, k_y, dks, theta_i[i], alpha, v_c, phi_c,
            #                                                           k_sw,
            #                                                           phi_sw, A_sw, phi_w, u_10, pol='V', rat=rat,
            #                                                           degrees='True')
            c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh = DopRIM2023_DP(S, k_x, k_y, dks,
                                                                                       np.deg2rad(theta_i[i]), u_10,
                                                                                       np.deg2rad(phi_w), k_r=0)
            #print(c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh)

            # plt.plot(theta_i[i],V,'k.')

            if i == 0:
                # plt.plot( theta_i[ i ], rat[ 0 ],'.b', label='specular' )
                # plt.plot( theta_i[ i ], rat[ 2 ],'.r', label='wave breaking' )
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp_bar, 'b*', label = 'bar{c}_{sp}' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb_bar, 'r*', label = 'bar{c}_{wb}' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br_bar, 'g*', label = 'bar{c}_{br}' )
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp, 'b.', label = 'c_{sp}' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb, 'r.', label = 'c_{wb}' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br, 'g.', label = 'c_{br}' )
                # plt.plot( theta_i[ i ], V, 'k.', label = 'total' )
                plt.plot(theta_i[i], rat[0] * (c_sp + c_sp_bar), 'b.', label='specular')
                plt.plot(theta_i[i], rat[2] * (c_wb + c_wb_bar), 'g.', label='breakers')
                plt.plot(theta_i[i], rat[1] * (c_br_bar + c_br_vv), 'r.', label='Bragg')
            if i != 0:
                # plt.plot( theta_i[i], rat[ 0 ],'.b')
                # plt.plot( theta_i[ i ], rat[ 2 ],'.r')
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp_bar, 'b*' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb_bar, 'r*' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br_bar, 'g*' )
                # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp, 'b.' )
                # plt.plot( theta_i[ i ], rat[ 2 ] * c_wb, 'r.' )
                # plt.plot( theta_i[ i ], rat[ 1 ] * c_br, 'g.' )
                # plt.plot(theta_i[i], V, 'k.')
                plt.plot(theta_i[i], rat[0] * (c_sp + c_sp_bar), 'b.')
                plt.plot(theta_i[i], rat[2] * (c_wb + c_wb_bar), 'g.')
                plt.plot(theta_i[i], rat[1] * (c_br_bar + c_br_vv), 'r.')

        plt.xlabel('incident angle [deg]')
        plt.ylabel('relative contribution [m/s]')
        tit = 'wind direction: ' + str(phi_w) + '$^\circ$'
        plt.title(tit)
        plt.ylim(-2, 2)
    plt.legend()
    plt.show()
    #'''
