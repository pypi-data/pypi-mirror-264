__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

from scipy.ndimage import median_filter
from stereoid.tropical_cyclones.Deprecated.constants import constants as co
from stereoid.tropical_cyclones.Deprecated import wave_spectra


# This in an implementation of eq. 44-47 of Kudry et al. (2005) for currents only
# Therefore we only include the first term of eq. 44 and only the divergence as in Johannessen et al. (2005)
def Kudry2005_divergence1d( B_neq, B_eq, I_swpc, kx, ky, res, u_10, phi_w, fetch, m_star = 1 ):
    # B_neq: non-equilibrium curvature spectrum
    # B_eq: equilibrium curvature spectrum (Kudry2005, Yuroskaya2013, KMC14)
    # I_swpc: rate of short wave energy generation (eq. 19/20, Kudry2005)
    # kx: two-dimensional wave number in the cross-track direction
    # ky: two-dimensional wave number in the along-track direction
    # res: one-dimensional resolution (assumed equal in both directions)
    # u_10: wind speed
    # phi_w [deg]: wind direction
    # fetch: fetch length

    # degrees to radians
    phi_w = np.deg2rad( phi_w )

    # angular velocity and group velocity
    k = np.sqrt( kx ** 2 + ky ** 2 )
    phi = np.arctan2( ky, kx )
    #omega=np.where( k > 0, np.sqrt( co.g * k + co.gamma * k ** 3 / co.rho_w ), 0)
    omega = np.sqrt( co.g * k )
    #C = np.where( k > 0, np.sqrt( co.g / k + co.gamma * k / co.rho_w ), 0 )  # phase speed
    C=np.where( k > 0,omega / k,0)
    Cx=kx/k*C
    Cy=ky/k*C


    # peak phase velocity and group velocity (deep water)
    kp = wave_spectra.spec_peak( u_10, fetch )
    #omegap= np.sqrt( co.g * kp + co.gamma * kp ** 3 / co.rho_w )
    omegap=np.sqrt( co.g * kp )
    cp = omegap / kp
    cg = 1 / 2 * cp
    f = wave_spectra.phi_func( (k / (10 * kp)) ** 2 ) # equivalent as in wave spectrum

    # full (curvature) spectrum
    B = (1 - f) * B_neq + f * B_eq
    B[ k == 0 ] = 0
    S = np.where( k > 0, k ** -4 * B, 0 )

    # some parameters for relaxation time (non-equilibrium and equilibrium)
    # FIXME: this gives a very irratic tau, so we will use the 'estimate' from Kudry2012 for now
    u_star = u_10 * np.sqrt( (0.8 + 0.065 * u_10) * 1e-3 )
    #alpha, n, C_b = wave_spectra.tuning_param_wb( u_star, C, k )
    #beta = C_b * (u_star / C) ** 2 * np.absolute( np.cos( phi - phi_w ) ) * np.cos(
    #    phi - phi_w )  # Kudry2005, eq. 17
    #beta_v = beta - 4 * co.nu * k ** 2 / omega
    #beta_0 = C_b * (u_star / C) ** 2  # Kudry2005, eq. 17

    # relaxation time (non-equilibrium and equilibrium)
    #tau_eq_inv = n * beta_v + (n + 1) * I_swpc / B  # Kudry2005, eq. 34
    #tau_neq_inv = np.maximum( (2 * beta) / m_star, beta_0 )  # Kudry2005, eq. 40
    #tau_neq_inv=(2 * beta) / m_star
    #tau = 1 / ((1-f)*tau_neq_inv + f*tau_eq_inv )
    #tau[k < kp]=1/tau_neq_inv[k < kp]
    # I think the C_b drops below 0 for low k's, with low C_b you get low beta and therefore massive tau
    #tau = median_filter( tau, 5 )
    C_b=0.03
    beta_0 = C_b * (u_star / C) ** 2  # Kudry2005, eq. 17
    tau = np.minimum(m_star/(2*C_b)*(u_star/C)**-2,1/beta_0) # Kudry et al. (2012) below equation 1



    # at the moment not used, as we apply a convolution in the spatial domain to avoid some artefacts
    L=int(1E6/res-1)
    dKx = 2 * np.pi / (L * res)
    dKy = 2 * np.pi / (L * res)
    Kx = dKx * np.arange( -np.floor(L / 2), np.ceil(L / 2), 1 )
    Ky = dKy * np.arange( -np.floor(L / 2), np.ceil(L / 2), 1 )

    # derivative of the wave action spectrum
    k_lim = kp*1.0
    # FIXME: check this, maybe we should use the 'absolute' values for kx here
    dlnk_x = np.gradient( np.log( np.absolute(kx) ), axis = 1 )
    dlnk_y = np.gradient( np.log( np.absolute(ky) ), axis = 0 )
    N = np.where( k > k_lim, omega * k ** -1 * S, 0 )
    dlnN_x = np.gradient( np.log( N ), axis = 1 )
    dlnN_y = np.gradient( np.log( N ), axis = 0 )
    mk_x = np.where( k > k_lim, dlnN_x / dlnk_x, 0 )
    mk_y = np.where( k > k_lim, dlnN_y / dlnk_y, 0 )
    # FIXME: fix some discontinuities, by median filter
    mk_x = median_filter( mk_x, 5 )
    mk_y = median_filter( mk_y, 5 )
    mk_x[mk_x != mk_x]=0
    mk_y[ mk_y != mk_y ] = 0

    # this for loop is based on Kudry2005, eq. 43-47
    shp = kx.shape
    Tx_3D = np.zeros( (shp[ 0 ], shp[ 1 ], L ) )
    Ty_3D = np.zeros( (shp[ 0 ], shp[ 1 ], L ) )
    # go through all kx,ky
    for i in range( 0, shp[ 0 ] ):
        for j in range( 0, shp[ 1 ] ):
            if k[ i, j ] > k_lim:
                # we only include the first two terms in Kudry et al. (2005), eq. 46
                # this is then the 'Cartesian version' of the transfer function
                rx = tau[ i, j ] * omega[ i, j ] ** -1 * Cx[i,j] * Kx
                ry = tau[ i, j ] * omega[ i, j ] ** -1 * Cy[i,j] * Ky

                # This is a combination of Kudry2005, eq. 44, Kudry2012 eq. 1 and Rascle2014 eq. 2 rewritten
                Tx_comp=tau[i,j]*omega[i,j]**-1/(1+rx**2)*(1-1j*rx)
                Ty_comp=tau[i,j]*omega[i,j]**-1/(1+ry**2)*(1-1j*ry)
                Tx =  Tx_comp * mk_x[ i, j ]
                Ty = Ty_comp * mk_y[ i, j ]
                Tx_sp =  np.fft.ifft( np.fft.ifftshift( Tx ) )   # T in spatial domain
                Ty_sp = np.fft.ifft( np.fft.ifftshift( Ty ) ) # T in spatial domain

                # compute T for kx,ky
                Tx_3D[ i, j, : ] = Tx_sp
                Ty_3D[ i, j, : ] = Ty_sp

    # in this form it returns one-dimensional impulse response functions for (kx,ky)
    return Tx_3D, Ty_3D

