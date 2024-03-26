import os

import numpy as np
import matplotlib.pyplot as plt

from drama import utils as utls
from drama.io import cfg
from drama import geo as sargeo
from drama.geo.bistatic_pol import CompanionPolarizations


def fullpol_rotation_matrix(dphi_p, dphi_q):
    """Comptes rotation matrix to change pol covariance matrix from one basis into
    another.

    Parameters
    ----------
    dphi_p : float or np.array
        Relative rotation of target transmit pol basis respect to source.
    dphi_q : float or np.array
        Relative rotation of target receive pol basis respect to source..

    Returns
    -------
    nd.array
        Description of returned object.

    """
    if not type(dphi_p) is np.ndarray:
        dphi_p = np.array(dphi_p)
    if not type(dphi_q) is np.ndarray:
        dphi_q = np.array(dphi_q)
    rp = np.zeros(dphi_p.shape + (2,2))
    rp[..., 0, 0] = np.cos(dphi_p)
    rp[..., 1, 1] = np.cos(dphi_p)
    rp[..., 0, 1] = np.sin(dphi_p)
    rp[..., 1, 0] = -np.sin(dphi_p)
    rq = np.zeros(dphi_q.shape + (2,2))
    rq[..., 0, 0] = np.cos(dphi_q)
    rq[..., 1, 1] = np.cos(dphi_q)
    rq[..., 0, 1] = np.sin(dphi_q)
    rq[..., 1, 0] = -np.sin(dphi_q)
    r_fp = np.zeros(dphi_q.shape + (4,4))
    r_fp[...,0:2, 0:2] = rq[..., 0, 0, np.newaxis, np.newaxis] * rp
    r_fp[...,0:2, 2:4] = rq[..., 0, 1, np.newaxis, np.newaxis] * rp
    r_fp[...,2:4, 0:2] = rq[..., 1, 0, np.newaxis, np.newaxis] * rp
    r_fp[...,2:4, 2:4] = rq[..., 1, 1, np.newaxis, np.newaxis] * rp
    return r_fp

