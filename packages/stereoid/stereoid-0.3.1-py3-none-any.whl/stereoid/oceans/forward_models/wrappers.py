"""
Author: Marcel Kleinherenbrink
"""
from typing import Optional, Tuple
import numpy as np
import scipy as sp
import stereoid.oceans.forward_models.backscatter as backscatter
from stereoid.oceans.forward_models.backscatter import backscatter_Kudry2023, backscatter_Kudry2023_polar
from stereoid.oceans.forward_models.Doppler import DopRIM, DopRIM_DP, DopRIM2023_DP, DopRIM2023_DP_polar
from stereoid.oceans.bistatic_pol import elfouhaily as Elf_pol
import scipy.spatial.qhull as qhull
from matplotlib import pyplot as plt

LIST_MONO = ['Bragg', 'specular', 'wave_breaking', 'wave_breaking_cross']
LIST_BI =['Bragg', 'specular', 'wave_breaking', 'Bragg_cross',
          'specular_cross', 'wave_breaking_cross']
LIST_BI_DOP = ['Bragg_hh','Bragg_vv', 'specular', 'wave_breaking', 'Bragg_cross',
               'specular_cross', 'wave_breaking_cross']


def make_grids_mono(shape:np.ndarray, list_key: Optional[list]=LIST_MONO):
    ''' Initialize matrix for mono sensor '''
    s_grd = {}
    d_grd = {}
    # monostatic (completely unnecessary, but okay)
    for key in list_key:
        d_grd[key] = np.zeros(shape)
        s_grd[key] = np.zeros(shape)
    q = np.zeros(shape)  # fraction of surface covered by breakers
    return s_grd, d_grd, q


def make_grids_bistatic(shape: np.ndarray, nrcs_list_key: Optional[list]=LIST_BI,
                        dop_list_key: Optional[list]=LIST_BI_DOP):
    # bistatic (completely unnecessary, but okay)
    s_grd = {}
    d_grd = {}
    for key in nrcs_list_key:
        s_grd[key] = np.zeros(shape)
    for key in dop_list_key:
        d_grd[key] = np.zeros(shape)
    # fraction of surface covered by breakers (just for checking)
    qb1 = np.zeros(shape)
    return s_grd, d_grd, qb1

# Monostatic wrapper for polar spectra
def backscatter_Doppler_mono_polar(S, k, phi, phi_w, obs_geo, U_mean,
                             fetch, degrees=True, u10_local=0, k_r=0):
    """

    Parameters
    ----------
    S
    k
    phi
    phi_w
    obs_geo
    U_mean
    fetch
    degrees
    u10_local
    model:
        Kudry2005: Kudry et al. (2005) for RIM and Hansen et al. (2012) for DopRIM
        Kudry2023: Kudry et al. (2005) with (2023) adjustments for RIM and Hansen et al. (2012) with a few Kudry et al. (2023) adjustments for DopRIM

    Returns
    -------

    """

    # monostatic backscatter (RIM)
    # Radar Imaging Model (RIM)
    sigma_los, dsigmadth, qt = backscatter_Kudry2023_polar(S, k, phi, phi_w=phi_w, theta=obs_geo.inc_m, u_10=U_mean,
                                                      k_r=k_r)
    _, s_wbcr = backscatter.backscatter_crosspol_polar(S, k, phi, theta=obs_geo.inc_m, u_10=U_mean, fetch=fetch)

    s_mono = {'Bragg': sigma_los[1], 'specular': sigma_los[0], 'wave_breaking': sigma_los[3],
              'wave_breaking_cross': s_wbcr}

    s_sp=sigma_los[0]
    s_br = sigma_los[1]
    s_wb = sigma_los[3]
    #s_wbcr = sigma_los[3]

    rat = (np.array([s_sp * (1 - qt), s_br * (1 - qt), s_wb * qt])
           / (s_sp * (1 - qt) + s_br * (1 - qt) + s_wb * qt))

    # monostatic Doppler RIM (DopRIM)
    # FIXME: this is a bit ugly, DopRIM2023_DP calls implicitly backscatter_Kudry2023
    c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh = DopRIM2023_DP_polar(S, k, phi,
                                                                               obs_geo.inc_m, U_mean,
                                                                               phi_w, k_r=k_r)

    # monostatic Doppler components (specular, Bragg, wave breaking)
    # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    d_sp = rat[ 0 ] * (c_sp_bar + c_sp)
    d_br = rat[ 1 ] * (c_br_bar + c_br_vv)
    d_wb = rat[ 2 ] * (c_wb_bar + c_wb)
    d_wbcr = (c_wb_bar + c_wb)
    d_mono = {'Bragg': d_br, 'specular': d_sp, 'wave_breaking': d_wb,
              'wave_breaking_cross': d_wbcr}
    return s_mono, d_mono, qt

