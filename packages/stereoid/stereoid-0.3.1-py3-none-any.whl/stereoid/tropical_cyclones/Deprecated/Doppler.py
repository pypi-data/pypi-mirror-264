__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
from stereoid.tropical_cyclones.Deprecated.wave_spectra import tuning_param_wb
from stereoid.tropical_cyclones.Deprecated.wave_spectra import Kudry_spec
from stereoid.tropical_cyclones.Deprecated.backscatter import Fresnel_coeff_normal
from stereoid.tropical_cyclones.Deprecated.backscatter import scattering_coeff
from stereoid.tropical_cyclones.Deprecated.constants import constants as co


# this is the implementation for a multi-wave system as defined in Hansen et al. (2012), equations refer to this paper
# for bi-static variants, rotate the input spectrum, wind direction, current direction and swell direction by -alpha_p/2 or alpha_p/2
def DopRIM( S, kx, ky, dks, theta, alpha_p, v_c, phi_c, k_sw, phi_sw, A_sw, phi_w, u_10, pol = 'V',
            rat = np.array( [ 0.1, 0.8, 0.1 ] ) ):
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
    # u_10[deg]: local wind speed
    # fetch[deg]: local wind fetch

    # convert to radians
    alpha_p = np.deg2rad( alpha_p )
    phi_c = np.deg2rad( phi_c )
    theta = np.deg2rad( theta )
    phi_sw = np.deg2rad( phi_sw )
    phi_w = np.deg2rad( phi_w )

    # radar wavelength
    k_r = 2 * np.pi / co.la_r
    if alpha_p != 0:  # for bistatic systems
        k_r = k_r * np.cos( alpha_p / 2 )

    # some computations
    u_star = u_10 * np.sqrt( (0.8 + 0.065 * u_10) * 1e-3 )  # drag velocity
    k_br = 2 * k_r * np.sin( theta )  # Bragg wave number

    # integration limits
    k_wb = k_r / 10  # wave number of the shortest breaking waves
    k_d = co.d * k_r

    # angular frequency and some conversions
    k = np.sqrt( kx ** 2 + ky ** 2 )
    k_inv = np.where( k > 0, 1 / k, 0 )
    C = np.sqrt( co.g * k_inv + co.gamma * k / co.rho_w )
    C[ 0, 0 ] = 0  # phase velocity
    C_sw = np.sqrt( co.g / k_sw + co.gamma * k_sw / co.rho_w )
    C_br = np.sqrt( co.g / k_br + co.gamma * k_br / co.rho_w )
    phi_k = np.arctan2( ky, kx )  # wave directions

    # spectral conversions
    B = k ** 4 * S  # saturation spectrum

    # large-scale wave mss (the assumption is that phi_r=0, the radar direction is 0 degrees)
    # based on eq. 16 in Hansen et al. (2012) and eq. 13 in Kudry et al. (2005)
    I_lim = np.logical_and(k > 0,k < k_d)
    sL_i = np.sqrt( np.sum( k[ I_lim ] ** 2 * np.cos( phi_k[ I_lim ]) ** 2 * S[ I_lim ] * dks[ I_lim ] ) )
    sL_ci = np.sqrt( np.sum( k[ I_lim ] ** 2 * np.sin( phi_k[ I_lim ]) ** 2 * S[ I_lim ] * dks[ I_lim ] ) )

    # swell wave mss (only in case there is swell)
    sL_sw = np.sqrt( A_sw ** 2 * k_sw ** 2 / 2 )

    # eq. 21 in Kudry et al. (2005), eq. 28 from Kudry et al. (2003) for derivation
    alpha, n, C_b = tuning_param_wb( u_star, C, k )
    Lambda = np.where( k > 0, k_inv / 2 * (B / alpha) ** (n + 1), 0 )

    ###### RIM: backscatter derivatives ######
    dtheta = 1E-5
    ## specular (eq. 8, Kudry et al, 2003)
    I_lim = k > k_d
    h_s = np.sqrt( np.sum( S[ I_lim ] * dks[ I_lim ] ) )  # below eq. 5 Kudry et al. (2005)
    R = Fresnel_coeff_normal( pol = pol, eps_w = co.eps_w ) * np.exp( -k_r ** 2 * h_s ** 2 )  # Fresnel coefficients
    sigma_0sp = R ** 2 / (np.cos( theta ) ** 4 * 2 * sL_ci * sL_i) * np.exp( -np.tan( theta ) ** 2 / (2 * sL_i ** 2) )
    dsigma_0sp = R ** 2 / (np.cos( theta + dtheta ) ** 4 * 2 * sL_ci * sL_i) * np.exp(
        -np.tan( theta + dtheta ) ** 2 / (2 * sL_i ** 2) ) - sigma_0sp

    ## Bragg scattering (eq. A5, Kudry et al, 2003)
    Sr_temp = 0.5 * S[ int( (len( ky ) - 1) / 2 ), : ] + 0.5 * np.flip( S[ int( (len( ky ) - 1) / 2 ), : ] )
    k_b0 = 1.0 * k_br  # radar Bragg number
    kx_temp=kx[ int( (len( ky ) - 1) / 2 ), : ] # go to logaritmic domain for better interpolation
    Sr0 = 10**np.interp( np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]) )
    Gp0 = scattering_coeff( theta, pol = pol )  # scattering coefficients
    sigma_0br = 16 * np.pi * k_r ** 4 * Gp0 ** 2 * Sr0
    #plt.plot( kx[ 0, : ], Sr_temp, '.' )
    #plt.plot( k_b0, Sr0, '*' )
    k_b0 = 2 * k_r * np.sin( theta + dtheta )
    Sr0 = 10**np.interp( np.log10(k_b0), np.log10(kx_temp[kx_temp > 0]), np.log10(Sr_temp[kx_temp > 0]) )
    Gp0 = scattering_coeff( theta + dtheta, pol = pol )
    dsigma_0br = 16 * np.pi * k_r ** 4 * Gp0 ** 2 * Sr0 - sigma_0br
    #plt.plot(k_b0,Sr0,'*')
    #plt.xscale('symlog')
    #plt.yscale( 'symlog' )
    #plt.ylim(5E-10,0.8E-9)
    #plt.show()

    ## wave breaking (eq. 60, Kudry et al, 2003)
    sigma_0wb = (1 / np.cos( theta ) ** 4 * np.exp( -np.tan( theta ) ** 2 / co.s_wb ** 2 ) + co.eps_wb) / co.s_wb ** 2
    dsigma_0wb = (1 / np.cos( theta + dtheta ) ** 4 * np.exp(
        -np.tan( theta + dtheta ) ** 2 / co.s_wb ** 2 ) + co.eps_wb) / co.s_wb ** 2 - sigma_0wb

    ###### Dopp: Doppler ######
    ## transfer functions
    # complex hydrodynamic modulation functions (I guess all the tau's should be the same)
    Mh_br = co.m_k * np.cos( phi_k ) ** 2 * (1 - 1j * co.tau_br) / (1 + co.tau_br ** 2)
    Mh_wb = -1 / 4 * co.m_k * (co.n_g + 1) * (1 + 2 * (kx * k_inv) ** 2) * (1 - 1j * co.tau_wb) / (1 + co.tau_wb ** 2)
    Mh = 0;  # m_k*(kx*k_inv)**2*(1-1j*tau_sp)/(1+tau_sp**2)
    Mh_sp = 0;  # (np.tan(theta)**2/sL_sw**2-1)*np.sum(Mh*S*k**2*dks)/sL_sw

    # these tilt functions are k-independent
    Mt_sp = 1 / sigma_0sp * dsigma_0sp / dtheta  # scalar
    Mt_br = 1 / sigma_0br * dsigma_0br / dtheta  # scalar
    Mt_wb = 1 / sigma_0wb * dsigma_0wb / dtheta  # scalar

    ## modulated contributions to Doppler
    # be aware c_br and c_wb are actually multiplied by sL**2, which is compensated in the last equation for Doppler velocity
    # we apply the same thing for c_sp
    # equation 5 for br and wb and equation 18 for sp
    I_lim = np.logical_and(k > 0,k < k_d)
    c_br = np.sum( ((-Mt_br / np.tan( theta ) + np.real( Mh_br[ I_lim ] )) * np.cos(
        0 - phi_k[ I_lim ] ) + np.imag( Mh_br[ I_lim ] ) / np.tan(
        theta )) * C[ I_lim ] * k[ I_lim ] ** 2 * S[ I_lim ] * dks[ I_lim ] )

    I_lim = np.logical_and(k > 0,k < k_wb / 10)
    c_wb = np.sum( ((-Mt_wb / np.tan( theta ) + np.real( Mh_wb[ I_lim ] )) * np.cos(
        0 - phi_k[ I_lim ] ) + np.imag( Mh_wb[ I_lim ] ) / np.tan( theta )) * C[ I_lim ] *
                   k[ I_lim ] ** 2 * S[ I_lim ] * dks[ I_lim ] )  # k_wb/10 is the limit

    c_sp = 0; #C_sw * (np.cos( 0 - phi_sw ) * (-Mt_sp / np.tan( theta ) + np.real( Mh_sp )) + np.imag( Mh_sp ) / np.tan(
        #theta )) * sL_sp ** 2 #(*sL_sp**2) # this one is currently turned off (Mh and Mh_sp are zero)

    ## mean doppler contributions from scattering facets
    # equation 15 for sp, equation 19 for wb and phase velocity for br (see between equation 8-9)
    c_br_bar = 1.0 * C_br

    I_lim = np.logical_and(k > 0,k < k_wb)
    c_wb_bar = np.sum( np.cos( phi_k[ I_lim ] - 0 ) * C[ I_lim ] * k_inv[ I_lim ] * Lambda[ I_lim ] * dks[ I_lim ] ) / \
               np.sum( k_inv[ I_lim ] * Lambda[ I_lim ] * dks[ I_lim ] )

    I_lim = k > 0 # FIXME: check the correct orientation
    c_sp_bar = np.cos( 0 ) / sL_i** 2 * \
               np.sum( np.cos( phi_k[ I_lim ] ) * C[ I_lim ] * k[ I_lim ] ** 2 * S[ I_lim ] * dks[ I_lim ] ) + \
               np.sin( 0 ) / sL_ci ** 2 * \
               np.sum( np.sin( phi_k[ I_lim ] ) * C[ I_lim ] * k[ I_lim ] ** 2 * S[ I_lim ] * dks[ I_lim ] )

    #### Doppler velocity in the direction of the mono-static receiver (equivalent) ####
    V = v_c * np.sin( theta ) * np.cos( phi_c ) + \
        rat[ 0 ] * (c_sp_bar + c_sp) + \
        rat[ 1 ] * (c_br_bar + c_br) + \
        rat[ 2 ] * (c_wb_bar + c_wb)

    return V, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br