# This in an implementation of eq. 44-47 of Kudry et al. (2005) for wind
# Therefore we only include the second term of eq. 44
def Kudry2005_wind1d( B_neq, B_eq, I_swpc, kx, ky, res, u_10, phi_w, fetch, m_star = 1 ):
    # B_neq: non-equilibrium curvature spectrum
    # B_eq: equilibrium curvature spectrum (Kudry2005, Yuroskaya2013, KMC14)
    # I_swpc: rate of short wave energy generation (eq. 19/20, Kudry2005)
    # kx: two-dimensional wave number in the cross-track direction
    # ky: two-dimensional wave number in the along-track direction
    # res: one-dimensional resolution (assumed equal in both directions)
    # u_10: wind speed
    # phi_w [deg]: wind direction
    # fetch: fetch length

    # degrees to radians
    phi_w = np.deg2rad( phi_w )

    # angular velocity and group velocity
    k = np.sqrt( kx ** 2 + ky ** 2 )
    phi = np.arctan2( ky, kx )
    #omega=np.where( k > 0, np.sqrt( co.g * k + co.gamma * k ** 3 / co.rho_w ), 0)
    omega = np.sqrt( co.g * k )
    #C = np.where( k > 0, np.sqrt( co.g / k + co.gamma * k / co.rho_w ), 0 )  # phase speed
    C=np.where( k > 0,omega / k,0)
    Cx=kx/k*C
    Cy=ky/k*C


    # peak phase velocity and group velocity (deep water)
    kp = wave_spectra.spec_peak( u_10, fetch )
    #omegap= np.sqrt( co.g * kp + co.gamma * kp ** 3 / co.rho_w )
    omegap=np.sqrt( co.g * kp )
    cp = omegap / kp
    cg = 1 / 2 * cp
    f = wave_spectra.phi_func( (k / (10 * kp)) ** 2 ) # equivalent as in wave spectrum

    # full (curvature) spectrum
    B = (1 - f) * B_neq + f * B_eq
    B[ k == 0 ] = 0

    # some parameters for relaxation time (non-equilibrium and equilibrium)
    # FIXME: this gives a very irratic tau, so we will use the 'estimate' from Kudry2012 for now
    u_star = u_10 * np.sqrt( (0.8 + 0.065 * u_10) * 1e-3 )
    alpha, n, C_b = wave_spectra.tuning_param_wb( u_star, C, k )
    beta = C_b * (u_star / C) ** 2 * np.absolute( np.cos( phi - phi_w ) ) * np.cos(
        phi - phi_w )  # Kudry2005, eq. 17
    #beta_v = beta - 4 * co.nu * k ** 2 / omega
    #beta_0 = C_b * (u_star / C) ** 2  # Kudry2005, eq. 17

    # relaxation time (non-equilibrium and equilibrium)
    #tau_eq_inv = n * beta_v + (n + 1) * I_swpc / B  # Kudry2005, eq. 34
    #tau_neq_inv = np.maximum( (2 * beta) / m_star, beta_0 )  # Kudry2005, eq. 40
    #tau_neq_inv=(2 * beta) / m_star
    #tau = 1 / ((1-f)*tau_neq_inv + f*tau_eq_inv )
    #tau[k < kp]=1/tau_neq_inv[k < kp]
    # I think the C_b drops below 0 for low k's, with low C_b you get low beta and therefore massive tau
    #tau = median_filter( tau, 5 )
    C_b=0.03
    beta_0 = C_b * (u_star / C) ** 2  # Kudry2005, eq. 17
    tau = np.minimum(m_star/(2*C_b)*(u_star/C)**-2,1/beta_0) # Kudry et al. (2012) below equation 1

    # at the moment not used, as we apply a convolution in the spatial domain to avoid some artefacts
    L=int(1E6/res-1)
    dKx = 2 * np.pi / (L * res)
    dKy = 2 * np.pi / (L * res)
    Kx = dKx * np.arange( -np.floor(L / 2), np.ceil(L / 2), 1 )
    Ky = dKy * np.arange( -np.floor(L / 2), np.ceil(L / 2), 1 )

    # derivative of the wave action spectrum
    k_lim = kp*1.0

    # this for loop is based on Kudry2005, eq. 43-47
    shp = kx.shape
    Tx_3D = np.zeros( (shp[ 0 ], shp[ 1 ], L ) )
    Ty_3D = np.zeros( (shp[ 0 ], shp[ 1 ], L ) )
    # go through all kx,ky
    for i in range( 0, shp[ 0 ] ):
        for j in range( 0, shp[ 1 ] ):
            if k[ i, j ] > k_lim:
                # we only include the first two terms in Kudry et al. (2005), eq. 46
                # this is then the 'Cartesian version' of the transfer function
                rx = tau[ i, j ] * omega[ i, j ] ** -1 * Cx[i,j] * Kx
                ry = tau[ i, j ] * omega[ i, j ] ** -1 * Cy[i,j] * Ky

                # This is a combination of Kudry2005, eq. 44, Kudry2012 eq. 1 and Rascle2014 eq. 2 rewritten
                Tx_comp=tau[i,j]/(1+rx**2)*(1-1j*rx)
                Ty_comp=tau[i,j]/(1+ry**2)*(1-1j*ry)
                Tx =  Tx_comp * 2 * beta[i,j]
                Ty = Ty_comp * 2 * beta[i,j]
                Tx_sp =  np.fft.ifft( np.fft.ifftshift( Tx ) )   # T in spatial domain
                Ty_sp = np.fft.ifft( np.fft.ifftshift( Ty ) ) # T in spatial domain

                # compute T for kx,ky
                Tx_3D[ i, j, : ] = Tx_sp
                Ty_3D[ i, j, : ] = Ty_sp

    # in this form it returns one-dimensional impulse response functions for (kx,ky)
    return Tx_3D, Ty_3D

