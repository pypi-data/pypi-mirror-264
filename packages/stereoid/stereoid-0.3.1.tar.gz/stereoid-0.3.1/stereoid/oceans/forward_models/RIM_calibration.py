######################## Kudryavtsev et al. (2005) #########################

# some constantsimport warnings
import numpy as np
from scipy.constants import g
import stereoid.oceans.waves.wave_spectra as wave_spectra
import stereoid.oceans.forward_models.backscatter as backscatter
from stereoid.oceans.forward_models.RIM_constants import constants as co


# Kudry et al. (2005) spectrum
# FIXME: there is an anomaly is S at low wave numbers in the upwind direction
# FIXME: possibly related to combination of B's in bottom of the code
# FIXME: there is a 'discontinuuity' caused by the combination of B's
def Kudry_spec( kx, ky, u_10, fetch, phi_w, dks , n_g, a, Cm_b):
    # constants that we vary
    # n_g
    # a
    # Cm_b

    # let's ignore the log(0) and 1/0 errors (they will be handled properly)
    import warnings
    warnings.simplefilter( action = "ignore", category = RuntimeWarning )

    # conversion of angles
    phi_w = np.deg2rad( phi_w )

    # wave numbers
    k = np.sqrt( kx ** 2 + ky ** 2 )
    phi_k = np.arctan2( ky, kx )  # wave directions
    I = k > 0
    k_inv = np.where( I, 1 / k, 0 )
    C = np.where( I, np.sqrt( g * k_inv + co.gamma * k / co.rho_w ), 0 )  # phase speed
    omega_k = np.where( I, np.sqrt( g * k + co.gamma * k ** 3 / co.rho_w ), 0 )  # angular velocity

    ## some required paramaters
    k_p = wave_spectra.spec_peak( u_10, fetch )
    k_wb = 2 * np.pi / 0.3
    k_gamma = np.sqrt( co.g / co.gamma * co.rho_w )
    u_star = u_10 * np.sqrt( (0.8 + 0.065 * u_10) * 1e-3 )
    alpha, n, C_b = tuning_param_wb( u_star, C, k, n_g, a, Cm_b)

    ## non-equilibrium from Elfouhaily et al. (1999)
    dphi = phi_k - phi_w
    dphi[ dphi < -np.pi ] = dphi[ dphi < -np.pi ] + np.pi * 2
    S = np.where( k > 0, wave_spectra.elfouhaily_spread( k, dphi, u_10, fetch ) * wave_spectra.elfouhaily( k, u_10, fetch ) / k, 0 )
    B_neq = k ** 4 * S
    # FIXME: I changed this function, check what the difference is (also, is k_p the correct limit or 10*k_p)
    f = wave_spectra.phi_func( (k / (10 * k_p)) ** 2 )  # np.where( k > 0, (1 + np.tanh( 2 * (np.log( k ) - np.log( k_p )) )) / 2, 0 )

    # wind wave growth rate # taken as eq. 17 of Kudry et al. (2005)
    I = k > 0
    beta = np.zeros( k.shape )
    beta_v = np.zeros( k.shape )
    beta[ I ] = C_b[ I ] * (u_star / C[ I ]) ** 2 * np.cos( phi_k[ I ] - phi_w ) * np.absolute(
        np.cos( phi_k[ I ] - phi_w ) )
    beta_v[ I ] = beta[ I ] - 4 * co.nu * k[ I ] ** 2 / omega_k[ I ]

    ## some initial values
    # equation 24, Kudry et al. (2005) reference spectrum
    I = np.logical_and( beta_v >= 0, k > 0 )
    B_d = np.where( I, alpha * beta_v ** (1 / n), 0 )
    B = (1 - f) * B_neq + f * B_d

    # based on KCM14, eq. A3
    # this is a bit annoying in a Cartesian system, limit k_m varies with k, so the integral changes
    # it should be similar to eq. 29 in Kudry2005
    Q_wb = wave_spectra.integral_wb( B, k_wb, C, beta, k_inv, dks, k )

    # estimate of spectrum in the cross direction, eq. 25, Kudry2005
    I = Q_wb > 0
    B_cr = np.where( I, alpha * (Q_wb / alpha) ** (1 / (n + 1)), 0 )
    # estimate of spectrum in the up direction, eq. 26, Kudry2005
    I = k > 0
    B_up = np.where( I, np.absolute( -Q_wb / beta_v ), 0 )

    # initial values, Yurovskaya et al. (2013), eq. A9
    B_w = np.maximum( np.maximum( B_d, np.minimum( B_cr, B_up ) ), 0 )

    # non-equilibrium low-frequencies from Elfouhaily
    B = (1 - f) * B_neq + f * B_w

    ## wind wave spectrum
    # this is based on the iteration system of eqs. A1, A10 in Yurovskaya et al. (2013)
    count = 0
    while count < 5:
        count = count + 1

        # update energy source
        # based on KCM14, eq. A3
        Q_wb = wave_spectra.integral_wb( B, k_wb, C, beta, k_inv, dks, k )

        # update energy balance
        Q = beta_v * B_w - B_w * (B_w / alpha) ** n + Q_wb
        dQ = beta_v - (n + 1) * (B_w / alpha) ** n

        # update spectrum
        Bupd_w = Q / dQ
        I_lim = np.absolute( Bupd_w ) > 0.001  # some hack not to let it blow up
        Bupd_w[ I_lim ] = np.sign( Bupd_w[ I_lim ] ) * B_w[ I_lim ] / 10
        B_w = B_w - Bupd_w
        B_w[ B_w < 0 ] = 0

        # use cut-off for non-equilibrium part
        B = (1 - f) * B_neq + f * B_w

    ## capillary wave spectrum
    # we need some interpolation here
    # based on the appendix of KCM14
    k_b = k_gamma ** 2 * k_inv
    kx_b = k_b * np.cos( phi_k )
    ky_b = k_b * np.sin( phi_k )

    # This dirty interpolation can be cleaned up
    Q_pc = np.zeros( k.shape ) # Note that in KMC14 they use Q_pc, but it is I_pc in Kudry2005
    for i in range( 0, len( kx_b[ 0, : ] ) ):
        for j in range( 0, len( ky_b[ :, 0 ] ) ):
            if k[ j, i ] != 0 and k_b[ j, i ] < 3 * k_gamma: # This '3' is arbitrarily set
                q1 = np.argmin( np.absolute( kx[ 0, : ] - kx_b[ j, i ] ) )
                q2 = np.argmin( np.absolute( ky[ :, 0 ] - ky_b[ j, i ] ) )
                Q_pc[ j, i ] = B_w[ q2, q1 ] * beta[ q2, q1 ]

    # filter function
    k_l = 3 / 2 * k_gamma
    k_h = k_gamma ** 2 / (co.d * k_gamma)
    pf = wave_spectra.phi_func( (k / k_l) ** 2 ) - wave_spectra.phi_func( (k / k_h) ** 2 )
    Q_pc = Q_pc * pf

    # parasitic capillaries
    B_pc = alpha / 2 * (
            -4 * co.nu * k ** 2 / omega_k + np.sqrt( (4 * co.nu * k ** 2 / omega_k) ** 2 + 4 * Q_pc / alpha ))
    # FIXME: we have to check this little issue, sometimes the argument in the square-root becomes negative
    B_pc[ B_pc != B_pc ] = 0
    B = (1 - f) * B_neq + f * (B_w + B_pc)
    B[ k == 0 ] = 0

    return B, B_neq, (B_w + B_pc), Q_wb+Q_pc