if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    import stereoid.tropical_cyclones.Deprecated.backscatter as backscatter

    # wavelengths and wave numbers
    g = 9.81
    n_k = 200  # number of frequencies single side (total 2*n_k - 1)
    lambda_min = 0.01  # minimum wave length
    lambda_max = 2000  # maximum wave length
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

    # DopRIM
    theta_i = np.arange( 10, 60, 1 )
    alpha = 0
    v_c = 0
    phi_c = 0
    k_sw = 0.02
    phi_sw = 90
    A_sw = 1
    for i in range( 0, len( theta_i ) ):
        # Gp0=scattering_coeff( np.deg2rad(theta_i[i]), pol = 'V' )
        # plt.plot(theta_i[i],Gp0,'.')
        # '''
        s_spec, s_bragg, s_break, q = backscatter.backscatter_Kudry2005( S, k_x, k_y, dks, phi_w, theta = theta_i[ i ],
                                                                         pol = 'V',
                                                                         u_10 = u_10, k_r = 0 )
        #print( 'check' )
        #print( s_spec, s_bragg, s_break )
        rat = np.array( [ s_spec * (1 - q), s_bragg * (1 - q), s_break * q ] ) / (
                s_spec * (1 - q) + s_bragg * (1 - q) + s_break * q)
        print(theta_i[i])
        print( rat )
        #print(s_spec, s_bragg, s_break)
        #print(q)
        # plt.plot(theta_i[i],s_spec,'r*')
        # plt.plot(theta_i[i], s_bragg, 'g*')
        # plt.plot(theta_i[i], s_break, 'b*')
        V, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br = DopRIM( S, k_x, k_y, dks, theta_i[ i ], alpha, v_c, phi_c, k_sw,
                                                                    phi_sw, A_sw, phi_w, u_10, pol = 'V', rat = rat )

        # plt.plot(theta_i[i],V,'k.')
        if i == 0:
            # plt.plot( theta_i[ i ], rat[ 0 ],'.b', label='specular' )
            # plt.plot( theta_i[ i ], rat[ 2 ],'.r', label='wave breaking' )
            # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp_bar, 'b*', label = 'bar{c}_{sp}' )
            #plt.plot( theta_i[ i ], rat[ 2 ] * c_wb_bar, 'r*', label = 'bar{c}_{wb}' )
            # plt.plot( theta_i[ i ], rat[ 1 ] * c_br_bar, 'g*', label = 'bar{c}_{br}' )
            # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp, 'b.', label = 'c_{sp}' )
            #plt.plot( theta_i[ i ], rat[ 2 ] * c_wb, 'r.', label = 'c_{wb}' )
            # plt.plot( theta_i[ i ], rat[ 1 ] * c_br, 'g.', label = 'c_{br}' )
            # plt.plot( theta_i[ i ], V, 'k.', label = 'total' )
            plt.plot( theta_i[ i ], rat[ 0 ] * (c_sp + c_sp_bar), 'b.', label = 'specular' )
            plt.plot( theta_i[ i ], rat[ 2 ] * (c_wb + c_wb_bar), 'r.', label = 'breakers' )
            plt.plot( theta_i[ i ], rat[ 1 ] * (c_br + c_br_bar), 'g.', label = 'Bragg' )
        if i != 0:
            # plt.plot( theta_i[i], rat[ 0 ],'.b')
            # plt.plot( theta_i[ i ], rat[ 2 ],'.r')
            # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp_bar, 'b*' )
            #plt.plot( theta_i[ i ], rat[ 2 ] * c_wb_bar, 'r*' )
            # plt.plot( theta_i[ i ], rat[ 1 ] * c_br_bar, 'g*' )
            # plt.plot( theta_i[ i ], rat[ 0 ] * c_sp, 'b.' )
            #plt.plot( theta_i[ i ], rat[ 2 ] * c_wb, 'r.' )
            # plt.plot( theta_i[ i ], rat[ 1 ] * c_br, 'g.' )
            plt.plot( theta_i[ i ], V, 'k.' )
            plt.plot( theta_i[ i ], rat[ 0 ] * (c_sp + c_sp_bar), 'b.' )
            plt.plot( theta_i[ i ], rat[ 2 ] * (c_wb + c_wb_bar), 'r.' )
            plt.plot( theta_i[ i ], rat[ 1 ] * (c_br + c_br_bar), 'g.' )
        # '''
    plt.xlabel( 'incident angle [deg]' )
    plt.ylabel( 'relative contribution [m/s]' )
    plt.ylim( -1, 5 )
    plt.legend()
    plt.show()