def monoeq2bistatic_fp(sigma_vv_r, sigma_s, sigma_cp, theta_i, polgeo, sigma_hh_r=None, txpol='V', ascending=True, rxpol='IO'):
    """Short summary.

    Parameters
    ----------
    sigma_vv_r : float or np.ndarray
        regular (Bragg-like) NRCS for the equivalent monostatic case assuming VV polarization.
    sigma_s : float or np.ndarray
        scalar (specular-like) NRCS for the equivalent monostatic case.
    sigma_cp : float or np.ndarray
        cross-pol  NRCS for the equivalent monostatic case.
    theta_i : float or np.ndarray
        Angle of incidence of transmitted signal, in radians
    polgeo : CompanionPolarizations
        Intance of CompanionPolarizations, which contains all relevant geometry.
    txpol : string
        This can be 'v' (default). 'h' or 'H', or anything else, which will be interpreted
        as full-pol.
    ascending : bool
        True for ascending orbit.

    Returns
    -------
    np.ndarray
        The the polarimetric covariance matrix of the received signal in I-O basis.
        The output will have dimenions consistent with sigma_r, sigma_vv_r and
        theta_i, with two dimenions added (2x2 or 4x4) for the covariance.

    """

    # Amplitude reference for equivalent monostatic case
    theta_i_me = polgeo.inc2me_inc(theta_i)
    from drama.geo.bistatic_pol import elfouhaily
    (rot_ang_1, rot_ang_2, rot_ang_tot,
     Ps_KA_mono, Ps2, Ps_2nd_mono) = elfouhaily(np.pi/2, 0,
                                                theta_i_me, 0,
                                                theta_i_me)
    phi_p = polgeo.inc2PTProt(theta_i, ascending=ascending)
    phi_q = polgeo.inc2PRProt(theta_i, ascending=ascending)
    if rxpol == 'mM':
        r_fp = fullpol_rotation_matrix(-phi_p, 0)
    else:
        phi_IO = polgeo.inc2IOrot(theta_i, ascending=ascending)
        r_fp = fullpol_rotation_matrix(-phi_p, -(phi_q - phi_IO))
    if np.iscomplexobj(sigma_vv_r):
        complexcov = True
        cov_mM = np.zeros(sigma_vv_r.shape + (4,4), dtype=complex)
    else:
        complexcov = False
        cov_mM = np.zeros(sigma_vv_r.shape + (4,4))
    # Add Bragg-like component
    sigma_norm_vv_r = sigma_vv_r / (np.linalg.norm(Ps_2nd_mono, axis=-1)**2)
    if sigma_hh_r is None:
        sigma_norm_hh_r = sigma_norm_vv_r
    else:
        # This is conceptually wrong and will only work if the user knows what he/she is doing
        # it is intended to for Doppler computations.
        sigma_norm_hh_r = sigma_hh_r / (np.linalg.norm(Ps_2nd_mono, axis=-1)**2)

    cov_mM[...,0, 0] = sigma_norm_hh_r * (polgeo.inc2Elfouhailiynorm(theta_i, txpol='m', ascending=ascending)**2)
    cov_mM[...,3, 3] = sigma_norm_vv_r * (polgeo.inc2Elfouhailiynorm(theta_i, txpol='M', ascending=ascending)**2)
    # Here we assume full correlation
    cov_mM[...,0, 3] = np.sqrt(cov_mM[...,0, 0] * cov_mM[...,3, 3])
    cov_mM[...,3, 0] = cov_mM[...,0, 3]
    # Add scalar component
    cov_mM[...,0, 0] += sigma_s
    cov_mM[...,3, 3] += sigma_s
    # Here we assume full correlation
    cov_mM[...,0, 3] += sigma_s
    cov_mM[...,3, 0] += sigma_s
    #cov_mM[...,0, 0] = sigma_norm_r * (2 - polgeo.inc2Elfouhailiynorm(inc, txpol='m'))
    # Cross-pol component. Assumptions
    # 1. cross-pol is uncorrelated from co-pol
    # 2. we assume, and this is wrong, that the two cross-pol scattering coeffients are the same, which is
    # true in the monostatic limit but must likely wrong in the bistatic case. For moderate bistatic geometries
    # the assumption should not be a dissaster, in particular considering that we operate dual-pol, so we never
    # really see the effect
    # 3. In the monostatic case sigma_hv = sigma_vh, which means that the magnitude of the cross-pol is
    # independent of the incidence polarization, event though the second order scattering isn't.
    cov_mM[...,1, 1] =  1.1*sigma_cp#[..., np.newaxis, np.newaxis]
    cov_mM[...,2, 2] =  sigma_cp#[..., np.newaxis, np.newaxis]
    cov_mM[...,1, 2] =  np.sqrt(1.1) * sigma_cp#[..., np.newaxis, np.newaxis]
    cov_mM[...,2, 1] =  np.sqrt(1.1) * sigma_cp
    # Now we rotate from minor-mayor basis to HV-IO
    aux = np.einsum("...ij,...jk->...ik", r_fp, cov_mM)
    cov_HV2IO = np.einsum("...ij,...kj->...ik", aux, r_fp)
    if (txpol == 'V' or txpol == 'v'):
        return cov_HV2IO[..., 1::2, 1::2]
    elif (txpol == 'H' or txpol == 'h'):
        return cov_HV2IO[..., 0::2, 0::2]
    else:
        # Full pol
        return cov_HV2IO


