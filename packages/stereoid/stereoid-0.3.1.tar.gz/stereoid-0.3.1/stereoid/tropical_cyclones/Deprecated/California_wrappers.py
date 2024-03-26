import numpy as np
import stereoid.tropical_cyclones.Deprecated.backscatter as backscatter
from stereoid.tropical_cyclones.Deprecated.Doppler import DopRIM
from stereoid.oceans.bistatic_pol import elfouhaily as Elf_pol
import scipy.spatial.qhull as qhull
from matplotlib import pyplot as plt

def make_grids_mono(SHP):
    # monostatic (completely unnecessary, but okay)
    s_sp = np.zeros( SHP )  # specular scattering
    s_br = np.zeros( SHP )  # Bragg scattering
    s_wb = np.zeros( SHP )  # wave breaking
    s_wbcr = np.zeros( SHP )  # wave breaking cross
    d_sp = np.zeros( SHP )  # specular scattering
    d_br = np.zeros( SHP )  # Bragg scattering
    d_wb = np.zeros( SHP )  # wave breaking
    q = np.zeros( SHP )  # fraction of surface covered by breakers
    return s_sp,s_br,s_wb,s_wbcr,d_sp,d_br,d_wb,q

def make_grids_bistatic(SHP):
    # bistatic (completely unnecessary, but okay)
    sb1_sp = np.zeros( SHP )  # specular scattering
    sb1_br = np.zeros( SHP )  # Bragg scattering
    sb1_wb = np.zeros( SHP )  # wave breaking
    sb1_spcr = np.zeros( SHP )  # specular cross
    sb1_brcr = np.zeros( SHP )  # Bragg cross
    sb1_wbcr = np.zeros( SHP )  # wave breaking cross
    db1_sp = np.zeros( SHP )  # specular Doppler
    db1_br = np.zeros( SHP )  # Bragg Doppler
    db1_wb = np.zeros( SHP )  # wave breaking Doppler
    db1_spcr = np.zeros( SHP )  # specular cross Doppler
    db1_brcr = np.zeros( SHP )  # Bragg cross Doppler
    db1_wbcr = np.zeros( SHP )  # wave breaking cross Doppler
    qb1 = np.zeros( SHP )  # fraction of surface covered by breakers (just for checking)
    return sb1_sp,sb1_br,sb1_wb,sb1_spcr,sb1_brcr,sb1_wbcr,db1_sp,db1_br,db1_wb,db1_spcr,db1_brcr,db1_wbcr,qb1


def backscatter_Doppler_mono(S, k_x, k_y, dks, phi_w, inc_m, bist_ang, U_mean, fetch):

    # for now turn swell and currents off
    v_c=0
    phi_c=0
    k_sw=1
    phi_sw=1
    A_sw=1

    # monostatic backscatter (RIM)
    s_sp, s_br, s_wb, q = backscatter.backscatter_Kudry2005( S, k_x, k_y, dks, phi_w,
                                                             theta = inc_m, pol = 'V',
                                                             u_10 = U_mean )
    _, s_wbcr = backscatter.backscatter_crosspol( S, k_x, k_y, dks, theta = bist_ang, alpha = 0,
                                                  u_10 = U_mean, fetch = fetch )

    # monostatic ratio of scattering
    rat = np.array( [ s_sp * (1 - q), s_br * (1 - q), s_wb * q ] ) / (
            s_sp * (1 - q) + s_br * (1 - q) + s_wb * q)

    # monostatic Doppler RIM (DopRIM)
    _, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br = DopRIM( S, k_x, k_y, dks, inc_m,
                                                                bist_ang, v_c,
                                                                phi_c, k_sw, phi_sw, A_sw, phi_w, U_mean, pol = 'V',
                                                                rat = rat )

    # monostatic Doppler components (specular, Bragg, wave breaking)
    d_sp = rat[ 0 ] * (c_sp_bar + c_sp)  # note that c_sp is actually c_sp*sL_sp (eq. 5 + 8 in H12)
    d_br = rat[ 1 ] * (c_br_bar + c_br)
    d_wb = rat[ 2 ] * (c_wb_bar + c_wb)  # this is the same in cross and co

    return s_sp, s_br, s_wb, q, s_wbcr, d_sp, d_br, d_wb

