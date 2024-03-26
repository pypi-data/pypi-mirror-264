import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.mplot3d.art3d import Poly3DCollection
#import matplotlib.animation as animation
from matplotlib import rc
import os

from drama import utils as utls
import drama.utils.gohlke_transf as trans
from drama.orbits import SingleOrbit
from drama.io import cfg
import drama.constants as cnsts
import drama.geo as sargeo
from drama.geo.bistatic_pol import CompanionPolarizations

from stereoid.polarimetry.pol_rotations import fullpol_rotation_matrix
import stereoid.utils.config as st_config

def random_dipols(n, vth=1):
    """
    This creates scatterers with a random orientation. vth controls the vertical w.r.t. the horizontal.
    The scatterers have a circular-Gaussian scattering coefficient to make sure they are uncorrelated
    when computint statitics
    """
    s = np.random.randn(n, 3)
    s[:, 2] = s[:, 2] * vth
    s = s * (np.random.randn(n) + 1j * np.random.randn(n))[:,  np.newaxis]
    # Normalize a bit
    s = s / np.sqrt(np.mean(np.linalg.norm(s, axis=-1)**2))
    return s

def calc_cov(polgeo, scats, base='HV', orbind=1000):
    """
    We project the scatterer on the tx polarization and on the receive polarization
    making sure that the magnitude of the scatterer is only accounted for once.
    We compute the received signal for the four receive-transmit polarization combinations
    and then estimate the polarimetric covariance matrix.
    """
    inc = polgeo.swth_t.master_inc[orbind,::10]
    scats_n = scats/ np.linalg.norm(scats, axis=-1)[:,np.newaxis]
    if base == 'HV':
        pp1 = np.einsum("mi,ni->mn", polgeo.pH[orbind, ::10], scats)
        pp2 = np.einsum("mi,ni->mn", polgeo.pV[orbind, ::10], scats)
        pq1 = np.einsum("mi,ni->mn", polgeo.qH[orbind, ::10], scats_n)
        pq2 = np.einsum("mi,ni->mn", polgeo.qV[orbind, ::10], scats_n)
    elif base == 'mono':
        # Monostatic HV
        print('Monostatic...')
        pp1 = np.einsum("mi,ni->mn", polgeo.pH[orbind, ::10], scats)
        pp2 = np.einsum("mi,ni->mn", polgeo.pV[orbind, ::10], scats)
        pq1 = np.einsum("mi,ni->mn", polgeo.pH[orbind, ::10], scats_n)
        pq2 = np.einsum("mi,ni->mn", polgeo.pV[orbind, ::10], scats_n)
    elif base == 'mM':
        print('Minor-Major...')
        pp1 = np.einsum("mi,ni->mn", polgeo.pm[orbind, ::10], scats)
        pp2 = np.einsum("mi,ni->mn", polgeo.pM[orbind, ::10], scats)
        pq1 = np.einsum("mi,ni->mn", polgeo.qm[orbind, ::10], scats_n)
        pq2 = np.einsum("mi,ni->mn", polgeo.qM[orbind, ::10], scats_n)
    elif base == 'IO':
        print('IO...')
        pp1 = np.einsum("mi,ni->mn", polgeo.pI[orbind, ::10], scats)
        pp2 = np.einsum("mi,ni->mn", polgeo.qO[orbind, ::10], scats)
        pq1 = np.einsum("mi,ni->mn", polgeo.qI[orbind, ::10], scats_n)
        pq2 = np.einsum("mi,ni->mn", polgeo.qO[orbind, ::10], scats_n)
    elif base == 'HVIO':
        print('HV2IO...')
        pp1 = np.einsum("mi,ni->mn", polgeo.pH[orbind, ::10], scats)
        pp2 = np.einsum("mi,ni->mn", polgeo.pV[orbind, ::10], scats)
        pq1 = np.einsum("mi,ni->mn", polgeo.qI[orbind, ::10], scats_n)
        pq2 = np.einsum("mi,ni->mn", polgeo.qO[orbind, ::10], scats_n)

    sv = np.zeros(pp1.shape + (4,), dtype=complex)
    sv[..., 0] = pq1 * pp1  # s11
    sv[..., 1] = pq1 * pp2  # s21
    sv[..., 2] = pq2 * pp1  # s12
    sv[..., 3] = pq2 * pp2  # s22
    cov = np.einsum("mni,mnj->mij", sv, np.conj(sv)) / scats.shape[0]
    # if base == "IO":
    #     phi_p = polandgeo.inc2IOrot(theta_i, ascending=True)
    #     phi_q = polandgeo.inc2IOrot(theta_i, ascending=True)
    return (cov, inc, base)