# This in an implementation of eq. 44-47 of Kudry et al. (2005) for currents only
# Therefore we only include the first term of eq. 44.
def Kudry2005_currents( B_neq, B_eq, I_swpc, kx, ky, dudx, dvdy, res, u_10, phi_w, fetch, m_star = 1 ):
    # B_neq: non-equilibrium curvature spectrum
    # B_eq: equilibrium curvature spectrum (Kudry2005, Yuroskaya2013, KMC14)
    # I_swpc: rate of short wave energy generation (eq. 19/20, Kudry2005)
    # kx: two-dimensional wave number in the cross-track direction
    # ky: two-dimensional wave number in the along-track direction
    # dudx: two-dimensional divergence in the cross-track direction
    # dvdy: two-dimensional divergence in the along-track direction
    # res: one-dimensional resolution (assumed equal in both directions)
    # u_10: wind speed
    # phi_w [deg]: wind direction
    # fetch: fetch length

    # degrees to radians
    phi_w = np.deg2rad( phi_w )

    # angular velocity and group velocity
    k = np.sqrt( kx ** 2 + ky ** 2 )
    phi = np.arctan2( ky, kx )
    #omega=np.where( k > 0, np.sqrt( co.g * k + co.gamma * k ** 3 / co.rho_w ), 0)
    omega = np.sqrt( co.g * k )
    #C = np.where( k > 0, np.sqrt( co.g / k + co.gamma * k / co.rho_w ), 0 )  # phase speed
    C=np.where( k > 0,omega / k,0)
    Cx=kx/k*C
    Cy=ky/k*C


    # peak phase velocity and group velocity (deep water)
    kp = wave_spectra.spec_peak( u_10, fetch )
    #omegap= np.sqrt( co.g * kp + co.gamma * kp ** 3 / co.rho_w )
    omegap=np.sqrt( co.g * kp )
    cp = omegap / kp
    cg = 1 / 2 * cp
    f = wave_spectra.phi_func( (k / (10 * kp)) ** 2 ) # equivalent as in wave spectrum

    # full (curvature) spectrum
    B = (1 - f) * B_neq + f * B_eq
    B[ k == 0 ] = 0
    S = np.where( k > 0, k ** -4 * B, 0 )

    # some parameters for relaxation time (non-equilibrium and equilibrium)
    # FIXME: this gives a very irratic tau, so we will use the 'estimate' from Kudry2012 for now
    u_star = u_10 * np.sqrt( (0.8 + 0.065 * u_10) * 1e-3 )
    #alpha, n, C_b = wave_spectra.tuning_param_wb( u_star, C, k )
    #beta = C_b * (u_star / C) ** 2 * np.absolute( np.cos( phi - phi_w ) ) * np.cos(
    #    phi - phi_w )  # Kudry2005, eq. 17
    #beta_v = beta - 4 * co.nu * k ** 2 / omega
    #beta_0 = C_b * (u_star / C) ** 2  # Kudry2005, eq. 17

    # relaxation time (non-equilibrium and equilibrium)
    #tau_eq_inv = n * beta_v + (n + 1) * I_swpc / B  # Kudry2005, eq. 34
    #tau_neq_inv = np.maximum( (2 * beta) / m_star, beta_0 )  # Kudry2005, eq. 40
    #tau_neq_inv=(2 * beta) / m_star
    #tau = 1 / ((1-f)*tau_neq_inv + f*tau_eq_inv )
    #tau[k < kp]=1/tau_neq_inv[k < kp]
    # I think the C_b drops below 0 for low k's, with low C_b you get low beta and therefore massive tau
    #tau = median_filter( tau, 5 )
    C_b=0.03
    beta_0 = C_b * (u_star / C) ** 2  # Kudry2005, eq. 17
    tau = np.minimum(m_star/(2*C_b)*(u_star/C)**-2,1/beta_0) # Kudry et al. (2012) below equation 1


    # get the DFT (watch out, in the paper they use 'Fourier amplitude')
    # since we later take the inverse DFT, this should be fine
    # at the moment not used, as we apply a convolution in the spatial domain to avoid some artefacts
    #DUDX = np.fft.fft2( dudx )
    #DVDY = np.fft.fft2( dvdy )
    #DUDX[ 0, 0 ] = 0
    #DVDY[ 0, 0 ] = 0
    #DUDX = np.fft.fftshift( DUDX )
    #DVDY = np.fft.fftshift( DVDY )
    SHP = dudx.shape
    dKx = 2 * np.pi / (SHP[ 1 ] * res)
    dKy = 2 * np.pi / (SHP[ 0 ] * res)
    Kx = dKx * np.arange( -np.floor(SHP[ 1 ] / 2), np.ceil(SHP[ 1 ] / 2), 1 )
    Ky = dKy * np.arange( -np.floor(SHP[ 0 ] / 2), np.ceil(SHP[ 0 ] / 2), 1 )
    Kx = np.dot( np.ones( (SHP[ 0 ], 1) ), Kx.reshape( 1, SHP[ 1 ] ) )
    Ky = np.dot( Ky.reshape( SHP[ 0 ], 1 ), np.ones( (1, SHP[ 1 ]) ) )

    # derivative of the wave action spectrum
    k_lim = kp*1.0
    # FIXME: check this, maybe we should use the 'absolute' values for kx here
    dlnk_x = np.gradient( np.log( np.absolute(kx) ), axis = 1 )
    dlnk_y = np.gradient( np.log( np.absolute(ky) ), axis = 0 )
    N = np.where( k > k_lim, omega * k ** -1 * S, 0 )
    dlnN_x = np.gradient( np.log( N ), axis = 1 )
    dlnN_y = np.gradient( np.log( N ), axis = 0 )
    mk_x = np.where( k > k_lim, dlnN_x / dlnk_x, 0 )
    mk_y = np.where( k > k_lim, dlnN_y / dlnk_y, 0 )
    # FIXME: fix some discontinuities, by median filter
    mk_x = median_filter( mk_x, 5 )
    mk_y = median_filter( mk_y, 5 )
    mk_x[mk_x != mk_x]=0
    mk_y[ mk_y != mk_y ] = 0

    # this for loop is based on Kudry2005, eq. 43-47
    shp = kx.shape
    Tx_4D = np.zeros( (shp[ 0 ], shp[ 1 ], SHP[ 0 ], SHP[ 1 ]) )
    Ty_4D = np.zeros( (shp[ 0 ], shp[ 1 ], SHP[ 0 ], SHP[ 1 ]) )
    # go through all kx,ky
    for i in range( 0, shp[ 0 ] ):
        for j in range( 0, shp[ 1 ] ):
            if k[ i, j ] > k_lim:
                # we only include the first two terms in Kudry et al. (2005), eq. 46
                # this is then the 'Cartesian version' of the transfer function
                rx = tau[ i, j ] * omega[ i, j ] ** -1 * Cx[i,j] * Kx
                ry = tau[ i, j ] * omega[ i, j ] ** -1 * Cy[i,j] * Ky

                # This is a combination of Kudry2005, eq. 44, Kudry2012 eq. 1 and Rascle2014 eq. 2 rewritten
                Tx_comp=tau[i,j]*omega[i,j]**-1/(1+rx**2)*(1-1j*rx)
                Ty_comp=tau[i,j]*omega[i,j]**-1/(1+ry**2)*(1-1j*ry)
                Tx =  Tx_comp * mk_x[ i, j ]
                Ty = Ty_comp * mk_y[ i, j ]
                Tx_sp =  np.fft.ifft2( np.fft.ifftshift( Tx ) )   # T in spatial domain
                Ty_sp = np.fft.ifft2( np.fft.ifftshift( Ty ) ) # T in spatial domain

                # compute T for kx,ky
                Tx_4D[ i, j, :, : ] = Tx_sp
                Ty_4D[ i, j, :, : ] = Ty_sp

    # in this form it returns two-dimensional impulse response functions for (kx,ky)
    return Tx_4D, Ty_4D, mk_x, tau*omega[i,j]**-1


