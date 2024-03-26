__author__ = "Marcel Kleinherenbrink"
__email__ = "m.kleinherenbrink@tudelft.nl"

import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import scipy.interpolate as interp
from scipy import ndimage
import scipy.ndimage.filters as filters


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
        PSD2=np.absolute(np.fft.fft2(img2))**2/shp[0]/shp[1] # periodogram true velocity
        sigma_n2=np.std(np.ravel(img1-img2))**2 # white noise level
        print(np.sqrt(sigma_n2))
        # The Wiener filter
        W=PSD2/(PSD2+f*sigma_n2)

    # if we enter a noise level, we have to do something dirty
    if sigma_n != 0:
        PSD1 = np.absolute(np.fft.fft2(img1)) ** 2 / shp[0] / shp[1]  # periodogram noisy velocity
        sigma_n2=sigma_n**2
        PSD2 = PSD1-sigma_n2 # this does not make a mathematician happy, because it might give negative values
        PSD2[PSD2 < 0]=0 # get rid of the negative values
        print(np.sqrt(sigma_n2))

        # The Wiener filter
        W=PSD2/(PSD2+f*sigma_n2)

    # if we do not have anything, we have to make a hard assumption
    # that the median value of signal is close to the noise level
    if sigma_n == 0 and np.mean(np.ravel(img2)) == 0:
        PSD1 = np.absolute(np.fft.fft2(img1)) ** 2 / shp[0] / shp[1]
        sigma_n2=np.median(PSD1)
        print(np.sqrt(sigma_n2))
        PSD2 = PSD1 - sigma_n2  # this does not make a mathematician happy, because it might give negative values
        PSD2[PSD2 < 0] = 0  # get rid of the negative values

        # The Wiener filter
        W = PSD2 / (PSD2+f*sigma_n2)

    # DFT of the noisy signal
    I=np.fft.fft2(img1)

    # Then IDFT
    img1_f=np.fft.ifft2(W*I)

    # returns a filtered velocity field
    return np.real(img1_f)

# hybrid median filter
def hybrid_median(img,n,K):
    # img is the input field
    # n is the size of the filter (take an odd number)
    # K is the number of iterations

    # size of image and half-size of filter
    shp=img.shape
    l=int((n-1)/2)

    f_img=np.zeros(shp) # filtered image
    m=np.zeros(4) # median in four directions
    k=0
    while k < K:
        print(k)
        k=k+1

        # loop through the image
        for i in range(0+l,shp[1]-l):
            for j in range(0+l,shp[0]-l):
                D=img[j-l:j+l,i-l:i+l]
                m[0]=np.median(D[:,l])
                m[1]=np.median(D[l,:])
                m[2]=np.median(np.diag(D))
                m[3]=np.median(np.diag(np.rot90(D)))

                f_img[j,i]=np.median(m)
    # returns filtered image
    return f_img


# explained variance algorithm version 1
# it compares the variance of just estimating a simple local mean with the variance of a model with discontinuities in four directions
# I think an F-test should be the one to use, but I doubt a statistician likes an F-test with four added parameters
# Before running this code, you could run a median filter
def explainedvariance_v1(img,n):
    # img is the input field
    # n is the size of the boxes considered in pixels (n x n)

    shp = img.shape

    # prepare a design matrix
    nn = n+1; # this is actually n+1
    f1 = np.zeros((nn, nn));f2 = np.zeros((nn, nn));f3 = np.ones((nn, nn));f4 = np.ones((nn, nn))
    f1[:int(n / 2), :n] = 1;f2[:n, :int(n / 2)] = 1;f3 = np.tril(f3);f4 = np.transpose(np.tril(f4))
    f1 = np.ravel(f1);f2 = np.ravel(f2);f3 = np.ravel(f3);f4 = np.ravel(f4)
    A = np.column_stack((np.ones(len(f1)), f1, f3, f2, f4)) # pay attention to the order

    # let's compute the explained variance
    EV = np.zeros(shp)
    C = np.zeros(shp)
    for i in range(int(n / 2), int(shp[1] - n / 2)-1):
        for j in range(int(n / 2), int(shp[0] - n / 2)-1):

            # take a block of data and compute the standard deviation
            u_temp = np.ravel(img[j - int(n / 2):j + int(n / 2) + 1, i - int(n / 2):i + int(n / 2) + 1])
            std_u = np.std(u_temp)

            # least-squares and residuals
            c = np.linalg.lstsq(A, u_temp, rcond=None)[0]
            e = u_temp - np.dot(A, c)
            C[j,i] = np.argmax(c[1:5])*45 # let's also get the angle

            # standard deviation of residuals and explained variance
            std_e = np.std(e)
            EV[j, i] = 1 - std_e ** 2 / std_u ** 2

    # returns the explained variance
    return EV,C

