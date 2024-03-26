"""
Author: Paco I guess

Elfouhaily et al. Omnidirectional Spectrum
Reference:
    Elfouhaily T., Chapron B., and Katsaros K. (1997). "A unified
    directional spectrum for long and short wind driven waves"
"""

import warnings
import numpy as np
import scipy as sp

rho = 1000.  # Density of water in kg/m^3
S = 0.072  # Surface tension of water in N/m
X_0 = 22e3  # Dimensionless fetch

from scipy.constants import g

# Sea water rel.dielectric constant
epsilon_sw = complex(73, 18)
# Constant in close agreement with [Thompson, 1988] Kudryavtsev [2005]
d = 1 / 4
# C-band radio wave number. Estimate of sea state from Sentinel-1 SAR imagery for maritime situation awareness 1.1, 5.6 cm
kr = 2 * np.pi / 5.6e-2
# Divide two intervals (small and large scale waves) [Kudryavstev, 2005]
kd = d * kr
# Mean square slope of enhanced roughness of the wave breaking zone [Kudryavstev, 2003]
Swb = 0.19
# Ratio of the breaker thickness to its length [Kudryavstev, 2003]
yitawb = 0.005
# Wave break wave number [Kudryavtsev, 2005]
kwb = 2 * np.pi / 0.3
# Density of water kg /mˆ3
rho_water = 1e3
# Density of air kg /mˆ3 at 15 degree
rho_air = 1.225
# Von Karman constant
kappa = 0.4
# Surface tension of water at 20 degree
gamma = 0.07275
# Wave number of minimum phase velocity
ky = np.sqrt(g * rho_water / gamma)
# Saturation level constant [Kudryavtsev, 2003]
a = 2.5e-3
# Tunning parameter [Kudryavstev, 2003]
alpha = 5e-3
# The constant of the equilibrium gravity range [Kudryavstev, 2003]
ng = 5
# Mean tilt of enhances scattering areas of breaking waves [Kudryavstev, 2003]
theta_wb = 5e-2
# Constant to compute fraction q [Kudryavstev, 2003]
cq = 10.5
# Constant implies that the length of waves providing non-Bragg scattering are more than 10 ten times longer than the radar wave length [Kudryavtsev, 2003]
br = 0.1
# Averaged tilt of parasitic capillary trains [Kudryavtsev, 2003]
theta_pc = 5e-2
# Coriolis parameter f-plane approximation (doesn't change with altitude)
f = 1e-4
# kinematic viscosity coefficient of sea water at 20 degree [m^2/s]
v = 1.15e-6
# kinematic viscosity coefficient of air at 15 degree [m^2/s]
v_air = 1.47e-5
# empirical constant for wave breaking
cb = 1.2e-2


def __gamma_function(Omega_c):
    # Eq. 3 (below)
    if (Omega_c > 0.84) and (Omega_c < 1.0):
        gamma = 1.7
    elif (Omega_c > 1.0) and (Omega_c < 5.0):
        gamma = 1.7 + 6. * np.log10(Omega_c)
    else:
        warnings.warn('Omega_c is out of range. Returning  value for 5.0', RuntimeWarning)
        gamma = 1.7 + 6. * np.log10(5.0)

    return gamma


def __alpha_m_function(ustar, c_m):
    # Eq. 44
    if ustar < c_m:
        alpha_m = 1e-2 * (1. + np.log(ustar / c_m))
    else:
        alpha_m = 1e-2 * (1. + 3. * np.log(ustar / c_m))

    return alpha_m


def elfouhaily(k, U_10, fetch):
    # Calculated variables
    k_m = 2 * np.pi / 0.017
    # Eq. 3 (below)
    k_0 = g / U_10 ** 2
    # Eq. 4 (below)
    X = k_0 * fetch
    # Eq. 37: Inverse wave age
    Omega_c = 0.84 * np.tanh((X / X_0) ** (0.4)) ** (-0.75)
    # Wave phase speed (assumes deep water)
    c = np.sqrt(g / k + S / rho * k)

    # B_l: Long-wave curvature spectrum
    # Note that in contrast to Elfouhaily's paper, the L_pm factor
    # is applied to the both B_l and B_h.

    # Eq. 3 (below)
    k_p = k_0 * Omega_c ** 2
    # Phase speed at the spectral peak
    c_p = np.sqrt(g / k_p + S / rho * k_p)
    # Eq. 32 (above): Inverse wave age parameter (dimensionless)
    Omega = U_10 / c_p
    # Eq. 34
    alpha_p = 6e-3 * np.sqrt(Omega)

    # Eq. 3 (below)
    sigma = 0.08 * (1. + 4. * Omega_c ** (-3.))
    Gamma = np.exp(-(np.sqrt(k / k_p) - 1.) ** 2 / (2. * sigma ** 2))
    # Eq. 3
    J_p = __gamma_function(Omega_c) ** Gamma
    # Eq. 2
    L_pm = np.exp(-5. / 4. * (k_p / k) ** 2)
    # Eq. 32
    F_p = L_pm * J_p * np.exp(-Omega / np.sqrt(10.) * (np.sqrt(k / k_p) - 1.))
    # Eq. 32
    B_l = 0.5 * alpha_p * c_p / c * F_p

    # B_s: Short-wave curvature spectrum
    # (McDaniel, 2001, above Equation 3.9)
    C_10 = (0.8 + 0.065 * U_10) * 1e-3
    # Eq. 61: Friction velocity
    ustar = np.sqrt(C_10) * U_10

    # Eq. 41 (above)
    c_m = np.sqrt(g / k_m + S / rho * k_m)
    # Eq. 41 (above)
    alpha_m = __alpha_m_function(ustar, c_m)
    # Eq. 41 with L_pm according to McDaniel, 2001 (in text below Equation 3.9)
    F_m = L_pm * np.exp(-0.25 * (k / k_m - 1.) ** 2)
    # Eq. 40
    B_h = 0.5 * alpha_m * c_m / c * F_m

    # Eq. 30 (Final spectrum)
    return (B_l + B_h) / k ** 3


