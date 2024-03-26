__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

from stereoid.tropical_cyclones.Deprecated.wave_spectra import tuning_param_wb
from stereoid.tropical_cyclones.Deprecated.wave_spectra import Kudry_spec
from stereoid.tropical_cyclones.Deprecated.wave_spectra import spec_peak
from stereoid.tropical_cyclones.Deprecated.constants import constants as co


# Kudryavtsev et al. (2005) backscatter
# for a bistatic system, a polarization rotation is required for each scattering mechanism 'backscatter_Kudry2005'
# for bi-static variants, rotate the input spectrum and wind speed by -alpha/2 or alpha/2
def backscatter_Kudry2005( S, kx, ky, dks, phi_w, theta = 35, alpha = 0, pol = 'V', u_10 = 10, k_r = 0 ):
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
    R = Fresnel_coeff_normal( pol = pol, eps_w = co.eps_w ) * np.exp( -4 * k_r ** 2 * h_s ** 2 )

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
    G = scattering_coeff( theta_prime, pol = pol )

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
    s_0wb = (1 / np.cos( theta )) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan( theta ) ** 2 / co.s_wb ** 2 ) + co.eps_wb / co.s_wb ** 2
    ds_0wb = (1 / np.cos( theta )) ** 4 / co.s_wb ** 2 * np.exp(
        -np.tan( theta + dtheta ) ** 2 / co.s_wb ** 2 ) + co.eps_wb / co.s_wb ** 2 - s_0wb
    M_wb = 1 / s_0wb * ds_0wb / dtheta

    # distribution of wave breakers
    # k_p = spec_peak( u_10, F )  # spectral peak
    alpha, n, C_b = tuning_param_wb( u_star, C, k )  # Yurovskaya et al. (2013)
    Lambda = k_inv / 2 * (B / alpha) ** (n + 1)

    # fraction of wave breakers
    # FIXME: check this, maybe the lowest k should be related to k_p (Lambda is only valid in the equilibrium range)
    I_lims = np.logical_and( k > 0, k < k_wb_r )
    Lambda_int = np.sum( Lambda[ I_lims ] * k_inv[ I_lims ] * dks[ I_lims ] )
    print(Lambda_int)
    A_wb = np.sum( Lambda[ I_lims ] * k_inv[ I_lims ] * dks[ I_lims ] * np.cos( -phi_k[ I_lims ] ) ) / Lambda_int
    q = co.c_q * Lambda_int  # eq. 27 in Kudry et al. (2005) and eq. 56 in Kudry et al. (2003)

    # wave breaking backscatter
    s_break = s_0wb * (1 + M_wb * co.theta_wb * A_wb)

    return s_spec, s_bragg, s_break, q  # output: NRCS of specular reflection, Bragg scattering and wave breaking + fraction