# Monostatic equivalent wrapper for polar spectra
def backscatter_Doppler_monoeq_polar(S, k, phi, phi_w, obs_geo_me_angles, obs_geo_angles,
                                 U_mean, fetch, pol, degrees=True, k_r=0, u10_local=0):
    """

    Parameters
    ----------
    S
    k
    phi
    phi_w
    obs_geo_me_angles
    obs_geo_angles
    U_mean
    fetch
    pol
    degrees
    k_r
    u10_local
    model:
        Kudry2005: Kudry et al. (2005) for RIM and Hansen et al. (2012) for DopRIM
        Kudry2023: Kudry et al. (2005) with (2023) adjustments for RIM and Hansen et al. (2012) with a few Kudry et al. (2023) adjustments for DopRIM

    Returns
    -------

    """
    """ This function calculates the contributions to the NRCS and Doppler for the
        monostatic-equivalent system, i.e. without considering the bistatic polarizations,
        which are handled separately. """

    # for now turn swell and currents off
    v_c = 0
    phi_c = 0
    k_sw = 1
    phi_sw = 1
    A_sw = 0.0001

    # polarimetry for rotations
    if pol == 'V':
        pol_in = 90
    if pol == 'H':
        pol_in = 0

    # bistatic backscatter (RIM)
    # start_time = time.time()
    # TODO: pass the monostatic equivalent incident angle instead of the mean of the two.
    # AT: REVIEW
    # TODO: also pass scaled k_r as to functions (right now they are computed inside function)
    # inc_me = obs_geo.swth_geo.inc2me_inc(np.deg2rad(obs_geo.inc_m))
    # bistatic_me = obs_geo.swth_geo.inc2bistatic_angle_az(inc_me)
    # inc_me = np.rad2deg(inc_me)
    # bistatic_me = np.rad2deg(bistatic_me)
    inc_me = obs_geo_me_angles.inc_m
    bistatic_me = obs_geo_angles.bist_ang


    # bistatic Radar Imaging Model (RIM)
    sigma_los, dsigmadth, qt = backscatter_Kudry2023_polar(S, k, phi, phi_w=phi_w, theta=inc_me,
                                                      u_10=U_mean,
                                                      k_r=k_r)
    _, st_wbcr = backscatter.backscatter_crosspol_polar(S, k, phi, theta=inc_me, u_10=U_mean, fetch=fetch,
                                                  k_r=k_r)

    st_sp=sigma_los[0]
    st_br = sigma_los[1]
    st_wb = sigma_los[3]
    st_wbcr = st_wbcr*1.0

    # bistatic Doppler RIM (DopRIM)
    # FIXME: this is a bit ugly, DopRIM2023_DP calls implicitly backscatter_Kudry2023
    c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh = DopRIM2023_DP_polar(S, k, phi,
                                                                               inc_me, U_mean,
                                                                               phi_w, k_r=k_r)


    # bistatic scattering (specular, Bragg, wave breaking)
    sb1_sp = st_sp * (1 - qt)
    sb1_br = st_br * (1 - qt)
    sb1_wb = st_wb * qt
    sb1_spcr = st_sp * (1 - qt) # @Paco, not sure why you did this. It is not used anyway
    sb1_brcr = st_br * (1 - qt)
    sb1_wbcr =  st_wbcr * qt
    s_me = {'Bragg': sb1_br, 'specular': sb1_sp, 'wave_breaking': sb1_wb,'Bragg_cross': sb1_brcr, 'specular_cross': sb1_spcr,'wave_breaking_cross': sb1_wbcr}

    # bistatic Doppler co-pol
    # rat = np.array( [ sb1_sp, sb1_br, sb1_wb ] ) / (
    #             sb1_sp + sb1_br + sb1_wb)
    # PLD: we take the ratios out from here and put them in later when we rotate the polarization
    # db1_sp = rat[ 0 ] * (c_sp_bar + c_sp)  # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    # db1_br = rat[ 1 ] * (c_br_bar + c_br)
    # db1_wb = rat[ 2 ] * (c_wb_bar + c_wb)
    db1_sp = (c_sp_bar + c_sp)  # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    db1_br_vv = (c_br_bar + c_br_vv)
    db1_br_hh = (c_br_bar + c_br_hh)
    db1_wb = (c_wb_bar + c_wb)
    db1_spcr = 0
    db1_brcr = 0
    db1_wbcr = (c_wb_bar + c_wb)
    d_bi = {'Bragg_hh': db1_br_hh, 'Bragg_vv': db1_br_vv, 'specular': db1_sp, 'wave_breaking': db1_wb,
            'Bragg_cross': db1_brcr, 'specular_cross': db1_spcr,
            'wave_breaking_cross': db1_wbcr}

    return s_me, d_bi


