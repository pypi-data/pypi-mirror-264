__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import stereoid.oceans.GMF.cmod5n as cmod5n
import numpy as np
import math


# Implementation of Engen and Johnsen (1995)
# This works with linear spacing in kx and ky, maybe we have to change this
# I will make another function for a log-scale spacing
def corr_func(S, kx, ky, mu=0.5, theta=35, R=850E3, V=7000, mtf='Schulz',
              phi_w=0.0, ws=15.0):
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
    ws: wind speed (necessary for GMF based mtf)
    """
    # angular frequency
    theta = np.deg2rad( theta )
    g = 9.81
    k = np.sqrt( kx ** 2 + ky ** 2 )
    omega = np.sqrt( g * k )
    # Nk = len(k[0, :])

    # transfer functions
    # T_x=1/np.tan(theta)
    T_y = -R / V * omega * (kx / k * np.sin( theta ) + 1j * np.cos( theta ))
    T_y[ T_y != T_y ] = 0
    T_I = np.zeros( k.shape )
    if mtf == 'Schulz':
        T_I = -1j * 4 * kx / (np.tan( theta ) * (1 + np.sin( theta ) ** 2)) - 1j * kx / np.tan(
            theta ) + 4.5 * omega * kx ** 2 * (omega - 1j * mu) / (k * (omega ** 2 + mu ** 2))
    if mtf == 'S1':
        dth = 0.001
        sigma = cmod5n.cmod5n_forward( np.array( [ ws, ws ] ), np.array( [ phi_w, phi_w ] ),
                                       np.rad2deg( np.array( [ theta, theta + dth ] ) ) )  # use CMOD5n here
        dsigma = (sigma[ 1 ] - sigma[ 0 ]) / dth
        T_I = kx * dsigma / sigma[ 0 ] / np.cos( theta ) * (
                kx / k * np.sin( theta ) + 1j * np.cos( theta ))  # combination of both equations (37)
    T_I[ T_I != T_I ] = 0

    # cross-spectral functions
    N_II_pos = 0.5 * T_I * np.conj( T_I )
    N_yy_pos = 0.5 * T_y * np.conj( T_y )
    N_Iy_pos = 0.5 * T_I * np.conj( T_y )
    N_yI_pos = 0.5 * T_y * np.conj( T_I )

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
    S_neg = np.fft.fftshift( S )
    S_neg = np.flipud( np.fliplr( S_neg ) )  # watch out this stays in the fft-shifted system
    N_II_neg = np.fft.fftshift( N_II_pos )
    N_yy_neg = np.fft.fftshift( N_yy_pos )
    N_Iy_neg = np.fft.fftshift( N_Iy_pos )
    N_yI_neg = np.fft.fftshift( N_yI_pos )
    N_II_neg = np.flipud( np.fliplr( N_II_neg ) )
    N_yy_neg = np.flipud( np.fliplr( N_yy_neg ) )
    N_Iy_neg = np.flipud( np.fliplr( N_Iy_neg ) )
    N_yI_neg = np.flipud( np.fliplr( N_yI_neg ) )
    SN_II_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_II_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_yy_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_yy_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_yI_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_yI_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_Iy_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_Iy_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )

    # plt.figure()
    # plt.subplot(2, 2, 1)
    # plt.scatter(kx,ky,c=np.real(N_II_pos * S))
    # plt.subplot(2, 2, 2)
    # plt.scatter(kx,ky,c=np.real(SN_II_neg))
    # plt.subplot(2, 2, 3)
    # plt.scatter(kx,ky,c=np.imag(N_II_pos * S))
    # plt.subplot(2, 2, 4)
    # plt.scatter(kx,ky,c=np.imag(SN_II_neg))
    # plt.show()

    # correlation functions
    rho_II = np.real( np.fft.ifft2( N_II_pos * S + SN_II_neg ) )  # / (2 * np.pi) ** 2
    rho_yy = np.real( np.fft.ifft2( N_yy_pos * S + SN_yy_neg ) )  # / (2 * np.pi) ** 2
    rho_Iy = np.real( np.fft.ifft2( N_Iy_pos * S + SN_Iy_neg ) )  # / (2 * np.pi) ** 2
    rho_yI = np.real( np.fft.ifft2( N_yI_pos * S + SN_yI_neg ) )  # / (2 * np.pi) ** 2
    # plt.imshow(np.absolute(S_neg), origin='lower')
    # plt.imshow(np.abs(np.fft.ifft2(0.5*S+0.5*S_neg)), origin='lower')
    # plt.colorbar()
    # plt.show()

    return rho_II, rho_yy, rho_Iy, rho_yI


# now based on Engen and Johnsen (1995) / Krogstad et al. (1994)
def SAR_spec( rho_II, rho_yy, rho_Iy, rho_yI, kx, ky, al = 1, be = 0, we = 1, ord = 4 ):  # ,rho_a,T_0,t_s): # if we want to include smearing
    # rho_ab: (co)variance functions of the
    # kx, ky: 2D waveform grid (cross and along)
    # al: cut-off inflation parameter
    # be: cut-off inflation parameter
    # we: weight of RAR
    # ord: order of expansion

    # dx
    dk = kx[ 0, 1 ] - kx[ 0, 0 ]
    dx = 2 * np.pi / dk / len( kx )  # scene size divided by the number of samples
    x = np.arange( 0, len( kx ) * dx, dx )
    x = x.reshape( 1, len( kx ) )
    # x = np.dot(np.ones((len(kx), 1)), x)
    y = np.transpose( x )

    # it is necessary to do a non-linear mapping, so for each ky (if you include range bunching each kx also) compute
    # the Fourier transform of G and select the row belonging to ky for the spectrum
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
                S[ i, j ] = np.sum( G * DFT ) * dx * dx
    '''

    # faster version (using an expansion)
    S2 = np.zeros( kx.shape, dtype = complex )
    for i in range( 0, ord ):
        S2 = S2 + 1 / math.factorial( i ) * ky ** (2 * i) * np.fft.fft2( rho_yy ** i * (1 + rho_II) )
    S2 = np.exp( -ky ** 2 * rho_yy[ 0, 0 ] ) * S2 * dx * dx
    # S=S-S2

    return S2


# this is the bistatic equivalent of corr_func (Kleinherenbrink et al. (2021))
# be aware the x- and y-axis are switched in the paper
def corr_func_bist(S, kx, ky, mu=0.5, theta_t=35, theta_r=35, alpha=0,
                   R_t=900E3, R_r=900E3, V=7000, mtf='Schulz', phi_w=0.0,
                   ws=15.0):
    """
    this is the bistatic equivalent of corr_func (Kleinherenbrink et al(2021))
    S: two-dimensional directional wave spectrum (Krogstad 1992: it is not symmetrical, but directional)
    kx: wave numbers in the cross-direction (as in an FFT)
    ky: wave numbers in the along-direction (as in an FFT)
    mu: hydrodynamic relaxation rate
    theta_t, theta_r: incidence angle
    R_t, R_r: range
    V: platform velocity
    phi_w: wind direction (necessary for GMF based mtf)
    ws: wind speed (necessary for GMF based mtf)

    """
    # angular frequency and some conversions
    theta_t = np.deg2rad(theta_t)
    theta_r = np.deg2rad(theta_r)
    alpha = np.deg2rad( alpha )
    g = 9.81
    k = np.sqrt( kx ** 2 + ky ** 2 )
    omega = np.sqrt( g * k )

    # compute some additional angles (now an approximation, probably better via stereoid geometry package)
    alpha_p = np.arccos( R_t / R_r )
    if alpha < 0:
        alpha_p = -alpha_p

    # auxiliary functions
    # since I reversed order this might become messy (check this)
    dxdy = (np.sin(alpha) * np.sin(theta_r) / (np.sin(theta_t)
            + np.cos(alpha) * np.sin(theta_r))
    dydx = 1 / dxdy
    aux = -R_t / V * omega * (1 / np.cos(alpha_p) ** 2 * (
            (kx * np.cos( alpha_p ) - ky * np.sin( alpha_p )) / k * np.sin( theta_r ) + 1j * np.cos( theta_r ))
                              + (kx / k * np.sin( theta_t ) + 1j * np.cos( theta_t )))
    aux_x = 1 / (dydx * (1 + np.cos( alpha_p )) + np.sin( alpha_p ) * np.sin( theta_t ))
    aux_y = 1 / (1 + np.cos( alpha_p ) + dxdy * np.sin( alpha_p ) * np.sin( theta_t ))
    k_l = (kx * np.cos( alpha / 2 ) - ky * np.sin( alpha / 2 )) * np.cos( alpha / 2 )

    # transfer functions
    theta_m = theta_t / 2 + theta_r / 2
    T_x = aux * aux_x
    T_y = aux * aux_y

    T_I = np.zeros( k.shape )
    if mtf == 'Schulz':
        # FIXME Be careful, this one should be rigorously checked
        # I guss that (kx * np.cos( alpha / 2 ) - ky * np.sin( alpha / 2 )) ** 2 has to be scaled with np.cos( alpha / 2 )
        # and k also
        T_I = -1j * 4 * k_l / (np.tan( theta_m ) * (1 + np.sin( theta_m ) ** 2)) - 1j * k_l / np.tan(
            theta_m ) + 4.5 * omega * k_l ** 2 * (omega - 1j * mu) / (k * (omega ** 2 + mu ** 2))
    if mtf == 'S1':
        # FIXME I guess this k_l should be like below, but this should be rigorously checked
        dth = 0.001
        sigma = cmod5n.cmod5n_forward( np.array( [ ws, ws ] ), np.array( [ phi_w, phi_w ] ),
                                       np.rad2deg( np.array( [ theta_m, theta_m + dth ] ) ) )  # use CMOD5n here
        dsigma = (sigma[ 1 ] - sigma[ 0 ]) / dth
        T_I = k_l * dsigma / sigma[ 0 ] / np.cos( theta_m ) * (
                k_l / k * np.sin( theta_m ) + 1j * np.cos( theta_m ))  # combination of both equations (37)

    T_x[ T_x != T_x ] = 0
    T_y[ T_y != T_y ] = 0
    T_I[ T_I != T_I ] = 0

    # cross-spectral functions
    N_II_pos = 0.5 * T_I * np.conj( T_I )
    N_yy_pos = 0.5 * T_y * np.conj( T_y )
    N_xx_pos = 0.5 * T_x * np.conj( T_x )
    N_Iy_pos = 0.5 * T_I * np.conj( T_y )
    N_yI_pos = 0.5 * T_y * np.conj( T_I )
    N_Ix_pos = 0.5 * T_I * np.conj( T_x )
    N_xI_pos = 0.5 * T_x * np.conj( T_I )
    N_yx_pos = 0.5 * T_y * np.conj( T_x )
    N_xy_pos = 0.5 * T_x * np.conj( T_y )

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
    S_neg = np.fft.fftshift( S )
    S_neg = np.flipud( np.fliplr( S_neg ) )
    N_II_neg = np.fft.fftshift( N_II_pos )
    N_yy_neg = np.fft.fftshift( N_yy_pos )
    N_xx_neg = np.fft.fftshift( N_xx_pos )
    N_Iy_neg = np.fft.fftshift( N_Iy_pos )
    N_yI_neg = np.fft.fftshift( N_yI_pos )
    N_Ix_neg = np.fft.fftshift( N_Ix_pos )
    N_xI_neg = np.fft.fftshift( N_xI_pos )
    N_yx_neg = np.fft.fftshift( N_yx_pos )
    N_xy_neg = np.fft.fftshift( N_xy_pos )
    N_II_neg = np.flipud( np.fliplr( N_II_neg ) )
    N_yy_neg = np.flipud( np.fliplr( N_yy_neg ) )
    N_xx_neg = np.flipud( np.fliplr( N_xx_neg ) )
    N_Iy_neg = np.flipud( np.fliplr( N_Iy_neg ) )
    N_yI_neg = np.flipud( np.fliplr( N_yI_neg ) )
    N_Ix_neg = np.flipud( np.fliplr( N_Ix_neg ) )
    N_xI_neg = np.flipud( np.fliplr( N_xI_neg ) )
    N_yx_neg = np.flipud( np.fliplr( N_yx_neg ) )
    N_xy_neg = np.flipud( np.fliplr( N_xy_neg ) )
    SN_II_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_II_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_yy_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_yy_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_xx_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_xx_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_yI_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_yI_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_Iy_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_Iy_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_xI_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_xI_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_Ix_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_Ix_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_yx_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_yx_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )
    SN_xy_neg = np.fft.ifftshift( np.roll( np.roll( np.conj( N_xy_neg ) * S_neg, 1, axis = 0 ), 1, axis = 1 ) )

    # correlation functions
    rho_II = np.real( np.fft.ifft2( N_II_pos * S + SN_II_neg ) )  # / (2 * np.pi) ** 2
    rho_yy = np.real( np.fft.ifft2( N_yy_pos * S + SN_yy_neg ) )  # / (2 * np.pi) ** 2
    rho_xx = np.real( np.fft.ifft2( N_xx_pos * S + SN_xx_neg ) )  # / (2 * np.pi) ** 2
    rho_Iy = np.real( np.fft.ifft2( N_Iy_pos * S + SN_Iy_neg ) )  # / (2 * np.pi) ** 2
    rho_yI = np.real( np.fft.ifft2( N_yI_pos * S + SN_yI_neg ) )  # / (2 * np.pi) ** 2
    rho_Ix = np.real( np.fft.ifft2( N_Ix_pos * S + SN_Ix_neg ) )  # / (2 * np.pi) ** 2
    rho_xI = np.real( np.fft.ifft2( N_xI_pos * S + SN_xI_neg ) )  # / (2 * np.pi) ** 2
    rho_yx = np.real( np.fft.ifft2( N_yx_pos * S + SN_yx_neg ) )  # / (2 * np.pi) ** 2
    rho_xy = np.real( np.fft.ifft2( N_xy_pos * S + SN_xy_neg ) )  # / (2 * np.pi) ** 2

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
                  rho_xy, rho_yx, kx, ky, al = 1, be = 0,
                   we = 1, ord=4 ):  # ,rho_a,T_0,t_s):
    # rho_ab: (co)variance functions
    # kx, ky: 2D waveform grid (cross and along)
    # al: cut-off inflation parameter
    # be: cut-off inflation parameter
    # we: weight of RAR
    # ord: length of expansion

    # auxiliary
    # mu_xx = rho_xx - rho_xx[ 0, 0 ] * al - be
    # mu_yy = rho_yy - rho_yy[ 0, 0 ] * al - be
    # mu_xy = rho_xy - rho_xy[ 0, 0 ] * al - be
    # mu_yx = rho_yx - rho_yx[ 0, 0 ] * al - be

    # dx
    dk = kx[ 0, 1 ] - kx[ 0, 0 ]
    dx = 2 * np.pi / dk / len( kx )  # scene size divided by the number of samples
    x = np.arange( 0, len( kx ) * dx, dx )
    x = x.reshape( 1, len( kx ) )
    # x = np.dot(np.ones((len(kx), 1)), x)
    y = np.transpose( x )

    # it is necessary to do a non-linear mapping, so for each ky (if you include range bunching each kx also) compute
    # the Fourier transform of G and select the row belonging to ky for the spectrum
    '''
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
                S[ i, j ] = np.sum( G * DFT ) * dx * dx

    print( time.time() - start )
    # faster version
    from matplotlib import pyplot as plt
    from matplotlib.colors import LogNorm
    '''

    # faster version (using an expansion)
    S2 = np.zeros( kx.shape, dtype = complex )
    for m in range( 0, ord ):
        xfac = (kx ** 2) ** m / math.factorial( m )
        for n in range( 0, ord ):
            yfac = (ky ** 2) ** n / math.factorial( n )
            for o in range( 0, ord ):
                xy_fac = (ky * kx) ** o / math.factorial( o )

                if o + n + m < ord:
                    dS = xfac * yfac * xy_fac * np.fft.fft2(
                        rho_xx ** m * rho_yy ** n * (rho_yx + rho_xy) ** o * (1 + rho_II * we) )
                    S2 = S2 + dS

    S2 = np.exp( - kx ** 2 * (rho_xx[ 0, 0 ] * al + be) - ky ** 2 * (rho_yy[ 0, 0 ] * al + be) - ky * kx * (
                rho_yx[ 0, 0 ] * al + rho_xy[ 0, 0 ] * al + 2 * be) ) * S2 * dx * dx
    return S2


# this is a version of SAR_spec_bist to estimate the wind-wave signal + the "cut-off of wind+swell"
# FIXME: don't use this. It is not fully working and weird things are happening
def SAR_spec_bist_windwaves( wrho_II, wrho_yy, wrho_xx, wrho_xy, wrho_yx, lambda_c, kx, ky, theta_t = 35, theta_r = 35, alpha = 0, al = 1, be = 0,
                   we = 1, ord = 4 ):  # ,rho_a,T_0,t_s):
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

    # convert to radians
    theta_t = np.deg2rad( theta_t )
    theta_r = np.deg2rad( theta_r )
    alpha = np.deg2rad( alpha )

    # get the effective range direction
    alpha_range = np.arctan(
        np.sin( alpha ) * np.sin( theta_r ) / (np.sin( theta_t ) + np.cos( alpha ) * np.sin( theta_r )) )
    print(np.degrees(alpha_range))

    # estimate the variance functions
    if alpha != 0:
        # FIXME: these sines and cosines are not correct
        rho_xx0=(lambda_c/np.pi)**2/np.cos(alpha_range)**2
        rho_yy0=(lambda_c/np.pi)**2/np.sin(alpha_range)**2
        rho_xy0=(lambda_c/np.pi)**2/np.sin(alpha_range)/np.cos(alpha_range)
        rho_yx0=(lambda_c/np.pi)**2/np.sin(alpha_range)/np.cos(alpha_range)

        print( rho_xx0, rho_yy0, rho_xy0, rho_yx0 )
        print( wrho_xx[ 0, 0 ], wrho_yy[ 0, 0 ], wrho_xy[ 0, 0 ], wrho_yx[ 0, 0 ] )
    if alpha == 0:
        rho_yy0 = (lambda_c / np.pi) ** 2
        print(rho_yy0)
        print( wrho_yy[0,0] )


    # dx
    dk = kx[ 0, 1 ] - kx[ 0, 0 ]
    dx = 2 * np.pi / dk / len( kx )  # scene size divided by the number of samples
    x = np.arange( 0, len( kx ) * dx, dx )
    x = x.reshape( 1, len( kx ) )
    y = np.transpose( x )

    # faster version (using an expansion)
    if alpha != 0:
        S2 = np.zeros( kx.shape, dtype = complex )
        for m in range( 0, ord ):
            xfac = (kx ** 2) ** m / math.factorial( m )
            for n in range( 0, ord ):
                yfac = (ky ** 2) ** n / math.factorial( n )
                for o in range( 0, ord ):
                    xy_fac = (ky * kx) ** o / math.factorial( o )

                    if o + n + m < ord:
                        dS = xfac * yfac * xy_fac * np.fft.fft2(
                            wrho_xx ** m * wrho_yy ** n * (wrho_yx + wrho_xy) ** o * (1 + wrho_II * we) )
                        S2 = S2 + dS

        S2 = np.exp( - kx ** 2 * (rho_xx0 * al + be) - ky ** 2 * (rho_yy0 * al + be) - ky * kx * (
                    rho_yx0 * al + rho_xy0 * al + 2 * be) ) * S2 * dx * dx
    if alpha == 0:
        S2 = np.zeros( kx.shape, dtype = complex )
        for i in range( 0, ord ):
            S2 = S2 + 1 / math.factorial( i ) * ky ** (2 * i) * np.fft.fft2( wrho_yy ** i * (1 + wrho_II) )
        S2 = np.exp( -ky ** 2 * rho_yy0 ) * S2 * dx * dx

    return S2



# Goldfinger 1981 FIXME: still to implemented
def add_noise_Goldfinger(S_SAR, kx, ky):
    # S_SAR: SAR spectrum
    # kx,ky: across-track and along-track wave numbers


    return 0


# very simple model for noise
def add_noise_simple(S_SAR, kx, ky, alpha=0.0, beta=0.1):
    # S_SAR: SAR spectrum
    # kx,ky: across-track and along-track wave numbers
    # alpha: add a bias (scaled with mean spectrum)
    # beta: add random noise (scaled with mean spectrum)

    # wave number
    k=np.sqrt(kx**2+ky**2)

    # add some bias
    S_mean=np.mean(S_SAR[k!=0])
    S_SAR[k!=0]=S_SAR[k!=0]+np.mean(S_SAR[k!=0])*alpha

    # add some noise (just Gaussian, not really good, but for cross-spectra maybe acceptable)
    r=np.random.randn(S_SAR.shape)
    S_SAR[ k != 0 ] = S_SAR[ k != 0 ] * (1 + beta*S_mean*r[ k != 0 ])
    S_SAR[S_SAR < 0]=0

    return S_SAR


def make_SAR_spec_bist(S, kx, ky, theta_t=INC, theta_r=INC, R_t=RT, R_r=RR,
                       alpha=0):
     _corr = corr_func_bist(S, kx, ky, theta_t=theta_t, theta_r=theta_r,
                            R_t=R_t, R_r=R_r, alpha=alpha)
     _res = SAR_model.SAR_spec_bist(_corr)
     # II, yy, xx, Iy, yI, Ix, xI, xy, yx, kx, ky)
     return _res

if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    import random

    # wave numbers in a Cartesian grids (kx=cross,ky=along)
    g = 9.81
    Nk = 128
    lambda_max = 5000  # maximum wavelength (size of image)
    kx = np.ones( (1, Nk) )
    dk = 2 * np.pi / lambda_max  # fundamental frequency
    fs = lambda_max / Nk  # sampling rate
    kx[ 0, 0:int( Nk / 2 ) ] = dk * np.arange( 0, Nk / 2 )
    kx[ 0, int( Nk / 2 ): ] = dk * np.arange( -Nk / 2, 0 )
    kx = np.dot( np.ones( (Nk, 1) ), kx )
    ky = np.transpose( kx )
    lambda_y = 2 * np.pi / ky
    lambda_x = 2 * np.pi / kx
    k = np.sqrt( kx ** 2 + ky ** 2 )
    omega = np.sqrt( g * k )  # angular velocity
    phi = np.arctan2( ky, kx )  # 0 is cross-track direction waves, 90 along-track

    phi_s = np.deg2rad( 45 )  # swell direction
    f_p = 0.068  # peak frequency
    sigma_f = 0.007  # spread in frequency
    sigma_phi = np.deg2rad( 8 )  # spreadk in direction
    Hs = 1  # significant wave height
    k_p = (f_p * 2 * np.pi) ** 2 / g
    lambda_p = (2 * np.pi) / k_p
    # print(lambda_p)

    # frequency spectrum
    f = 0.5 / np.pi * np.sqrt( g * k )
    fac_f = 0.25 / np.pi * np.sqrt( g / k )
    amp = (Hs / 4) ** 2 / (sigma_f * np.sqrt( 2 * np.pi ))
    Sp = (amp * np.exp( -(f - f_p) ** 2 / (2 * sigma_f ** 2) ) + 1E-5) * fac_f

    # directional distribution
    dphi = (phi_s - phi + np.pi) % (2 * np.pi) - np.pi  # including unwrapping
    D = np.exp( -dphi ** 2 / (2 * sigma_phi ** 2) ) / (2 * np.pi * sigma_phi ** 2) ** 0.5  # directional component
    S = Sp * D / k
    S[ 0, 0 ] = 0

    # scaling
    S = S * Nk * Nk * dk * dk

    # create some kind of spectrum
    Hs = 6
    S = np.zeros( (Nk, Nk) )
    S[ 0, 4 ] = (Hs / 4) ** 2 * Nk * Nk
    # lambda_p = (2*np.pi)/(np.sqrt(kx[10,10]**2+ky[10,10]**2))
    # print(lambda_p)

    # compute the correlations
    rho_II, rho_yy, rho_Iy, rho_yI = corr_func( S, kx, ky, dk, theta = 35 )
    # rho_II, rho_yy, rho_xx, rho_Iy, rho_yI, rho_Ix, rho_xI, rho_xy, rho_yx = corr_func_bist(S, kx, ky, theta_t=35, theta_r=39, R_t=900E3, R_r=950E3, alpha=32)
    # rho_II, rho_yy, rho_xx, rho_Iy, rho_yI, rho_Ix, rho_xI, rho_xy, rho_yx = corr_func_bist( S, kx, ky, theta_t=35, theta_r=35, R_t=900E3, R_r=900E3, alpha=0 )
    # print(ky[15,0])
    print( rho_yy[ 0, 0 ] / (900E3 / 7E3) ** 2 )
    # print(Hs**2*omega[0,4])
    # plt.figure()
    plt.plot( rho_yy[ 0, : ] / (900E3 / 7E3) ** 2 )
    # plt.show()

    # plots
    '''
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.imshow((rho_II), origin='lower')
    plt.colorbar(orientation='horizontal')
    plt.subplot(2, 2, 2)
    plt.imshow((rho_yy), origin='lower')
    plt.colorbar(orientation='horizontal')
    #plt.subplot(2, 2, 3)
    #plt.imshow((rho_xx), origin='lower')
    #plt.colorbar(orientation='horizontal')
    #plt.subplot(2, 2, 4)
    #plt.imshow((rho_xy), origin='lower')
    #plt.colorbar(orientation='horizontal')
    plt.show()
    '''

    # compute the SAR spectrum
    S_SAR = SAR_spec( rho_II, rho_yy, rho_Iy, rho_yI, kx, ky )
    # S_SAR = SAR_spec_bist(rho_II, rho_yy, rho_xx, rho_Iy, rho_yI, rho_Ix, rho_xI, rho_xy, rho_yx, kx, ky)

    # plots
    S_SAR[ 0, 0 ] = 0
    # S_SAR[S_SAR == 0] = 1E-30
    # S[S == 0] = 1E-30

    # plt.figure()
    # plt.subplot(1,2,1)
    # plt.imshow(np.fft.fftshift(np.absolute(S)), origin='lower',extent=(np.min(kx),np.max(kx),np.min(ky),np.max(ky)))
    # plt.colorbar(orientation='horizontal')
    # plt.subplot(1, 2, 2)
    # plt.imshow(np.fft.fftshift(np.absolute(S_SAR)), origin='lower',extent=(np.min(kx),np.max(kx),np.min(ky),np.max(ky)))
    # plt.colorbar(orientation='horizontal')
    # plt.show()

    # compute a realization of the surface
    Im = 0.1
    x, I1, I2, SX = spec2realization( S_SAR, kx, ky, Im )

    plt.figure()
    plt.subplot( 1, 2, 1 )
    plt.imshow( np.real( x ), origin = 'lower', extent = (0, lambda_max, 0, lambda_max) )
    plt.xlabel( 'cross-track distance [km]' )
    plt.ylabel( 'along-track distance [km]' )
    plt.colorbar( orientation = 'horizontal' )
    plt.subplot( 1, 2, 2 )
    plt.imshow( np.real( I ), origin = 'lower', extent = (0, lambda_max, 0, lambda_max) )
    plt.xlabel( 'cross-track distance [km]' )
    plt.colorbar( orientation = 'horizontal' )
    plt.show()
