__author__ = "Marcel Kleinherenbrink"
__email__ = "m.kleinherenbrink@tudelft.nl"

import warnings
import numpy as np
import scipy.interpolate
from matplotlib import pyplot as plt

# Ignore overflow errors for wind calculations over land
warnings.simplefilter("ignore", RuntimeWarning)

def IWRAP_model_parameters_Sapp(pol):
    # Note that there is another set of parameters in Sapp, but only for two angles.
    # I will add these parameters later, because they fit the data much better.
    # Figures 3.17-3.21 show that the IWRAP models apparently do not fit the data properly.
    """!     ---------
        !         inputs:
        !              pol 'VV' or 'VH'
        !         output:
        !              CMOD5_N NORMALIZED BACKSCATTER (LINEAR)
        !
        !        Based on PhD thesis of Sapp
        !
        !
        !---------------------------------------------------------------------
           """

    if pol == 'VV':
        # incidence angles model
        theta_m = np.deg2rad([29.0, 34.0, 40.0, 50.0])

        beta = [-3.1803, -4.1806, -4.9856, -6.2902]
        gamma_1 = [3.3693, 4.2092, 4.8417, 6.2018]
        gamma_2 = [-0.9923, -1.1996, -1.3290, -1.7647]

        c0 = [7.6260E-3, -4.2310E-3, -1.0300E-1, -3.9680E-1]
        c1 = [4.9330E-3, 7.6040E-3, 1.2600E-2, 2.1360E-2]
        c2 = [-3.1680E-5, -5.7510E-5, -1.2520E-4, -2.2440E-4]

        d0 = [-1.7960E-1,-7.7830E-2,1.1890E-1,5.9390E-2]
        d1 = [3.9680E-2,5.9610E-2,3.5170E-2,4.1520E-2]
        d2 = [-3.7520E-2,-5.7680E-2,-3.6610E-2,-4.1980E-2]
        d3 = [30.0, 20.0, 18.0, 19.0]

    # for the horizontal polarizations
    if pol == 'HH':
        theta_m = np.deg2rad([31.0, 36.0, 42.0, 49.0])

        beta = [-4.2560,-5.3874,-5.9355,-6.6837]
        gamma_1 = [4.0461,5.0899,5.3750,5.8551]
        gamma_2 = [-1.1776,-1.4213,-1.4185,-14971]

        c0 = [7.0380E-2, -4.6340E-2, 9.4450E-2, -1.8120E-2]
        c1 = [3.5170E-3, 1.1460E-2, 3.7730E-3, 9.1030E-3]
        c2 = [-2.5170E-5,-1.1180E-4,-3.3660E-5,-1.0720E-4]

        d0 = [-1.0340E-1,-2.2980E-1,1.8210E-1,7.4150E-2]
        d1 = [2.9500E-2,7.4780E-2,1.6900E-2,4.0130E-2]
        d2 = [-2.8490E-2,-7.0600E-2,-1.9890E-2,-4.0950E-2]
        d3 = [30.0, 20.0, 18.0, 19.0]

    return theta_m,beta,gamma_1,gamma_2,c0,c1,c2,d0,d1,d2,d3

def IWRAP_model_parameters_Belmonte(pol):
    # Before usage, not that the same holds for these parameters as for Sapp's set:
    # They do not fit the data properly. Check out figures 3.17-3.21 in Sapp's thesis.
    """!     ---------
        !         inputs:
        !              pol 'VV' or 'VH'
        !         output:
        !              CMOD5_N NORMALIZED BACKSCATTER (LINEAR)
        !
        !        Based on the technical report
        !        NWP/SAF associate scientist mission report: polarization
        !        options for the EPS-SG scatterometer by Belmonte-Rivas et al. (2012).
        !
        !
        !---------------------------------------------------------------------
           """

    if pol == 'VV':
        # incidence angles model
        theta_m = np.deg2rad([29.0, 34.0, 40.0, 50.0])

        beta = [-3.807, -4.631, -5.081, -6.931]
        gamma_1 = [4.064, 4.641, 4.784, 6.808]
        gamma_2 = [-1.185, -1.300, -1.266, -1.903]

        c0 = [1.500E-2, -1.080E-2, -1.757E-1, -5.453E-1]
        c1 = [3.917E-3, 7.046E-3, 1.515E-2, 2.710E-2]
        c2 = [-1.6595E-5, -4.6334E-5, -14.830E-5, -28.064E-5]

        d0 = [6.021E-2, -4.288E-2, 1.972E-1, 1.291E-1]
        d1 = [1.904E-2, 6.199E-2, 2.561E-2, 3.551E-2]
        d2 = [-2.026E-2, -6.066E-2, -2.837E-2, -3.714E-2]
        d3 = [30.0, 20.0, 18.0, 19.0]

    # for the horizontal polarizations
    if pol == 'HH':
        theta_m = np.deg2rad([31.0, 36.0, 42.0, 49.0])

        beta = [-4.892, -5.689, -5.570, -5.886]
        gamma_1 = [4.7275, 5.2932, 4.6925, 4.5876]
        gamma_2 = [-1.3598, -1.4401, -1.1496, -1.0355]

        c0 = [7.030E-2, -1.083E-1, 8.060E-2, -1.053E-1]
        c1 = [3.093E-3, 1.354E-2, 4.091E-3, 1.289E-2]
        c2 = [-1.8011E-5, -13.004E-5, -3.5243E-5, -14.723E-5]

        d0 = [1.337E-1, -2.461E-1, 2.864E-1, 1.534E-1]
        d1 = [8.883E-3, 8.731E-2, -1.006E-3, 3.223E-3]
        d2 = [-1.121E-2, -8.289E-2, -3.737E-3, -3.438E-2]
        d3 = [30.0, 20.0, 18.0, 19.0]

    return theta_m,beta,gamma_1,gamma_2,c0,c1,c2,d0,d1,d2,d3

