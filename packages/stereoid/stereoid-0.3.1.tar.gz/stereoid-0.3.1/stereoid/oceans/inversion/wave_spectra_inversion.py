__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
from stereoid.oceans.waves.wave_spectra import elfouhaily
from stereoid.oceans.waves.wave_spectra import elfouhaily_spread
from stereoid.oceans.waves.wave_spectra import Kudry_spec
from stereoid.oceans.forward_models import SAR_spectra as SAR_model
from skimage.feature import peak_local_max

# this function couples swell parameter ('y') to spectral moments by testing various models
# FIXME: var has no axis 'order' or (Nm). It is possible a design matrix is made with multiple times var in the columns.
def find_best_fit( y, spectral_moments, cut_off, pols=[0,4,5], Nm=3, NoM=4, NoM_co=2, Na=10):
    """

    Parameters
    ----------
    y: vector of swell parameters (for example: k_s, k_s*cos(phi_s), phi_s, sigma_phi, etc.)
    spectral_moments: distionary of spectral moments ('Kx','Ky','var',...) with axes [pols,Nm,len(y)]
    cut_off: cut-offs with axis [pols,len(y)]
    pols: polarization you want to use, normally 3 sats x 2 pols = 6 pols available
    Nm: order of the moments/moment arms
    NoM: number of unw. moments you want to use in the model (total parameters: NoM*len(pols), unless 'var' is a moment)
    NoM_co: number cut-off weighted moments you want to use
    Na: number of models to try

    Returns
    -------

    """

    # spectral moment names
    moments=list( spectral_moments.keys() )
    Ns=len(y)

    # this thing searches automatically for the best result
    save_ind = np.zeros( (len( moments ), Nm, Na) )
    save_ind_co = np.zeros( (len( moments ), Nm, Na) )
    sigma_unb = np.zeros( Na )
    for l in range( 0, Na ):
        # I gives a selection of moments to be used
        rnd = np.random.rand( len( moments ), Nm )
        I = rnd < np.sort( rnd.ravel() )[ NoM ]
        save_ind[ :, :, l ] = rnd

        # I2 gives a selection of cut-off weighted moments to be used
        rnd = np.random.rand( len( moments ), Nm )
        I2 = rnd < np.sort( rnd.ravel() )[ NoM_co ]
        save_ind_co[ :, :, l ] = rnd

        # construct a design matrix
        A=construct_model( moments, spectral_moments, cut_off, pols, Nm, Ns, I, I2 )

        # regression
        Ival=range(0,len(y))
        emax = 10
        std_e = 3
        while emax > 3 * std_e:
            xhat, yhat, ehat, varN, dof=estimate_model_parameters(y[Ival],A[Ival,:])
            sigma_unb[l]=varN/dof

            # handle outliers
            emax=np.max(np.absolute(ehat))
            std_e=np.sqrt(sigma_unb[l])
            if emax > 3 *std_e:
                Ival=np.delete(Ival,np.argmax(np.absolute(ehat)))



    # select the best model
    J=np.argmin(sigma_unb)
    rnd=save_ind[:,:,J]
    I = rnd < np.sort( rnd.ravel() )[ NoM ]
    rnd = save_ind_co[ :, :, J ]
    I2 = rnd < np.sort( rnd.ravel() )[ NoM_co ]

    # recompute the best model
    A = construct_model( moments, spectral_moments, cut_off, pols, Nm, Ns, I, I2 )
    Ival = range(0, len(y))
    emax = 10
    std_e = 3
    while emax > 3 * std_e:
        xhat, yhat, ehat, varN, dof = estimate_model_parameters(y[Ival], A[Ival, :])
        sigma_unb[l] = varN / dof

        # handle outliers
        emax = np.max(np.absolute(ehat))
        std_e = np.sqrt(sigma_unb[l])
        if emax > 3 * std_e:
            Ival = np.delete(Ival, np.argmax(np.absolute(ehat)))


    return xhat, yhat, ehat, varN, dof, I, I2, Ival

