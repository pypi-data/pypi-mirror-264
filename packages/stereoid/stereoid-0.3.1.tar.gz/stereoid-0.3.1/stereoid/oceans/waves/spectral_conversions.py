"""
Author: Marcel Kleinherenbrink
"""

import os
import numpy as np
import scipy as sp
from scipy.interpolate import griddata


# converts a polar SWAN-type spectrum (f,phi) to a Cartesian (kx,ky) spectrum
# assumes deep-water conditions
def SWAN2Cartesian( E, f_s, phi_s, kx, ky, dks ):
    # E [m^2/Hz/deg]: two-dimensional wave spectrum from SWAN (in polar coordinates
    # f [Hz]: one-dimensional frequency (as output from SWAN)
    # phi [deg]: one-dimensional direction (as output from SWAN)
    # kx [rad/m]: two-dimensional cross-track wave number
    # ky [rad/m]: two-dimensional along-track wave number
    # grid cell size [(rad/m)^2]: two-dimensional grid cell size

    # to radians
    dphi = np.absolute( phi_s[ 1 ] - phi_s[ 0 ] )
    phi_s = np.deg2rad( phi_s )

    # compute wave numbers
    g = 9.81
    omega_s = 2 * np.pi * f_s
    k_s = omega_s ** 2 / g
    kx_s = np.outer( k_s, np.cos( phi_s ) )
    ky_s = np.outer( k_s, np.sin( phi_s ) )

    # df
    df = np.reshape( np.gradient( f_s ), [ len( f_s ), 1 ] )
    df = np.outer( df, np.ones( (len( phi_s ), 1) ) )

    # regridding to Cartesian
    E_int = griddata( (kx_s.ravel(), ky_s.ravel()), E.ravel(), (kx.ravel(), ky.ravel()) )
    E_int = np.reshape( E_int, (kx.shape) )

    # rescaling (the wave height, i.e. spectral energy, should be the same)
    k = np.sqrt( kx ** 2 + ky ** 2 )
    I = np.logical_and( E_int == E_int, k != 0 )
    sc = 1 / (2 * k) * np.sqrt( g / k ) * 180 / np.pi / (2 * np.pi)
    S = np.where( I, E_int * sc, 0 )

    return S

# scales and interpolated a polar SWAN-type spectrum (f,phi) to another polar (k,phi) spectrum
# assumes deep-water conditions
def SWAN2Polar( E, f_s, phi_s, k, phi ):
    """

    Parameters
    ----------
    E: SWAN wave spectrum read with the wavespectra package
    f_s: frequency vector (1D) of SWAN wave spectrum
    phi_s: direction vector (1D) of SWAN wave spectrum (converted from Nautical to Cartesian convention)
    k: wave number vector (1D) for interpolation
    phi: direction vector (1D) for interpolation (radians)

    Returns
    -------
    S: polar spectrum normalized such that Hs=4*sqrt(int int S k dphi dk)
    """

    # to radians
    #dphi = np.absolute( phi_s[ 1 ] - phi_s[ 0 ] )
    phi_s = np.deg2rad( phi_s )

    # we do the interpolation on Cartesian coordinates
    # compute wave numbers for SWAN
    g = 9.81
    omega_s = 2 * np.pi * f_s
    k_s = omega_s ** 2 / g
    kx_s = np.outer( k_s, np.cos( phi_s ) )
    ky_s = np.outer( k_s, np.sin( phi_s ) )

    # compute wave numbers for the interpolation grid
    k, phi = np.meshgrid(k, phi)
    kx = k * np.cos(phi)
    ky = k * np.sin(phi)

    # df
    df = np.reshape( np.gradient( f_s ), [ len( f_s ), 1 ] )
    #df = np.outer( df, np.ones( (len( phi_s ), 1) ) )

    # regridding to Cartesian
    E_int = griddata( (kx_s.ravel(), ky_s.ravel()), E.ravel(), (kx.ravel(), ky.ravel()) )
    E_int = np.reshape( E_int, (k.shape) )

    # rescaling (the wave height, i.e. spectral energy, should be the same)
    k = np.sqrt( kx ** 2 + ky ** 2 )
    I = np.logical_and( E_int == E_int, k != 0 )
    sc = 1 / (2 * k) * np.sqrt( g / k ) * 180 / np.pi / (2 * np.pi)
    S = np.where( I, E_int * sc, 0 )

    return S


if __name__ == "__main__":
    import matplotlib.pyplot as plt