def IWRAP_forward(v, phi, theta, pol):
    """!     ---------
    !     cmod5n_forward(v, phi, theta)
    !         inputs:
    !              v     in [m/s] wind velocity (always >= 0)
    !              phi   in [deg] angle between azimuth and wind direction
    !                    (= D - AZM)
    !              theta in [deg] incidence angle
    !         output:
    !              CMOD5_N NORMALIZED BACKSCATTER (LINEAR)
    !
    !        Based on the technical report
    !        NWP/SAF associate scientist mission report: polarization
    !        options for the EPS-SG scatterometer by Belmonte-Rivas et al. (2012).
    !
    !
    !---------------------------------------------------------------------
       """

    #thetm = 60.0
    #thethr = 20.0

    # get model parameters
    theta_m, beta, gamma_1, gamma_2, c0, c1, c2, d0, d1, d2, d3=IWRAP_model_parameters_Belmonte(pol)

    # convert to radians
    phi = np.deg2rad(phi)
    theta = np.deg2rad(theta)

    # interpolate the parameters linearly to the 'exact' incidence angle
    f = scipy.interpolate.interp1d(theta_m, beta, fill_value='extrapolate');
    betai = f(theta)
    f = scipy.interpolate.interp1d(theta_m, gamma_1, fill_value='extrapolate');
    gamma_1i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, gamma_2, fill_value='extrapolate');
    gamma_2i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, c0, fill_value='extrapolate');
    c0i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, c1, fill_value='extrapolate');
    c1i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, c2, fill_value='extrapolate');
    c2i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d0, fill_value='extrapolate');
    d0i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d1, fill_value='extrapolate');
    d1i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d2, fill_value='extrapolate');
    d2i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d3, fill_value='extrapolate');
    d3i = f(theta)

    a1 = c0i + c1i * v + c2i * v ** 2
    a2 = d0i + d1i * v + d2i * v * np.tanh(v / d3i)

    # FIXME: the paper states alog10, it guess this is just log10,
    #  because alog10 is a fortran function
    A0 = 10 ** betai * v ** (gamma_1i + gamma_2i * np.log10(v))

    sigma_0 = A0 * (1 + a1 * np.cos(phi) + a2 * np.cos(2 * phi))
    #print(a2)

    return sigma_0, a1, a2, A0

# FIXME: dont' use this, not properly tested
def IWRAP_inverse_MonteCarlo(sigma_0, theta, phi, pol='VV', est_dir=0, est_v=0):
    """

    Parameters
    ----------
    sigma_0: 3*N vector of backscatter [dB]
    theta: 3*N vector of monostatic equivalent incident angles [rad]
    phi: 3*N vector of ground-range directions [rad]
    pol: polarization ('VV' or 'HH')
    est_dir: first estimate of wind direction [rad]

    N is the number of observation sets (three directions)

    Returns
    -------

    """

    # get model parameters
    theta_m, beta, gamma_1, gamma_2, c0, c1, c2, d0, d1, d2, d3=IWRAP_model_parameters_Belmonte(pol)
    shp=theta.shape

    # interpolation
    f = scipy.interpolate.interp1d(theta_m, beta, fill_value='extrapolate');
    betai = f(theta)
    f = scipy.interpolate.interp1d(theta_m, gamma_1, fill_value='extrapolate');
    gamma_1i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, gamma_2, fill_value='extrapolate');
    gamma_2i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, c0, fill_value='extrapolate');
    c0i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, c1, fill_value='extrapolate');
    c1i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, c2, fill_value='extrapolate');
    c2i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d0, fill_value='extrapolate');
    d0i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d1, fill_value='extrapolate');
    d1i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d2, fill_value='extrapolate');
    d2i = f(theta)
    f = scipy.interpolate.interp1d(theta_m, d3, fill_value='extrapolate');
    d3i = f(theta)

    ## go through all locations
    vx = np.arange(-60, 60.01, 1)
    vy = np.arange(-60, 60.01, 1)
    vx,vy=np.meshgrid(vx,vy)
    v= np.sqrt(vx**2 + vy**2)
    vdir=np.arctan2(vy,vx)
    vx=vx.ravel()
    vy=vy.ravel()
    v=v.ravel()
    vdir=vdir.ravel()

    vx_est=np.zeros(shp[1])
    vy_est = np.zeros(shp[1])
    for i in range(0,theta.shape[1]):
        for j in range(0,theta.shape[0]):
            I=np.logical_and(np.absolute(np.angle(np.exp(1j*(est_dir[i]-vdir)))) < np.pi/8,np.absolute(v-est_v[i]) < 10)
            if len(I) == 0:
                I = np.logical_and(np.absolute(np.angle(np.exp(1j * (est_dir[i] - vdir)))) < np.pi / 4,
                                   np.absolute(v - est_v[i]) < 10)

            v_temp=v[I]
            vdir_temp=vdir[I]
            vx_temp=vx[I]
            vy_temp = vy[I]
            sigma_est = np.zeros((len(v_temp), shp[0]))
            A0 = 10 ** betai[j,i] * v_temp ** (gamma_1i[j,i] + gamma_2i[j,i] * np.log10(v_temp))
            a1 = c0i[j,i] + c1i[j,i] * v_temp + c2i[j,i] * v_temp ** 2
            a2 = d0i[j,i] + d1i[j,i] * v_temp + d2i[j,i] * v_temp * np.tanh(v_temp / d3i[j,i])
            sigma_est[:,j] = A0 * (1 + a1 * np.cos(vdir_temp + np.pi - phi[j,i]) + a2 * np.cos(2 * (vdir_temp + np.pi - phi[j,i])))

        I=np.argmin(np.sum(np.absolute(sigma_0[:,i]-sigma_est)**2,axis=1))
        #print(np.sum(np.absolute(sigma_0[:,i]-sigma_est)**2,axis=1))
        vx_est[i] = vx_temp[I]
        vy_est[i] = vy_temp[I]


    return vx_est, vy_est

