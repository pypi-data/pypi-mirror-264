__author__ = "Marcel Kleinherenbrink"
__email__ = "m.kleinherenbrink@tudelft.nl"

import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import scipy.interpolate as interp
from scipy import ndimage

# contains a set of functions for filtering and edge detection

# adaptive Wiener filter
# FIX ME: periodogram should be computed using Welch's method or something, now it is noisy
# it also assumes white noise
def aWiener(img1,img2,sigma_n,f):
    # img is a noise distorted velocity field (m x n)
    # img2 is the true velocity field (m x n)
    # sigma_n is the noise level
    # f is a scaling of the noise

    # you either should give the true velocity field or set the noise level
    # if you have the true velocity field, set sigma_n to zero
    # if you do not have the true velocity field, enter zeros in img2 in and set sigma_n to the noise level
    # if you do not have the true velocity and no noise level, we compute an estimate of the noise level,
    # but this assumes a limited amount of discontinuities

    shp=img1.shape

    # we have a true velocity field, so we can construct a true Wiener filter
    if np.mean(np.ravel(img2)) != 0:
        #PSD1=np.fft.fft2(img1)**2/shp[0]/shp[1] # periodogram noisy velocity
        PSD2=np.fft.fft2(img2)**2/shp[0]/shp[1] # periodogram true velocity
        sigma_n=np.mean(np.fft.fft2(img1-img2)**2/shp[0]/shp[1]) # white noise level

        # The Wiener filter
        W=PSD2/(PSD2+f*sigma_n)

    # if we enter a noise level, we have to do something dirty
    if sigma_n != 0:
        PSD1 = np.fft.fft2(img1) ** 2 / shp[0] / shp[1]  # periodogram noisy velocity
        PSD2 = PSD1-sigma_n # this does not make a mathematician happy, because it might give negative values
        PSD2[PSD2 < sigma_n/100]=sigma_n/100 # get rid of the negative values

        # The Wiener filter
        W=PSD2/(PSD2+f*sigma_n)

    # if we do not have anything, we have to make a hard assumption
    # that the median value of signal is close to the noise level
    if sigma_n == 0 and np.mean(np.ravel(img2)) != 0:
        PSD1 = np.fft.fft2(img1) ** 2 / shp[0] / shp[1]
        sigma_n=np.median(PSD1)
        PSD2 = PSD1 - sigma_n  # this does not make a mathematician happy, because it might give negative values
        PSD2[PSD2 < sigma_n / 100] = sigma_n / 100  # get rid of the negative values

        # The Wiener filter
        W = PSD2 / (PSD2 + f * sigma_n)

    # DFT of the noisy signal
    I=np.fft.fft2(img1)

    # Then IDFT
    img1_f=np.fft.fft2(W*I)

    # returns a filtered velocity field
    return img1_f


