__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
import netCDF4
from scipy.interpolate import griddata


# inversion of the RIM
'''
def RIM_inversion( obsfile, LUTdir, wdir_est, pol = 'V', atd = 300 ):
    """Invert wind speed and direction from backscatter

        Parameters
        ----------

        Returns
        -------

    """

    # Read LUTs
    f_sigma = LUTdir + '/Backscatter/LUT_multistatic_' + str( atd ) + '_' + pol + '.nc4'
    f_dopp=LUTdir + '/WaveDoppler/LUT_multistatic_' + str(atd) + '_' + pol + '.nc4'
    LUT_sigma = netCDF4.Dataset( f_sigma )
    LUT_dopp = netCDF4.Dataset( f_dopp )

    # Read scenario data
    obs = netCDF4.Dataset( obsfile )

    # shape
    shp = (obs.dimensions[ 'Y' ].size, obs.dimensions[ 'X' ].size)
    SHP = LUT_sigma[ "S1_prin" ][ :, :, :, : ].shape

    # assume a fully developed wave spectrum
    print( 'Preparing LUTS' )
    nrcs_LUT, U10, WDIR, INCM = prepare_LUTS( LUT_sigma[ "S1_prin" ][ :, :, :, SHP[ 3 ] - 1 ],
                                              LUT_sigma[ "HA_prin" ][ :, :, :, SHP[ 3 ] - 1 ],
                                              LUT_sigma[ "HB_prin" ][ :, :, :, SHP[ 3 ] - 1 ],
                                              LUT_sigma[ "wind_speed" ], LUT_sigma[ "wind_direction" ],
                                              LUT_sigma[ "incident_angle" ] )
    SHP=nrcs_LUT.shape

    # extract nrcs from obs
    nrcs = np.zeros( (shp[ 0 ], shp[ 1 ], 3) )
    nrcs[ :, :, 0 ] = obs[ "S1_prin_sigma" ][ :, : ]
    nrcs[ :, :, 1 ] = obs[ "HA_prin_sigma" ][ :, : ]
    nrcs[ :, :, 2 ] = obs[ "HB_prin_sigma" ][ :, : ]
    incm = obs['transmitter_incident_angle'][:]*1.0

    # go through all pixels
    print( 'step 1: wind inversion' )
    u10 = np.zeros( shp )
    wdir = np.zeros( shp )
    for j in range( 0, shp[ 1 ] ):
        if np.mod( j, 50 ) == 0:
            print( j )

        # LUT nrcs for incident angle
        I = np.argmin( np.absolute( incm[j] - INCM ) )
        nrcs_temp = nrcs_LUT[ :, :, I, : ]

        for i in range( 0, shp[ 0 ] ):
            # LUT nrcs with wind dir est
            dphi = WDIR - wdir_est[ i, j ]
            I = np.logical_or( np.absolute( dphi ) < 45, np.absolute( dphi ) > 315 )
            nrcs_temp2 = nrcs_temp[ :, I, : ]
            wdir_temp = WDIR[ I ]

            J = np.unravel_index( np.argmin( np.sum( (nrcs_temp2 - nrcs[ i, j, : ]) ** 2, 2 ) ),
                                  (SHP[ 0 ], nrcs_temp2.shape[ 1 ]) )

            # get wind speed
            u10[ i, j ] = U10[ J[ 0 ] ]
            wdir[ i, j ] = wdir_temp[ J[ 1 ] ]


    # get wave age from cut-off
    print( 'step 2: wave-age inversion' )
    # FIXME: this is hardcoded now, but should come from the spectra
    iwa=np.ones(shp)*2

    # improve wind speed/direction and get wave-Doppler
    print( 'step 3: get wave-Doppler')

    wdopp = np.zeros( (shp[0],shp[1],3) )
    for j in range(0, shp[ 1 ] ):
        if np.mod( j, 10 ) == 0:
            print( j )
        for i in range( 0, shp[ 0 ] ):
            I1 = np.argmin( np.absolute( iwa[ i, j ] - LUT_sigma[ "inv_wave_age"][:] ) )
            dphi = LUT_sigma[ "wind_direction"][:] - wdir[ i, j ]
            I2 = np.logical_or( np.absolute( dphi ) < 30, np.absolute( dphi ) > 330 )
            du10 = LUT_sigma[ "wind_speed"][:] - u10[ i, j ]
            I3 = np.absolute(du10) < 3
            dinc = LUT_sigma[ "incident_angle"][:] - incm[ j ]
            I4 = np.absolute(dinc) < 5
            wdir_LUT_temp=LUT_sigma[ "wind_direction" ][I2]
            if np.logical_or(wdir[i,j] < 90, wdir[i,j] > 270):
                wdir_LUT_temp[wdir_LUT_temp > 180]=wdir_LUT_temp[wdir_LUT_temp > 180]-360

            nrcs_LUT, U10, WDIR, INCM = prepare_LUTS( LUT_sigma[ "S1_prin" ][ I3, I2, I4, I1 ],
                                                      LUT_sigma[ "HA_prin" ][ I3, I2, I4, I1 ],
                                                      LUT_sigma[ "HB_prin" ][ I3, I2, I4, I1 ],
                                                      LUT_sigma[ "wind_speed" ][I3], wdir_LUT_temp,
                                                      LUT_sigma[ "incident_angle" ][I4], nws = 11, nwd = 11, ninc = 32 )
            SHP=nrcs_LUT.shape
            dopp_LUT, U10, WDIR, INCM = prepare_LUTS( LUT_dopp[ "S1_prin" ][ I3, I2, I4, I1 ],
                                                      LUT_dopp[ "HA_prin" ][ I3, I2, I4, I1 ],
                                                      LUT_dopp[ "HB_prin" ][ I3, I2, I4, I1 ],
                                                      LUT_sigma[ "wind_speed" ][ I3 ], wdir_LUT_temp,
                                                      LUT_sigma[ "incident_angle" ][ I4 ], nws = 11, nwd = 11,
                                                      ninc = 32 )

            I = np.argmin( np.absolute( incm[ j ] - INCM ) )
            nrcs_temp = nrcs_LUT[ :, :, I, : ]
            J = np.unravel_index( np.argmin( np.sum( (nrcs_temp - nrcs[ i, j, : ]) ** 2, 2 ) ),
                                  (SHP[ 0 ], nrcs_temp.shape[ 1 ]) )
            u10[ i, j ] = U10[ J[ 0 ] ]
            wdir[ i, j ] = WDIR[ J[ 1 ] ]
            wdopp[ i, j, : ] = dopp_LUT[ J[ 0 ], J[ 1 ], I, : ]


    wdir[wdir < 0]=wdir[wdir < 0]+360

    # close the netCDF's
    LUT_sigma.close()
    LUT_dopp.close()
    obs.close()

    return u10, wdir, iwa, wdopp


def prepare_LUTS( S1_data, HA_data, HB_data, u10, wdir, incm, nws = 21, nwd = 72, ninc = 64 ):
    """Interpolates LUTS

            Parameters
            ----------

            Returns
            -------

    """
    # proper shape for griddata
    xi, yi, zi = np.meshgrid( wdir, u10, incm )
    xi = xi.ravel()
    yi = yi.ravel()
    zi = zi.ravel()

    # for interpolation
    U10 = np.linspace( np.min( u10 ), np.max( u10 ), nws, endpoint = True )
    WDIR = np.linspace( np.min(wdir), np.max(wdir), nwd, endpoint = False )
    INCM = np.linspace( np.min( incm ), np.max( incm ), ninc, endpoint = True )
    X, Y, Z = np.meshgrid( WDIR, U10, INCM )
    SHP = Z.shape
    X = X.ravel()
    Y = Y.ravel()
    Z = Z.ravel()

    # Full LUT
    nrcs_LUT = np.zeros( (SHP[ 0 ], SHP[ 1 ], SHP[ 2 ], 3) )
    nrcs_LUT[ :, :, :, 0 ] = griddata( (xi, yi, zi), S1_data.ravel(), (X, Y, Z), method = 'linear' ).reshape( SHP )
    nrcs_LUT[ :, :, :, 1 ] = griddata( (xi, yi, zi), HA_data.ravel(), (X, Y, Z), method = 'linear' ).reshape( SHP )
    nrcs_LUT[ :, :, :, 2 ] = griddata( (xi, yi, zi), HB_data.ravel(), (X, Y, Z), method = 'linear' ).reshape( SHP )

    print(nrcs_LUT.shape)
    print(SHP)
    print(INCM.shape)

    from matplotlib import pyplot as plt
    plt.figure( figsize = (15, 6) )
    plt.subplot( 1, 3, 1 )
    plt.plot( nrcs_LUT[ 5, :, 10, 0 ] )
    plt.subplot( 1, 3, 2 )
    plt.plot( nrcs_LUT[ 5, :, 10, 1 ] )
    plt.subplot( 1, 3, 3 )
    plt.plot( nrcs_LUT[ 5, :, 10, 2 ] )
    plt.show()

    return nrcs_LUT, U10, WDIR, INCM
'''