# this is based on Kudryavtsev et al. (2019)
def backscatter_crosspol( S, kx, ky, dks, theta = 35, alpha = 0, u_10 = 20, k_r = 0, fetch = 500E3 ):
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
    theta = np.deg2rad( theta )
    alpha = np.deg2rad( alpha )

    # angular frequency and some conversions
    k = np.sqrt( kx ** 2 + ky ** 2 )
    k_inv = 1 / k
    k_inv[ 0, 0 ] = 0
    C = np.sqrt( co.g / k + co.gamma * k / co.rho_w )
    C[ 0, 0 ] = 0  # phase velocity
    phi_k = np.arctan2( ky, kx )  # wave directions

    # radar wave length
    if k_r == 0:
        la_r = co.c / co.f_c  # radar wave length
        k_r = 2 * np.pi / la_r  # radar wave number
    if alpha != 0:
        k_r = k_r * np.cos( alpha / 2 )

    #### Bragg scattering
    # we have to check the 'absolute of Gpp-Gqq', in our function we already take G already absolute
    k_b = 2 * k_r * np.sin( theta )
    k_d = co.d * k_b  # this is for the Kudryavtsev 2019 equation for s_n
    # FIXME: I use the scattering coefficients from Kudry et al. (2019) here, this gives different results as 2003 or Plant
    Gvv = scattering_coeff_Kudry2019( theta, 'V' )
    Ghh = scattering_coeff_Kudry2019( theta, 'H' )
    k_p = spec_peak( u_10, fetch )
    Omega = u_10 * np.sqrt( k_p / co.g )
    s_n = np.sqrt( 0.5 * co.c_sn * np.log( Omega ** -2 * k_d * u_10 ** 2 / co.g ) )  # take half of A4
    # print(s_n)
    # print('check')
    # k_d = co.d * k_r # this is for the Kudryavtser 2005 equation for s_n
    # s_n = np.sqrt( np.sum( np.cos( phi_k[ k < k_d ] ) ** 2 * k[ k < k_d ] ** 2 * S[ k < k_d ] * dks[ k < k_d ] ) )
    # print( s_n )
    # FIXME: check this, in Kudry et al. (2005) double sided in (2019) not?
    Sr_temp = 0.5 * S[ int( (len( ky ) - 1) / 2 ), : ] + 0.5 * np.flip( S[ int( (len( ky ) - 1) / 2 ), : ] )
    S_r = np.interp( k_b, kx[ int( (len( ky ) - 1) / 2 ), : ], Sr_temp )
    B_r = S_r * k_r ** 4
    # eq. A1c, Kudry et al. (2019)
    s_bragg = np.pi * np.tan( theta ) ** -4 * np.absolute( Gvv - Ghh ) ** 2 * s_n ** 2 / np.sin( theta ) ** 2 * B_r
    #### wave breaking
    # eq. 11, Kudry et al. (2019)
    s_break = np.pi * np.absolute( Gvv - Ghh ) ** 2 / np.tan( theta ) ** 4 * co.s_wb ** 2 / (
            2 * np.sin( theta ) ** 2) * co.B_wb

    return s_bragg, s_break


# this is the one of plant (basically Kudry et al. (2019), but multiplied by cos(theta)**2
def scattering_coeff( theta, pol = 'V', eps_w = 73 + 1j * 18 ):
    # theta: incident angle [rad]
    # pol: polarization (H,V)
    if pol == 'V':  # scattering coefficients from Kudry et al. (2019), eq. A2 (cos(theta)**2 missing I think)
        Gpp = np.absolute(
            (eps_w - 1) * (eps_w * (1 + np.sin( theta ) ** 2) - np.sin( theta ) ** 2) * np.cos( theta ) ** 2 / \
            (eps_w * np.cos( theta ) + (eps_w - np.sin( theta ) ** 2) ** 0.5) ** 2 )
    if pol == 'H':
        Gpp = np.absolute(
            (eps_w - 1) * np.cos( theta ) ** 2 / (np.cos( theta ) + (eps_w - np.sin( theta ) ** 2) ** 0.5) ** 2 )
    return (Gpp)


# this is the one of  Kudry et al. (2019), which differs from Plant by cos(theta)**2 and we do not take the absolute value
def scattering_coeff_Kudry2019( theta, pol = 'V', eps_w = 73 + 1j * 18 ):
    # theta: incident angle [rad]
    # pol: polarization (H,V)
    if pol == 'V':  # scattering coefficients from Kudry et al. (2019), eq. A2 (cos(theta)**2 missing I think)
        Gpp = (eps_w - 1) * (eps_w * (1 + np.sin( theta ) ** 2) - np.sin( theta ) ** 2) / \
              (eps_w * np.cos( theta ) + (eps_w - np.sin( theta ) ** 2) ** 0.5) ** 2
    if pol == 'H':
        Gpp = (eps_w - 1) / (np.cos( theta ) + (eps_w - np.sin( theta ) ** 2) ** 0.5) ** 2
    return (Gpp)