"""
Implementation of the directional function to construct a
directional wave spectrum, following Elfouhaily et al.
Elfouhaily T., Chapron B., and Katsaros K. (1997). "A unified
directional spectrum for long and short wind driven waves"
J. Geophys. Res. 102 15.781-96
LOG:
2011-08-26 Gordon Farquharson: Removed an extra factor of 2. the code that implements from Equation 49.
2013-01-25 Paco Lopez Dekker: Renormalized function so that the integral in theta gives 1 (instead of 0.5)
"""

import numpy as np
from scipy.constants import g

rho = 1000.  # Density of water in kg/m^3
S = 0.072  # Surface tension of water in N/m
X_0 = 22e3  # Dimensionless fetch


def elfouhaily_spread(k, theta, U_10, fetch, dtheta=0):
    # print(dtheta)
    # Eq. 3 (below)
    k_0 = g / U_10 ** 2
    # Eq. 4 (below)
    X = k_0 * fetch
    # Eq. 37
    Omega_c = 0.84 * np.tanh((X / X_0) ** (0.4)) ** (-0.75)
    cK = np.sqrt(g / k + S / rho * k)

    # Eq. 3 (below)
    k_p = k_0 * Omega_c ** 2
    cK_p = np.sqrt(g / k_p + S / rho * k_p)

    # Eq. 24
    k_m = np.sqrt(rho * g / S)
    cK_m = np.sqrt(g / k_m + S / rho * k_m)

    # (McDaniel, 2001, above Equation 3.9)
    C_10 = (0.8 + 0.065 * U_10) * 1e-3
    # Eq. 61
    ustar = np.sqrt(C_10) * U_10

    # Eq. 59
    a_0 = np.log(2.) / 4.
    a_p = 4.
    a_m = 0.13 * ustar / cK_m
    # Eq. 57
    Delta = np.tanh(a_0 + a_p * (cK / cK_p) ** 2.5 + a_m * (cK_m / cK) ** 2.5)
    # Eq. 49
    if dtheta == 0:
        G = np.where((theta >= -np.pi / 2.) & (theta < np.pi / 2.), (1. + Delta * np.cos(2. * theta)) / (np.pi), 0)
    else:
        dphi1 = np.pi / 2 - theta
        dphi2 = theta + np.pi / 2
        G = (1. + Delta * np.cos(2. * theta)) / (2 * np.pi) * (1 + np.tanh(dphi1 / dtheta) * np.tanh(dphi2 / dtheta))

    return G


# Elfhouhaily et al. (1997)
def spec_peak(u_10, fetch):
    X_0 = 22e3  # Dimensionless fetch
    k_0 = g / u_10 ** 2
    # Eq. 4 (below)
    X = k_0 * fetch
    # Eq. 37: Inverse wave age
    Omega_c = 0.84 * np.tanh((X / X_0) ** (0.4)) ** (-0.75)
    # Eq. 3 (below)
    k_p = k_0 * Omega_c ** 2
    return k_p


######################## Additional spreading functions #########################
# Longuet-Higgins et al. (1963); Mitsuyasu et al. (1975); Denis and Pearson (1953)
def DandP_spread(k, theta, u_10, fetch):
    """

    Parameters
    ----------
    k
    theta
    u_10
    fetch

    Returns
    -------

    """

    # Based on chapter 6 in Holthuijsen (2007): Waves in oceanic and coastal waters
    # Only use this function for deep-water waves

    # some conversions
    g = 9.81
    omega = np.sqrt(g * k)
    f = 2 * np.pi * omega
    k_p = spec_peak(u_10, fetch)
    omega_p = np.sqrt(g * k_p)
    f_p = 2 * np.pi * omega_p

    # angular spread
    sigma = np.radians(26.9 * (f / f_p) ** -1.05)
    sigma[f >= f_p] = np.radians(26.9 * (f[f >= f_p] / f_p) ** 0.68)
    # FIXME: I set constraints on s and sigma to avoid blowing up and limit discontinuities, not sure this is correct
    sigma[sigma > np.radians(50)]=np.radians(50)

    # width parameter
    s = 2 / sigma ** 2 - 1

    # normalization factor
    A2 = sp.special.gamma(s + 1) / (sp.special.gamma(s + 0.5) * 2 * np.sqrt(np.pi))

    # directional distribution
    D = np.where(s > 0.0, A2 * np.cos(0.5 * theta) ** (2 * s),0)

    return D


######################## Kudryavtsev et al. (2005) #########################

# some constants
from stereoid.oceans.forward_models.RIM_constants import constants as co