def monoeq2bistatic_dp(sigma_vv_r, sigma_s, sigma_cp, theta_i, polgeo, txpol='V', ascending=True):
    """Short summary.

    Parameters
    ----------
    sigma_vv_r : float or np.ndarray
        regular (Bragg-like) NRCS for the equivalent monostatic case assuming VV polarization.
    sigma_s : float or np.ndarray
        scalar (specular-like) NRCS for the equivalent monostatic case.
    sigma_cp : float or np.ndarray
        cross-pol  NRCS for the equivalent monostatic case.
    theta_i : float or np.ndarray
        Angle of incidence of transmitted signal, in radians
    polgeo : CompanionPolarizations
        Intance of CompanionPolarizations, which contains all relevant geometry.
    txpol : string
        This can be 'v' (default) or 'h' or 'H'.
    ascending : bool
        True for ascending orbit.

    Returns
    -------
    np.ndarray
        The the polarimetric covariance matrix of the received signal in I-O basis.
        The output will have dimenions consistent with sigma_r, sigma_vv_r and
        theta_i, with two dimenions added (2x2) for the covariance.

    """

    # Amplitude reference for equivalent monostatic case
    theta_i_me = polgeo.inc2me_inc(theta_i)
    from drama.geo.bistatic_pol import elfouhaily
    (rot_ang_1, rot_ang_2, rot_ang_tot,
     Ps_KA_mono, Ps2, Ps_2nd_mono) = elfouhaily(np.pi/2, 0,
                                                theta_i_me, 0,
                                                theta_i_me)
    phi_p = polgeo.inc2PTProt(theta_i, ascending=ascending)
    phi_q = polgeo.inc2PRProt(theta_i, ascending=ascending)
    phi_IO = polgeo.inc2IOrot(theta_i, ascending=ascending)
    phi_p2 = polgeo.inc2Elfouhailiyrot(theta_i, order=2, txpol = txpol, ascending=ascending)
    scl_p2 = polgeo.inc2Elfouhailiynorm(theta_i, order=2, txpol = txpol, ascending=ascending)
    phi_p1 = polgeo.inc2Elfouhailiyrot(theta_i, order=1, txpol = txpol, ascending=ascending)
    # scl_p1 = polgeo.inc2Elfouhailiynorm(theta_i, order=1, txpol = txpol, ascending=ascending)
    p2IO = np.zeros(phi_p2.shape + (2,))
    p1IO = np.zeros(phi_p2.shape + (2,))
    if (txpol == 'v' or txpol == 'V'):
        dphi2 = phi_IO - phi_p2
        #print(dphi2)
        p2IO[..., 0] = np.sin(dphi2)
        p2IO[..., 1] = np.cos(dphi2)
        dphi1 = phi_IO - phi_p1
        p1IO[..., 0] = np.sin(dphi1)
        p1IO[..., 1] = np.cos(dphi1)
    else:
        dphi2 = phi_IO - phi_p2
        p2IO[..., 1] = - np.sin(dphi2)
        p2IO[..., 0] = np.cos(dphi2)
        dphi1 = phi_IO - phi_p1
        p1IO[..., 1] = - np.sin(dphi1)
        p1IO[..., 0] = np.cos(dphi1)
    # Add Bragg-like component
    sigma_norm_r = sigma_vv_r / (np.linalg.norm(Ps_2nd_mono, axis=-1)**2) * scl_p2**2
    cov_r_IO = np.einsum("...i,...j->...ij", p2IO, p2IO) * sigma_norm_r[..., np.newaxis, np.newaxis]
    # And specular component
    cov_s_IO = np.einsum("...i,...j->...ij", p1IO, p1IO) *  sigma_s[..., np.newaxis, np.newaxis]
    # cross
    p2IOx = np.zeros_like(p2IO)
    p2IOx[...,0] = p2IO[...,1]
    p2IOx[...,1] = - p2IO[...,0]
    cov_s_cp = np.einsum("...i,...j->...ij", p2IOx, p2IOx) *  sigma_cp[..., np.newaxis, np.newaxis]
    #cov_mM[...,0, 0] = sigma_norm_r * (2 - polgeo.inc2Elfouhailiynorm(inc, txpol='m'))
    # Cross-pol component. Assumptions
    # 1. cross-pol is uncorrelated from co-pol
    # 2. we assume, and this is wrong, that the two cross-pol scattering coeffients are the same, which is
    # true in the monostatic limit but must likely wrong in the bistatic case. For moderate bistatic geometries
    # the assumption should not be a dissaster, in particular considering that we operate dual-pol, so we never
    # really see the effect
    # 3. we assume that the scaling is like for Bragg; assuming that this is mostly ressonant scattering depolarized due to significant tilts
    #cov_mM[...,1:3, 1:3] =  sigma_cp
    return cov_r_IO + cov_s_IO + cov_s_cp


def monoeq2bistatic(sigma_vv_r, sigma_s, sigma_cp, theta_i, polgeo, sigma_hh_r=None, txpol='V', ascending=True, method='fp', rxpol='IO'):
    """Short summary.

    Parameters
    ----------
    sigma_vv_r : float or np.ndarray
        regular (Bragg-like) NRCS for the equivalent monostatic case assuming VV polarization.
    sigma_s : float or np.ndarray
        scalar (specular-like) NRCS for the equivalent monostatic case.
    sigma_cp : float or np.ndarray
        cross-pol  NRCS for the equivalent monostatic case.
    theta_i : float or np.ndarray
        Angle of incidence of transmitted signal, in radians
    polgeo : CompanionPolarizations
        Intance of CompanionPolarizations, which contains all relevant geometry.
    sigma_hh_r : float or np.ndarray
        optional and delicate (Bragg-like) NRCS for the equivalent monostatic case assuming HH polarization.
    txpol : string
        This can be 'v' (default). 'h' or 'H', or anything else, which will be interpreted
        as full-pol.
    ascending : bool
        True for ascending orbit.
    method: string
      "dp" (default) for dual-pol approach, which should be quicker, "fp" for full-pol
      approach. fp is forced if tx pol is neither 'h' nor 'v'

    Returns
    -------
    np.ndarray
        The the polarimetric covariance matrix of the received signal in I-O basis.
        The output will have dimenions consistent with sigma_r, sigma_vv_r and
        theta_i, with two dimenions added (2x2 or 4x4) for the covariance.

    """
    if not (txpol in ['v', 'V', 'h', "H"]):
        method = 'fp'
    if method in ['fp', 'FP']:
        return monoeq2bistatic_fp(sigma_vv_r, sigma_s, sigma_cp, theta_i, polgeo, sigma_hh_r, txpol, ascending, rxpol)
    else:
        return monoeq2bistatic_dp(sigma_vv_r, sigma_s, sigma_cp, theta_i, polgeo, txpol, ascending)