# this method is called by find_best_fit and constructs a design matrix
def construct_model(moments,spectral_moments,cut_off,pols,Nm,Ns,I,I2):
    """

    Parameters
    ----------
    moments
    spectral_moments
    cut_off
    pols
    Nm
    Ns
    I: indices of moments to be used
    I2: indices of moments weighted by the cut-off to be used

    Returns
    -------
    A
    """
    k = 0
    for i in range( 0, len( moments ) ):
        for j in range( 0, Nm ):
            if I[ i, j ]:
                if k == 0:
                    k = k + 1
                    if moments[ i ] == 'var':
                        A = spectral_moments[ moments[ i ] ][ pols, : ].reshape( Ns, len(pols) )
                    else:
                        A = spectral_moments[ moments[ i ] ][ pols, j, : ].T
                else:
                    k = k + 1
                    if moments[ i ] == 'var':
                        A = np.concatenate( (A, spectral_moments[ moments[ i ] ][ pols, : ].reshape( Ns, len(pols) )),
                                            axis = 1 )
                    else:
                        A = np.concatenate( (A, spectral_moments[ moments[ i ] ][ pols, j, : ].T), axis = 1 )

            if I2[ i, j ]:
                if k == 0:
                    k = k + 1
                    if moments[ i ] == 'var':
                        A = cut_off[ pols, : ].T ** j
                    else:
                        A = spectral_moments[ moments[ i ] ][ pols, j, : ].T * cut_off[ pols, : ].T ** j
                else:
                    k = k + 1
                    if moments[ i ] == 'var':
                        A = np.concatenate( (A, cut_off[ pols, : ].T ** j), axis = 1 )
                    else:
                        A = np.concatenate(
                            (A, spectral_moments[ moments[ i ] ][ pols, j, : ].T * cut_off[ pols, : ].T ** j),
                            axis = 1 )

    return A

# do a simple least-squares
def estimate_model_parameters( y, A ):
    """
    Parameters
    ----------
    y: model input (example k_s*np.sin(phi_s))
    A: design matrix with spectral parameters (moments, cutoff or a combination)

    Returns
    -------
    xhat: model parameters
    yhat: model fit
    ehat: residuals
    varN: rms**2 of residuals * N
    dof: degrees-of-freedom
    """

    # degrees of freedom
    shp = A.shape
    dof = shp[ 0 ] - shp[ 1 ]

    # least-squares
    xhat = np.linalg.lstsq( A, y )
    yhat = A.dot( xhat[ 0 ] )
    ehat = y - yhat

    # standard deviation
    varN = np.sum( ehat ** 2 )

    return xhat, yhat, ehat, varN, dof

# forward model
def apply_model( A, xhat, y = np.zeros( 2 ) ):
    """
    Parameters
    ----------
    xhat: model parameters
    A: design matrix with spectral parameters (moments, cutoff or a combination)

    Optional input
    ----------
    y: model input (example k_s*np.sin(phi_s))

    ---------------------------------------------------------------
    Returns
    -------
    yhat: model fit

    Optional returns
    ----------
    ehat: residuals
    varN: rms**2 of residuals * N
    dof: degrees-of-freedom
    """

    # degrees of freedom
    shp = A.shape
    dof = shp[ 0 ] - shp[ 1 ]

    # errors
    yhat = A.dot( xhat )

    if np.mean( y ** 2 ) != 0:
        ehat = y - yhat

        # standard deviation
        varN = np.sum( ehat ** 2 )

        return yhat, ehat, varN, dof

    if np.mean( y ** 2 ) == 0:
        return yhat


# this computes spectra and cross-spectra if there would be a wind-wave system only
# set lambda_c is you want to use another cut-off (currently not implemented)
def wind_wave_correction( obsgeo, inc_m, kx, ky, kx_ku, ky_ku, u10, phi_w, fetch, n, cross = True, noise = False,
                          ord = 4, lambda_c = 0 ):
    """

    Parameters
    ----------
    obsgeo
    inc_m
    kx
    ky
    kx_ku
    ky_ku
    u10
    phi_w
    fetch
    n
    cross
    noise
    ord
    lambda_c

    Returns
    -------
    co_spectra: co_spectra of wind waves only
    cr_spectra: cr_spectra of wind waves only

    """

    if lambda_c != 0:
        print( "This option is currently not implemented!" )

    # 'long-wave' spectrum for the SAR spectra
    SHP = kx.shape
    dkx = kx[ 0, 1 ] - kx[ 0, 0 ]
    dky = ky[ 1, 0 ] - ky[ 0, 0 ]
    k = np.sqrt( kx ** 2 + ky ** 2 )
    phi_k = np.arctan2( ky, kx )
    dphi = phi_k - phi_w
    dphi = np.angle( np.exp( 1j * dphi ) )
    S = np.where( k > 0, elfouhaily_spread( k, dphi, u10, fetch ) * elfouhaily( k, u10, fetch ) / k, 0 )
    S = S * dkx * dky * SHP[ 0 ] * SHP[ 1 ]  # normalization for the ffts

    # 'short-wave' spectrum for the modulation transfer functions
    k_ku = np.sqrt( kx_ku ** 2 + ky_ku ** 2 )
    dk_ku = np.gradient( kx_ku[ 0, : ] )
    dks_ku = np.outer( dk_ku, dk_ku )
    B, _, _, _ = Kudry_spec( kx_ku, ky_ku, u10, fetch, phi_w, dks_ku )
    S_ku = np.where( k_ku > 0, B * k_ku ** -4, 0 )

    wn_grid = {"S": S, "k_x": kx, "k_y": ky}
    wn = {"S": S_ku, "k_x": kx_ku, "k_y": ky_ku, "dks": dks_ku}
    return SAR_model.run_spectra_SWB( obsgeo, inc_m, wn_grid, wn, u10, phi_w, n, cross = cross,
                                      noise = noise,
                                      nord = ord )