# Kudry et al. (2005) spectrum
# FIXME: there is an anomaly is S at low wave numbers in the upwind direction
# FIXME: possibly related to combination of B's in bottom of the code
# FIXME: there is a 'disconuity' caused by the combination of B's
def Kudry_spec_polar(k, phi_k, u_10, fetch, phi_w, S=0, k_cut=None):
    """

    Parameters
    ----------
    kx
    phi_k
    u_10
    fetch
    phi_w
    S
    k_cut: wavenumber limit between long and short waves, if None it is set to 10*k_p
    note, in other functions this is k_l, but it is here already used

    Returns
    -------

    """

    # let's ignore the log(0) and 1/0 errors (they will be handled properly)
    import warnings
    warnings.simplefilter(action="ignore", category=RuntimeWarning)

    # conversion of angles
    # phi_w = np.deg2rad( phi_w )

    # gradients and grids
    dk = np.gradient(k)
    dphi = (phi_k[1] - phi_k[0]) * np.ones(len(phi_k))
    k, phi_k = np.meshgrid(k, phi_k)
    dk, dphi = np.meshgrid(dk, dphi)

    # wave numbers
    I = k > 0
    k_inv = np.where(I, 1 / k, 0)
    C = np.where(I, np.sqrt(g * k_inv + co.gamma * k / co.rho_w), 0)  # phase speed
    omega_k = np.where(I, np.sqrt(g * k + co.gamma * k ** 3 / co.rho_w), 0)  # angular velocity

    ## some required paramaters
    if fetch != 0:
        k_p = spec_peak(u_10, fetch)
    if fetch == 0:
        I_kp = np.argmax(S)
        k_p = k.ravel()[I_kp]
    k_wb = 2 * np.pi / 0.3
    k_gamma = np.sqrt(co.g / co.gamma * co.rho_w)
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)
    alpha, n, C_b = tuning_param_wb(u_star, C, k)

    ## non-equilibrium from Elfouhaily et al. (1999)
    # dphi = phi_k - phi_w
    # dphi[ dphi < -np.pi ] = dphi[ dphi < -np.pi ] + np.pi * 2
    # PLD 2022/08/04 fixed wrapping of angles to make sure dphi is always betweem
    # -pi and pi
    deltaphi = np.angle(np.exp(1j * (phi_k - phi_w)))
    if fetch != 0:
        # FIXME: we use now an alternative spreading function to avoid discontinuities at the edges
        #S = np.where(k > 0, elfouhaily_spread(k, dphi, u_10, fetch) * elfouhaily(k, u_10, fetch) / k, 0)
        S = np.where(k > 0, DandP_spread(k, deltaphi, u_10, fetch) * elfouhaily(k, u_10, fetch) / k, 0)

    B_neq = k ** 4 * S
    if k_cut == None:
        f = phi_func((k / (10 * k_p)) ** 2)
    else:
        if 10 * k_p > k_cut:
            f = phi_func((k / (10 * k_p)) ** 2)
        else:
            f = phi_func((k / k_cut) ** 2)
    # wind wave growth rate # taken as eq. 17 of Kudry et al. (2005)
    I = k > 0
    beta = np.zeros(k.shape)
    beta_v = np.zeros(k.shape)
    beta[I] = C_b[I] * (u_star / C[I]) ** 2 * np.cos(phi_k[I] - phi_w) * np.absolute(
        np.cos(phi_k[I] - phi_w))
    beta_v[I] = beta[I] - 4 * co.nu * k[I] ** 2 / omega_k[I]

    ## some initial values
    # equation 24, Kudry et al. (2005) reference spectrum
    I = np.logical_and(beta_v >= 0, k > 0)
    B_d = np.where(I, alpha * beta_v ** (1 / n), 0)
    B = (1 - f) * B_neq + f * B_d

    # based on KCM14, eq. A3
    # this is a bit annoying in a Cartesian system, limit k_m varies with k, so the integral changes
    # it should be similar to eq. 29 in Kudry2005
    Q_wb = integral_wb_polar(B, k_wb, C, beta, k_inv, k, dk, dphi)

    # estimate of spectrum in the cross direction, eq. 25, Kudry2005
    I = Q_wb > 0
    B_cr = np.where(I, alpha * (Q_wb / alpha) ** (1 / (n + 1)), 0)
    # estimate of spectrum in the up direction, eq. 26, Kudry2005
    I = k > 0
    B_up = np.where(I, np.absolute(-Q_wb / beta_v), 0)

    # initial values, Yurovskaya et al. (2013), eq. A9
    B_w = np.maximum(np.maximum(B_d, np.minimum(B_cr, B_up)), 0)

    # non-equilibrium low-frequencies from Elfouhaily
    B = (1 - f) * B_neq + f * B_w

    ## wind wave spectrum
    # this is based on the iteration system of eqs. A1, A10 in Yurovskaya et al. (2013)
    # should converge within a few steps
    count = 0
    while count < 5:
        count = count + 1

        # update energy source
        # based on KCM14, eq. A3
        Q_wb = integral_wb_polar(B, k_wb, C, beta, k_inv, k, dk, dphi)

        # update energy balance
        Q = beta_v * B_w - B_w * (B_w / alpha) ** n + Q_wb
        dQ = beta_v - (n + 1) * (B_w / alpha) ** n

        # update spectrum
        Bupd_w = Q / dQ
        # FIXME: some things are dirty here
        I_lim = np.absolute(Bupd_w) > 0.001  # some hack not to let it blow up
        Bupd_w[I_lim] = np.sign(Bupd_w[I_lim]) * B_w[I_lim] / 10  # some hack not to let it blow up
        B_w = B_w - Bupd_w
        B_w[B_w < 0] = 0

        # use cut-off for non-equilibrium part
        B = (1 - f) * B_neq + f * B_w

        # from matplotlib import pyplot as plt
        # plt.imshow( B , origin = 'lower')
        # plt.colorbar()
        # plt.show()

    ## capillary wave spectrum
    # we need some interpolation here
    # based on the appendix of KCM14
    k_b = k_gamma ** 2 * k_inv

    # This dirty interpolation can be cleaned up
    # FIXME: we can remove a for loop here
    # FIXME: I think the energy goes now both ways, even though there is not much energy is the parasitics
    Q_pc = np.zeros(k.shape)  # Note that in KMC14 they use Q_pc, but it is I_pc in Kudry2005
    for i in range(0, len(phi_k[:, 0])):
        for j in range(0, len(k[0, :])):
            if k_b[i, j] < 3 * k_gamma:  # This '3' is arbitrarily set
                q1 = np.argmin(np.absolute(k[i, :] - k_b[i, j]))
                Q_pc[i, j] = B_w[i, q1] * beta[i, q1]

    # filter function
    k_l = 3 / 2 * k_gamma
    k_h = k_gamma ** 2 / (co.d * k_gamma)
    pf = phi_func((k / k_l) ** 2) - phi_func((k / k_h) ** 2)
    Q_pc = Q_pc * pf

    # parasitic capillaries
    B_pc = alpha / 2 * (
            -4 * co.nu * k ** 2 / omega_k + np.sqrt((4 * co.nu * k ** 2 / omega_k) ** 2 + 4 * Q_pc / alpha))
    # FIXME: we have to check this little issue, sometimes the argument in the square-root becomes negative
    B_pc[B_pc != B_pc] = 0
    B = (1 - f) * B_neq + f * (B_w + B_pc)
    B[k == 0] = 0
    # FIXME: negative B's occur in the opposite direction as the wind
    B[B < 0] = 0

    # from matplotlib import pyplot as plt
    # plt.plot(k[500,500:],B[500,500:])
    # plt.plot( k[ 500, 500: ], B_w[ 500, 500: ] )
    # plt.xlim([1E1,1E4])
    # plt.ylim( [ 1E-4, 1E-2 ] )
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.show()

    return B, B_neq, B_w, B_pc

