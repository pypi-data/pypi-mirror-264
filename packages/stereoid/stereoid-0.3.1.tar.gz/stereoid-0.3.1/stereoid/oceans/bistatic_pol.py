# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 15:18:39 2019

@author: Lorenzo Iannini
"""

import numpy as np
import os
from scipy import interpolate
from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from drama.io import cfg
import drama.geo as sargeo
from drama.geo import geometry as geometry
import drama.orbits as drorb
# from drama.orbits import sunsync_orbit as sso
from drama.geo.swath_geo import SingleSwathBistatic as SwathBis


def bispolangle( theta_i, theta_s, theta_f, phi_i, phi_s, phi_f ):
    """
    OLD MODEL - DO NOT USE THIS
    Compute the scattered field polarization (angle with respect to the V-field
    axis of the Rx) as an effect of the interaction with a flat surface

    GEOMETRY NOTES:
     - Right-handed coordinate system
     - Phi is the angle of the projection in the x,y plane with respect to x axis
       It is positive in the positive y semiplane
     - Theta is the angle with respect to the z axis
       It is positive in the positive z semiplane

    Assume now:
        - x is the ground range axis with direction towards the satellite
        - y is then the azimuth axis

    :param theta_i: zenith angle for incident field [degrees]
    :param theta_s: zenith angle for scattered field [degrees]
    :param theta_f: zenith angle of surface normal
    :param phi_i: azimuth angle for incident field [degrees]
    :param phi_s: azimuth angle for scattered field [degrees]
                  phi_i = phi_s -> backscatter
    :param phi_f: azimuth angle of surface normal
    """
    # compute surface normal
    n_f = np.zeros( 3 )
    n_f[ 0 ] = np.sin( np.radians( theta_f ) ) * np.cos( np.radians( phi_f ) )
    n_f[ 1 ] = np.sin( np.radians( theta_f ) ) * np.sin( np.radians( phi_f ) )
    n_f[ 2 ] = np.cos( np.radians( theta_f ) )

    # Compute indicence (Sentinel-1) plane normal
    k_i = np.zeros( 3 )
    k_i[ 0 ] = np.sin( np.radians( theta_i ) ) * np.cos( np.radians( phi_i ) )
    k_i[ 1 ] = np.sin( np.radians( theta_i ) ) * np.sin( np.radians( phi_i ) )
    k_i[ 2 ] = np.cos( np.radians( theta_i ) )

    # Compute scattering (STEREOID) plane normal
    k_s = np.zeros( 3 )
    k_s[ 0 ] = np.sin( np.radians( theta_s ) ) * np.cos( np.radians( phi_s ) )
    k_s[ 1 ] = np.sin( np.radians( theta_s ) ) * np.sin( np.radians( phi_s ) )
    k_s[ 2 ] = np.cos( np.radians( theta_s ) )

    # V-field versor - Sentinel-1
    v_i = np.zeros( 3 )
    v_i[ 0 ] = - np.cos( np.radians( theta_i ) ) * np.cos( np.radians( phi_i ) )
    v_i[ 1 ] = - np.cos( np.radians( theta_i ) ) * np.sin( np.radians( phi_i ) )
    v_i[ 2 ] = np.sin( np.radians( theta_i ) )

    # H-field versor - Sentinel-1
    h_i = np.cross( v_i, k_i )

    # V-field versor - STEREOID
    v_s = np.zeros( 3 )
    v_s[ 0 ] = - np.cos( np.radians( theta_s ) ) * np.cos( np.radians( phi_s ) )
    v_s[ 1 ] = - np.cos( np.radians( theta_s ) ) * np.sin( np.radians( phi_s ) )
    v_s[ 2 ] = np.sin( np.radians( theta_s ) )

    # H-field versor - STEREOID
    h_s = np.cross( v_s, k_s )

    # --------------------------------------------
    # Find projection of V-field (S1) on surface
    # --------------------------------------------
    # intersection between V-plane and surface
    field_f = - np.cross( h_i, n_f )
    field_f = field_f / np.linalg.norm( field_f )

    # -----------------------------------------------------------------
    # Find projection of surface field on scattering plane (STEREOID)
    # -----------------------------------------------------------------
    field_s = field_f - k_s * np.inner( field_f, k_s ) / np.linalg.norm( k_s ) ** 2
    field_s = field_s / np.linalg.norm( field_s )

    # ---------------------------------------------------------------
    # Compute polarization angle with respect to V-field (STEREOID)
    # ---------------------------------------------------------------
    cos_pol = max( -1, min( 1, np.inner( field_s, v_s ) ) )
    pol_ang = np.rad2deg( np.arccos( cos_pol ) )
    return pol_ang


def plotseaspec( S, P, k_vec, theta_vec ):
    """
    Plot 2D wave spectrum in polar axes

    :param S: wavenumber spectrum [array Nk x Ntheta]
    :param P: angular (modulating) function [array Nk x Ntheta]
    :param k_vec: vector with wavenumbers [Nk elements]
    :param theta_vec: vector with angles [Ntheta elements]
    """

    kx = np.concatenate( (np.flip( -1 * k_vec[ 1: ], axis = 0 ), k_vec) )
    ky = np.concatenate( (np.flip( -1 * k_vec[ 1: ], axis = 0 ), k_vec) )

    x_vec = np.arange( -len( k_vec ) + 1, len( k_vec ) )
    y_vec = np.arange( -len( k_vec ) + 1, len( k_vec ) )
    x_mat, y_mat = np.meshgrid( x_vec, y_vec )
    k_idx = np.sqrt( x_mat ** 2 + y_mat ** 2 ).astype( 'int' )
    theta_int = np.arctan2( y_mat, x_mat )

    spectrum = P * S

    # Interpolate polar grid to cartesian
    fk = interpolate.interp1d( k_vec, np.arange( k_vec.size ),
                               kind = 'nearest', fill_value = 'extrapolate' )
    ft = interpolate.interp1d( theta_vec, np.arange( theta_vec.size ),
                               kind = 'nearest', fill_value = 'extrapolate' )
    #    k_idx = fk(k_int.flatten()).astype('int')
    theta_idx = ft( theta_int.flatten() ).astype( 'int' )
    idx_valid = np.where( np.abs( k_idx.flatten() ) < len( k_vec ) )[ 0 ]
    idx_notvalid = np.where( np.abs( k_idx.flatten() ) >= len( k_vec ) )[ 0 ]

    spectrum_int = np.zeros( k_idx.size )
    spectrum_int[ idx_notvalid ] = np.nan
    spectrum_int[ idx_valid ] = spectrum[ theta_idx[ idx_valid ], k_idx.flatten()[ idx_valid ] ]
    spectrum_int = spectrum_int.reshape( k_idx.shape )

    Snz = spectrum_int
    Snz[ Snz == 0 ] = 1e-100

    fig = plt.figure()
    # create axes in the background to show cartesian image
    ax0 = fig.add_subplot( 111 )
    ax0.imshow( 10 * np.log10( Snz ), extent = [ min( kx ), max( kx ), min( ky ), max( ky ) ] )
    ax0.get_images()[ 0 ].set_clim( (10 * np.log10( np.nanmax( Snz.flatten() ) ) - 20,
                                     10 * np.log10( np.nanmax( Snz.flatten() ) )) )
    ax0.get_images()[ 0 ].set_cmap( 'CMRmap_r' )
    ax0.axis( "off" )

    # create polar axes in the foreground and remove its background
    # to see through
    ax = fig.add_subplot( 111, polar = True, label = "polar" )
    ax.set_facecolor( "None" )

    kticks = fk( np.array( [ 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2 ] ) )
    kticks_label = [ '$10^{-3}$', '$10^{-2}$', '$10^{-1}$', '$10^{0}$',
                     '$10^{1}$', '$10^{2}$' ]

    ax.set_yticks( kticks )
    ax.set_yticklabels( kticks_label )

    plt.show()
    return fig


def plot2Dpolar( phi, rho, data,
                 res = 1, rho_axis = None,
                 levels = None, fmt = '%1.0f',
                 color_lines = 'w', color_im = 'twilight' ):
    """
    Plot 2D array polar axes

    Parameters
    ----------
    phi: numpy.ndarray (nphi, )
        vector of angles (-pi <= phi <pi) in degrees
    rho: numpy.ndarray (nrho, )
        grid in the rho axis
    data: numpy.ndarray (nrho, nphi)
        data to plot
    res: float
        Sampling step. Default is 1
    rho_axis: numpy.ndarray (nrho0, )
        sampled axis to plot. None (default) takes rho as the axis
    levels: numpy.ndarray (nlevels, )
        levels for contour lines. Set to None (default) for no contour lines
    fmt : string
        format for contour lines. Default is '%1.0f'
    color_lines: string
        string with color of the contour lines (if present). Default is 'w'
    color_im: numpy.ndarray (nphi, ) or string
        vector with colors of the map or string with predefined colormap name

    Returns
    -------
    fig: pyplot object
        plotted figure handle
    fig: axis object
        axes handle
    im : imshow object
        image handle
    """
    phi = phi.flatten()
    rho = rho.flatten()
    if rho_axis is None:
        rho_axis = rho

    x_vec = np.arange( -len( rho_axis ) + 1, len( rho_axis ) )
    x_mat, y_mat = np.meshgrid( x_vec, x_vec )
    rho_idx = np.sqrt( x_mat ** 2 + y_mat ** 2 )
    phi_mat = np.degrees( np.arctan2( y_mat, x_mat ) )

    get_rho = interpolate.interp1d( np.arange( rho_axis.size ), rho_axis,
                                    kind = 'linear', bounds_error = False,
                                    fill_value = 'extrapolate' )
    get_rho_idx = interpolate.interp1d( rho_axis, np.arange( rho_axis.size ),
                                        kind = 'linear', bounds_error = False,
                                        fill_value = 'extrapolate' )

    rho_mat = get_rho( rho_idx )
    # Interpolate polar grid to cartesian
    f = interpolate.interp2d( phi, rho, data, kind = 'linear',
                              bounds_error = False, fill_value = np.nan )
    data_intp = np.zeros_like( x_mat, dtype = float )
    for x in range( len( x_vec ) ):
        for y in range( len( x_vec ) ):
            data_intp[ x, y ] = f( phi_mat[ x, y ], rho_mat[ x, y ] )
    idx_notvalid = np.where( np.abs( rho_idx.flatten() ) >= len( x_vec ) )[ 0 ]
    data_intp[ idx_notvalid ] = np.nan

    fig = plt.figure()
    # create axes in the background to show cartesian image
    ax0 = fig.add_subplot( 111 )
    im = ax0.imshow( np.flipud( data_intp ), cmap = color_im,
                     extent = [ min( x_vec ), max( x_vec ), min( x_vec ), max( x_vec ) ] )
    im.set_clim( -180, 180 )
    if levels is not None:
        clines = ax0.contour( x_mat, y_mat, data_intp, levels, origin = 'lower',
                              colors = color_lines, linewidths = 2 )
        ax0.clabel( clines, levels, fmt = fmt, fontsize = 12 )
    else:
        clines = None
    ax0.axis( "off" )

    # create polar axes in the foreground and remove its background
    # to see through
    ax = fig.add_subplot( 111, polar = True, label = "polar" )
    ax.set_facecolor( "None" )

    rho_lines = np.unique( np.floor( rho / 10 ) ) * 10

    ax.set_yticks( get_rho_idx( rho_lines ) )
    ax.set_yticklabels( rho_lines.astype( int ) )
    return fig, ax, im


def specularnorm( theta_i, theta_s, phi_i, phi_s ):
    """Compute indicence (Sentinel-1) plane normal."""
    k_i = np.zeros( 3 )
    k_i[ 0 ] = np.sin( np.radians( theta_i ) ) * np.cos( np.radians( phi_i ) )
    k_i[ 1 ] = np.sin( np.radians( theta_i ) ) * np.sin( np.radians( phi_i ) )
    k_i[ 2 ] = np.cos( np.radians( theta_i ) )

    # Compute scattering (STEREOID) plane normal
    k_s = np.zeros( 3 )
    k_s[ 0 ] = np.sin( np.radians( theta_s ) ) * np.cos( np.radians( phi_s ) )
    k_s[ 1 ] = np.sin( np.radians( theta_s ) ) * np.sin( np.radians( phi_s ) )
    k_s[ 2 ] = np.cos( np.radians( theta_s ) )

    # Compute surface normal
    k_f = k_i + k_s
    k_f = k_f / np.linalg.norm( k_f )

    phi_f = np.arctan2( k_f[ 1 ], k_f[ 0 ] )
    theta_f = np.arccos( k_f[ 2 ] )

    return theta_f, phi_f


def baseline2ang( dau, inc ):
    """
    Get the incidence and azimuth/northing angles in the S1-Harmony bistatic
    configuration for lat=0 and a vector of incidence angles

    Parameters
    ----------
    dau : float
        along-track baseline [m]
    inc : numpy.ndarray or float
        incidence angles [deg]

    Returns
    -------
    phi_bis : numpy.ndarray or float
        bistatic azimuth angles (northing S1 - northing companion) [deg]
    theta_bis : numpy.ndarray or float
        incidence angles for companion [deg]
    """
    # Set parameters to extract Sentinel-STEREOID configuration
    # FIXME
    main_dir = "C:\\Users\\Lorenzo Iannini\\Dropbox\\Python\\site-packages\\stereoid"
    runid = 'KO_1'

    pardir = os.path.join( main_dir, 'PAR' )
    parfile = os.path.join( pardir, ("SATRoSS_%s.cfg" % runid) )
    conf = cfg.ConfigFile( parfile )
    # extract relevant info from conf
    # b_at = rxcnf.b_at
    # Formation timeline
    n_days = conf.orbit.days_cycle
    n_revs = conf.orbit.orbits_nbr

    #    # Calculate orbit geometry
    #    Torb = 3600 * 24. * n_days / n_revs
    #    (a, e, i) = sso.get_sunsync_repeat_orbit(n_days, n_revs)
    #    comp_orb_delay = dau / a / (np.pi * 2) * Torb
    swath = SwathBis( look = 'right', dau = dau,
                      par_file = parfile, orb_type = 'sunsync' )
    phi_bis = np.degrees( swath.inc2bist_ang_az( np.radians( inc ) ) )
    theta_bis = np.degrees( swath.inc2slave_inc( np.radians( inc ) ) )
    return phi_bis, theta_bis


def geo2orbit( lat, lon, alt, look_angle,
               bl_at = 0, orb_type = 'sunsync',
               look = 'right', parFile = None ):
    """
    Computes the orbit from the point coordinates (geographic format) on
    the ground and the look angle. The function provides the possibility
    of retrieving e.g. the orbit illuminating a specific point in the swath
    center. If a bistatic baseline different from 0 is provided the orbit
    coordinates of a bistatic satellite companion are also returned

    :param lat: point latitude
    :param lon: point longitude
    :param alt: point altitude
    :param look_angle: look angle
    :param bl_at: along-track baseline
    :param look: 'left' or 'right'
    :param orb_type: 'sunsync' or 'repeat'
    :param parFile: All orbit parameters should be in parFile

    :returns: SingleOrbit object mono,
              SingleOrbit object bistatic (if bl_at>0),
              time of zero-Doppler (for Mono) orbit location
    """
    if parFile is None:
        # Assign standard orbit configuration parameters
        class Orbit:
            # Orbit height [m]
            Horb = 514e3
            # desired days per cycle [d]
            days_cycle = 6  # 11
            # number of orbits for repeat
            orbits_nbr = 91
            omega_p = 90
            # right ascension of ascending node [deg]
            asc_node = 359.145
            # fraction of an orbit period
            starttime = 3.
            # orbit calculation time [d]
            timeduration = 12
            # Time step [s]
            timestep = 1.

        class Conf:
            orbit = Orbit()

        conf = Conf()
    else:
        conf = cfg.ConfigFile( parFile )

    # point ecef coordinates
    coords_geo = np.array( [ [ lat, lon, alt ] ] )
    coords_ecef = sargeo.ecef_to_geodetic( coords_geo, inverse = True )

    # Try to make a coarse estimate of the ascending node
    Single_orbData = drorb.SingleOrbit( conftuple = conf )
    r_geo = sargeo.ecef_to_geodetic( Single_orbData.r_ecef, inverse = False )
    r_geo_half = r_geo[ 0:np.ceil( r_geo.shape[ 0 ] / 2 ).astype( int ), : ]
    zeroLat_index = np.where( np.abs( r_geo_half[ :, 0 ] ) == min( np.abs( r_geo_half[ :, 0 ] ) ) )[ 0 ]
    ptLat_index = np.where( np.abs( r_geo_half[ :, 0 ] - lat ) == min( np.abs( r_geo_half[ :, 0 ] - lat ) ) )[ 0 ]

    zeroLon = r_geo_half[ zeroLat_index, 1 ]
    ptLon = r_geo_half[ ptLat_index, 1 ]

    asc_node_coarse = lon - (ptLon - zeroLon)

    # ascending nodes to use for interpolation
    asc_node_vec = np.arange( asc_node_coarse - 10, asc_node_coarse + 10, 0.2, dtype = float )
    n_nodes = len( asc_node_vec )

    Single_orbArray = [ None ] * n_nodes
    la_vec = np.empty( n_nodes ) * np.nan
    # vector filled with 0 if 'left' looking or 1 if 'right' looking
    look_vec = np.empty( n_nodes )
    d_vec = np.empty( n_nodes ) * np.nan

    for i in range( n_nodes ):
        conf.orbit.asc_node = asc_node_vec[ i ]

        # orbit ecef coordinates
        Single_orbArray[ i ] = drorb.SingleOrbit( conftuple = conf )

        # Compute zeroDoppler parameters
        r_ecef, v_ecef, t, la_vec[ i ], look_dir = geometry.geo2zeroDop( lat, lon, alt, Single_orbArray[ i ] )

        look_vec[ i ] = 1 if look_dir == 'right' else 0
        d_vec[ i ] = np.linalg.norm( r_ecef - coords_ecef )

        if 0:
            fig = plt.figure()
            ax = fig.add_subplot( 111, projection = '3d' )
            ax.plot( Single_orbArray[ i ].r_ecef[ :, 0 ], Single_orbArray[ i ].r_ecef[ :, 1 ],
                     Single_orbArray[ i ].r_ecef[ :, 2 ] )
            ax.plot( r_ecef[ :, 0 ], r_ecef[ :, 1 ], r_ecef[ :, 2 ], linewidth = 2 )
            ax.plot( r_ecef[ zeroDop, 0 ], r_ecef[ zeroDop, 1 ], r_ecef[ zeroDop, 2 ], linewidth = 2 )
            ax.scatter( coords_ecef[ 0, 0 ], coords_ecef[ 0, 1 ], coords_ecef[ 0, 2 ] )

    if look == 'right':
        valid_node = np.where( np.logical_and( look_vec == 1,
                                               (d_vec - 100e3) < conf.orbit.Horb / np.cos(
                                                   np.radians( look_angle ) ) ) )[ 0 ]
    else:
        valid_node = np.where( np.logical_and( look_vec == 0,
                                               (d_vec - 100e3) < conf.orbit.Horb / np.cos(
                                                   np.radians( look_angle ) ) ) )[ 0 ]

    asc_interp = interpolate.interp1d( la_vec[ valid_node ], asc_node_vec[ valid_node ], kind = 'linear' )
    asc_node_est = asc_interp( look_angle )
    print( asc_node_est )

    conf.orbit.asc_node = asc_node_est
    orb_Mono = drorb.SingleOrbit( conftuple = conf )

    r_ecef, v_ecef, t, la, look_dir = geometry.geo2zeroDop( lat, lon, alt, orb_Mono )

    # Visual check of the orbit solution
    if 0:
        fig = plt.figure()
        ax = fig.add_subplot( 111, projection = '3d' )
        ax.plot( orb_Mono.r_ecef[ :, 0 ], orb_Mono.r_ecef[ :, 1 ], orb_Mono.r_ecef[ :, 2 ] )
        ax.scatter( r_ecef[ 0 ], r_ecef[ 1 ], r_ecef[ 2 ], color = 'blue', marker = 'o' )
        ax.scatter( coords_ecef[ 0, 0 ], coords_ecef[ 0, 1 ], coords_ecef[ 0, 2 ], color = 'red', marker = 'o' )

    if bl_at > 0:
        # v_orb_m = np.mean(np.linalg.norm(orb_Mono.v_ecef, axis=1))

        # n_days = conf.orbit.days_cycle
        # n_revs = conf.orbit.orbits_nbr
        # Torb = 3600 * 24. * n_days / n_revs
        # (a, e, i) = sso.get_sunsync_repeat_orbit(n_days, n_revs)

        # orb_delay = bl_at / a / (np.pi * 2) * Torb
        orb_delay = bl_at / np.linalg.norm( v_ecef )

        print( "Orbit delay for companion: %f" % orb_delay )

        orb_Bis = drorb.SingleOrbit( conftuple = conf, aei = orb_Mono.aei, companion_delay = orb_delay )

        r_ecef_bis, v_ecef_bis = orb_Bis.interp_orbit( t )
    else:
        orb_Bis = None
        r_ecef_bis = None

    return orb_Mono, orb_Bis, t  # r_ecef, r_ecef_bis


def fresnelcoeff( v_i, eps, mu = 1, v_n = None ):
    """
    Compute Fresnel coefficients for horizontal (TE) and vertical (TM)
    polarizations with respect to the surface normal

    Parameters
    ----------
    v_i: numpy.ndarray (3,)
        versor for wave incidence
    eps: float
        medium relative permittivity
    mu: float
        medium relative permeability. Default is 1
    v_n: numpy.ndarray (3,) or None
        surface normal. Set to None (default) to have v_n = [0, 0, 1]

    Returns
    -------
    r_h: float
        Reflection coefficient for TE mode
    r_v: float
        Reflection coefficient for TM mode
    """
    if v_n is None:
        v_n = np.array( [ 0., 0., 1. ] )
    v_n = v_n / np.linalg.norm( v_n )
    v_i = v_i / np.linalg.norm( v_i )
    eta = np.sqrt( mu / eps )
    n = np.sqrt( mu * eps )
    cos_i = np.inner( -v_i, v_n )
    sin_i = np.sqrt( 1 - cos_i ** 2 )
    cos_t = np.sqrt( 1 - sin_i ** 2 / n ** 2 )
    r_h = (eta * cos_i - cos_t) / (eta * cos_i + cos_t)
    r_v = (cos_i - eta * cos_t) / (cos_i + eta * cos_t)
    return r_h, r_v


def farfield( Ei, p, v_i, v_s, eps, v_n = None, mu = 1 ):
    """
    Compute far field from a single flat facet, defined by its normal v_n, by
    applying the tangential field equations

    Parameters
    ----------
    E_i : float
        amplitude of the incident field
    p : numpy.ndarray (3,)
        3d versor referring to the linear polarization of the incident field
    v_i : numpy.ndarray (3,)
        versor of the incident wave direction (pointing away from the source)
    v_s : numpy.ndarray (3,)
        versor of the scattered wave direction (pointing to the receiver)
    eps : float or complex
        relative permittivity of the dielectric medium
    v_n : numpy.ndarray (3,)
        surface normal. Default is [0, 0, 1], i.e. horizontal surface
    mu : float
        relative permeability of the medium. Default is 1

    Returns
    -------
    Es_h : float or complex
        scattered/received field H-polarized
    Es_h : float or complex
        scattered/received field V-polarized
    """
    if v_n is None:
        v_n = np.array( [ 0., 0., 1. ] )
    v_i = v_i / np.linalg.norm( v_i )
    v_s = v_s / np.linalg.norm( v_s )
    v_n = v_n / np.linalg.norm( v_n )
    eta = np.sqrt( mu / eps )
    # Receive polarization
    q_h = np.cross( -v_s, np.array( [ 0., 0., 1. ] ) )
    q_v = np.cross( q_h, -v_s )
    q_h = q_h / np.linalg.norm( q_h )
    q_v = q_v / np.linalg.norm( q_v )
    # Compute tangential fields
    if np.linalg.norm( np.cross( v_i, v_n ) ) == 0:  # Normal incidence
        t = p
    else:
        t = np.cross( v_i, v_n )
    d = np.cross( v_i, t )
    t = t / np.linalg.norm( t )
    if np.linalg.norm( t ) < 0.01:
        print( np.linalg.norm( t ) )
    d = d / np.linalg.norm( d )
    E_t = np.inner( p, t ) * t * Ei
    E_d = np.inner( p, d ) * d * Ei
    H_t = np.inner( p, d ) * t * Ei / eta
    H_d = np.inner( p, t ) * d * Ei / eta
    (r_h, r_v) = fresnelcoeff( v_i, eps, mu = mu, v_n = v_n )
    n_E = np.cross( v_n, (1 + r_h) * E_t + (1 - r_v) * E_d )
    n_H = np.cross( v_n, (1 - r_h) * H_d - (1 + r_v) * H_t )
    #    n_E_t = np.cross(v_n, E_t)
    #    n_E_tr = np.cross(v_n, r_h * E_t)
    #    n_H_d = np.cross(v_n, H_d)
    #    n_H_dr = np.cross(v_n, -r_h * H_d)
    # Far-field scattering without accounting for amplitude attenuation and
    # phase due to propagation
    Es_h = np.inner( q_h, np.cross( v_s, n_E ) + eta * n_H )
    Es_v = np.inner( q_v, np.cross( v_s, n_E ) + eta * n_H )
    #    print(np.inner(q_h, np.cross(v_s, n_E_t)))
    #    print(np.inner(q_h, np.cross(v_s, n_E_tr)))
    #    print(np.inner(q_h, eta * n_H_d))
    #    print(np.inner(q_h, eta * n_H_dr))
    #    print(np.inner(q_v, np.cross(v_s, n_E_t)))
    #    print(np.inner(q_v, np.cross(v_s, n_E_tr)))
    #    print(np.inner(q_v, eta * n_H_d))
    #    print(np.inner(q_v, eta * n_H_dr))
    #    cos_i = -v_i[2]
    #    cos_s = v_s[2]
    #    sin_s = np.sqrt(1 - cos_s**2)
    #    sin_omega = v_s[0] / sin_s
    #    cos_omega = np.sqrt(1 - sin_omega**2)
    #    f_hh = -cos_omega * (r_h * (cos_s + cos_i) + cos_s - cos_i)
    #    f_vh = sin_omega * (r_h * (1 + cos_s*cos_i) + 1 - cos_s*cos_i)
    #    f_vv = cos_omega * (r_v * (cos_i + cos_s) + cos_s - cos_i)
    #    f_hv = sin_omega * (r_v * (1 + cos_s*cos_i) + 1 - cos_s*cos_i)
    #    if 1:
    #        print('f_hh = ' + str(f_hh))
    #        print('f_vh = ' + str(f_vh))
    #        print('f_vv = ' + str(f_vv))
    #        print('f_hv = ' + str(f_hv))
    return Es_h, Es_v


def ang_to_scat( Ei, psi_i,
                 phi_i, theta_i,
                 phi_s, theta_s,
                 eps, plane_type = 'horizontal', mu = 1 ):
    """
    Compute scattered field parameters by applying the tangential field
    approximation

    Parameters
    ----------
    E_i : float
        amplitude of the incident field
    psi_i : float
        polarization orientation of the incident field. psi=0,90 -> H,V
    phi_i : float
        azimuth angle of the source
    theta_i : float
        elevation angle of the source
    phi_s : float
        azimuth angle of the receiver
    theta_s : float
        elevation angle of the receiver
    eps : float or complex
        relative permittivity of the dielectric medium
    plane_type : string or numpy.ndarray (3,)
        surface normal parameter. Options:
        'horizontal' (default) correspond to v_n = [0, 0, 1]
        'specular' correspond to  v_n = v_s-v_i
        [nx, ny, nz] for user-defined v_n versor
    mu : float
        relative permeability of the medium. Default is 1

    Returns
    -------
    pol_rot: float
        polarization rotation / orientation of the scattettered field with
        respect to the incident one
    ellipticity : float
        ellipticity of the scattered field
    Es_h : float or complex
        scattered/received field H-polarized
    Es_h : float or complex
        scattered/received field V-polarized
    """
    v_i = np.zeros( 3 )
    v_i[ 0 ] = - np.sin( np.radians( theta_i ) ) * np.sin( np.radians( phi_i ) )
    v_i[ 1 ] = np.sin( np.radians( theta_i ) ) * np.cos( np.radians( phi_i ) )
    v_i[ 2 ] = -np.cos( np.radians( theta_i ) )

    # Compute scattering (STEREOID) plane normal
    v_s = np.zeros( 3 )
    v_s[ 0 ] = np.sin( np.radians( theta_s ) ) * np.sin( np.radians( phi_s ) )
    v_s[ 1 ] = - np.sin( np.radians( theta_s ) ) * np.cos( np.radians( phi_s ) )
    v_s[ 2 ] = np.cos( np.radians( theta_s ) )

    # Surface normal
    if isinstance( plane_type, str ):
        if plane_type == 'horizontal':
            v_n = np.array( [ 0., 0., 1. ] )
        elif plane_type == 'specular':
            v_n = -v_i + v_s
            v_n = v_n / np.linalg.norm( v_n )
        else:
            raise ValueError( "unknown plane_type parameter" )
    else:
        v_n = plane_type
        v_n = v_n / np.linalg.norm( v_n )

    # Incidence field polarization
    p_h = np.cross( v_i, np.array( [ 0., 0., 1. ] ) )
    p_v = np.cross( p_h, v_i )
    p_h = p_h / np.linalg.norm( p_h )
    p_v = p_v / np.linalg.norm( p_v )

    # Compute scattered fields
    (Es_hh0, Es_vh0) = farfield( 1, p_h, v_i, v_s, eps, v_n = v_n )
    (Es_hv0, Es_vv0) = farfield( 1, p_v, v_i, v_s, eps, v_n = v_n )

    Es_h = np.cos( np.radians( psi_i ) ) * Es_hh0 + \
           np.sin( np.radians( psi_i ) ) * Es_hv0
    Es_v = np.cos( np.radians( psi_i ) ) * Es_vh0 + \
           np.sin( np.radians( psi_i ) ) * Es_vv0

    # Compute orientation/rotation
    #    alpha = np.arctan2(np.abs(Es_v), np.abs(Es_h))
    #    delta = np.angle(Es_v) - np.angle(Es_h)
    #    if plane_type == 'specular':
    #        if phi_i == phi_s:
    #            alpha = 0
    #            delta = 0
    #
    #    pol_ang = 0.5 * np.degrees(
    #                                np.arctan(
    #                                        np.tan(2 * alpha) * np.cos(delta)
    #                                        )
    #                                ) - psi_i
    #
    #    pol_ang_0 = np.degrees(np.arctan2(np.real(Es_v), np.real(Es_h))) - psi_i
    #    diff_0 = np.round((pol_ang - pol_ang_0) / 90) * 90
    #    pol_ang = pol_ang - diff_0
    #
    #
    #    # Compute ellipticity
    #    ellipticity = 0.5 * np.degrees(
    #                                    np.arcsin(
    #                                            np.sin(2 * alpha) * np.sin(delta)
    #                                            )
    #                                    )
    pol_ang, ellipticity = field_to_ellipse( Es_h, Es_v, psi_i = psi_i )
    if plane_type == 'specular':
        if phi_i == phi_s:
            pol_ang = 0
    if plane_type == 'specular':
        ellipticity = 0

    return pol_ang, ellipticity, Es_h, Es_v


def elfouhaily( psi_i, phi_i, theta_i,
                phi_s, theta_s ):
    """
    Compute the polarization angle of the wave scattered by a perfectly
    conducting surface (with respect to the incident wave polarization), based
    on:
        Elfouhaily, T. et al, A new bistatic model for electromagnetic
        scattering from perfectly conducting random surfaces, Waves in Random
        Media, 1999.

    Parameters
    ----------
    psi_i : float
        polarization orientation of the incident field. psi=0,90 -> H,V
    phi_i : float
        azimuth angle of the source
    theta_i : float
        elevation angle of the source
    phi_s : float
        azimuth angle of the receiver
    theta_s : float
        elevation angle of the receiver

    Returns
    -------
    pol_ang_1: float
        first-iteration polarization rotation of the scattered field with
        respect to the incident one
    pol_ang_2: float
        second-iteration polarization rotation of the scattered field with
        respect to the incident one
    pol_ang_2: float
        first + second-iteration polarization rotation
    P_s_1 : float
        Polarization vector of first-iteration field
    P_s_2 : float
        Polarization vector of second-iteration field
    P_s : float
        P_s_1 + P_s_2. Total polarization vector
    """
    # v_i = np.zeros(3)
    v_i1 = - np.sin( np.radians( theta_i ) ) * np.sin( np.radians( phi_i ) )
    v_i2 = np.sin( np.radians( theta_i ) ) * np.cos( np.radians( phi_i ) )
    v_i3 = -np.cos( np.radians( theta_i ) )
    v_i = np.stack( (v_i1, v_i2, v_i3), axis = -1 )
    # Compute scattering (STEREOID) plane normal
    # v_s = np.zeros(3)
    v_s1 = np.sin( np.radians( theta_s ) ) * np.sin( np.radians( phi_s ) )
    v_s2 = - np.sin( np.radians( theta_s ) ) * np.cos( np.radians( phi_s ) )
    v_s3 = np.cos( np.radians( theta_s ) )
    v_s = np.stack( (v_s1, v_s2, v_s3), axis = -1 )

    # Wave vector difference
    q = v_s - v_i
    q_h = q.copy()
    q_h[ ..., 2 ] = 0

    Q_h = (v_s / (v_s[ ..., 2 ])[ ..., np.newaxis ] + v_i / (v_i[ ..., 2 ])[ ..., np.newaxis ]) / 2
    Q_h[ ..., 2 ] = 0
    # Incidence field polarization vector
    p_i_v = np.cross( v_i, np.array( [ 0., 0., 1. ] ) )
    p_i_h = np.cross( v_i, p_i_v )
    p_i_v = p_i_v / np.linalg.norm( p_i_v, axis = -1 )[ ..., np.newaxis ]
    p_i_h = p_i_h / np.linalg.norm( p_i_h, axis = -1 )[ ..., np.newaxis ]

    P_i = (np.cos( np.radians( psi_i ) )[ ..., np.newaxis ] * p_i_h
           + np.sin( np.radians( psi_i ) )[ ..., np.newaxis ] * p_i_v)
    P_h = np.cross( np.array( [ 0., 0., 1. ] ), P_i )

    # Scattered field polarization vectors
    p_s_v = np.cross( -v_s, np.array( [ 0., 0., 1. ] ) )
    p_s_h = np.cross( -v_s, p_s_v )
    p_s_v = p_s_v / np.linalg.norm( p_s_v, axis = -1 )[ ..., np.newaxis ]
    p_s_h = p_s_h / np.linalg.norm( p_s_h, axis = -1 )[ ..., np.newaxis ]

    ################################
    # First-iteration polarization #
    ################################

    P_s_1 = np.cross( np.cross( q / (q[ ..., 2 ])[ ..., np.newaxis ], P_i ), v_s )
    P_s_1 = P_s_1 / np.linalg.norm( P_s_1, axis = -1 )[ ..., np.newaxis ]

    # Polarization rotation
    cos_psi_s = np.einsum( "...i,...i", P_s_1, p_s_h )
    sin_psi_s = np.einsum( "...i,...i", P_s_1, p_s_v )

    # print(psi_i.shape)
    pol_ang_1 = np.degrees( np.arctan2( sin_psi_s, cos_psi_s ) ) - psi_i

    #################################
    # Second-iteration polarization #
    #################################
    P_s_2 = np.cross( 2 * np.einsum( "...i,...i", q_h / (q[ ..., 2 ])[ ..., np.newaxis ], P_h )[ ..., np.newaxis ] * Q_h
                      - np.einsum( "...i,...i", q_h / (q[ ..., 2 ])[ ..., np.newaxis ], Q_h )[ ..., np.newaxis ] * P_h,
                      v_s )
    cos_psi_s = np.einsum( "...i,...i", P_s_2, p_s_h )
    sin_psi_s = np.einsum( "...i,...i", P_s_2, p_s_v )
    pol_ang_2 = np.degrees( np.arctan2( sin_psi_s, cos_psi_s ) ) - psi_i

    ######################
    # Total polarization #
    ######################
    P_s = P_s_1 + P_s_2
    cos_psi_s = np.einsum( "...i,...i", P_s, p_s_h )
    sin_psi_s = np.einsum( "...i,...i", P_s, p_s_v )
    pol_ang = np.degrees( np.arctan2( sin_psi_s, cos_psi_s ) ) - psi_i

    return pol_ang_1, pol_ang_2, pol_ang, P_s_1, P_s_2, P_s


def elfouhaily_coefficient( psi_i, phi_i, theta_i,
                            phi_s, theta_s, k_r ):
    """
    Compute the polarization angle of the wave scattered by a perfectly
    conducting surface (with respect to the incident wave polarization), based
    on:
        Elfouhaily, T. et al, A new bistatic model for electromagnetic
        scattering from perfectly conducting random surfaces, Waves in Random
        Media, 1999.

    Parameters
    ----------
    psi_i : float
        polarization orientation of the incident field. psi=0,90 -> H,V
    phi_i : float
        azimuth angle of the source
    theta_i : float
        elevation angle of the source
    phi_s : float
        azimuth angle of the receiver
    theta_s : float
        elevation angle of the receiver
    k_r : float
        radar wave number

    Returns
    -------
    sigma_pq : float
        NRCS
    """
    # v_i = np.zeros(3)
    v_i1 = - np.sin( np.radians( theta_i ) ) * np.sin( np.radians( phi_i ) )
    v_i2 = np.sin( np.radians( theta_i ) ) * np.cos( np.radians( phi_i ) )
    v_i3 = -np.cos( np.radians( theta_i ) )
    v_i = np.stack( (v_i1, v_i2, v_i3), axis = -1 )
    # Compute scattering (STEREOID) plane normal
    # v_s = np.zeros(3)
    v_s1 = np.sin( np.radians( theta_s ) ) * np.sin( np.radians( phi_s ) )
    v_s2 = - np.sin( np.radians( theta_s ) ) * np.cos( np.radians( phi_s ) )
    v_s3 = np.cos( np.radians( theta_s ) )
    v_s = np.stack( (v_s1, v_s2, v_s3), axis = -1 )

    # Wave vector difference
    q = v_s - v_i
    q_h = q.copy()
    q_h[ ..., 2 ] = 0

    Q_h = (v_s / (v_s[ ..., 2 ])[ ..., np.newaxis ] + v_i / (v_i[ ..., 2 ])[ ..., np.newaxis ]) / 2
    Q_h[ ..., 2 ] = 0
    # Incidence field polarization vector
    p_i_v = np.cross( v_i, np.array( [ 0., 0., 1. ] ) )
    p_i_h = np.cross( v_i, p_i_v )
    p_i_v = p_i_v / np.linalg.norm( p_i_v, axis = -1 )[ ..., np.newaxis ]
    p_i_h = p_i_h / np.linalg.norm( p_i_h, axis = -1 )[ ..., np.newaxis ]

    # incoming polarization vector
    P_i = (np.cos( np.radians( psi_i ) )[ ..., np.newaxis ] * p_i_h
           + np.sin( np.radians( psi_i ) )[ ..., np.newaxis ] * p_i_v)

    # get scattered polarization vectors
    pol_ang_1, pol_ang_2, pol_ang, P_s_1, P_s_2, P_s = elfouhaily( psi_i, phi_i, theta_i, phi_s, theta_s )

    # scattering coefficient
    g_pq = ( k_r * q[ 2 ] ) ** 2 * np.sum( P_i * P_s ) ** 2

    return g_pq


def field_to_ellipse( E_h, E_v, psi_i = 0 ):
    """
    Compute orientation and ellipticity of the polarized field component

    Parameters
    ----------
    E_h : complex or numpy.ndarray (n1,..nD, nsims)
        horizontal field. In case of array the polarization is retrieved by
        averaging over the nsims fields
    E_v : complex or numpy.ndarray (n1,..nD, nsims)
        vertical field. In case of array the polarization is retrieved by
        averaging over the nsims fields
    psi_i : float
        Orientation of incidence field (default is 0) [deg]. If psi <> 0, the
        difference (rotation) is computed

    Returns
    -------
    psi_s : float
        Orientation of scattered/received field [deg]
    ellipticity : float
        Ellipticity of scattered/received field [deg]
    """
    # Covariances
    if isinstance( E_h, np.ndarray ):
        Ch = np.squeeze( np.mean( np.abs( E_h ) ** 2, axis = -1 ) )
        Cv = np.squeeze( np.mean( np.abs( E_v ) ** 2, axis = -1 ) )
        Cx = np.squeeze( np.mean( E_h * np.conj( E_v ), axis = -1 ) )

        pol_ang = np.zeros( Ch.size )
        ellipticity = np.zeros( Ch.size )
        for i in range( Ch.size ):
            pol_ang[ i ], ellipticity[ i ] = cov_to_ellipse( Ch.flatten()[ i ],
                                                             Cv.flatten()[ i ],
                                                             Cx.flatten()[ i ] )
        pol_ang = np.reshape( pol_ang, Ch.shape )
        ellipticity = np.reshape( ellipticity, Ch.shape )
    else:
        Ch = np.abs( E_h ) ** 2
        Cv = np.abs( E_v ) ** 2
        Cx = E_h * np.conj( E_v )

        pol_ang, ellipticity = cov_to_ellipse( Ch, Cv, Cx )

    psi_s = np.mod( pol_ang - psi_i + 90, 180 ) - 90
    return psi_s, ellipticity


def cov_to_ellipse( Ch, Cv, Cx, psi_i = 0 ):
    """
    Compute orientation and ellipticity of the polarized field component

    Parameters
    ----------
    Ch : float
        mean[Eh * conj(Eh)]
    Cv : float
        mean[Ev * conj(Ev)]
    Cx : float
        mean[Eh * conj(Ev)]
    psi_i : float
        Orientation of incidence field (default is 0) [deg]. If psi <> 0, the
        difference (rotation) is computed

    Returns
    -------
    psi_s : float
        Orientation of scattered/received field [deg]
    ellipticity : float
        Ellipticity of scattered/received field [deg]
    """
    # Stokes parameters
    Q = Ch - Cv
    U = 2 * np.real( Cx )
    V = -2 * np.imag( Cx )

    pol_ang = 0.5 * np.arctan( U / Q )
    ellipticity = 0.5 * np.arctan( V / np.sqrt( V ** 2 + Q ** 2 ) )
    if (np.abs( pol_ang ) < np.pi / 4) and (Q < 0):
        pol_ang = pol_ang + np.pi / 2
        pol_ang = np.mod( pol_ang + np.pi / 2, np.pi ) - np.pi / 2
    if (np.abs( pol_ang ) > np.pi / 4) and (Q > 0):
        pol_ang = pol_ang + np.pi / 2
        pol_ang = np.mod( pol_ang + np.pi / 2, np.pi ) - np.pi / 2
    if np.abs( pol_ang ) == np.pi / 4:
        pol_ang = np.pi / 4 * np.sign( U )

    psi_s = np.mod( pol_ang - np.radians( psi_i ) + np.pi / 2, np.pi ) - np.pi / 2
    return np.degrees( psi_s ), ellipticity


def field_to_dop( E_h, E_v, psi_i = 0 ):
    """
    Compute degree of polarization from the field (h, v) covariance matrix

    Parameters
    ----------
    Ch : float
        E[E_h*conj(E_h)]
    Cv : float
        E[E_v*conj(E_v)]
    Cx : complex
    Ch : float
        E[E_v*conj(E_h)]

    Returns
    -------
    dop : float
        Degree of polarization (in the 0-1 range, 1 is fully polarized)
    """
    I = np.abs( E_h ) ** 2 + np.abs( E_v ) ** 2
    Q = np.abs( E_h ) ** 2 - np.abs( E_v ) ** 2
    U = 2 * np.real( E_h * np.conj( E_v ) )
    V = -2 * np.imag( E_h * np.conj( E_v ) )

    dop = np.sqrt( Q ** 2 + U ** 2 + V ** 2 ) / I
    return dop


# %%
if __name__ == '__main__':
    theta_i = np.linspace( 20, 45 )
    theta_s = np.linspace( 18, 44 )
    phi_s = 1 * np.linspace( 50, 20 )
    (rot_ang_1, rot_ang_2, rot_ang_tot, Ps1, Ps2, Ps_tot) = elfouhaily( 90, 0, theta_i, phi_s, theta_s )
    plt.figure()
    plt.plot( np.linalg.norm( Ps1, axis = -1 ) )
    plt.plot( np.linalg.norm( Ps2, axis = -1 ) )
    plt.plot( np.linalg.norm( Ps_tot, axis = -1 ) )