# this corrects all spectra (and/or absolute cross_spectra) for the wind-wave signal
def apply_wind_wave_correction( spec, spec_wind, polbase = [ 'm', 'M' ] ):
    """

    Parameters
    ----------
    spec: absolute values of a (cross-)spectrum
    spec_wind: absolute values of a wind only (cross-)spectrum
    polbase: polarization basis

    Returns
    -------
    spec_corr:
    """

    # make a dictionary for the corrected spectrum
    shp = spec[ 'S1' ][ 'V' ].shape
    spec_corr = { "S1": { }, "HA": { }, "HB": { } }
    for key in spec.keys():
        if key == "S1":
            spec_corr[ key ] = { "H": np.zeros( shp ), "V": np.zeros( shp ) }

        else:
            spec_corr[ key ] = { polbase[ 0 ]: np.zeros( shp ), polbase[ 1 ]: np.zeros( shp ) }

    # corrected spectrum
    spec_corr[ 'S1' ][ 'V' ] = np.absolute( spec[ 'S1' ][ 'V' ] ) - np.absolute( spec_wind[ 'S1' ][ 'V' ] )
    spec_corr[ 'S1' ][ 'H' ] = np.absolute( spec[ 'S1' ][ 'H' ] ) - np.absolute( spec_wind[ 'S1' ][ 'H' ] )
    spec_corr[ 'HA' ][ 'M' ] = np.absolute( spec[ 'HA' ][ 'M' ] ) - np.absolute( spec_wind[ 'HA' ][ 'M' ] )
    spec_corr[ 'HA' ][ 'm' ] = np.absolute( spec[ 'HA' ][ 'm' ] ) - np.absolute( spec_wind[ 'HA' ][ 'm' ] )
    spec_corr[ 'HB' ][ 'M' ] = np.absolute( spec[ 'HB' ][ 'M' ] ) - np.absolute( spec_wind[ 'HB' ][ 'M' ] )
    spec_corr[ 'HB' ][ 'm' ] = np.absolute( spec[ 'HB' ][ 'm' ] ) - np.absolute( spec_wind[ 'HB' ][ 'm' ] )

    # handle negative values
    spec_corr[ 'S1' ][ 'V' ][ spec_corr[ 'S1' ][ 'V' ] < 0 ] = 0
    spec_corr[ 'S1' ][ 'H' ][ spec_corr[ 'S1' ][ 'H' ] < 0 ] = 0
    spec_corr[ 'HA' ][ 'M' ][ spec_corr[ 'HA' ][ 'M' ] < 0 ] = 0
    spec_corr[ 'HA' ][ 'm' ][ spec_corr[ 'HA' ][ 'm' ] < 0 ] = 0
    spec_corr[ 'HB' ][ 'M' ][ spec_corr[ 'HB' ][ 'M' ] < 0 ] = 0
    spec_corr[ 'HB' ][ 'm' ][ spec_corr[ 'HB' ][ 'm' ] < 0 ] = 0

    return spec_corr