# Kudry et al. (2005) spectrum
# FIXME: there is an anomaly is S at low wave numbers in the upwind direction
# FIXME: possibly related to combination of B's in bottom of the code
# FIXME: there is a 'disconuity' caused by the combination of B's
def Kudry_spec(kx, ky, u_10, fetch, phi_w, dks, S=0, k_cut=None):
    # kx,ky [rad/m]: two-dimension wave numbers
    # u_10 [m/s]: wind speed
    # fetch [m]: fetch length for the non-equilibrium part of the spectrum
    # phi_w [rad]: wind direction
    # dks [(rad/m)^2]: two-dimensional grid resolution
    # S: Cartesian long-wave spectrum (non-equilibrium waves), optional: if set, set fetch=0
    # if you set fetch=0, we take the non-equilibrium spectrum S from the input

    # let's ignore the log(0) and 1/0 errors (they will be handled properly)
    import warnings
    warnings.simplefilter(action="ignore", category=RuntimeWarning)

    # conversion of angles
    # phi_w = np.deg2rad( phi_w )

    # wave numbers
    k = np.sqrt(kx ** 2 + ky ** 2)
    phi_k = np.arctan2(ky, kx)  # wave directions
    I = k > 0
    k_inv = np.where(I, 1 / k, 0)
    C = np.where(I, np.sqrt(g * k_inv + co.gamma * k / co.rho_w), 0)  # phase speed
    omega_k = np.where(I, np.sqrt(g * k + co.gamma * k ** 3 / co.rho_w), 0)  # angular velocity

    ## some required paramaters
    if fetch != 0:
        k_p = spec_peak(u_10, fetch)
    if fetch == 0:
        I_kp = np.argmax(S)
        k_p = np.sqrt(kx.ravel()[I_kp] ** 2 + ky.ravel()[I_kp] ** 2)
    k_wb = 2 * np.pi / 0.3
    k_gamma = np.sqrt(co.g / co.gamma * co.rho_w)
    u_star = u_10 * np.sqrt((0.8 + 0.065 * u_10) * 1e-3)
    alpha, n, C_b = tuning_param_wb(u_star, C, k)

    ## non-equilibrium from Elfouhaily et al. (1999)
    # dphi = phi_k - phi_w
    # dphi[ dphi < -np.pi ] = dphi[ dphi < -np.pi ] + np.pi * 2
    # PLD 2022/08/04 fixed wrapping of angles to make sure dphi is always betweem
    # -pi and pi
    dphi = np.angle(np.exp(1j * (phi_k - phi_w)))
    if fetch != 0:
        # FIXME: we use now an alternative spreading function to avoid discontinuities at the edges
        #S = np.where(k > 0, elfouhaily_spread(k, dphi, u_10, fetch) * elfouhaily(k, u_10, fetch) / k, 0)
        S = np.where(k > 0, DandP_spread(k, dphi, u_10, fetch) * elfouhaily(k, u_10, fetch) / k, 0)

    B_neq = k ** 4 * S
    if k_cut == None:
        f = phi_func((k / (10 * k_p)) ** 2)
    else:
        if 10 * k_p > k_cut:
            f = phi_func((k / (10 * k_p)) ** 2)
        else:
            f = phi_func((k / k_cut) ** 2)

    # wind wave growth rate # taken as eq. 17 of Kudry et al. (2005)
    I = k > 0
    beta = np.zeros(k.shape)
    beta_v = np.zeros(k.shape)
    beta[I] = C_b[I] * (u_star / C[I]) ** 2 * np.cos(phi_k[I] - phi_w) * np.absolute(
        np.cos(phi_k[I] - phi_w))
    beta_v[I] = beta[I] - 4 * co.nu * k[I] ** 2 / omega_k[I]

    ## some initial values
    # equation 24, Kudry et al. (2005) reference spectrum
    I = np.logical_and(beta_v >= 0, k > 0)
    B_d = np.where(I, alpha * beta_v ** (1 / n), 0)
    B = (1 - f) * B_neq + f * B_d
    #print(np.sum(B*dks))


    # based on KCM14, eq. A3
    # this is a bit annoying in a Cartesian system, limit k_m varies with k, so the integral changes
    # it should be similar to eq. 29 in Kudry2005
    Q_wb = integral_wb(B, k_wb, C, beta, k_inv, dks, k)

    # estimate of spectrum in the cross direction, eq. 25, Kudry2005
    I = Q_wb > 0
    B_cr = np.where(I, alpha * (Q_wb / alpha) ** (1 / (n + 1)), 0)
    # estimate of spectrum in the up direction, eq. 26, Kudry2005
    I = k > 0
    B_up = np.where(I, np.absolute(-Q_wb / beta_v), 0)

    # initial values, Yurovskaya et al. (2013), eq. A9
    B_w = np.maximum(np.maximum(B_d, np.minimum(B_cr, B_up)), 0)

    # non-equilibrium low-frequencies from Elfouhaily
    B = (1 - f) * B_neq + f * B_w

    ## wind wave spectrum
    # this is based on the iteration system of eqs. A1, A10 in Yurovskaya et al. (2013)
    # should converge within a few steps
    count = 0
    while count < 5:
        count = count + 1

        # update energy source
        # based on KCM14, eq. A3
        Q_wb = integral_wb(B, k_wb, C, beta, k_inv, dks, k)

        # update energy balance
        Q = beta_v * B_w - B_w * (B_w / alpha) ** n + Q_wb
        dQ = beta_v - (n + 1) * (B_w / alpha) ** n

        # update spectrum
        Bupd_w = Q / dQ
        #FIXME: some things are dirty here
        I_lim = np.absolute(Bupd_w) > 0.001  # some hack not to let it blow up
        Bupd_w[I_lim] = np.sign(Bupd_w[I_lim]) * B_w[I_lim] / 10  # some hack not to let it blow up
        B_w = B_w - Bupd_w
        B_w[B_w < 0] = 0

        # use cut-off for non-equilibrium part
        B = (1 - f) * B_neq + f * B_w

        # from matplotlib import pyplot as plt
        # plt.imshow( B , origin = 'lower')
        # plt.colorbar()
        # plt.show()

    ## capillary wave spectrum
    # we need some interpolation here
    # based on the appendix of KCM14
    k_b = k_gamma ** 2 * k_inv
    kx_b = k_b * np.cos(phi_k)
    ky_b = k_b * np.sin(phi_k)

    # This dirty interpolation can be cleaned up
    # FIXME: I think the energy goes now both ways, even though there is not much energy is the parasitics
    Q_pc = np.zeros(k.shape)  # Note that in KMC14 they use Q_pc, but it is I_pc in Kudry2005
    for i in range(0, len(kx_b[0, :])):
        for j in range(0, len(ky_b[:, 0])):
            if k[j, i] != 0 and k_b[j, i] < 3 * k_gamma:  # This '3' is arbitrarily set
                q1 = np.argmin(np.absolute(kx[0, :] - kx_b[j, i]))
                q2 = np.argmin(np.absolute(ky[:, 0] - ky_b[j, i]))
                Q_pc[j, i] = B_w[q2, q1] * beta[q2, q1]

    # filter function
    k_l = 3 / 2 * k_gamma
    k_h = k_gamma ** 2 / (co.d * k_gamma)
    pf = phi_func((k / k_l) ** 2) - phi_func((k / k_h) ** 2)
    Q_pc = Q_pc * pf

    # parasitic capillaries
    B_pc = alpha / 2 * (
            -4 * co.nu * k ** 2 / omega_k + np.sqrt((4 * co.nu * k ** 2 / omega_k) ** 2 + 4 * Q_pc / alpha))
    # FIXME: we have to check this little issue, sometimes the argument in the square-root becomes negative
    B_pc[B_pc != B_pc] = 0
    B = (1 - f) * B_neq + f * (B_w + B_pc)
    B[k == 0] = 0
    # FIXME: negative B's occur in the opposite direction as the wind
    B[B < 0] = 0

    # from matplotlib import pyplot as plt
    # plt.plot(k[500,500:],B[500,500:])
    # plt.plot( k[ 500, 500: ], B_w[ 500, 500: ] )
    # plt.xlim([1E1,1E4])
    # plt.ylim( [ 1E-4, 1E-2 ] )
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.show()

    return B, B_neq, B_w + B_pc, Q_wb + Q_pc