# non-maximum suppression to get thin lines instead of thick ones
# this code is adapted from: https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123
def non_max_suppression(img,theta):
    # img is a field of potential edges
    # theta is a set of angle (if they are all zero, they will be computed using Sobel filters)

    if np.mean(theta) == 0:
        # Sobel filters to detect the edge direction
        Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
        Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
        Ix = ndimage.filters.convolve(img, Kx)
        Iy = ndimage.filters.convolve(img, Ky)
        G = np.hypot(Ix, Iy)
        G = G / G.max() * 255
        theta = np.arctan2(Iy, Ix)

    # some preparations
    shp = img.shape
    Z = np.zeros(shp, dtype=np.int32)
    angle = theta * 180. / np.pi
    angle[angle < 0] += 180

    # here starts the actual maximum suppression
    for i in range(1, shp[0] - 1):
        for j in range(1, shp[1] - 1):
            try:
                q = 255
                r = 255

                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j + 1]
                    r = img[i, j - 1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i + 1, j - 1]
                    r = img[i - 1, j + 1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i + 1, j]
                    r = img[i - 1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i - 1, j - 1]
                    r = img[i + 1, j + 1]

                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0

            except IndexError as e:
                pass

    # returns thin edges
    return Z

# this code reconstructs a velocity field from a singular value decomposition
# usefulness currently unknown, primarily because the variance increases near the strip edges, which spoils most of it
# might work after the application of an appropriate filter
def svd_recon(img,n_min,n_max):
    # img input field
    # n_min first eigenvalue of reconstruction (normally set to zero)
    # n_max max eigenvalue of reconstruction

    # svd
    u, d, v = np.linalg.svd(img)

    # reconstruction
    img_r = np.matrix(u[:,n_min:n_max]) * np.diag(d[n_min:n_max]) * np.matrix(v[n_min:n_max, :])

    # reconstructed image
    return img_r

# code to find maxima in velocity, gradient or explained value fields
# based on: https://stackoverflow.com/questions/9111711/get-coordinates-of-local-maxima-in-2d-array-above-certain-value
def local_max_twofields(u,v,nsu,nsv,thru,thrv):

    # for v first
    data_max = filters.maximum_filter(v, nsv)
    maxima = (v == data_max)
    data_min = filters.minimum_filter(v, nsv)
    diff = ((data_max - data_min) > thrv)
    maxima[diff == 0] = 0
    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)
    x, y = [], []
    for dy,dx in slices:
        x_center = (dx.start + dx.stop - 1)/2
        x.append(x_center)
        y_center = (dy.start + dy.stop - 1)/2
        y.append(y_center)

    # for u second
    data_max = filters.maximum_filter(u, nsu)
    maxima = (u == data_max)
    data_min = filters.minimum_filter(u, nsu)
    diff = ((data_max - data_min) > thru)
    maxima[diff == 0] = 0
    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)
    for dy,dx in slices:
        x_center = (dx.start + dx.stop - 1)/2
        x.append(x_center)
        y_center = (dy.start + dy.stop - 1)/2
        y.append(y_center)

    # returns x,y coordinates of local maxima
    return x,y

# some thresholding, which can be done after the non-maximum suppression
# this code is adapted from: https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123
def thresholding(Z,lowThresholdRatio,highThresholdRatio):
    # Z is a field with gradients/EVs
    # lowThresholdRatio is the threshold ratio for weak gradients
    # lowThresholdRatio is the threshold ratio for strong gradients

    shp=Z.shape

    # search for weak gradients and strong gradients
    highThreshold = Z.max() * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio
    res = np.zeros(shp, dtype=np.int32)
    weak = np.int32(25)
    strong = np.int32(255)
    strong_i, strong_j = np.where(Z >= highThreshold)
    weak_i, weak_j = np.where((Z <= highThreshold) & (Z >= lowThreshold))
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    # output is a field with weak and strong gradients
    return res