# crops away part of the spectrum
# also performs an fftshift
def crop_spec( spec, kx, ky, kx_lim = 2 * np.pi / 150, ky_lim = 2 * np.pi / 150, polbase = [ 'm', 'M' ], abso = 1 ):
    """

    Parameters
    ----------
    spec
    kx
    ky
    kx_lim
    ky_lim
    polbase
    abso

    Returns
    -------
    spec_crop
    kx_sh
    ky_sh
    """

    # do an fftshift an make new vectors
    kx_sh = np.fft.fftshift( kx )
    ky_sh = np.fft.fftshift( ky )
    Ix = np.absolute( kx_sh[ 0, : ] ) < kx_lim
    Iy = np.absolute( ky_sh[ :, 0 ] ) < ky_lim
    kx_sh = kx_sh[ :, Ix ]
    ky_sh = ky_sh[ :, Ix ]
    kx_sh = kx_sh[ Iy, : ]
    ky_sh = ky_sh[ Iy, : ]

    # make a dictionary for the corrected spectrum
    shp = spec[ 'S1' ][ 'V' ].shape
    spec_crop = { "S1": { }, "HA": { }, "HB": { } }
    for key in spec.keys():
        if key == "S1":
            if abso == 1:
                spec_crop[ key ] = { "H": np.zeros( shp ), "V": np.zeros( shp ) }
            else:
                spec_crop[ key ] = { "H": np.zeros( shp, dtype = 'complex' ), "V": np.zeros( shp, dtype = 'complex' ) }

        else:
            if abso == 1:
                spec_crop[ key ] = { polbase[ 0 ]: np.zeros( shp ),
                                     polbase[ 1 ]: np.zeros( shp ) }
            else:
                spec_crop[ key ] = { polbase[ 0 ]: np.zeros( shp, dtype = 'complex' ),
                                     polbase[ 1 ]: np.zeros( shp, dtype = 'complex' ) }

    # crop
    if abso == 1:
        spec_temp = np.fft.fftshift( np.absolute( spec[ 'S1' ][ 'V' ] ) )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'S1' ][ 'V' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( np.absolute( spec[ 'S1' ][ 'H' ] ) )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'S1' ][ 'H' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( np.absolute( spec[ 'HA' ][ 'm' ] ) )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HA' ][ 'm' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( np.absolute( spec[ 'HA' ][ 'M' ] ) )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HA' ][ 'M' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( np.absolute( spec[ 'HB' ][ 'm' ] ) )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HB' ][ 'm' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( np.absolute( spec[ 'HB' ][ 'M' ] ) )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HB' ][ 'M' ] = spec_temp[ Iy, : ]
    else:
        spec_temp = np.fft.fftshift( spec[ 'S1' ][ 'V' ] )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'S1' ][ 'V' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( spec[ 'S1' ][ 'H' ] )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'S1' ][ 'H' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( spec[ 'HA' ][ 'm' ] )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HA' ][ 'm' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( spec[ 'HA' ][ 'M' ] )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HA' ][ 'M' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( spec[ 'HB' ][ 'm' ] )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HB' ][ 'm' ] = spec_temp[ Iy, : ]
        spec_temp = np.fft.fftshift( spec[ 'HB' ][ 'M' ] )
        spec_temp = spec_temp[ :, Ix ]
        spec_crop[ 'HB' ][ 'M' ] = spec_temp[ Iy, : ]

    return spec_crop, kx_sh, ky_sh


# this method filters the spectrum
def filter_Gauss( spec, sx, sy, nx = 3, ny = 3, polbase = [ 'm', 'M' ], abso = 1 ):
    """

    Parameters
    ----------
    spec: input spectra (dictionary)
    sx: 'standard deviation' x-direction (integer)
    sy: 'standard deviation' y-direction (integer)
    nx: number of standard deviation filter width (integer)
    ny: number of standard deviation filter width (integer)
    abso: set to 1 to take absolute values

    Returns
    -------

    """
    # make a dictionary for the corrected spectrum
    shp = spec[ 'S1' ][ 'V' ].shape
    spec_filt = { "S1": { }, "HA": { }, "HB": { } }
    for key in spec.keys():
        if key == "S1":
            if abso == 1:
                spec_filt[ key ] = { "H": np.zeros( shp ), "V": np.zeros( shp ) }
            else:
                spec_filt[ key ] = { "H": np.zeros( shp, dtype = 'complex' ), "V": np.zeros( shp, dtype = 'complex' ) }

        else:
            if abso == 1:
                spec_filt[ key ] = { polbase[ 0 ]: np.zeros( shp ), polbase[ 1 ]: np.zeros( shp ) }
            else:
                spec_filt[ key ] = { polbase[ 0 ]: np.zeros( shp, dtype = 'complex' ),
                                     polbase[ 1 ]: np.zeros( shp, dtype = 'complex' ) }

    # make filter kernel
    x = np.arange( -sx * nx, sx * nx + 1 )
    filt_x = np.exp( -x ** 2 / sx ** 2 )
    y = np.arange( -sy * ny, sy * ny + 1 )
    filt_y = np.exp( -y ** 2 / sy ** 2 )
    filt = np.outer( filt_y, filt_x )
    filt = filt / np.sum( filt )

    # apply filter
    if abso == 1:
        spec_filt[ 'S1' ][ 'V' ] = conv2( np.absolute( spec[ 'S1' ][ 'V' ] ), filt, mode = 'same' )
        spec_filt[ 'S1' ][ 'H' ] = conv2( np.absolute( spec[ 'S1' ][ 'H' ] ), filt, mode = 'same' )
        spec_filt[ 'HA' ][ 'm' ] = conv2( np.absolute( spec[ 'HA' ][ 'm' ] ), filt, mode = 'same' )
        spec_filt[ 'HA' ][ 'M' ] = conv2( np.absolute( spec[ 'HA' ][ 'M' ] ), filt, mode = 'same' )
        spec_filt[ 'HB' ][ 'm' ] = conv2( np.absolute( spec[ 'HB' ][ 'm' ] ), filt, mode = 'same' )
        spec_filt[ 'HB' ][ 'M' ] = conv2( np.absolute( spec[ 'HB' ][ 'M' ] ), filt, mode = 'same' )

    else:
        spec_filt[ 'S1' ][ 'V' ] = conv2( spec[ 'S1' ][ 'V' ], filt, mode = 'same' )
        spec_filt[ 'S1' ][ 'H' ] = conv2( spec[ 'S1' ][ 'H' ], filt, mode = 'same' )
        spec_filt[ 'HA' ][ 'm' ] = conv2( spec[ 'HA' ][ 'm' ], filt, mode = 'same' )
        spec_filt[ 'HA' ][ 'M' ] = conv2( spec[ 'HA' ][ 'M' ], filt, mode = 'same' )
        spec_filt[ 'HB' ][ 'm' ] = conv2( spec[ 'HB' ][ 'm' ], filt, mode = 'same' )
        spec_filt[ 'HB' ][ 'M' ] = conv2( spec[ 'HB' ][ 'M' ], filt, mode = 'same' )

    return spec_filt


from scipy.signal import convolve2d


def conv2( x, y, mode = 'same' ):
    return np.rot90( convolve2d( np.rot90( x, 2 ), np.rot90( y, 2 ), mode = mode ), 2 )


# first estimate of local swell peaks and checks if swell is present
def swell_peaks_rough( spec, crspec, kx, ky, min_distance, polbase = [ 'm', 'M' ] ):
    """

    Parameters
    ----------
    spec
    crspec
    kx
    ky
    min_distance
    polbase

    Returns
    -------

    """

    # direction
    #phi = np.arctan2( ky, kx )

    # make dict
    spec_peaks = { "S1": { }, "HA": { }, "HB": { } }
    for key in spec.keys():
        if key == "S1":
            spec_peaks[ key ] = { "H": peak_local_max( spec[ 'S1' ][ 'H' ], min_distance ),
                                  "V": peak_local_max( spec[ 'S1' ][ 'V' ], min_distance ) }
        else:
            spec_peaks[ key ] = { polbase[ 0 ]: peak_local_max( spec[ key ][ polbase[ 0 ] ], min_distance ),
                                  polbase[ 1 ]: peak_local_max( spec[ key ][ polbase[ 1 ] ], min_distance ) }

    # this makes it just easier
    sats = [ "S1", "HA", "HB", "S1", "HA", "HB" ]
    pols = [ "V", polbase[ 0 ], polbase[ 0 ], "H", polbase[ 1 ], polbase[ 1 ] ]

    # keep the two biggest values
    # FIXME: we assume there are only two peaks belonging to one swell spectrum
    for i in range(0,len(sats)):
        peak_vals = spec[ sats[i] ][ pols[i] ][ spec_peaks[ sats[i] ][ pols[i] ][ :, 0 ], spec_peaks[ sats[i] ][ pols[i] ][ :, 1 ] ]
        I=np.flip(np.argsort(peak_vals))
        spec_peaks[ sats[i] ][ pols[i] ] = spec_peaks[ sats[i] ][ pols[i] ][ I[0:2], : ]

    # reorder the peaks to their respective direction (so we have matching peaks)
    #print( 'check values' )
    for i in range(0,len(sats)):
        if i == 0:
            kx_ref = kx[ spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 0 ], spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 1 ] ][
                0 ]
            ky_ref = ky[ spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 0 ], spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 1 ] ][
                0 ]
            #print( spec_peaks[ sats[ i ] ][ pols[ i ] ] )
        else:
            kx_p = kx[ spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 0 ], spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 1 ] ]
            ky_p = ky[ spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 0 ], spec_peaks[ sats[ i ] ][ pols[ i ] ][ :, 1 ] ]
            k_dist=np.sqrt((kx_ref-kx_p)**2 + (ky_ref-ky_p)**2)
            I=np.argsort(k_dist)
            spec_peaks[ sats[i] ][ pols[i] ] = spec_peaks[ sats[i] ][ pols[i] ][ I, : ]
            #print( spec_peaks[ sats[i] ][ pols[i] ] )
    #print(spec_peaks)
    # use the imaginary values to determine wave direction
    # FIXME: we assume that a negative imaginary value is the wave direction
    # '''
    im_vals=np.zeros((6,spec_peaks[ 'HB' ][ 'M' ].shape[0]))
    im_vals[0,:] = np.imag(crspec[ 'S1' ][ 'V' ][ spec_peaks[ 'S1' ][ 'V' ][ :, 0 ], spec_peaks[ 'S1' ][ 'V' ][ :, 1 ] ])
    im_vals[1,:] = np.imag(crspec[ 'S1' ][ 'H' ][ spec_peaks[ 'S1' ][ 'H' ][ :, 0 ], spec_peaks[ 'S1' ][ 'H' ][ :, 1 ] ])
    im_vals[2,:] = np.imag(crspec[ 'HA' ][ 'm' ][ spec_peaks[ 'HA' ][ 'm' ][ :, 0 ], spec_peaks[ 'HA' ][ 'm' ][ :, 1 ] ])
    im_vals[3,:] = np.imag(crspec[ 'HA' ][ 'M' ][ spec_peaks[ 'HA' ][ 'M' ][ :, 0 ], spec_peaks[ 'HA' ][ 'M' ][ :, 1 ] ])
    im_vals[4,:] = np.imag(crspec[ 'HB' ][ 'm' ][ spec_peaks[ 'HB' ][ 'm' ][ :, 0 ], spec_peaks[ 'HB' ][ 'm' ][ :, 1 ] ])
    im_vals[5,:] = np.imag(crspec[ 'HB' ][ 'M' ][ spec_peaks[ 'HB' ][ 'M' ][ :, 0 ], spec_peaks[ 'HB' ][ 'M' ][ :, 1 ] ])
    #print(im_vals)
    im_mean=np.mean(im_vals,axis=0)
    Im=np.argmin(im_mean)
    #print(Im)
    #print(spec_peaks[ 'S1' ][ 'V' ][ Im, : ].shape)
    #print(spec_peaks[ 'S1' ][ 'V' ].shape)
    spec_peaks[ 'S1' ][ 'V' ] = spec_peaks[ 'S1' ][ 'V' ][ Im, : ].reshape(1,2)
    spec_peaks[ 'S1' ][ 'H' ] = spec_peaks[ 'S1' ][ 'H' ][ Im, : ].reshape(1,2)
    spec_peaks[ 'HA' ][ 'm' ] = spec_peaks[ 'HA' ][ 'm' ][ Im, : ].reshape(1,2)
    spec_peaks[ 'HA' ][ 'M' ] = spec_peaks[ 'HA' ][ 'M' ][ Im, : ].reshape(1,2)
    spec_peaks[ 'HB' ][ 'm' ] = spec_peaks[ 'HB' ][ 'm' ][ Im, : ].reshape(1,2)
    spec_peaks[ 'HB' ][ 'M' ] = spec_peaks[ 'HB' ][ 'M' ][ Im, : ].reshape(1,2)
    # '''
    #print(spec_peaks)
    #from matplotlib import pyplot as plt
    #plt.imshow(np.imag(crspec['S1']['V']))
    #plt.show()

    # make some flag to indicate whether there is 0, 1, 2 swell system present (based on energy on something)
    # FIXME: not done yet
    swell_flag = 1

    return spec_peaks, swell_flag