# this is based on Yuroskaya et al. (2013) and KCM14, and should resemble eq. 20 of Kudry2005
def integral_wb(B, k_wb, C, beta, k_inv, dks, k):
    # let's evaluate the integral in the relevant range
    # in this interval the integral varies
    k_int = np.linspace(np.min(k[k > 0]) * 10, k_wb * 10, 20, endpoint=True)
    k_m = k_int / 10  # for each k_int a limit for the integral

    # integrals for each k_int and fit it
    integ = np.zeros(len(k_int))
    for i in range(0, len(k_int)):
        I = np.logical_and(k > 0, k < k_m[i])
        # this function is a combination of eq. 16 and A2
        # (replace Lambda by beta*B*k_inv, the alpha will be captured later in the c_b_w)
        integ[i] = np.sum(C[I] * beta[I] * B[I] * k_inv[I] ** 2 * dks[I])
    poly = np.polyfit(k_int, integ, 5) # to smooth the discrete nature

    # for each k in the Cartesian system kx, ky, we need the integral
    # above k_wb*10 the integral is constant
    I = np.logical_and(k > 0, k < k_wb)
    integ_2D = np.where(k > k_wb * 10, np.sum(C[I] * beta[I] * B[I] * k_inv[I] ** 2 * dks[I]), 0)

    # below k_wb*10 it varies
    I = np.logical_and(k > 0, k <= k_wb * 10)
    integ_2D[I] = np.polyval(poly, k[I])

    # energy
    Q_wb = np.where(k > 0, co.c_b_w * C ** -1 * integ_2D, 0)

    return Q_wb

