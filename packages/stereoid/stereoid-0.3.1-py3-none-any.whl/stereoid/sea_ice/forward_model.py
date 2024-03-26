__author__ = "Marcel Kleinherenbrink"
__email__ = "m.kleinherenbrink@tudelft.nl"

import numpy as np
from drama import constants as const
from drama.io import cfg as cfg
import drama.utils as drtls

class FwdModel(object):
    def __init__(self, par_file,snow_props,ice_props):
        self.par_file = par_file
        self.snow_props = snow_props # snow props requires 4 inputs [CDC,roughness,correlation length,depth]
        self.ice_props = ice_props # ice props requires 3 inputs [CDC,roughness,correlation length]

    @property
    def par_file(self):
        return self.__par_file

    @par_file.setter
    def par_file(self, par_file):
        self.__par_file = par_file

    @property
    def snow_props(self):
        return self.__snow_props

    @snow_props.setter
    def snow_props(self, snow_props):
        self.__snow_props = snow_props

    @property
    def ice_props(self):
        return self.__ice_props

    @ice_props.setter
    def ice_props(self, ice_props):
        self.__ice_props = ice_props


    # compute interferometric phase difference and dca
    def fwd_ph_dca(self, u, v, inc_m, inc_b, bist_ang):
        """

        Parameters
        ----------
        u
        v
        inc_m
        inc_b
        bist_ang

        Returns
        -------

        """
        # get some settings
        cfgdata = cfg.ConfigFile(drtls.get_par_file(self.par_file))

        # some equations to compute phase diff
        f = cfgdata.sar.f0
        c = const.c
        la= c / f

        # vectors and unit vectors
        rthat=[np.sin(inc_m), 0, np.cos(inc_m)]
        rrhat=[np.cos(bist_ang)*np.sin(inc_b), np.sin(bist_ang)*np.sin(inc_b), np.cos(inc_b)]

        # positive phase when moving towards the satellite (this is equation 3+4 in Kleinherenbrink et al. (2021))
        # we express it as Doppler to stay consistent with dca of S1, note that this requires noise scaling
        dopp = 1 / la * ( -(rthat[0] + rrhat[0] ) * u + rrhat[1] * v)

        return dopp

    # compute di-electric constants for two layer-model
    def CDC(self):
        rho_pi = 900  # density ice # this stuff should move to the scene generator or par file
        rho_s = 300  # density snow
        rho_b = 1050  # brine density
        gamma = 0.8  # varies between 0.5 (refractive) and 1 (linear)
        eps_pi = 3.15  # di-electric constant of pure ice
        eps_bs = 40  # di-electric constant brine in snow (estimate from Stogryn and Desargant)
        v_b = 0.1  # brine volume ratio snow estimate from Drinkwater and Crocker
        W_pi = rho_s * (1 - v_b) / (((1 - v_b) * rho_pi) + v_b * rho_b)  # ice volume fraction snow
        W_b = W_pi * v_b / (1 - v_b)  # brine volume in snow
        eps_bi = eps_bs  # di-electric constant brine in sea ice (check values)
        V_b = 2 * W_b  # volume of brine in sea ice (check values)

        # di-electric constants of air
        eps_a = 1

        # di-electric constants of snow
        eps_ds = (1 + (eps_pi ** gamma - 1) * W_pi)  # di-electric constant of dry snow
        eps_s = (eps_ds ** gamma + (eps_bs ** gamma - 1) * W_b) ** (1 / gamma)  # di-electric constant of snow
        #eps_s = 1

        # di-electric constants of ice
        eps_i = (eps_pi ** gamma ** (1 - V_b) + eps_bi ** gamma * V_b)  # at the moment all of the CDC's are real

        return eps_a, eps_s, eps_i

    # downward Fresnel reflection and transmission coefficients
    def Fresnel_downward(self,k_0,eps_a,eps_s,eps_i,inc_m,delta_z):
        # Fresnel reflection/transmission coefficients and phase changes
        omega_0 = k_0 * np.sqrt(eps_a - np.sin(inc_m) ** 2) # air
        omega_1 = k_0 * np.sqrt(eps_s - np.sin(inc_m) ** 2) # snow
        omega_2 = k_0 * np.sqrt(eps_i - np.sin(inc_m) ** 2) # ice
        u_1 = np.exp(1j * omega_1 * delta_z)  # phase change in the snow layer (only one necessary)
        r_dH_01 = (omega_0 - omega_1) / (
                omega_0 + omega_1)  # Fresnel reflection coefficient at air-snow interface (downward)
        t_dH_01 = 2*omega_0/(omega_0+omega_1) # get this from Imperatore et al. (2009)
        r_dH_12 = (omega_1 - omega_2) / (
                omega_1 + omega_2)  # Fresnel reflection coefficient at snow-ice interface (downward)
        t_dH_12 = 2*omega_1/(omega_1+omega_2)
        r_dV_01 = (eps_s * omega_0 - eps_a * omega_1) / (eps_s * omega_0 + eps_a * omega_1)  # vertical polarization
        t_dV_01 = 2*eps_s*omega_0/(eps_s*omega_0+eps_a*omega_1)
        r_dV_12 = (eps_i * omega_1 - eps_s * omega_2) / (eps_i * omega_1 + eps_s * omega_2)
        t_dV_12 = 2*eps_i*omega_1/(eps_i*omega_1+eps_s*omega_2)

        return u_1,r_dH_01,t_dH_01,r_dH_12,t_dH_12,r_dV_01,t_dV_01,r_dV_12,t_dV_12

    # upward Fresnel reflection and transmission coefficients
    def Fresnel_upward(self,r_dH_01,t_dH_01,r_dH_12,t_dH_12,r_dV_01,t_dV_01,r_dV_12,t_dV_12):
        # upward Fresnel coefficients (maybe not all used)
        r_uH_01 = -r_dH_01  # according to Kolmarov et al. (2015) appendix
        r_uH_12 = -r_dH_12
        r_uV_01 = -r_dV_01
        r_uV_12 = -r_dV_12
        t_uH_01 = 1 + r_uH_01 # according to Kolmarov et al. (2015) appendix
        t_uH_12 = 1 + r_uH_12
        t_uV_01 = 1 + r_uV_01
        t_uV_12 = 1 + r_uV_12

        return r_uH_01,t_uH_01,r_uH_12,t_uH_12,r_uV_01,t_uV_01,r_uV_12,t_uV_12

    # reflection and transmission coefficients for the entire snow-covered ice structure
    #"sig_hh should be equal to sig_vv for zero incidence for both components (rough air-snow and rough ice-snow interfaces).
    #To calculate reflection coefficients in Eq. 3-4, you would need to calculate reflection coefficients from the entire
    # snow-covered ice structure. In the simple case you consider, you still have two boundaries (air-snow and snow-ice). So, you would need to do two iterations as shown in Appendix as follows:
    #
    #Iteration 1 results in:
    #T1 = t1(0,1), R1 = r1(0,1), T2 = t2(0,1), R2 = r2(0,1)

    #Iteration 2 results in:
    #T1 = t1(0,1)*t1(1,2)*u / ( 1 – r2(0,1)*r1(1,2)*u^2 )
    #R1 = r1(0,1) + t1(0,1)*t2(0,1)*r1(1,2)*u^2 / ( 1 – r2(0,1)*r1(1,2)*u^2 )
    #0 is air, 1 is snow, 2 is ice; u = exp( 1i * w(1) * delta_z )
    #R1 is the coefficient to plug in Eq. 3-4."
    def Refl_coeff(self,t_dH_01,t_dH_12,r_uH_01,r_dH_12,t_dV_01,t_dV_12,r_uV_01,r_dV_12,r_dH_01,t_uH_01,r_dV_01,t_uV_01,u):
        #R1,r1 means downward reflection coefficients, for which I will use a 'd' and for upward (R2,r2) 'u'
        #The polarization will be given with capital 'H' of 'V'
        #T indicated transmission coefficient

        # iteration 2
        T_dH_1 = t_dH_01 * t_dH_12 * u / (1 - r_uH_01 * r_dH_12 * u ** 2)
        T_dV_1 = t_dV_01 * t_dV_12 * u / (1 - r_uV_01 * r_dV_12 * u ** 2)
        R_dH_1 = r_dH_01 + t_dH_01 * t_uH_01 * r_dH_12 * u ** 2 / (1 - r_uH_01 * r_dH_12 * u ** 2)
        R_dV_1 = r_dV_01 + t_dV_01 * t_uV_01 * r_dV_12 * u ** 2 / (1 - r_uV_01 * r_dV_12 * u ** 2)
        T_uH_1 = 10000 # not required (set high, in case we use it accidentically it will be identified)
        T_uV_1 = 10000
        R_uH_1 = 10000
        R_uV_1 = 10000

        return T_dH_1,T_dV_1,R_dH_1,R_dV_1,T_uH_1,T_uV_1,R_uH_1,R_uV_1

    # compute monostatic nrcs two-layer model (Komarov et al., 2014,2015)
    def fwd_nrcs_monostatic(self, inc_m, f0=5.4e9):
        """

        Parameters
        ----------
        inc_m
        f0

        Returns
        -------
        nrcs:
            nrcs in four polarizations
        """

        ### compute monostatic nrcs
        # some constants
        k_0 = 2 * np.pi * f0 / const.c  # wavenumber
        delta_z = self.snow_props[3]  # snow thickness
        L_i = self.ice_props[2]  # correlation length ice
        L_s = self.snow_props[2]  # correlation length snow
        sigma_s = self.snow_props[1]  # RMS of snow surface height
        sigma_i = self.ice_props[1]  # RMS of ice surface height

        # get di-electric constants
        eps_a = 1;
        eps_s = self.snow_props[0];
        eps_i = self.ice_props[0]
        if eps_s == 0 or eps_i == 0:
            eps_a, eps_s, eps_i = self.CDC()

        # delta of the di-electric constants
        delta_Es = eps_s - eps_a  # di-electric constants are discretely modelled now, possibly better a function of 'z'
        delta_Ei = eps_i - eps_s

        # get downward Fresnel reflection coefficients
        u_1,r_dH_01,t_dH_01,r_dH_12,t_dH_12,r_dV_01,t_dV_01,r_dV_12,t_dV_12=self.Fresnel_downward(k_0,eps_a,eps_s,eps_i,inc_m,delta_z)

        # get upward Fresnel reflection coefficients
        r_uH_01,t_uH_01,r_uH_12,t_uH_12,r_uV_01,t_uV_01,r_uV_12,t_uV_12=self.Fresnel_upward(r_dH_01, t_dH_01, r_dH_12, t_dH_12, r_dV_01, t_dV_01, r_dV_12, t_dV_12)

        # reflection and transmission coefficients through layers
        T_dH_1,T_dV_1,R_dH_1,R_dV_1,T_uH_1,T_uV_1,R_uH_1,R_uV_1=self.Refl_coeff(t_dH_01,t_dH_12,r_uH_01,r_dH_12,t_dV_01,t_dV_12,r_uV_01,r_dV_12,r_dH_01,t_uH_01,r_dV_01,t_uV_01,u_1)

        # auxiliariy variables (only required for the ice layer)
        # eventually q_0 should be vectorised for the bi-static stuff
        q_0 = k_0 * np.sin(inc_m)  # assume that surface is anisotropic (spectrum is independent of azimuth angle, azimuth angle is anyway zero)
        w_s = np.sqrt(k_0 ** 2 * eps_s - q_0 ** 2)
        w_0 = np.sqrt(k_0 ** 2 - q_0 ** 2)
        L_H = w_0 / w_s * t_uH_01 * u_1 / (1 + r_dH_12 * r_dH_01 * u_1 ** 2) * (1 + r_dH_12)  # this is actually L_H(q_0)
        L_V = w_0 / w_s * t_uV_01 * u_1 / (1 + r_dV_12 * r_dV_01 * u_1 ** 2) * (1 + r_dV_12)  # this is actually L_V(q_0)
        M_V = w_0 / k_0 * t_uV_01 * u_1 / (1 + r_dV_12 * r_dV_01 * u_1 ** 2) * (1 - r_dV_12)

        # surface spectra
        # this is how I interpret q:
        # the input here actually is q=q1-q0, where q1 and q0 are incoming and outgoing vectors
        # since in the monostatic case q1=-q0, we can write -2*q0
        q = -2 * q_0  # assumption that the surface is isotropic (sign doesn't matter, squared anyway)
        K_i = 2 * np.pi * L_i ** 2 * sigma_i ** 2 / (1 + q ** 2 * L_i ** 2) ** 1.5
        K_s = 2 * np.pi * L_s ** 2 * sigma_s ** 2 / (1 + q ** 2 * L_s ** 2) ** 1.5

        # ice
        nrcs_ice_hh = k_0 ** 4 * np.absolute(delta_Ei) ** 2 / (4 * np.pi) * np.absolute(L_H) ** 4 * K_i
        nrcs_ice_vv = k_0 ** 4 * np.absolute(delta_Ei) ** 2 / (4 * np.pi) * np.absolute(
            eps_s / eps_i * np.sin(inc_m) ** 2 * L_V ** 2 + M_V ** 2) ** 2 * K_i

        # snow
        nrcs_snow_hh = k_0 ** 4 * np.absolute(delta_Es) ** 2 / (4 * np.pi) * np.absolute(1 + R_dH_1) ** 4 * K_s
        nrcs_snow_vv = k_0 ** 4 * np.absolute(delta_Es) ** 2 / (4 * np.pi) * np.absolute(
            np.sin(inc_m) ** 2 / eps_s * (1 + R_dV_1) ** 2 + (1 - R_dV_1) ** 2 * np.cos(inc_m) ** 2) ** 2 * K_s

        # total
        nrcs_hh = nrcs_ice_hh + nrcs_snow_hh
        nrcs_vv = nrcs_ice_vv + nrcs_snow_vv

        # compute bistatic nrcs
        nrcs_vh = 0
        nrcs_hv = 0

        return nrcs_hh, nrcs_vv, nrcs_hv, nrcs_vh

    # compute bistatic nrcs two-layer model (Komarov et al., 2014,2015)
    def fwd_nrcs_bistatic(self, inc_m, inc_b, bist_ang, f0=5.4e9):
        """

        Parameters
        ----------
        inc_m
        inc_b
        bist_ang
        f0

        Returns
        -------
        nrcs:
            nrcs in four polarizations
        """
        ### compute bistatic nrcs
        # some constants
        k_0 = 2 * np.pi * f0 / const.c  # wavenumber
        delta_z = self.snow_props[3]  # snow thickness
        L_i = self.ice_props[2]  # correlation length ice
        L_s = self.snow_props[2]  # correlation length snow
        sigma_s = self.snow_props[1]   # RMS of snow surface height
        sigma_i = self.ice_props[1]   # RMS of ice surface height

        # get di-electric constants
        eps_a=1; eps_s=self.snow_props[0]; eps_i=self.ice_props[0]
        if eps_s == 0 or eps_i == 0:
            eps_a,eps_s,eps_i = self.CDC()

        # delta of the di-electric constants
        delta_Es = eps_s - eps_a  # di-electric constants are discretely modelled now, possibly better a function of 'z'
        delta_Ei = eps_i - eps_s

        # get downward Fresnel reflection coefficients (everything has to be computed twice: for q and for q0)
        u_1_0, r_dH_01_0, t_dH_01_0, r_dH_12_0, t_dH_12_0, r_dV_01_0, t_dV_01_0, r_dV_12_0, t_dV_12_0=self.Fresnel_downward(k_0,eps_a,eps_s,eps_i,inc_m,delta_z)
        u_1, r_dH_01, t_dH_01, r_dH_12, t_dH_12, r_dV_01, t_dV_01, r_dV_12, t_dV_12 = self.Fresnel_downward(k_0, eps_a,eps_s,eps_i,inc_b,delta_z)

        # get upward Fresnel reflection coefficients
        r_uH_01_0,t_uH_01_0,r_uH_12_0,t_uH_12_0,r_uV_01_0,t_uV_01_0,r_uV_12_0,t_uV_12_0=self.Fresnel_upward(r_dH_01_0, t_dH_01_0, r_dH_12_0, t_dH_12_0, r_dV_01_0, t_dV_01_0, r_dV_12_0, t_dV_12_0)
        r_uH_01, t_uH_01, r_uH_12, t_uH_12, r_uV_01, t_uV_01, r_uV_12, t_uV_12 = self.Fresnel_upward(r_dH_01, t_dH_01,r_dH_12, t_dH_12,r_dV_01, t_dV_01,r_dV_12, t_dV_12)

        # reflection and transmission coefficients through layers
        T_dH_1_0,T_dV_1_0,R_dH_1_0,R_dV_1_0,T_uH_1_0,T_uV_1_0,R_uH_1_0,R_uV_1_0=self.Refl_coeff(t_dH_01_0,t_dH_12_0,r_uH_01_0,r_dH_12_0,t_dV_01_0,t_dV_12_0,r_uV_01_0,r_dV_12_0,r_dH_01_0,t_uH_01_0,r_dV_01_0,t_uV_01_0,u_1_0)
        T_dH_1, T_dV_1, R_dH_1, R_dV_1, T_uH_1, T_uV_1, R_uH_1, R_uV_1 = self.Refl_coeff(t_dH_01,t_dH_12,r_uH_01,r_dH_12,t_dV_01,t_dV_12,r_uV_01,r_dV_12,r_dH_01,t_uH_01,r_dV_01,t_uV_01,u_1)

        # auxiliariy variables (only required for the ice layer)
        # here we use the amplitudes of q_0
        q_0 = k_0 * np.sin(inc_m)  # assume that surface is anisotropic (spectrum is independent of azimuth angle, azimuth angle is anyway zero)
        w_s_q0 = np.sqrt(k_0 ** 2 * eps_s - q_0 ** 2)
        w_0_q0 = np.sqrt(k_0 ** 2 - q_0 ** 2)
        L_H_q0 = w_0_q0 / w_s_q0 * t_uH_01_0 * u_1_0 / (1 + r_dH_12_0 * r_dH_01_0 * u_1_0 ** 2) * (1 + r_dH_12_0)
        L_V_q0 = w_0_q0 / w_s_q0 * t_uV_01_0 * u_1_0 / (1 + r_dV_12_0 * r_dV_01_0 * u_1_0 ** 2) * (1 + r_dV_12_0)
        M_V_q0 = w_0_q0 / k_0 * t_uV_01_0 * u_1_0 / (1 + r_dV_12_0 * r_dV_01_0 * u_1_0 ** 2) * (1 - r_dV_12_0)

        # repeat the previous steps for q instead of q_0
        q = k_0 * np.sin(inc_b)
        w_s_q = np.sqrt(k_0 ** 2 * eps_s - q ** 2)
        w_0_q = np.sqrt(k_0 ** 2 - q ** 2)
        L_H_q = w_0_q / w_s_q * t_uH_01 * u_1 / (1 + r_dH_12 * r_dH_01 * u_1 ** 2) * (1 + r_dH_12)
        L_V_q = w_0_q / w_s_q * t_uV_01 * u_1 / (1 + r_dV_12 * r_dV_01 * u_1 ** 2) * (1 + r_dV_12)
        M_V_q = w_0_q / k_0 * t_uV_01 * u_1 / (1 + r_dV_12 * r_dV_01 * u_1 ** 2) * (1 - r_dV_12)

        # surface spectra
        # we have to use some vectors here
        bist_ang = np.pi - bist_ang # reversed direction for 'q'
        xvec=np.zeros((2,1)); xvec[0]=1
        yvec=np.zeros((2,1)); yvec[1]=1

        # According to Komarov et al. (2014), validity is between 20 and 60 degrees
        q_0=k_0 * np.sin(inc_m)*(xvec*np.cos(0)+yvec*np.sin(0))
        q=k_0 * np.sin(inc_b)*(xvec*np.cos(bist_ang)+yvec*np.sin(bist_ang))

        # in case of monostatic q_enter is -2*q_0, besides the small inclination change we expect q2 to be smaller,
        # because of the effect of the bistatic angle
        qd = q - q_0  # assumption that the surface is isotropic (this is what we enter into the spectrum)
        q2 = np.sqrt(qd[0] ** 2 + qd[1] ** 2) # watch out, compared to the monostatic this can give a sign change (later squared so no problem)
        q2 = q2[0]
        K_i = 2 * np.pi * L_i ** 2 * sigma_i ** 2 / ( 1 + q2 ** 2 * L_i ** 2) ** 1.5
        K_s = 2 * np.pi * L_s ** 2 * sigma_s ** 2 / (1 + q2 ** 2 * L_s ** 2) ** 1.5

        # ice
        bist_ang=-bist_ang + np.pi # revert back
        nrcs_ice_hh = k_0 ** 4 * np.absolute(delta_Ei) ** 2 / (4 * np.pi) * np.absolute(L_H_q0*L_H_q) ** 2 * np.cos(bist_ang-0) ** 2 * K_i
        nrcs_ice_vv = k_0 ** 4 * np.absolute(delta_Ei) ** 2 / (4 * np.pi) * np.absolute(eps_s / eps_i *
            np.sin(inc_m) * np.sin(inc_b) * L_V_q0 * L_V_q - M_V_q0 * M_V_q * np.cos(bist_ang-0)) ** 2 * K_i
        nrcs_ice_hv = k_0 ** 4 * np.absolute(delta_Ei) ** 2 / (4 * np.pi) * np.absolute(L_H_q0 * M_V_q) ** 2 * np.sin(bist_ang-0) ** 2 * K_i
        nrcs_ice_vh = k_0 ** 4 * np.absolute(delta_Ei) ** 2 / (4 * np.pi) * np.absolute(L_H_q * M_V_q0) ** 2 * np.sin(bist_ang - 0) ** 2 * K_i

        # snow
        nrcs_snow_hh = k_0 ** 4 * np.absolute(delta_Es) ** 2 / (4 * np.pi) * np.absolute((1 + R_dH_1_0)*(1+R_dH_1)) ** 2 * np.cos(bist_ang-0) ** 2 * K_s
        nrcs_snow_vv = k_0 ** 4 * np.absolute(delta_Es) ** 2 / (4 * np.pi) * np.absolute(np.sin(inc_m) * np.sin(inc_b) / eps_s *
            (1 + R_dV_1_0) * (1 + R_dV_1) - (1 - R_dV_1_0) * (1 - R_dV_1) * np.cos(bist_ang-0) * np.cos(inc_m) * np.cos(inc_b)) ** 2 * K_s
        nrcs_snow_hv = k_0 ** 4 * np.absolute(delta_Es) ** 2 / (4 * np.pi) * np.absolute((1+R_dH_1_0)*(1 - R_dV_1) * np.sin(bist_ang-0) * np.cos(inc_b)) ** 2 * K_s
        nrcs_snow_vh = k_0 ** 4 * np.absolute(delta_Es) ** 2 / (4 * np.pi) * np.absolute((1 - R_dV_1_0) * (1 + R_dH_1) * np.sin(bist_ang - 0) * np.cos(inc_m)) ** 2 * K_s

        # total
        nrcs_hh = nrcs_ice_hh + nrcs_snow_hh
        nrcs_vv = nrcs_ice_vv + nrcs_snow_vv
        nrcs_hv = nrcs_ice_hv + nrcs_snow_hv
        nrcs_vh = nrcs_ice_vh + nrcs_snow_vh

        return nrcs_hh, nrcs_vv, nrcs_hv, nrcs_vh # only 'hh' and 'hv' required