# this method masks the spectrum, so that it is more adequate for the computation of spectral moments
# FIXME: assumes only one peak is left at the moment
def spec_mask(spec,spec_peaks, kx,ky,kmin=0,kmax=2*np.pi/150,phi_lim=np.pi/4,polbase=['m','M']):
    """

    Parameters
    ----------
    spec
    spec_peaks
    kx
    ky
    kmin
    kmax
    phi_lim

    Returns
    -------

    """

    # wave numbers and directions
    k=np.sqrt(kx**2+ky**2)
    phi=np.arctan2(ky,kx)

    # make a dictionary for the corrected spectrum
    shp = spec[ 'S1' ][ 'V' ].shape
    spec_masked = { "S1": { }, "HA": { }, "HB": { } }
    for key in spec.keys():
        if key == "S1":
            spec_masked[ key ] = { "H": np.zeros( shp ), "V": np.zeros( shp ) }

        else:
            spec_masked[ key ] = { polbase[ 0 ]: np.zeros( shp ), polbase[ 1 ]: np.zeros( shp ) }

    # this makes it just easier
    sats = [ "S1", "HA", "HB", "S1", "HA", "HB" ]
    pols = [ "V", polbase[ 0 ], polbase[ 0 ], "H", polbase[ 1 ], polbase[ 1 ] ]

    for i in range(0,len(sats)):

        # compute reference wavenumber and direction (belonging to the peak)
        pks = spec_peaks[ sats[ i ] ][ pols[ i ] ]
        kx_ref = kx[ pks[ 0 ][ 0 ], pks[ 0 ][ 1 ] ]
        ky_ref = ky[ pks[ 0 ][ 0 ], pks[ 0 ][ 1 ] ]
        k_ref = np.sqrt( kx_ref ** 2 + ky_ref ** 2 )
        phi_ref = np.arctan2( ky_ref, kx_ref )
        dphi=np.angle(np.exp(1j*(phi - phi_ref)))

        if kmin == 0:
            kmin=k_ref / 2

        # mask spectrum
        I = np.logical_and( np.logical_and( k > kmin, k < kmax ), np.absolute( dphi ) < np.pi / 4 )
        spec_masked[sats[i]][pols[i]]=I*spec[sats[i]][pols[i]]

    return spec_masked