# this is based on Yuroskaya et al. (2013) and KCM14, and should resemble eq. 20 of Kudry2005
def integral_wb_polar(B, k_wb, C, beta, k_inv, k, dk, dphi):
    # let's evaluate the integral in the relevant range
    # in this interval the integral varies
    k_int = np.linspace(np.min(k[k > 0]) * 10, k_wb * 10, 20, endpoint=True)
    k_m = k_int / 10  # for each k_int a limit for the integral

    # integrals for each k_int and fit it
    integ = np.zeros(len(k_int))
    for i in range(0, len(k_int)):
        I = np.logical_and(k > 0, k < k_m[i])
        # this function is a combination of eq. 16 and A2
        # (replace Lambda by beta*B*k_inv, the alpha will be captured later in the c_b_w)
        integ[i] = np.sum(C[I] * beta[I] * B[I] * k_inv[I] * dk[I] * dphi[I])
    poly = np.polyfit(k_int, integ, 5) # to smooth the discrete nature

    # for each k in the Cartesian system kx, ky, we need the integral
    # above k_wb*10 the integral is constant
    I = np.logical_and(k > 0, k < k_wb)
    integ_2D = np.where(k > k_wb * 10, np.sum(C[I] * beta[I] * B[I] * k_inv[I] * dk[I] * dphi[I]), 0)

    # below k_wb*10 it varies
    I = np.logical_and(k > 0, k <= k_wb * 10)
    integ_2D[I] = np.polyval(poly, k[I])

    # energy
    Q_wb = np.where(k > 0, co.c_b_w * C ** -1 * integ_2D, 0)

    return Q_wb

# based on A10 in Kydry et al. (2014)
def phi_func(x):
    f = x ** 4 / (1 + x ** 4)
    return f


# based on Kudry et al. (2003) eqs. 19-28
def tuning_param_wb(u_star, C, k):
    # inverse k
    I = k > 0
    k_inv = np.where(I, 1 / k, 0)

    # filter function
    k_gamma = np.sqrt(g * co.rho_w / co.gamma)  # wave number of minimum phase velocity (from Elfouhaily et al. 1997)
    k_b = 1 / 4 * k_gamma
    f = np.zeros(k.shape)
    #f[I] = (1 + np.tanh(2 * (np.log(k[I]) - np.log(k_b)))) / 2
    f[I] = phi_func(k[I]/k_b)

    # tuning parameter n
    n = np.zeros(k.shape)
    n[I] = 1 / ((1 - 1 / co.n_g) * f[I] + 1 / co.n_g)

    # roughness scale Kudry et al. (2003) eq. 21
    z0 = co.a_star * u_star ** 2 / g + co.a_v * co.nu_a / u_star

    # growth parameter (below eq. 17, Kydry et al. 2005 and eq. 19 in 2003)
    C_b = np.zeros(k.shape)
    C_b[I] = 1.5 * co.rho_a / co.rho_w * (1 / co.Kappa * np.log(np.pi * k_inv[I] / z0) - C[I] / u_star)
    # C_b[ C_b < 0 ] = 0

    # tuning parameter alpha
    alpha = np.zeros(k.shape)
    alpha[I] = np.exp(np.log(co.a) - np.log(co.Cm_b) / n[I])

    return alpha, n, C_b