# based on Kudry et al. (2003) eqs. 19-28
def tuning_param_wb( u_star, C, k, n_g, a, Cm_b):
    # variables that we vary
    # n_g
    # a
    # Cm_b

    # inverse k
    I = k > 0
    k_inv = np.where( I, 1 / k, 0 )

    # filter function
    k_gamma = np.sqrt( g * co.rho_w / co.gamma )  # wave number of minimum phase velocity (from Elfouhaily et al. 1997)
    k_b = 1 / 4 * k_gamma
    f = np.zeros( k.shape )
    f[ I ] = (1 + np.tanh( 2 * (np.log( k[ I ] ) - np.log( k_b )) )) / 2

    # tuning parameter n
    n = np.zeros( k.shape )
    n[ I ] = 1 / ((1 - 1 / n_g) * f[ I ] + 1 / n_g)

    # roughness scale Kudry et al. (2003) eq. 21
    z0 = co.a_star * u_star ** 2 / g + co.a_v * co.nu_a / u_star

    # growth parameter (below eq. 17, Kydry et al. 2005 and eq. 19 in 2003)
    C_b = np.zeros( k.shape )
    C_b[ I ] = 1.5 * co.rho_a / co.rho_w * (1 / co.Kappa * np.log( np.pi * k_inv[ I ] / z0 ) - C[ I ] / u_star)
    #C_b[ C_b < 0 ] = 0  # this is only in or close to the non-equilibrium part

    # tuning parameter alpha
    alpha = np.zeros( k.shape )
    alpha[ I ] = np.exp( np.log( a ) - np.log( Cm_b ) / n[ I ] )

    return alpha, n, C_b