class PolInMedium(object):
    def __init__(self, polgeo, eps_i):
        # Snell's law
        self.theta_i = polgeo.swth_t.master_inc
        self.theta_s = polgeo.inc2slave_inc(self.theta_i)
        # sin_theta_s_p = np.sin(theta_s) / np.sqrt(eps_r)
        # sin_theta_i_p = np.sin(theta_i) / np.sqrt(eps_r)
        # k = 2pi/wl = 2pi * f / c
        # c = c0/np.sqrt(eps_r)
        self.polgeo = polgeo
        self.eps_i = eps_i
        self.eps_a = 1
        c0 = cnsts.speed_of_light
        self.k0 = 2 * np.pi * 5.4e9 / c0
        self.k0_m = self.k0 * np.sqrt(eps_i)
        self.ki_a = polgeo.r_v_t * self.k0
        self.ks_a = polgeo.r_v_r * self.k0
        self.ki_m = self.ki_a.copy()
        self.ks_m = self.ks_a.copy()
        self.ki_m[..., 2] = - np.sqrt(self.k0_m**2 - self.ki_a[...,0]**2 - self.ki_a[...,1]**2)
        self.ks_m[..., 2] = - np.sqrt(self.k0_m**2 - self.ks_a[...,0]**2 - self.ks_a[...,1]**2)
        self.r_v_t_m = self.ki_m / np.linalg.norm(self.ki_m, axis=-1)[..., np.newaxis]
        self.r_v_r_m = self.ks_m / np.linalg.norm(self.ks_m, axis=-1)[..., np.newaxis]
        self.pH_m = polgeo.pH
        self.pV_m = np.cross(self.r_v_t_m, self.pH_m, axis=-1)
        self.qH_m = polgeo.qH
        self.qV_m = np.cross(self.r_v_r_m, self.qH_m, axis=-1)
        self.fresnel_coefs()

    def calc_cov(self, scats, mono=False, base='HV', transfer=True, orbind=1000):
        """
        We project the scatterer on the tx polarization and on the receive polarization
        making sure that the magnitude of the scatterer is only accounted for once.
        We compute the received signal for the four receive-transmit polarization combinations
        and then estimate the polarimetric covariance matrix.
        """
        stride = 10
        scats_n = scats/ np.linalg.norm(scats, axis=-1)[:,np.newaxis]
        if mono:
            # Monostatic HV
            print('Monostatic...')
            pp1 = np.einsum("mi,ni->mn", self.pH_m[orbind, ::stride], scats)
            pp2 = np.einsum("mi,ni->mn", self.pV_m[orbind, ::stride], scats)
            pq1 = np.einsum("mi,ni->mn", self.pH_m[orbind, ::stride], scats_n)
            pq2 = np.einsum("mi,ni->mn", self.pV_m[orbind, ::stride], scats_n)
        else:
            pp1 = np.einsum("mi,ni->mn", self.pH_m[orbind, ::stride], scats)
            pp2 = np.einsum("mi,ni->mn", self.pV_m[orbind, ::stride], scats)
            pq1 = np.einsum("mi,ni->mn", self.qH_m[orbind, ::stride], scats_n)
            pq2 = np.einsum("mi,ni->mn", self.qV_m[orbind, ::stride], scats_n)


        sv = np.zeros(pp1.shape + (4,), dtype=complex)
        if transfer:
            th01 = self.t_h01[orbind,::stride, np.newaxis]
            tv01 = self.t_v01[orbind,::stride, np.newaxis]
            if mono:
                tv10 = self.t_v10_mono[orbind,::stride, np.newaxis]
                th10 = self.t_h10_mono[orbind,::stride, np.newaxis]
            else:
                tv10 = self.t_v10[orbind,::stride, np.newaxis]
                th10 = self.t_h10[orbind,::stride, np.newaxis]
            sv[..., 0] = th01 * th10 * pq1 * pp1  # s11
            sv[..., 1] = tv01 * th10 * pq1 * pp2  # s21
            sv[..., 2] = th01 * tv10 * pq2 * pp1  # s12
            sv[..., 3] = tv01 * tv10 * pq2 * pp2
        else:
            sv[..., 0] = pq1 * pp1  # s11
            sv[..., 1] = pq1 * pp2  # s21
            sv[..., 2] = pq2 * pp1  # s12
            sv[..., 3] = pq2 * pp2  # s22
        cov = np.einsum("mni,mnj->mij", sv, np.conj(sv)) / scats.shape[0]
        if base == "IO":
            phi_p = self.polgeo.inc2IOTrot(self.theta_i[orbind, ::stride], ascending=True)
            phi_q = self.polgeo.inc2IOrot(self.theta_i[orbind, ::stride], ascending=True)
        elif base == "mM":
            phi_p = self.polgeo.inc2PTProt(self.theta_i[orbind, ::stride], ascending=True)
            phi_q = self.polgeo.inc2PRProt(self.theta_i[orbind, ::stride], ascending=True)
        elif base == 'HVIO':
                phi_q = self.polgeo.inc2IOrot(self.theta_i[orbind, ::stride], ascending=True)
                phi_p = np.zeros_like(phi_q)  # Tx not rotated
        if base != "HV":
            r_fp = fullpol_rotation_matrix(phi_p, phi_q)
            #print(r_fp.shape)
            #print(cov.shape)
            aux = np.einsum("...ij,...jk->...ik", r_fp, cov)
            cov = np.einsum("...ij,...kj->...ik", aux, r_fp)
        if mono:
            base = "mono"   # For plotting function
        return (cov, self.theta_i[orbind, ::stride], base)

    def fresnel_coefs(self, delta_z=0):
        """Adapted from Marcel's implementation of Komarov"""
        # Fresnel reflection/transmission coefficients and phase changes
        # The following we don't need, these are the vertical components of k
        #omega_0 = k_0 * np.sqrt(eps_a - np.sin(np.deg2rad(inc_m)) ** 2) # air
        #omega_1 = k_0 * np.sqrt(eps_s - np.sin(np.deg2rad(inc_m)) ** 2) # snow
        #omega_2 = k_0 * np.sqrt(eps_i - np.sin(np.deg2rad(inc_m)) ** 2) # ice
        eps_0 = self.eps_a
        n_0 = np.sqrt(eps_0)
        eps_1 = self.eps_i
        n_1 = np.sqrt(eps_1)
        ki_z_a = np.abs(self.ki_a[..., 2])
        ki_z_m = np.abs(self.ki_m[..., 2])
        ks_z_a = np.abs(self.ks_a[..., 2])
        ks_z_m = np.abs(self.ks_m[..., 2])
        cos_i_a = ki_z_a / np.linalg.norm(self.ki_a, axis=-1)
        cos_i_m = ki_z_m / np.linalg.norm(self.ki_m, axis=-1)
        cos_s_a = ks_z_a / np.linalg.norm(self.ks_a, axis=-1)
        cos_s_m = ks_z_m / np.linalg.norm(self.ks_m, axis=-1)
        # u_1 = np.exp(1j * omega_1 * delta_z)  # phase change in the snow layer (only one necessary)
        r_dH_01 = (ki_z_a - ki_z_m) / (ki_z_a + ki_z_m)  # Fresnel reflection coefficient at air-snow interface (downward)
        #t_dH_01 = 2 * ki_z_a/(ki_z_a + ki_z_m) # get this from Imperatore et al. (2009)
        #Wikipedia version
        t_dH_01 = 2 * n_0 * cos_i_a / (n_0 * cos_i_a + n_1 * cos_i_m)
        r_dV_01 = (eps_1 * ki_z_a -  eps_0 * ki_z_m) / (eps_1 * ki_z_a + eps_0 * ki_z_m)  # vertical polarization
        #t_dV_01 = 2 * eps_1 * ki_z_a / (eps_1 * ki_z_a + eps_0 * ki_z_m)
        # Wikipedia...
        t_dV_01 = 2 * n_0 * cos_i_a / (n_1 * cos_i_a + n_0 * cos_i_m)
        self.t_h01 = t_dH_01
        self.t_v01 = t_dV_01
        self.r_h01 = r_dH_01
        self.r_v01 = r_dV_01
        # self.t_h10_mono = 2 * ki_z_m/(ki_z_a + ki_z_m) #1 - r_dH_01
        # self.t_v10_mono = 2 * eps_0 * ki_z_m / (eps_1 * ki_z_a + eps_0 * ki_z_m) #1 - r_dV_01
        self.t_h10_mono = 2 * n_1 * cos_i_m / (n_1 * cos_i_m + n_0 * cos_i_a)
        self.t_v10_mono = 2 * n_1 * cos_i_m / (n_0 * cos_i_m + n_1 * cos_i_a)
        # Now the other ones
        r_dH_01 = (ks_z_a - ks_z_m) / (ks_z_a + ks_z_m)  # Fresnel reflection coefficient at air-snow interface (downward)
        t_dH_01 = 2 * ks_z_a/(ks_z_a + ks_z_m) # get this from Imperatore et al. (2009)
        r_dV_01 = (eps_1 * ks_z_a -  eps_0 * ks_z_m) / (eps_1 * ks_z_a + eps_0 * ks_z_m)  # vertical polarization
        t_dV_01 = 2 * eps_1 * ks_z_a / (eps_1 * ks_z_a + eps_0 * ks_z_m)
        # The following not needed, as tx is always the same
        # self.t_h01 = t_dH_01
        # self.t_v01 = t_dV_01
        # self.r_h01 = r_dH_01
        # self.r_v01 = r_dV_01
        self.t_h10 = 2 * n_1 * cos_s_m / (n_1 * cos_s_m + n_0 * cos_s_a)
        self.t_v10 = 2 * n_1 * cos_s_m / (n_1 * cos_s_m + n_0 * cos_s_a)