def scattering_coeff_Kudry2003( theta, pol = 'V' ):
    # theta: incident angle [rad]
    # pol: polarization (H,V)
    if pol == 'V':  # scattering coefficients from Kudry et al. (2003), eq. 3/4
        Gp0 = np.sqrt(
            np.absolute( np.cos( theta ) ** 4 * (1 + np.sin( theta ) ** 2) ** 2 / (np.cos( theta ) + 0.111) ** 4 ) )
    if pol == 'H':
        Gp0 = np.sqrt( np.absolute( np.cos( theta ) ** 4 / (0.111 * np.cos( theta ) + 1) ** 4 ) )
    return (Gp0)


def Fresnel_coeff_normal( pol = 'V', eps_w = 73 + 1j * 18 ):
    # pol: polarization (H,V)
    # eps_w: dielectric constant of water
    if pol == 'H':
        R = np.absolute( (np.cos( 0 ) - np.sqrt( eps_w - np.sin( 0 ) ** 2 )) / (
                np.cos( 0 ) + np.sqrt( eps_w - np.sin( 0 ) ** 2 )) )
    if pol == 'V':
        R = np.absolute( (np.cos( 0 ) - np.sqrt( eps_w - np.sin( 0 ) ** 2 )) / (
                np.cos( 0 ) + np.sqrt( eps_w - np.sin( 0 ) ** 2 )) )
    return (R)


if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    import stereoid.tropical_cyclones.Deprecated.backscatter as backscatter

    # wavelengths and wave numbers
    g = 9.81
    n_k = 100  # number of frequencies single side (total 2*n_k - 1)
    lambda_min = 0.01  # minimum wave length
    lambda_max = 1000  # maximum wave length
    k_min = 2 * np.pi / lambda_max  # minimum wave number
    k_max = 2 * np.pi / lambda_min  # should at least pass the Bragg wave number
    # k_x = k_min * np.arange( 1, n_k + 1 )  # vector of wave numbers (single side)
    k_x = np.reshape( 10 ** np.linspace( np.log10( k_min ), np.log10( k_max ), n_k ), (1, n_k) )
    # k_x[ 20: ] = k_x[ 20: ] * 1.015 ** np.arange( 1, n_k - 20 )  # extend domain (distance increase higher wave noms)
    k_x = np.append( np.append( -np.flip( k_x ), 0 ), k_x )  # double sided spectrum
    dk = np.gradient( k_x, 1 )
    k_x = np.dot( np.ones( (n_k * 2 + 1, 1) ), k_x.reshape( 1, n_k * 2 + 1 ) )  # two dimensional
    k_y = np.transpose( k_x )
    k = np.sqrt( k_x ** 2 + k_y ** 2 )
    omega = np.where( k > 0, np.sqrt( g * k ), 0 )
    phi = np.arctan2( k_y, k_x )  # 0 is cross-track direction waves, 90 along-track
    dks = np.outer( dk, dk )  # patch size

    # wave spectrum using Elfouhaily et al. (1997)
    u_10 = 10
    fetch = 500E3
    phi_w = 0
    B,_,_,_ = Kudry_spec( k_x, k_y, u_10, fetch, phi_w, dks )
    S = np.where( k > 0, B * k ** -4, 0 )

    # RIM
    theta_i = np.arange( 2, 80, 2 )
    for i in range( 0, len( theta_i ) ):
        s_spec, s_bragg, s_break, q = backscatter.backscatter_Kudry2005( S, k_x, k_y, dks, phi_w, theta = theta_i[ i ], pol = 'V', u_10 = u_10, k_r = 0 )
        plt.plot( theta_i[ i ], 10 * np.log10( s_spec * (1 - q) ), 'r*' )
        plt.plot( theta_i[ i ], 10 * np.log10( s_bragg * (1 - q) ), 'g*' )
        plt.plot( theta_i[ i ], 10 * np.log10( s_break * q ), 'b*' )
        plt.ylim( -40, 20 )

        #sigma_br_cr, sigma_wb_cr = backscatter.backscatter_crosspol( S, k_x, k_y, dks, theta = theta_i[ i ], alpha = 0,
        #                                                             u_10 = u_10, k_r = 0, fetch = fetch )

    plt.show()