# Kudryavtsev et al. (2005) backscatter
# for a bistatic system, a polarization rotation is required for each scattering mechanism 'backscatter_Kudry2005'
# for bi-static variants, rotate the input spectrum and wind speed by -alpha/2 or alpha/2
def backscatter_Kudry2005( S, kx, ky, dks, phi_w, n_g, a, c_q, theta_wb, s_wb, eps_wb, Cm_b, eps_w, theta = 35, alpha = 0, pol = 'V', u_10 = 10, k_r = 0 ):
    # S: long-wave two-dimensional spectrum
    # kx,ky: wave numbers
    # dks: two-dimensional wave number resolution of the spectrum
    # theta: incidence angle [deg]
    # pol: transmit polarization
    # u_10: wind speed
    # phi_w: wave direction with respect to the radar [deg]
    # k_r: radar wave length [m]
    # alpha: bistatic angle [deg]

    # constants that we vary
    # n_g
    # a
    # c_q
    # theta_wb
    # s_wb
    # eps_wb
    # Cm_b
    # eps_w

    # to radians
    theta = np.deg2rad( theta )
    phi_w = np.deg2rad( phi_w )
    alpha = np.deg2rad( alpha )
    u_star = u_10 * np.sqrt( (0.8 + 0.065 * u_10) * 1e-3 )

    # angular frequency and some conversions
    k = np.sqrt( kx ** 2 + ky ** 2 )
    k_inv = 1 / k
    k_inv[ 0, 0 ] = 0
    C = np.sqrt( co.g / k + co.gamma * k / co.rho_w )
    C[ 0, 0 ] = 0  # phase velocity
    phi_k = np.arctan2( ky, kx )  # wave directions

    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length (this should be picked up from the Harmony cards)
        k_r = 2 * np.pi / la_r  # radar wave number
    if alpha != 0:
        k_r = k_r * np.cos( alpha / 2 )

    k_d = co.d * k_r
    k_wb = 2 * np.pi / 0.3  # Kudry et al. 2005, above eq. 19
    k_wb_r = np.min( (co.b_r * k_r, k_wb) )

    # spectral conversions
    # we have to be careful, single sided B might be required
    B = k ** 4 * S  # saturation spectrum
    B[ 0, 0 ] = 0

    #### specular reflection
    # large-scale wave mss  # limits for integration not needed if we input S(k < k_d)
    s_i = np.sqrt(
        np.sum( k[ k < k_d ] ** 2 * np.cos( phi_k[ k < k_d ] ) ** 2 * S[ k < k_d ] * dks[ k < k_d ] ) )
    s_ci = np.sqrt(
        np.sum( k[ k < k_d ] ** 2 * np.sin( phi_k[ k < k_d ] ) ** 2 * S[ k < k_d ] * dks[ k < k_d ] ) )

    # Fresnel coefficients at zero incidence angle (the exponential factor below eq. 5, Kudry2005)
    # FIXME: check if this is not double accounting
    h_s = np.sqrt( np.sum( S[ k > k_d ] * dks[ k > k_d ] ) )
    R = backscatter.Fresnel_coeff_normal( pol = pol, eps_w = eps_w ) * np.exp( -4 * k_r ** 2 * h_s ** 2 )

    # specular reflection (factor 2 missing in Kudry et al. (2005), compare with Yan Yuan and Kudry et al. (2003)
    s_spec = np.absolute( R ) ** 2 / (2 * np.cos( theta ) ** 4 * s_i * s_ci) * np.exp(
        -np.tan( theta ) ** 2 / (2 * s_i ** 2) )

    #### Bragg scattering
    # set of slopes, incidence angles and a new set of wave numbers for Bragg scattering
    # the probability density function for n
    s_br = np.sqrt( np.sum( np.cos( phi_k[ k < k_d ] ) ** 2 * k[ k < k_d ] ** 2 * S[ k < k_d ] * dks[ k < k_d ] ) )
    nk = 200  # hardcoded
    n = np.linspace( -5 * s_br, 5 * s_br, nk, endpoint = True )
    dn = n[ 1 ] - n[ 0 ]
    P = 1 / (np.sqrt( 2 * np.pi ) * s_br) * np.exp( -0.5 * n ** 2 / s_br ** 2 )

    # incidence angles and a new set of wave numbers for Bragg scattering
    theta_prime = theta - np.arctan( n )
    P = P[ np.absolute( theta_prime ) < np.pi / 2 ]  # angles larger than 90 degree cannot exist
    theta_prime = theta_prime[ np.absolute( theta_prime ) < np.pi / 2 ]
    k_b = 2 * k_r * np.sin( theta_prime )  # check this np.absolute()

    # reflection coefficients (for each local incidence angle)
    G = backscatter.scattering_coeff( theta_prime, pol = pol, eps_w=eps_w )

    # recompute the spectrum for the wave numbers k_b # this has to be fixed, it works with a double sided spectrum
    # FIXME: we assume the radar direction is 0, so we can simply interpolate at ky=0
    Sr_temp = 0.5 * S[ int( (len( ky ) - 1) / 2 ), : ] + 0.5 * np.flip( S[ int( (len( ky ) - 1) / 2 ), : ] )
    Sr_bragg = np.interp( k_b, kx[ int( (len( ky ) - 1) / 2 ), : ], Sr_temp )

    # compute bragg scattering for each wave number k_b, eq. 3, Kudry et al. (2005)
    s_bragg = 16 * np.pi * k_r ** 4 * np.absolute( G ) ** 2 * Sr_bragg

    # Bragg scattering (integrate over certain limits to exclude specular reflections)
    I_lim = 2 * k_r * np.sin( np.absolute( theta_prime ) ) >= k_d  # eq. 4, Kudry et al. (2005)
    s_bragg = np.sum( s_bragg[ I_lim ] * P[ I_lim ] * dn )  # eq. 3, Kudry et al. (2005)

    #### wave breaking
    # NRCS and tilting function
    dtheta = 1E-5  # equation 60, Kudry et al. (2003)
    # Note, below eq. 60 they make claims that the below is -3.4 an -8.8 at theta=40,45 deg, this is not exactly correct
    s_0wb = (1 / np.cos( theta )) ** 4 / s_wb ** 2 * np.exp(
        -np.tan( theta ) ** 2 / s_wb ** 2 ) + eps_wb / s_wb ** 2
    ds_0wb = (1 / np.cos( theta )) ** 4 / s_wb ** 2 * np.exp(
        -np.tan( theta + dtheta ) ** 2 / s_wb ** 2 ) + eps_wb / s_wb ** 2 - s_0wb
    M_wb = 1 / s_0wb * ds_0wb / dtheta

    # distribution of wave breakers
    # k_p = spec_peak( u_10, F )  # spectral peak
    alpha, n, C_b = tuning_param_wb( u_star, C, k, n_g, a, Cm_b)  # Yurovskaya et al. (2013)
    Lambda = k_inv / 2 * (B / alpha) ** (n + 1)

    # fraction of wave breakers
    # FIXME: check this, maybe the lowest k should be related to k_p (Lambda is only valid in the equilibrium range)
    I_lims = np.logical_and( k > 0, k < k_wb_r )
    Lambda_int = np.sum( Lambda[ I_lims ] * k_inv[ I_lims ] * dks[ I_lims ] )
    A_wb = np.sum( Lambda[ I_lims ] * k_inv[ I_lims ] * dks[ I_lims ] * np.cos( -phi_k[ I_lims ] ) ) / Lambda_int
    q = c_q * Lambda_int  # eq. 27 in Kudry et al. (2005) and eq. 56 in Kudry et al. (2003)

    # wave breaking backscatter
    s_break = s_0wb * (1 + M_wb * theta_wb * A_wb)

    return s_spec, s_bragg, s_break, q  # output: NRCS of specular reflection, Bragg scattering and wave breaking + fraction

if __name__ == "__main__":
    pass

