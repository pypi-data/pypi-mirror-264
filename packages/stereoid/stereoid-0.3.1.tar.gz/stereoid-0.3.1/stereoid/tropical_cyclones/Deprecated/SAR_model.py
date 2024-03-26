__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import stereoid.oceans.cmod5n as cmod5n


# Implementation of Engen and Johnsen (1995)
# This works with linear spacing in kx and ky, maybe we have to change this
# I will make another function for a log-scale spacing
def corr_func( S, kx, ky, mu = 0.5, theta = 35, R = 850E3, V = 7000, mtf = 'Schulz', phi_w = 0.0, ws = 15.0 ):
    # S: two-dimensional directional wave spectrum (Krogstad 1992: it is not symmetrical, but directional)
    # kx: wave numbers in the cross-direction (as in an FFT)
    # ky: wave numbers in the along-direction (as in an FFT)
    # mu: hydrodynamic relaxation rate

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
def SAR_spec( rho_II, rho_yy, rho_Iy, rho_yI, kx, ky,
              max_k = 0.2 ):  # ,rho_a,T_0,t_s): # if we want to include smearing
    # rho_ab: (co)variance functions of the
    # kx, ky: 2D waveform grid (cross and along)
    # max_k: limit the analysis to a range of wave numbers

    # dx
    dk = kx[ 0, 1 ] - kx[ 0, 0 ]
    dx = 2 * np.pi / dk / len( kx )  # scene size divided by the number of samples
    x = np.arange( 0, len( kx ) * dx, dx )
    x = x.reshape( 1, len( kx ) )
    # x = np.dot(np.ones((len(kx), 1)), x)
    y = np.transpose( x )

    # it is necessary to do a non-linear mapping, so for each ky (if you include range bunching each kx also) compute
    # the Fourier transform of G and select the row belonging to ky for the spectrum
    S = np.zeros( kx.shape, dtype = complex )
    for i in range( 0, len( ky[ :, 0 ] ) ):
        for j in range( 0, len( kx[ 0, : ] ) ):
            # this will be equation 9 in Krogstad et al. (1994) excl. the I0-term or equation 31 in Engen and Johnsen (1995)
            if np.absolute( kx[ i, j ] ) < max_k and np.absolute( ky[ i, j ] ) < max_k:
                G = np.exp( ky[ i, j ] ** 2 * (rho_yy) ) * \
                    (1 + rho_II)  # +
                # 1j * ky[i, j] * (rho_Iy - rho_yI) +
                # ky[i, j] ** 2 * (rho_Iy[i, j] - rho_Iy) * (rho_yI[i, j] - rho_yI))

                # take the 'dft of G' (for one frequency)
                DFT = np.exp( ky[ i, j ] ** 2 * (-rho_yy[ 0, 0 ]) ) * np.outer( np.exp( -1j * ky[ i, j ] * y ),
                                                                                np.exp( -1j * kx[ i, j ] * x ) )
                S[ i, j ] = np.sum( G * DFT ) * dx * dx
    return S