def backscatter_Doppler_mono(S, k_x, k_y, dks, phi_w, obs_geo, U_mean,
                             fetch, degrees=True, u10_local=0, model='Kudry2005'):
    """

    Parameters
    ----------
    S
    k_x
    k_y
    dks
    phi_w
    obs_geo
    U_mean
    fetch
    degrees
    u10_local
    model:
        Kudry2005: Kudry et al. (2005) for RIM and Hansen et al. (2012) for DopRIM
        Kudry2023: Kudry et al. (2005) with (2023) adjustments for RIM and Hansen et al. (2012) with a few Kudry et al. (2023) adjustments for DopRIM

    Returns
    -------

    """


    # for now turn swell and currents off
    v_c = 0
    phi_c = 0
    k_sw = 1
    phi_sw = 1
    A_sw = 0.0001

    # monostatic backscatter (RIM)
    if model == 'Kudry2005':
        s_sp, s_br, s_wb, q = backscatter.backscatter_Kudry2005(S, k_x, k_y, dks,
                                                                phi_w, theta=obs_geo.inc_m,
                                                                pol='V',
                                                                u_10=U_mean, degrees=degrees)
        _, s_wbcr = backscatter.backscatter_crosspol(S, k_x, k_y, dks, theta=obs_geo.inc_m,
                                                     alpha=0,
                                                     u_10=U_mean, fetch=fetch, degrees=degrees)
        s_mono = {'Bragg': s_br, 'specular': s_sp, 'wave_breaking': s_wb,
                  'wave_breaking_cross': s_wbcr}

        # monostatic ratio of scattering
        rat = (np.array([s_sp * (1 - q), s_br * (1 - q), s_wb * q ])
                / (s_sp * (1 - q) + s_br * (1 - q) + s_wb * q))

        # monostatic Doppler RIM (DopRIM)
        _, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br = DopRIM(S, k_x, k_y, dks, obs_geo.inc_m,
                                                                    obs_geo.bist_ang, v_c,
                                                                    phi_c, k_sw,
                                                                    phi_sw, A_sw,
                                                                    phi_w, U_mean,
                                                                    pol ='V', rat=rat,
                                                                    u_10_local=u10_local)

    if model == 'Kudry2023':
        # Radar Imaging Model (RIM)
        sigma_los, dsigmadth, q_s = backscatter_Kudry2023(S, k_x, k_y, dks, phi_w=phi_w, theta=obs_geo.inc_m, u_10=U_mean,
                                                          k_r=0, degrees=False)
        _, s_wbcr = backscatter.backscatter_crosspol(S, k_x, k_y, dks, theta=obs_geo.inc_m,
                                                     alpha=0,
                                                     u_10=U_mean, fetch=fetch, degrees=degrees)

        s_mono = {'Bragg': sigma_los[1], 'specular': sigma_los[0], 'wave_breaking': sigma_los[3],
                  'wave_breaking_cross': s_wbcr}
        s_sp = sigma_los[0]
        s_br = sigma_los[1]
        s_wb = sigma_los[3]
        #s_wbcr = sigma_los[3]

        rat = (np.array([s_sp * (1 - q_s), s_br * (1 - q_s), s_wb * q_s])
               / (s_sp * (1 - q_s) + s_br * (1 - q_s) + s_wb * q_s))

        # monostatic Doppler RIM (DopRIM)
        # FIXME: this is a bit ugly, DopRIM2023_DP calls implicitly backscatter_Kudry2023
        c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh = DopRIM2023_DP(S, k_x, k_y, dks,
                                                                                   obs_geo.inc_m, U_mean,
                                                                                   phi_w, k_r=0)

    # monostatic Doppler components (specular, Bragg, wave breaking)
    # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    d_sp = rat[ 0 ] * (c_sp_bar + c_sp)
    d_br = rat[ 1 ] * (c_br_bar + c_br_vv)
    d_wb = rat[ 2 ] * (c_wb_bar + c_wb)
    d_wbcr = (c_wb_bar + c_wb)
    d_mono = {'Bragg': d_br, 'specular': d_sp, 'wave_breaking': d_wb,
              'wave_breaking_cross': d_wbcr}
    return s_mono, d_mono, q