def plot_cov(cov, inc, base, ref=0.201):
    if base == 'HV':
        ps = ['H', 'V']
        qs = ps
        title='HV-HV basis'
    elif base == 'mono':
        ps = ['H', 'V']
        qs = ps
        title='HV-HV (monostatic) basis'
    elif base == 'mM':
        ps = ['p_m', 'p_M']
        qs = ['q_m', 'q_M']
        title='$p_mp_M - q_mq_M$ basis'
    elif base == 'IO':
        ps = ['I', 'O']
        qs = ps
        title='IO-IO basis'
    elif base == 'HVIO':
        ps = ['H', 'V']
        qs = ['I', 'O']
        title='HV-IO (Harmony L1) basis'
    fig, axs = plt.subplots(1,2, figsize=(10,5))

    for i in range(2):
        for j in range(2):
            axs[0].plot(np.degrees(inc), np.abs(cov[:,2*i+j,2*i+j])/ref, label="$\sigma_{%s%s}$" % (qs[i],ps[j]))
    axs[0].legend()
    axs[0].grid(True)
    axs[0].set_ylim((0, np.nanmax(np.abs(cov)) / ref * 1.05))
    gamma_cp =np.abs(cov[:,0,3]) / np.sqrt(np.abs(cov[:,0,0] * cov[:,3,3]))
    axs[1].plot(np.degrees(inc), gamma_cp, label='$\gamma_{%s%s%s%s}$' % (qs[0], ps[0], qs[1], ps[1]))
    gamma_xp =np.abs(cov[:,1,2]) / np.sqrt(np.abs(cov[:,1,1] * cov[:,2,2]))
    axs[1].plot(np.degrees(inc), gamma_xp, label='$\gamma_{%s%s%s%s}$' % (qs[0], ps[1], qs[1], ps[0]))

    gamma_mp =np.abs(cov[:,1,3]) / np.sqrt(np.abs(cov[:,1,1] * cov[:,3,3]))
    axs[1].plot(np.degrees(inc), gamma_mp, label='$\gamma_{%s%s%s%s}$' % (qs[0], ps[1], qs[1], ps[1]))

    gamma_mp =np.abs(cov[:,0,2]) / np.sqrt(np.abs(cov[:,0,0] * cov[:,2,2])) #+0.01
    axs[1].plot(np.degrees(inc), gamma_mp, label='$\gamma_{%s%s%s%s}$' % (qs[1], ps[0], qs[0], ps[0]))
    axs[1].legend()
    axs[1].grid(True)
    axs[1].set_ylim((0,1.05))
    fig.suptitle(title)