# %%
if __name__ == '__main__':
    # Test code
    import stereoid.utils.config as st_config


    paths = st_config.parse(section="Paths")
    # Unpack the paths read from user.cfg. If user.cfg is not found user_defaults.cfg is used.
    main_dir = paths["main"]
    datadir = paths["data"]
    pardir = paths["par"]
    resultsdir = paths["results"]
    parfile_name = 'Hrmny_2021_1.cfg'
    mode = "IWS"
    parfile = os.path.join(pardir, parfile_name)
    companion_delay = 350e3/7e3
    polandgeo = CompanionPolarizations(par_file=parfile, companion_delay = companion_delay)
    #polandgeo_2 = CompanionPolarizations(par_file=parfile, companion_delay = -companion_delay)
    # %%
    #polandgeo.inc2IOrot(np.radians(30))
    #polandgeo.inc2Elfouhailiyrot(np.radians(30))
    inc = np.radians(np.linspace(30,45))
    inc = np.radians(40)
    sigma_r = np.linspace(0.1, 0.05) * 0 +0.5
    sigma_s = np.zeros_like(inc) + 0.2
    sigma_cp = np.zeros_like(inc) +0.1

    wdop_r = sigma_r *  np.exp(1j*0.1)
    wdop_r_h = sigma_r *  np.exp(1j*0.1)
    wdop_s = sigma_s *  np.exp(1j*0.2)
    wdop_cp = sigma_cp *  np.exp(1j*0.2)
    cov_IO = monoeq2bistatic(sigma_r, sigma_s, sigma_cp, inc, polandgeo, txpol='v', method='fp')
    #xcov_mM = monoeq2bistatic(wdop_r, wdop_s, wdop_cp, inc, polandgeo, sigma_hh_r=wdop_r_h, txpol='V', method='fp', rxpol='mM')
    #xcov_mM2 = monoeq2bistatic(wdop_r, wdop_s, wdop_cp, inc, polandgeo_2, sigma_hh_r=wdop_r_h, txpol='V', method='fp', rxpol='mM')
    #xcov_IO= monoeq2bistatic(wdop_r, wdop_s, wdop_cp, inc, polandgeo, sigma_hh_r=wdop_r_h, txpol='V', method='fp', rxpol='IO')
    ind = 10
    print("FP approach")
    print(cov_IO[ind])
    print(np.linalg.eigvals(cov_IO[ind]))
    eigv = np.linalg.eig(cov_IO[ind])[1]
    print(eigv)
    print(np.degrees(np.arctan2(-eigv[0,np.argmax(np.linalg.eigvals(cov_IO[ind]))], -eigv[1,np.argmax(np.linalg.eigvals(cov_IO[ind]))])))
    cov_IO.shape
    print("DP approach")
    cov_IO2 = monoeq2bistatic(sigma_r, sigma_s, sigma_cp, inc, polandgeo, txpol='v', method='dp')
    print(cov_IO2[ind])
    print(np.linalg.eigvals(cov_IO2[ind]))
    eigv = np.linalg.eig(cov_IO2[ind])[1]
    print(eigv)
    print(np.degrees(np.arctan2(-eigv[0,np.argmax(np.linalg.eigvals(cov_IO[ind]))], -eigv[1,np.argmax(np.linalg.eigvals(cov_IO[ind]))])))
    print("xCov IO")
    print(np.angle(xcov_IO[ind]))# - np.array([[0,-np.pi],[-np.pi,0]]))
    print(np.abs(xcov_IO[ind]))
    print("xCov mM")
    print(np.angle(xcov_mM[ind]))
    print(np.abs(xcov_mM[ind]))
    print("xCov mM2")
    print(np.angle(xcov_mM2[ind]))
    print(np.abs(xcov_mM2[ind]))
    10*np.log10(0.664/0.645)
    np.iscomplexobj(sigma_r)
    # %%
    r_fp = fullpol_rotation_matrix(0.1, -0.2)
    r_fp_r = fullpol_rotation_matrix(-0.1, 0.2)
    print(r_fp)
    print(np.einsum("...ij,...jk->...ik", r_fp, r_fp_r))
    print(np.einsum("...ij,...kj->...ik", r_fp, r_fp))
    fullpol_rotation_matrix([0.0,0.1],[0.0,-0.1])
    fullpol_rotation_matrix(np.pi/2,np.pi/2)
    'p' in ['v', 'h']