def backscatter_Doppler_monoeq(S, k_x, k_y, dks, phi_w, obs_geo_me_angles, obs_geo_angles,
                                 U_mean, fetch, pol, degrees=True, k_r=0, u10_local=0, model='Kudry2005'):
    """

    Parameters
    ----------
    S
    k_x
    k_y
    dks
    phi_w
    obs_geo_me_angles
    obs_geo_angles
    U_mean
    fetch
    pol
    degrees
    k_r
    u10_local
    model:
        Kudry2005: Kudry et al. (2005) for RIM and Hansen et al. (2012) for DopRIM
        Kudry2023: Kudry et al. (2005) with (2023) adjustments for RIM and Hansen et al. (2012) with a few Kudry et al. (2023) adjustments for DopRIM

    Returns
    -------

    """
    """ This function calculates the contributions to the NRCS and Doppler for the
        monostatic-equivalent system, i.e. without considering the bistatic polarizations,
        which are handled separately. """

    # for now turn swell and currents off
    v_c = 0
    phi_c = 0
    k_sw = 1
    phi_sw = 1
    A_sw = 0.0001

    # polarimetry for rotations
    if pol == 'V':
        pol_in = 90
    if pol == 'H':
        pol_in = 0

    # bistatic backscatter (RIM)
    # start_time = time.time()
    # TODO: pass the monostatic equivalent incident angle instead of the mean of the two.
    # AT: REVIEW
    # TODO: also pass scaled k_r as to functions (right now they are computed inside function)
    # inc_me = obs_geo.swth_geo.inc2me_inc(np.deg2rad(obs_geo.inc_m))
    # bistatic_me = obs_geo.swth_geo.inc2bistatic_angle_az(inc_me)
    # inc_me = np.rad2deg(inc_me)
    # bistatic_me = np.rad2deg(bistatic_me)
    inc_me = obs_geo_me_angles.inc_m
    bistatic_me = obs_geo_angles.bist_ang
    if model == 'Kudry2005':
        st_sp, st_br, st_wb, qt = backscatter.backscatter_Kudry2005( S, k_x, k_y, dks, phi_w, theta=inc_me,
                                                                     alpha = bistatic_me, pol = pol,
                                                                     u_10 = U_mean, degrees=degrees,
                                                                     k_r=k_r )
        _, st_wbcr = backscatter.backscatter_crosspol( S, k_x, k_y, dks, theta=inc_me,
                                                       alpha = bistatic_me, u_10 = U_mean, fetch = fetch, degrees=degrees,
                                                       k_r=k_r )
        # print('RIM: ' + str(start_time-time.time()))

        # bistatic polarization rotations
        # start_time = time.time()

        # ratio of scattering (this is fake, but it does not matter)
        rat = [0, 0, 0]

        # bistatic Doppler RIM (DopRIM)
        # start_time = time.time()
        # AT: REVIEW use the ME inc angle.
        (c_sp_bar, c_wb_bar, c_br_bar,
         c_sp, c_wb, c_br_hh, c_br_vv) = DopRIM_DP(S, k_x, k_y, dks, inc_me,
                                                   obs_geo_angles.bist_ang, v_c, phi_c, k_sw, phi_sw, A_sw,
                                                   phi_w, U_mean, rat = rat, k_r=k_r,
                                                   u_10_local=u10_local)
        # print('DopRIM: ' + str(start_time-time.time()))

    if model == 'Kudry2023':
        # bistatic Radar Imaging Model (RIM)
        sigma_los, dsigmadth, qt = backscatter_Kudry2023(S, k_x, k_y, dks, phi_w=phi_w, theta=inc_me,
                                                          u_10=U_mean,
                                                          k_r=k_r, degrees=False)
        _, st_wbcr = backscatter.backscatter_crosspol(S, k_x, k_y, dks, theta=inc_me,
                                                      alpha=bistatic_me, u_10=U_mean, fetch=fetch, degrees=degrees,
                                                      k_r=k_r)

        st_sp=sigma_los[0]
        st_br = sigma_los[1]
        st_wb = sigma_los[3]
        st_wbcr = st_wbcr*1.0

        # bistatic Doppler RIM (DopRIM)
        # FIXME: this is a bit ugly, DopRIM2023_DP calls implicitly backscatter_Kudry2023
        c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br_vv, c_br_hh = DopRIM2023_DP(S, k_x, k_y, dks,
                                                                                   inc_me, U_mean,
                                                                                   phi_w, k_r=k_r)


    # bistatic scattering (specular, Bragg, wave breaking)
    sb1_sp = st_sp * (1 - qt)
    sb1_br = st_br * (1 - qt)
    sb1_wb = st_wb * qt
    sb1_spcr = st_sp * (1 - qt) # @Paco, not sure why you did this. It is not used anyway
    sb1_brcr = st_br * (1 - qt)
    sb1_wbcr =  st_wbcr * qt
    s_me = {'Bragg': sb1_br, 'specular': sb1_sp, 'wave_breaking': sb1_wb,'Bragg_cross': sb1_brcr, 'specular_cross': sb1_spcr,'wave_breaking_cross': sb1_wbcr}

    # bistatic Doppler co-pol
    # rat = np.array( [ sb1_sp, sb1_br, sb1_wb ] ) / (
    #             sb1_sp + sb1_br + sb1_wb)
    # PLD: we take the ratios out from here and put them in later when we rotate the polarization
    # db1_sp = rat[ 0 ] * (c_sp_bar + c_sp)  # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    # db1_br = rat[ 1 ] * (c_br_bar + c_br)
    # db1_wb = rat[ 2 ] * (c_wb_bar + c_wb)
    db1_sp = (c_sp_bar + c_sp)  # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    db1_br_vv = (c_br_bar + c_br_vv)
    db1_br_hh = (c_br_bar + c_br_hh)
    db1_wb = (c_wb_bar + c_wb)
    db1_spcr = 0
    db1_brcr = 0
    db1_wbcr = (c_wb_bar + c_wb)
    d_bi = {'Bragg_hh': db1_br_hh, 'Bragg_vv': db1_br_vv, 'specular': db1_sp, 'wave_breaking': db1_wb,
            'Bragg_cross': db1_brcr, 'specular_cross': db1_spcr,
            'wave_breaking_cross': db1_wbcr}

    return s_me, d_bi