#%%

if __name__ == '__main__':
    paths = st_config.parse(section="Paths")
    # Unpack the paths read from user.cfg. If user.cfg is not found user_defaults.cfg is used.
    main_dir = paths["main"]
    datadir = paths["data"]
    pardir = paths["par"]
    resultsdir = paths["results"]
    parfile_name = 'Hrmny_2021_1.cfg'
    mode = "IWS"
    parfile = os.path.join(pardir, parfile_name)
    companion_delay = 2*350e3/7e3
    # swth_t = sargeo.SingleSwath(par_file=parfile, inc_angle=[30,45])
    # swth_r = sargeo.SingleSwath(par_file=parfile, inc_angle=[30,45], companion_delay = companion_delay)
    polandgeo_1 = CompanionPolarizations(par_file=parfile, companion_delay = companion_delay)
    # polandgeo_2 = CompanionPolarizations(par_file=parfile, companion_delay = -companion_delay)
    #%%
    pol_air = PolInMedium(polandgeo_1, 1)
    pol_m = PolInMedium(polandgeo_1, 3)
    polandgeo_1.qV[1000,100]
    pol_m.qV_m[1000,100]
    polandgeo_1.r_v_r[1000,100]
    pol_m.r_v_r_m[1000,100]
    #%%
    scats = random_dipols(100000, vth=1)
    #polandgeo_1.pH.shape
    cov_mono_a = pol_air.calc_cov(scats, mono=True)
    cov_IOIO_a = pol_air.calc_cov(scats, base="IO")
    cov_mono = pol_m.calc_cov(scats, mono=True)
    cov_IOIO = pol_m.calc_cov(scats, base="IO")
    cov_HVIO = pol_m.calc_cov(scats, base="HVIO")
    #print(np.abs(cov_mono[0][30]/0.2))
    #print("Second method")
    #print(np.abs(cov_IOIO[0][30]/0.2))
    ref = 0.201 #np.abs(cov_mono[0][:,3,3])
    #plot_cov(*cov_mono_a, ref=ref)
    #plot_cov(*cov_IOIO_a, ref=ref)
    plot_cov(*cov_mono, ref=ref)
    plot_cov(*cov_IOIO, ref=ref)
    plot_cov(*cov_HVIO, ref=ref)

    #%%
    print(pol_m.t_h01[1000,10])
    print(pol_m.t_v10_mono[1000,10])
    print(pol_m.t_v01[1000,10])
    print(pol_m.t_h10_mono[1000,10])