if __name__ == '__main__':
    import numpy as np
    # import scipy as sp
    from matplotlib import pyplot as plt

    # from stereoid.tropical_cyclones.high_resolution_var import Kudry2005_currents

    g = 9.81
    n_k = 200  # number of frequencies single side (total 2*n_k - 1)
    lambda_min = 0.01  # minimum wave length
    lambda_max = 5000  # maximum wave length
    k_min = 2 * np.pi / lambda_max  # minimum wave number
    k_max = 2 * np.pi / lambda_min  # should at least pass the Bragg wave number
    k = np.reshape( 10 ** np.linspace( np.log10( k_min ), np.log10( k_max ), n_k ), (1, n_k) )
    k = np.append( np.append( -np.flip( k ), 0 ), k )  # double sided spectrum
    omega = np.sqrt( g * np.absolute(k) )
    C = np.where( k != 0, omega / k, 0 )

    # group velocity
    u_10=10
    fetch=100E3
    kp = wave_spectra.spec_peak( u_10, fetch )
    # omegap= np.sqrt( co.g * kp + co.gamma * kp ** 3 / co.rho_w )
    omegap = np.sqrt( co.g * kp )
    cp = omegap / kp
    cg = 1 / 2 * cp

    # relaxation scale
    C_b = 0.04
    m_star=1
    u_star = u_10 * np.sqrt( (0.8 + 0.065 * u_10) * 1e-3 )
    tau = m_star / (2 * C_b) * (u_star / C) ** -2
    l=tau * omega ** -1 * np.absolute(C)
    plt.figure( figsize = (9, 9) )
    plt.plot( k, l, '.' )
    plt.xscale( 'symlog' )
    plt.yscale( 'symlog' )
    plt.show()

    # transfer function
    L=10000
    K= 2*np.pi/L
    print(K)
    r = tau * omega ** -1 * C * K
    T = tau * omega ** -1 / (1 + 1j * r)

    # plot T
    plt.figure(figsize=(9,9))
    plt.plot(k,np.imag(T),'.')
    plt.xscale('symlog')
    plt.show()

    plt.figure( figsize = (9, 9) )
    plt.plot( k, np.absolute( T ), '.' )
    plt.xscale( 'symlog' )
    plt.show()