# this is the bistatic equivalent of corr_func (Kleinherenbrink et al. (2021))
# be aware the x- and y-axis are switched in the paper
def corr_func_bist( S, kx, ky, mu = 0.5, theta_t = 35, theta_r = 35, alpha = 0, R_t = 900E3, R_r = 900E3, V = 7000,
                    mtf = 'Schulz', phi_w = 0.0, ws = 15.0 ):
    # S: two-dimensional directional wave spectrum (Krogstad 1992: it is not symmetrical, but directional)
    # kx: wave numbers in the cross-direction (as in an FFT)
    # ky: wave numbers in the along-direction (as in an FFT)
    # mu: hydrodynamic relaxation rate

    # angular frequency and some conversions
    theta_t = np.deg2rad( theta_t )
    theta_r = np.deg2rad( theta_r )
    alpha = np.deg2rad( alpha )
    g = 9.81
    k = np.sqrt( kx ** 2 + ky ** 2 )
    omega = np.sqrt( g * k )

    # compute some additional angles (now an approximation, probably better via stereoid geometry package)
    alpha_p = np.arccos( R_t / R_r )
    if alpha < 0:
        alpha_p = -alpha_p

    # auxiliary functions
    dxdy = np.sin( alpha ) * np.sin( theta_r ) / (np.sin( theta_t ) + np.cos( alpha ) * np.sin(
        theta_r ))  # since I reversed order this might become messy (check this)
    dydx = 1 / dxdy
    aux = -R_t / V * omega * (1 / np.cos( alpha_p ) ** 2 * (
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
def SAR_spec_bist( rho_II, rho_yy, rho_xx, rho_Iy, rho_yI, rho_Ix, rho_xI, rho_xy, rho_yx, kx, ky,
                   max_k = 0.2 ):  # ,rho_a,T_0,t_s):
    # rho_ab: (co)variance functions
    # kx, ky: 2D waveform grid (cross and along)
    # max_k: limit the analysis to a range of wave numbers

    # auxiliary
    mu_xx = rho_xx - rho_xx[ 0, 0 ]
    mu_yy = rho_yy - rho_yy[ 0, 0 ]
    mu_xy = rho_xy - rho_xy[ 0, 0 ]
    mu_yx = rho_yx - rho_yx[ 0, 0 ]

    # dx
    dk = kx[ 0, 1 ] - kx[ 0, 0 ]
    dx = 2 * np.pi / dk / len( kx )  # scene size divided by the number of samples
    x = np.arange( 0, len( kx ) * dx, dx )
    x = x.reshape( 1, len( kx ) )
    # x = np.dot(np.ones((len(kx), 1)), x)
    y = np.transpose( x )

    # it is necessary to do a non-linear mapping, so for each ky (if you include range bunching each kx also) compute
    # the Fourier transform of G and select the row belonging to ky for the spectrum
    S = np.zeros( kx.shape, dtype = complex )
    for i in range( 0, len( ky[ :, 0 ] ) ):
        for j in range( 0, len( kx[ 0, : ] ) ):
            # this will be equation 9 in Krogstad et al. (1994) excl. the I0-term or equation 31 in Engen and Johnsen (1995)
            if np.absolute( kx[ i, j ] ) < max_k and np.absolute( ky[ i, j ] ) < max_k:
                G = np.exp(
                    ky[ i, j ] ** 2 * mu_yy + kx[ i, j ] ** 2 * mu_xx + ky[ i, j ] * kx[ i, j ] * (mu_xy + mu_yx) ) * \
                    (1 + rho_II)  # + \
                # 1j * ky[i, j] * (rho_Iy - rho_yI) + \
                # ky[i, j] ** 2 * (rho_Iy- rho_Iy[0, 0] ) * (rho_yI - rho_yI[0, 0] ) + \
                # 1j * kx[i, j] * (rho_Ix - rho_xI) +\
                # kx[i, j] ** 2 * (rho_Ix - rho_Ix[0, 0]) * (rho_xI - rho_xI[0, 0]) + \
                # kx[i, j] * ky[i, j] * (rho_Ix - rho_Ix[0, 0]) * (rho_yI - rho_yI[0, 0]) + \
                # kx[i, j] * ky[i, j] * (rho_Iy - rho_Iy[0, 0]) * (rho_xI - rho_xI[0, 0]) )

                DFT = np.outer( np.exp( -1j * ky[ i, j ] * y ), np.exp( -1j * kx[ i, j ] * x ) )
                S[ i, j ] = np.sum( G * DFT ) * dx * dx

    return S


# compute a realization from the SAR spectrum
# not tested yet (the phases cannot be completely random)
def spec2realization( S, kx, ky, I0 ):
    # S: two-dimensional SAR spectrum (normalized as periodogram)
    # kx: cross-track wavenumber
    # ky: along-track wavenumber
    # IO: mean backscatter

    # note that we assume a spectrum of Nk*Nk

    # from spectrum to magnitudes
    Nk = len( kx[ :, 0 ] )
    X = np.sqrt( S * Nk * Nk )

    # we have to add some random phase
    phasor = np.zeros( (Nk, Nk), dtype = 'complex_' )
    Np = int( Nk / 2 ) - 1
    Nn = int( Nk / 2 )
    # four quadrants
    phasor[ 1:Nn, 1:Nn ] = np.exp( 1j * 2 * np.pi * np.random.random( (Np, Np) ) )  # pos-pos
    phasor[ Nn + 1:, Nn + 1: ] = np.conjugate( np.flipud( np.fliplr( phasor[ 1:Nn, 1:Nn ] ) ) )  # neg-neg
    phasor[ 1:Nn, Nn + 1: ] = np.exp( 1j * 2 * np.pi * np.random.random( (Np, Np) ) )  # pos ky - neg kx
    phasor[ Nn + 1:, 1:Nn ] = np.conjugate( np.flipud( np.fliplr( phasor[ 1:Nn, Nn + 1: ] ) ) )  # neg ky - pos kx
    # zero frequency
    phasor[ 0, 1:Nn ] = np.exp( 1j * 2 * np.pi * np.random.random( (1, Np) ) )
    phasor[ 0, Nn + 1: ] = np.conjugate( np.flipud( phasor[ 0, 1:Nn ] ) )
    phasor[ 1:Nn, 0 ] = np.exp( 1j * 2 * np.pi * np.random.random( (Np, 1) ) ).T
    phasor[ Nn + 1:, 0 ] = np.conjugate( np.flipud( phasor[ 1:Nn, 0 ] ) )

    # phasor
    # phasor=np.exp(1j*(kx+ky))

    # add phase
    X = X * phasor

    # into the distance domain
    x = np.fft.ifft2( X )

    # lets pretend to have an distribution for the intensity
    Irel1 = 0.5 * np.abs( (np.random.randn( Nk, Nk ) + 1j * np.random.randn( Nk, Nk )) ** 2 )
    Irel2 = 0.5 * np.abs( (np.random.randn( Nk, Nk ) + 1j * np.random.randn( Nk, Nk )) ** 2 )

    # go to intensity
    I1 = (x * I0 + I0) * Irel1
    I2 = (x * I0 + I0) * Irel1

    # we can also go back to the cross-spectrum
    x1 = (I1 - I0) / I0
    x2 = (I2 - I0) / I0
    X1 = np.fft.fft2( x1 )
    X2 = np.fft.fft2( x2 )
    SX = np.absolute( X1 * np.conj( X2 ) )

    return x, I1, I2, SX


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