if __name__ == '__main__':
    import drama.utils as drtls
    import matplotlib.pyplot as plt
    fwdm = FwdModel(1,'bla',[1.5, 0.0025, 0.019, 0.1], [3.6, 0.0025, 0.017])
    ampl = fwdm.fwd_nrcs_bistatic(1, 35, 35, 45, f0=5.4e9)
    print(drtls.db(ampl))
    #ampl = fwdm.fwd_nrcs_bistatic(1, 45, 0, 0, f0=5.4e9)
    #print(drtls.db(ampl))


    max_x=500 # maximum along-track distance
    x=np.arange(0,max_x)
    ampl_hh=np.zeros(max_x)
    ampl_vv = np.zeros(max_x)
    ampl_hv = np.zeros(max_x)
    ampl_vh = np.zeros(max_x)
    inc_m=35 # incidence angle Sentinel-1
    h=700 # satellite altitude
    y=np.tan(inc_m/180*np.pi)*h # distance ground track to center scene
    for i in range(0,len(x)):
        # compute approximate geometry
        bist_ang=np.arctan(x[i]/y)*180/np.pi # bistatic angle projected on the ground
        gr=np.sqrt(y**2+x[i]**2) # ground range to receiving satellite
        inc_s=np.arctan(gr/h)*180/np.pi # incidence angle receiver

        ampl=fwdm.fwd_nrcs_bistatic(1, inc_m, inc_s, bist_ang, f0=5.4e9)
        ampl_hh[i]=ampl[0]
        ampl_vv[i] = ampl[1]
        ampl_hv[i] = ampl[2]
        ampl_vh[i] = ampl[3]

    fig = plt.figure(figsize=(6, 6))
    plt.plot(x,drtls.db(ampl_hh))
    plt.plot(x, drtls.db(ampl_hv))
    plt.plot(x, drtls.db(ampl_hh+ampl_hv))
    #plt.plot(x, drtls.db(ampl_vv))
    #plt.plot(x, drtls.db(ampl_vh))
    plt.xlabel('bistatic distance [km]')
    plt.ylabel('NRCS [dB]')
    plt.legend(['HH','HV','HH+HV','VV','VH'])
    plt.axis([0,np.max(x),-50,0])
    plt.show()

    # check backscatter over incidence angle
    fwdm = FwdModel(1, 'bla', [1.5, 0.0025, 0.019, 0.1], [3.6, 0.0025, 0.017])
    i=0
    for inc_m in range(20,47):
        ampl = fwdm.fwd_nrcs_monostatic(1, inc_m, f0=5.4e9)
        ampl_hh[i] = ampl[0]
        ampl_vv[i] = ampl[1]
        ampl_hv[i] = ampl[2]
        ampl_vh[i] = ampl[3]
        i=i+1

    ampl_hh=ampl_hh[0:i]; ampl_vv=ampl_vv[0:i]; ampl_hv=ampl_hv[0:i]; ampl_vh=ampl_vh[0:i];

    plt.plot(range(20,47), drtls.db(ampl_hh))
    plt.plot(range(20,47), drtls.db(ampl_vv))
    plt.plot(range(20,47), drtls.db(ampl_hv))
    plt.plot(range(20,47), drtls.db(ampl_vh))
    plt.xlabel('incidence angle [deg]')
    plt.ylabel('NRCS [dB]')
    plt.axis([19, 48, -50, 0])
    plt.legend(['HH', 'VV', 'HV', 'VH'])
    plt.show()