def backscatter_Doppler_bistatic(S, k_x, k_y, dks, phi_w, inc_m, inc_b, bist_ang, U_mean, fetch, pol):

    # for now turn swell and currents off
    v_c=0
    phi_c=0
    k_sw=1
    phi_sw=1
    A_sw=1

    # polarimetry for rotations
    if pol == 'V':
        pol_in = 90
    if pol == 'H':
        pol_in = 0

    # bistatic backscatter (RIM)
    # start_time = time.time()
    st_sp, st_br, st_wb, qt = backscatter.backscatter_Kudry2005( S, k_x, k_y, dks, phi_w, theta = inc_m,
                                                                 alpha = bist_ang, pol = pol,
                                                                 u_10 = U_mean )
    _, st_wbcr = backscatter.backscatter_crosspol( S, k_x, k_y, dks, theta = inc_m,
                                                   alpha = bist_ang, u_10 = U_mean, fetch = fetch )
    # print('RIM: ' + str(start_time-time.time()))

    # bistatic polarization rotations
    # start_time = time.time()
    (rot1, rot2, rot12, P1, P2, P12) = Elf_pol( pol_in, 0, inc_m, 0, inc_m )
    Pbr = np.sum( P12 ** 2 )  # Bragg scattering
    Pnbr = np.sum( P1 ** 2 )  # non-Bragg scattering
    (rot1, rot2, rot12, P1, P2, P12) = Elf_pol( pol_in, -bist_ang / 2, inc_m,
                                                bist_ang / 2, inc_b )
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

    # ratio of scattering (this is fake, but it does not matter)
    rat = [ 0, 0, 0 ]

    # bistatic Doppler RIM (DopRIM)
    # start_time = time.time()
    _, c_sp_bar, c_wb_bar, c_br_bar, c_sp, c_wb, c_br = DopRIM( S, k_x, k_y, dks, inc_m,
                                                                bist_ang, v_c, phi_c, k_sw, phi_sw, A_sw,
                                                                phi_w, U_mean, pol = pol, rat = rat )
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

    return sb1_sp, sb1_br, sb1_wb, sb1_spcr, sb1_brcr, sb1_wbcr, db1_sp, db1_br, db1_wb, db1_spcr, db1_brcr, db1_wbcr

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


def plot_grids(SP,BR,WB,res,grid_type='Doppler',ti='co-pol mono',co='plasma'):
    # res: resolution of the grid
    # co: colormap
    # ti: add text for title

    # get shape
    SHP=SP.shape

    plt.figure( figsize = (15, 6) )
    plt.subplot( 1, 4, 1 )
    plt.imshow( SP, origin = 'lower', extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co )
    plt.colorbar( orientation = 'horizontal' )
    plt.title( 'specular ' + grid_type )
    plt.xlabel('cross-track distance [m]')
    plt.ylabel( 'along-track distance [m]' )
    plt.subplot( 1, 4, 2 )
    plt.imshow( BR, origin = 'lower', extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co )
    plt.colorbar( orientation = 'horizontal' )
    plt.title( 'Bragg ' + grid_type )
    plt.xlabel('cross-track distance [m]')
    # plt.ylabel('along-track distance [m]')
    plt.subplot( 1, 4, 3 )
    plt.imshow( WB, origin = 'lower', extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co )
    plt.colorbar( orientation = 'horizontal' )
    plt.title( 'wave breaking ' + grid_type )
    plt.xlabel( 'cross-track distance [m]' )
    # plt.ylabel('along-track distance [m]')
    plt.subplot( 1, 4, 4 )
    plt.imshow( SP+BR+WB, origin = 'lower',
                extent = (0, SHP[ 1 ] * res, 0, SHP[ 0 ] * res), cmap = co )
    plt.colorbar( orientation = 'horizontal' )
    plt.title( ti + grid_type )
    plt.xlabel( 'cross-track distance [m]' )
    # plt.ylabel('along-track distance [m]')

    return 0