# computes moments
# FIXME: assumes only one peak is left at the moment
def compute_spectral_moments( spec, spec_peaks, kx, ky, ord = 3, polbase = [ 'm', 'M' ], multi_static = 1 ):
    """

    Parameters
    ----------
    spec: (masked) spectrum
    spec_peaks: at the moment only accepts a single spectral peak
    kx
    ky
    ord: number of moments
    polbase
    multi_static

    Returns
    -------
    spec_mom
    """

    # number of moments
    if multi_static == 1:
        sats = [ "S1", "HA", "HB" ]
    else:
        sats = [ "S1" ]
    Ns = int( len( sats ) * len( polbase ) )  # number of spectra
    Nm = int( ord * 1 )  # order of moments

    # create moment structure (we may now forget about the spectra structure)
    spec_mom = { "K": np.zeros( (Ns, Nm) ), "Kx": np.zeros( (Ns, Nm) ), "Ky": np.zeros( (Ns, Nm) ),
                 "K_rel": np.zeros( (Ns, Nm) ), "phi_rel": np.zeros( (Ns, Nm) ), "var": np.zeros( Ns ),
                 "M": np.zeros( (Ns, Nm) ), "Mx": np.zeros( (Ns, Nm) ), "My": np.zeros( (Ns, Nm) ) }

    # some spectral information
    k=np.sqrt(kx**2+ky**2)
    phi=np.arctan2(ky,kx)
    dk=kx[0,1]-kx[0,0]

    # this makes it just easier
    sats=[ "S1", "HA", "HB", "S1", "HA", "HB"]
    pols=[ "V", polbase[0], polbase[0], "H", polbase[1], polbase[1]]

    # go through the spectra
    for i in range(0,Ns):

        # variance
        spec_mom[ 'var' ][ i ]=np.sum(spec[sats[i]][pols[i]])*dk*dk

        # compute reference wavenumber and direction (belonging to the peak)
        pks=spec_peaks[sats[i]][pols[i]]
        kx_ref=kx[pks[0][0],pks[0][1]]
        ky_ref=ky[pks[0][0],pks[0][1]]
        k_ref=np.sqrt(kx_ref**2+ky_ref**2)
        phi_ref = np.arctan2( ky_ref, kx_ref )

        for j in range(0,Nm):
            # spectral moment arms
            spec_mom[ 'M' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * k ** (j + 1) )
            spec_mom[ 'Mx' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * kx ** (j + 1) )
            spec_mom[ 'My' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * ky ** (j + 1) )

            # spectral moment arms
            spec_mom[ 'K' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * k ** (j+1) ) / np.sum(
                spec[ sats[ i ] ][ pols[ i ] ] )
            spec_mom[ 'Kx' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * kx ** (j+1) ) / np.sum(
                spec[ sats[ i ] ][ pols[ i ] ] )
            spec_mom[ 'Ky' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * ky ** (j+1) ) / np.sum(
                spec[ sats[ i ] ][ pols[ i ] ] )

            # relative moment arms
            spec_mom[ 'K_rel' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * (k-k_ref) ** (j+1) ) / np.sum(
                spec[ sats[ i ] ][ pols[ i ] ] )
            spec_mom[ 'phi_rel' ][ i ][ j ] = np.sum( spec[ sats[ i ] ][ pols[ i ] ] * np.angle(np.exp(1j*(phi-phi_ref))) ** (j+1) ) / np.sum(
                spec[ sats[ i ] ][ pols[ i ] ] )

    return spec_mom