# this breaks up the griddata interpolator to get indices
# got this from: https://stackoverflow.com/questions/20915502/speedup-scipy-griddata-for-multiple-interpolations-between-two-irregular-grids
def interp_weights(xy, uv,d=2):
    tri = qhull.Delaunay(xy)
    simplex = tri.find_simplex(uv)
    vertices = np.take(tri.simplices, simplex, axis=0)
    temp = np.take(tri.transform, simplex, axis=0)
    delta = uv - temp[:, d]
    bary = np.einsum('njk,nk->nj', temp[:, :d, :], delta)
    return vertices, np.hstack((bary, 1 - bary.sum(axis=1, keepdims=True)))

def interpolate(values, vtx, wts):
    return np.einsum('nj,nj->n', np.take(values, vtx), wts)


def plot_grids(SP,BR,WB,res,grid_type='Doppler',ti='co-pol mono',co='plasma',vmin=0,vmax=0):
    # res: resolution of the grid
    # co: colormap
    # ti: add text for title
    if np.logical_and(vmin==0,vmax==0):
        if grid_type == 'Doppler':
            vmin=-3
            vmax=3
        else:
            vmin=0
            vmax=0.25

    # get shape
    SHP=SP.shape

    plt.figure( figsize = (15, 6) )
    plt.subplot( 1, 4, 1 )
    plt.imshow( SP, origin = 'lower', extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co, vmin=vmin, vmax=vmax)
    plt.colorbar( orientation = 'horizontal' )
    plt.title( 'specular ' + grid_type )
    plt.xlabel('cross-track distance [m]')
    plt.ylabel( 'along-track distance [m]' )
    plt.subplot( 1, 4, 2 )
    plt.imshow( BR, origin = 'lower', extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co, vmin=vmin, vmax=vmax )
    plt.colorbar( orientation = 'horizontal' )
    plt.title( 'Bragg ' + grid_type )
    plt.xlabel('cross-track distance [m]')
    # plt.ylabel('along-track distance [m]')
    plt.subplot( 1, 4, 3 )
    plt.imshow( WB, origin = 'lower', extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co, vmin=vmin, vmax=vmax )
    plt.colorbar( orientation = 'horizontal' )
    plt.title( 'wave breaking ' + grid_type )
    plt.xlabel( 'cross-track distance [m]' )
    # plt.ylabel('along-track distance [m]')
    plt.subplot( 1, 4, 4 )
    plt.imshow( SP+BR+WB, origin = 'lower',
                extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co, vmin=vmin, vmax=vmax )
    plt.colorbar( orientation = 'horizontal' )
    plt.title( ti + grid_type )
    plt.xlabel( 'cross-track distance [m]' )
    # plt.ylabel('along-track distance [m]')


    return 0