# merge long-wave spectrum with short-wave spectrum (assumption is that they are on the same grid)
# not checked yet, but should work fine
def merge_spectra(B_lw, B_sw, k_x, k_y, k_l):
    # B_lw: long-wave curvature spectrum
    # B_sh: short-wave curvature spectrum
    # k_x,k_y: two-dimensional grid of wave numbers
    # k_l: separating wave number for merging lw,sw
    # merge spectra
    k = np.sqrt(k_x ** 2 + k_y ** 2)
    f = phi_func((k / k_l) ** 2)  # I want to have multiple phi-functions, this one rolls off very fast
    B = (1 - f) * B_lw + f * B_sw

    # returns merged spectrum
    return B


def merge_spectra_polar(B_lw, B_sw, k, phi, k_l):
    '''

    Parameters
    ----------
    B_lw: long-wave curvature
    B_sw: short-wave curvature
    k: wave number vector (1D)
    phi: wave direction (1D)
    k_l: wave number limit

    Returns
    -------

    '''
    k, phi = np.meshgrid(k, phi)
    f = phi_func((k / k_l) ** 2)  # I want to have multiple phi-functions, this one rolls off very fast
    B = (1 - f) * B_lw + f * B_sw

    # returns merged spectrum
    return B

######################### JONSWAP ########################
# Based on Jocelyn Frechot (2006). Realistic simulation of ocean surface using wave spectra (not checked, be careful)
'''
def jonswap_frechot( k, phi, omega_p, phi_w, alpha = 0.0081, gamma = 3.3 ):
    # Input:
    # k [rad/m]: two-dimensional wave numbers (from Cartesian grid)
    # phi [rad]: two-dimensional direction grid
    # omega_p [rad/s]: peak angular frequency
    # phi_w [rad]: wave system mean direction
    # gamma: peak enhancement factor

    # some parameters
    g = 9.81
    omega = np.sqrt( k * g )
    sigma = np.ones( k.shape ) * 0.07
    sigma[ omega > omega_p ] = 0.09
    mu = np.ones( k.shape ) * 5
    mu[ omega > omega_p ] = -2.5
    U10 = 0.855 * g / omega_p  # below equation 21 for input into the equation for 's'
    s = 11.5 * (g / omega_p / U10) ** 2.5 * (omega / omega_p) ** mu

    ## jonswap spectrum
    Sp = alpha * g ** 2 / omega ** 5
    Spm = Sp * np.exp( -5 / 4 * (omega_p / omega) ** 4 )
    r = np.exp( -(omega - omega_p) ** 2 / (2 * sigma ** 2 * omega_p ** 2) )
    Sj = Spm * gamma ** r

    # go to wave number
    Sk = 1 / 2 * np.sqrt( g / k ) * Sj

    ## spread
    N = 1 / 2 / np.sqrt( np.pi ) * sp.special.gamma( s + 1 ) / sp.special.gamma( s + 0.5 )
    dphi = (phi_w - phi + np.pi) % (2 * np.pi) - np.pi  # including unwrapping
    D = N * np.cos( (dphi) / 2 ) ** (2 * s)

    ## two-dimensional Cartesian spectrum
    S = Sk * D / k

    return S
'''


# another JONSWAP, so that we can input Hs, phi, omega_p
# outputs on a Cartesian grid
def jonswap_hs(k, phi, omega_p, phi_p, Hs, dks, gamma=3.3, phi_w=None, k_w=2 * np.pi / 5):
    """

    Parameters
    ----------
    k [rad/m]: two-dimensional wave numbers (from Cartesian grid)
    phi [rad]: two-dimensional direction grid
    omega_p [rad/s]: peak angular frequency
    phi_p [rad]: peak wave direction
    Hs [m]: significant wave height
    dks [(rad/m)^2]: two-dimensional Cartesian grid spacing
    gamma: peak enhancement factor
    phi_w: wind direction (set only if you want a 'curving' spectrum)
    k_w:

    Returns
    -------
    S: wind-wave spectrum
    """

    # some parameters
    g = 9.81
    k_p = omega_p ** 2 / g
    omega = np.sqrt(g * k)
    sigma = np.ones(k.shape) * 0.07
    sigma[omega > omega_p] = 0.09
    mu = np.ones(k.shape) * 5
    mu[omega > omega_p] = -2.5

    # 'one-dimensional' spectrum (Brettschneider1959, Hasselmann1973, OchiHubble1976)
    # FIXME: check normalization with peak_enh (we now simply normalize by a scaling in the last line of this script)
    peak_enh = gamma ** (np.exp(-(omega - omega_p) ** 2 / (2 * sigma ** 2 * omega_p ** 2)))
    S_omega = 5 / 16 * Hs ** 2 * omega_p ** 4 / omega ** 5 * np.exp(-5 / 4 * (omega_p / omega) ** 4) * peak_enh

    # scaling from 'omega' to 'k' (Frechot2006)
    S_k = np.where(k != 0, 1 / 2 * np.sqrt(g / k) * S_omega, 0)

    # spread parameter (Frechot2006, Mitsuayasu1975)
    u = 0.855 * g / omega_p
    s = 11.5 * (g / (omega_p * u)) ** 2.5 * (omega / omega_p) ** mu
    s[omega / omega_p < 1] = 11.5 * (g / (omega_p * u)) ** 2.5

    # spread (Longuet-Higgins 1963) with some curving trick
    phi_d = phi_p * np.ones(k.shape)  # wave direction
    if phi_w != None:  # this introduces the curving
        phi_d = np.where(k >= k_p, np.angle(
            np.exp(1j * (phi_p)) * (1 - (k - k_p) / (k_w - k_p)) + np.exp(1j * (phi_w)) * (k - k_p) / (k_w - k_p)),
                         phi_p)
    N = 1 / 2 / np.sqrt(np.pi) * sp.special.gamma(s + 1) / sp.special.gamma(s + 0.5)
    dphi = np.angle(np.exp(1j * (phi_d - phi)))  # including unwrapping
    D = N * np.cos(dphi / 2) ** (2 * s)

    # takes into account scaling to two-dimensional Cartesian (1/k)
    S = S_k * D / k
    # from matplotlib import pyplot as plt
    # from pylab import figure, cm
    # cmap2 = cm.get_cmap('plasma', 15)
    # plt.figure(figsize=(10,10))
    # plt.imshow(np.log10(np.fft.fftshift(S_k * D)),origin='lower',cmap=cmap2, vmin=-10)
    # plt.colorbar()
    # plt.show()

    # normalization
    # print(np.sum(S[S==S]*dks),(Hs ** 2 / 16 )) # Check Torsethaugen1993
    S = S * (Hs ** 2 / 16) / np.sum(S[S == S] * dks)

    return S