if __name__ == "__main__":
    wdir_est = np.ones( (500, 240) ) * 270

    LUTdir = "/home/marcelmarina/Data/Harmony/RESULTS/LUT/"
    obsfile = "/home/marcelmarina/Data/Harmony/RESULTS/Scenarios/California/AllObs/Cal_R13_S02_300_10.nc4"
    u10, wdir, iwa, wdopp = RIM_inversion( obsfile, LUTdir, wdir_est, pol = 'V', atd = 300 )

    from matplotlib import pyplot as plt

    plt.figure( figsize = (15, 10) )
    plt.subplot( 1, 2, 1 )
    plt.imshow( u10, origin = 'lower', vmin = -15, vmax = 15, cmap = 'plasma' )
    plt.xlabel( 'u [m/s]' )
    plt.colorbar()
    plt.subplot( 1, 2, 2 )
    plt.imshow( wdir, origin = 'lower', vmin = 0, vmax = 360, cmap = 'hsv' )
    plt.xlabel( 'wdir [deg]' )
    plt.colorbar()
    plt.show()

    plt.figure( figsize = (15, 10) )
    plt.subplot( 1, 2, 1 )
    plt.imshow( u10 * np.cos( np.deg2rad( wdir ) ), origin = 'lower', vmin = -15, vmax = 15, cmap = 'plasma' )
    plt.xlabel( 'u [m/s]' )
    plt.colorbar()
    plt.subplot( 1, 2, 2 )
    plt.imshow( u10 * np.sin( np.deg2rad( wdir ) ), origin = 'lower', vmin = -15, vmax = 15, cmap = 'plasma' )
    plt.xlabel( 'v [m/s]' )
    plt.colorbar()
    plt.show()