### Do not use this one ###
def backscatter_Doppler_bistatic(S, k_x, k_y, dks, phi_w, obs_geo_me_angles, obs_geo_angles,
                                 U_mean, fetch, pol, degrees=True,k_r=0, u10_local=0):

    # for now turn swell and currents off
    v_c = 0
    phi_c = 0
    k_sw = 1
    phi_sw = 1
    A_sw = 0.0001

    # polarimetry for rotations
    if pol == 'V':
        pol_in = 90
    if pol == 'H':
        pol_in = 0

    # bistatic backscatter (RIM)
    # start_time = time.time()
    # TODO: pass the monostatic equivalent incident angle instead of the mean of the two.
    # AT: REVIEW
    # TODO: also pass scaled k_r as to functions (right now they are computed inside function)
    # inc_me = obs_geo.swth_geo.inc2me_inc(np.deg2rad(obs_geo.inc_m))
    # bistatic_me = obs_geo.swth_geo.inc2bistatic_angle_az(inc_me)
    # inc_me = np.rad2deg(inc_me)
    # bistatic_me = np.rad2deg(bistatic_me)
    inc_me = obs_geo_me_angles.inc_m
    bistatic_me = obs_geo_angles.bist_ang
    st_sp, st_br, st_wb, qt = backscatter.backscatter_Kudry2005( S, k_x, k_y, dks, phi_w, theta=inc_me,
                                                                 alpha = bistatic_me, pol = pol,
                                                                 u_10 = U_mean, degrees=degrees,
                                                                 k_r=k_r )
    _, st_wbcr = backscatter.backscatter_crosspol( S, k_x, k_y, dks, theta=inc_me,
                                                   alpha = bistatic_me, u_10 = U_mean, fetch = fetch, degrees=degrees,
                                                   k_r=k_r )
    # print('RIM: ' + str(start_time-time.time()))

    # bistatic polarization rotations
    # start_time = time.time()
    # TODO: we will remove from here the bistatic conversion and do it later
    # starting from the per-polarization combined monostatic equivalent
    # componemts
    (rot1, rot2, rot12, P1, P2, P12) = Elf_pol( pol_in, 0, inc_me, 0, inc_me )
    Pbr = np.sum( P12 ** 2 )  # Bragg scattering
    Pnbr = np.sum( P1 ** 2 )  # non-Bragg scattering
    (rot1, rot2, rot12, P1, P2, P12) = Elf_pol( pol_in, -obs_geo_angles.bist_ang / 2, obs_geo_angles.inc_m,
                                                obs_geo_angles.bist_ang / 2, obs_geo_angles.inc_b )
    Pbr = np.sum( P12 ** 2 ) / Pbr  # scaled power for Bragg scattering
    Pnbr = np.sum( P1 ** 2 ) / Pnbr  # scaled power for non-Bragg scattering
    # print('polarization: ' + str(start_time-time.time()))

    # bistatic scattering (specular, Bragg, wave breaking)
    sb1_sp = st_sp * (1 - qt) * np.cos( np.deg2rad( rot1 ) ) ** 2 * Pnbr
    sb1_br = st_br * (1 - qt) * np.cos( np.deg2rad( rot12 ) ) ** 2 * Pbr
    sb1_wb = st_wb * qt * np.cos( np.deg2rad( rot1 ) ) ** 2 * Pnbr + st_wbcr * qt * np.sin(
        np.deg2rad( rot1 ) ) ** 2 * Pnbr
    sb1_spcr = st_sp * (1 - qt) * np.sin( np.deg2rad( rot1 ) ) ** 2 * Pnbr
    sb1_brcr = st_br * (1 - qt) * np.sin( np.deg2rad( rot12 ) ) ** 2 * Pbr
    sb1_wbcr = st_wb * qt * np.sin( np.deg2rad( rot1 ) ) ** 2 * Pnbr + st_wbcr * qt * np.cos(
        np.deg2rad( rot1 ) ) ** 2 * Pnbr
    s_bi = {'Bragg': sb1_br, 'specular': sb1_sp, 'wave_breaking': sb1_wb,
            'Bragg_cross': sb1_brcr, 'specular_cross': sb1_spcr,
            'wave_breaking_cross': sb1_wbcr}

    # ratio of scattering (this is fake, but it does not matter)
    rat = [0, 0, 0]

    # bistatic Doppler RIM (DopRIM)
    # start_time = time.time()
    # AT: REVIEW use the ME inc angle.
    _, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br = DopRIM( S, k_x, k_y, dks, inc_me,
                                                                obs_geo_angles.bist_ang, v_c, phi_c, k_sw, phi_sw, A_sw,
                                                                phi_w, U_mean, pol = pol, rat = rat,
                                                                u_10_local=u10_local )
    # print('DopRIM: ' + str(start_time-time.time()))

    # bistatic Doppler co-pol
    rat = np.array( [ sb1_sp, sb1_br, sb1_wb ] ) / (
                sb1_sp + sb1_br + sb1_wb)
    db1_sp = rat[ 0 ] * (c_sp_bar + c_sp)  # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    db1_br = rat[ 1 ] * (c_br_bar + c_br)
    db1_wb = rat[ 2 ] * (c_wb_bar + c_wb)

    # bistatic Doppler cross-pol
    rat = np.array( [ sb1_spcr, sb1_brcr, sb1_wbcr ] ) / (
                sb1_spcr + sb1_brcr + sb1_wbcr)
    db1_spcr = rat[ 0 ] * (c_sp_bar + c_sp)
    db1_brcr = rat[ 1 ] * (c_br_bar + c_br)
    db1_wbcr = rat[ 2 ] * (c_wb_bar + c_wb)
    d_bi = {'Bragg': db1_br, 'specular': db1_sp, 'wave_breaking': db1_wb,
            'Bragg_cross': db1_brcr, 'specular_cross': db1_spcr,
            'wave_breaking_cross': db1_wbcr}

    return s_bi, d_bi