if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt

    u10=5
    fetch=300E3
    print(2*np.pi/spec_peak(u10, fetch))

    k_m = 2 * np.pi / 0.017
    # Eq. 3 (below)
    k_0 = g / u10 ** 2
    # Eq. 4 (below)
    X = k_0 * fetch
    # Eq. 37: Inverse wave age
    Omega_c = 0.84 * np.tanh((X / X_0) ** (0.4)) ** (-0.75)
    print(Omega_c)
    '''
    # wavelengths and wave numbers
    g = 9.81
    n_k = 100  # number of frequencies single side (total 2*n_k - 1)
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

    u_10 = 10
    fetch = 200E3
    phi_w = 90
    Bk, B_lw, B_sw, _ = Kudry_spec(k_x, k_y, u_10, fetch, np.deg2rad(phi_w), dks)
    Sk = np.where(k > 0, Bk * k ** -4, 0)

    dphi = np.angle(np.exp(1j * (phi - np.deg2rad(phi_w))))
    Se = np.where(k > 0, elfouhaily_spread(k, dphi, u_10, fetch) * elfouhaily(k, u_10, fetch) / k, 0)
    Be = k ** 4 * Se
    # print(np.sum(Se*dks))

    # Se2 = np.where(k > 0, elfouhaily_spread(k, dphi, u_10, fetch, dtheta=0.01) * elfouhaily(k, u_10, fetch) / k, 0)
    Se2 = np.where(k > 0, DandP_spread(k, dphi, u_10, fetch) * elfouhaily(k, u_10, fetch) / k, 0)
    Be2 = k ** 4 * Se2
    # print(np.sum(Se2 * dks))
    D=DandP_spread(k, dphi, u_10, fetch)
    # plt.figure(figsize=(15, 5))
    # plt.subplot(1, 3, 1)
    # plt.imshow(dphi, origin='lower', vmin=-np.pi, vmax=np.pi,cmap='hsv')
    # plt.colorbar()
    # plt.show()

    plt.figure(figsize=(15, 5))
    plt.subplot(1,3,1)
    plt.imshow(np.log10(Bk),origin='lower',vmin=-5, vmax=-2)
    plt.colorbar()
    plt.subplot(1, 3, 2)
    plt.imshow(np.log10(Be), origin='lower', vmin=-5, vmax=-2)
    plt.colorbar()
    plt.subplot(1, 3, 3)
    plt.imshow(np.log10(Be2), origin='lower', vmin=-5, vmax=-2)
    plt.colorbar()
    plt.show()

    # plt.plot(B[:,250])
    # plt.show()

    
    Nr = 128
    Nd = 72
    r0 = 800
    r1 = 5
    k0 = 2 * np.pi / r1
    k1 = 2 * np.pi / r0
    ## Evenly spaced wavenumber in log scale
    drho = np.log( 2 * np.pi / (k0 * r0) ) / (Nr - 1)
    ## define k as row vector
    k = np.reshape( k0 * np.exp( drho * np.arange( Nr ) ), (1, Nr) )
    r = np.reshape( r0 * np.exp( drho * np.arange( Nr ) ), (1, Nr) )
    d = np.reshape( np.arange( Nd ) * (2 * np.pi / Nd), (Nd, 1) )
    for u in np.arange( 6, 15, 2 ):
        wspec = wavespec( k, d, u, 0, iwa = 0.84 )
        wspec[ wspec < 0 ] = 0
        enn = np.ones( (Nd, 1), dtype = np.double )
        wspec = wspec * np.dot( enn, k ** (-4) )
        plt.loglog( k[ 0, : ], np.sum( wspec, axis = 0 ) );
        plt.grid();
        plt.ylim( [ 1e-5, 1e5 ] );
        plt.show()
    '''
