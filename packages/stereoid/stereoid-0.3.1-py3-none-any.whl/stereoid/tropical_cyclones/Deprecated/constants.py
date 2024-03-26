import numpy as np

class constants:
    # some constants
    g = 9.81 # gravitational constant
    gamma = 0.07275  # surface tension
    eps_w = complex(73, 18)  # dielectric constant water
    c = 3E8 # speed-of-light
    f_c = 9.6E9 #5.405E9  # carrier frequency (hardcoded)
    la_r = 0.056  # wavelength C-band radar (hardcoded)
    s_wb = np.sqrt( 0.19 )  # square of the mean square slope of enhanced surface roughness (Kudryavtsev et al, 2003)
    eps_wb = 5E-3  # ratio of vert. to horiz. scale of breaking zone (Kudry et al, 2003)
    theta_wb = 5E-2  # mean tilt of non-Bragg scattering (Kudryavtsev et al, 2003)
    n_g = 5#10  # power number (Kudryavtsev et al, 2014)
    alpha_g = 5E-3  # some constant (Kudryavtsev et al, 2005)
    a = 3E-3#5E-3  # saturation level (Kydry et al, 2014), probably the same as alpha_g
    rho_w = 1000  # density of sea water
    c_q = 10.5  # constant for wave breaking (Kudry et al, 2003)
    Kappa = 0.4  # Van Karman constant (Kudry et al, 2003, eq. 19)
    a_star = 0.018  # (Kudry et al, 2003, eq. 21)
    a_v = 0.1  # (Kudry et al, 2003, eq. 21)
    rho_a = 1.225 # air density at sea level
    nu_a = 1.47E-5  # kinematic viscosity air
    d = 1 / 4 # two-scale cut for Bragg (Kudry et al. 2005)
    b_r = 0.1  # minimum wavelength ratio to radar wavenumber
    nu = 1.15E-6  # kinematic viscosity
    c_b = 1.2E-2  # empirical constant (below eq. 20, Kudry et al, 2005)
    c_b_w = 2.7E-2 # empirical constant (below eq. A3, Kudry et al, 2014)
    B_wb = 1E-2 # Kudry et al. (2019)
    m_k = 9/2 # Hansen et al. (2012)
    tau_wb=2 # Relaxation parameters
    tau_br=0.5
    tau_sp=0.5
    c_sn=4.5E-3 # cross-pol parameter for Bragg scattering (eq. A4, Kudryavtsev et al. 2019)
    Cm_b = 0.03  # mean value of C_b over transition interval (below A14, Yurovskaya et al. (2013))
