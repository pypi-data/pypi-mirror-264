__author__ = "Marcel Kleinherenbrink"
__email__ = "m.kleinherenbrink@tudelft.nl"

import warnings
import numpy as np
import scipy.interpolate
from matplotlib import pyplot as plt

# Ignore overflow errors for wind calculations over land
warnings.simplefilter("ignore", RuntimeWarning)

def Zadelhoff_modelparameters(pol,model):
    """!     ---------
        !         inputs:
        !              pol 'VH'
                       model 'ECWMF' or 'SFMR' (Vachon and Wolfe, 2011)
        !         output:
        !              model parameters
        !
        !        Retrieving hurricane wind speeds using cross-polarization C-band
        !        measurements by Zadelhoff et al. (2014).
        !
        !---------------------------------------------------------------------
           """
    # Better set it to SFMR for now, the ECMWF have to be corrected for incidence angle,
    # which we cannot directly do, because we need an estimate for the wind speed first
    if pol == 'VH':
        if model == 'ECMWF':
            A=[-39.53, -28.09]
            B=[0.76,0.213]
        if model == 'SFMR':
            A=[-35.60, -29.07]
            B=[0.59,0.218]

    return A,B

def Zadelhoff_forward(v, pol):
    """!     ---------
    !     cmod5n_forward(v, theta, pol)
    !         inputs:
    !              v     in [m/s] wind velocity (always >= 0)
    !              theta in [deg] incidence angle
    !               pol   only 'VH' at the moment
    !         output:
    !              NRCS
    !
    !---------------------------------------------------------------------
       """
    # get parameters
    A,B=Zadelhoff_modelparameters(pol,'SFMR')

    # model
    sigma_0=np.zeros(len(v))
    sigma_0[v < 20]=A[0]+B[0]*v[v < 20]
    sigma_0[v > 20]=A[1]+B[1]*v[v > 20]

    return sigma_0


def Zadelhoff_inverse(sigma_0, pol):
    # this function uses a Monte Carlo for the wind speed and wind direction
    # input:
    # sigma_0: NRCS vector
    # theta: incidence angle [deg]
    # pol: polarization only 'VH' at the moment

    # only returns wind speed
    # get parameters
    A,B=Zadelhoff_modelparameters(pol,'ECMWF')

    # convert to decibels
    sigma_0=10*np.log10(sigma_0)

    #  inversion
    ws=np.mean((sigma_0-A[0])/B[0])
    #plt.plot((sigma_0-A[0])/B[0],sigma_0)
    #plt.show()

    # if the wind speed is above 20 m/s, no incidence angle correction can be applied
    if ws > 20:
        ws=np.mean((sigma_0-A[1])/B[1])

    return ws


if __name__ == "__main__":
    from matplotlib import pyplot as plt


    pol = 'VH'
    v = np.linspace(5,45)
    sigma_0 = Zadelhoff_forward(v, pol)

    plt.figure()
    plt.plot(v, sigma_0)
    plt.xlabel('wind speed [m/s]')
    plt.ylabel('NRCS')
    plt.show()