'''
# first guess of the wave spectrum
def first_guess_wave_spectrum( SAR_spec, kx, ky, u10, phi_w, IWA, phi_s, k_s, k_w, theta, R, V, mu = 0.5, mtf = 'Schulz' ):
    # kx,ky: wave numbers (two-dimensional)
    # SAR_spec: 3 x two-dimensional wave spectrum
    # u10: wind speed (from the inversion of wind speed/stress)
    # phi_w: wind direction [deg] (from the inversion of wind speed/stress)
    # phi_s: guess of swell direction [deg] (from the imaginary part of the cross-spectrum)
    # k_s: guess of swell wave number (from the peak in the cross-spectrum)
    # k_w: guess of swell wave spectrum width (from the cross-spectrum)
    # IWA: inverse wave age (from the cut-off)
    # theta: master incident angle
    # R: range to target
    # V: platform velocity
    # mu: hydrodynamic relaxation rate (necessary for Schulz RAR mtf)
    # mtf: RAR transfer function

    # wave number and direction
    g = 9.81
    k = np.sqrt( kx ** 2 + ky ** 2 )
    phi = np.arctan2( ky, kx )  # 0 is cross-track direction waves, 90 along-track
    omega = np.sqrt( g * k )  # angular velocity
    theta = np.deg2rad( theta )
    phi_w = np.deg2rad( phi_w )
    phi_s = np.deg2rad( phi_s )

    ############### first guess wind wave spectrum ###############
    # compute fetch from inverse wave age
    X_0 = 22E3
    X = np.arctanh( (IWA / 0.84) ** (-1 / 0.75) ) ** (1 / 0.4) * X_0
    k_0 = g / u10 ** 2
    fetch = X / k_0

    # wave-number spectrum
    Sp = elfouhaily( k, u10, fetch )

    # directional distribution
    dphi = (phi_w - phi + np.pi) % (2 * np.pi) - np.pi  # including unwrapping
    D = elfouhaily_spread( k, dphi, u10, fetch )

    # two dimensional spectrum
    S = Sp * D / k
    S[ 0, 0 ] = 0

    ############### first guess swell spectrum ###############
    # FIXME: we get it from the monostatic one only
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
        sigma = cmod5n.cmod5n_forward( np.array( [ u10, u10 ] ), np.rad2deg( np.array( [ phi_w, phi_w ] ) ),
                                       np.rad2deg( np.array( [ theta, theta + dth ] ) ) )  # use CMOD5n here
        dsigma = (sigma[ 1 ] - sigma[ 0 ]) / dth
        T_I = kx * dsigma / sigma[ 0 ] / np.cos( theta ) * (
                kx / k * np.sin( theta ) + 1j * np.cos( theta ))  # combination of both equations (37)
    T_I[ T_I != T_I ] = 0

    # approximate scaling factor between SAR spectrum and wave spectrum
    T2 = np.absolute( 1j * ky * T_y + T_I ) ** 2 / 2
    SAR_temp = SAR_spec[ :, :, 0 ]
    S_temp = SAR_temp / T2

    # only fit something near the peak
    kx_s = k_s * np.cos( phi_s )
    ky_s = k_s * np.sin( phi_s )
    I = ((kx - kx_s) ** 2 + (ky - ky_s) ** 2) ** 0.5 < k_w
    S[ I ] = S[ I ] + S_temp[ I ]

    return S
'''

if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from matplotlib.colors import LogNorm
    from stereoid.oceans.forward_models import SAR_spectra as SAR_model