if __name__ == "__main__":
    from matplotlib import pyplot as plt

    '''
    # make a look-up table for v only
    wdir_rel = 0
    pol = 'VV'

    v = np.arange(20, 60, 0.2)
    theta_i = np.ones(len(v))*47.0
    A0 = np.zeros(len(v))
    a1 = np.zeros(len(v))
    a2 = np.zeros(len(v))
    for i in range(0, len(v)):
        sigma, a1[i], a2[i], A0[i] = IWRAP_forward(v[i], wdir_rel, theta_i[i], pol)

    theta_m, beta, gamma_1, gamma_2, c0, c1, c2, d0, d1, d2, d3=IWRAP_model_parameters_Sapp(pol)

    x=3;
    plt.plot(v,10 ** beta[x] * v ** (gamma_1[x] + gamma_2[x] * np.log10(v)))
    plt.plot(v,c0[x] + c1[x] * v + c2[x] * v ** 2)
    plt.plot(v,d0[x] + d1[x] * v + d2[x] * v *np.tanh(v/d3[x]))
    plt.show()
    print(np.rad2deg(theta_m))
    '''

    # test for relative wind direction
    pol = 'VV'
    wdir = 0
    wdir_rel = wdir - np.linspace(0, 360, 32, endpoint=False)
    theta_i = 30 * np.ones(32)  # np.linspace(49,51,64)
    vi = 45
    sigma_0, a1_i, a2_i, A0_i = IWRAP_forward(vi, wdir_rel, theta_i, pol)
    sigma_0n = np.random.randn(len(sigma_0)) * (0.001)
    sigma_0 = sigma_0 #+ sigma_0n
    
    plt.figure()
    plt.plot(wdir_rel, 10 * np.log10(sigma_0))
    plt.grid()
    plt.xlabel("wind direction [deg]")
    plt.ylabel("$\sigma_0$ [dB]")
    plt.show()
    '''
    # inversion
    wdir_e = wdir + np.random.randn(1) * 10  # give it some estimate of wind direction
    phi = np.linspace(0, 360, 32, endpoint=False)
    vo,wdir_o,A0_o,a1_o,a2_o=IWRAP_inverse_fast(sigma_0, theta_i, phi, wdir_e,A0,a1,a2,v)
    #vo, wdir_o, sigma_0o = IWRAP_inverse_MonteCarlo(sigma_0, theta_i, phi, pol)

    print('output velocity:', vo, 'm/s')
    print('input velocity:', vi, 'm/s')
    print('output direction:', wdir, 'deg')
    print('input direction:', wdir_o, 'deg')
    
    plt.figure()
    plt.plot(wdir_rel, 10 * np.log10(sigma_0))
    plt.plot(wdir_rel, 10 * np.log10(sigma_0o))
    plt.grid()
    plt.xlabel("wind direction [deg]")
    plt.ylabel("$\sigma_0$ [dB]")
    plt.show()
    '''
    '''
    plt.figure()
    plt.plot(v, A0,'b',label='A0')
    plt.plot(v, a1,'r',label='a1')
    plt.plot(v, a2,'g',label='a2')
    plt.plot(vi,A0_o,'b*')
    plt.plot(vi, a1_o,'r*')
    plt.plot(vi, a2_o,'g*')
    plt.grid()
    plt.xlabel("v [m/s]")
    plt.ylabel("parameter")
    plt.show()
    '''
