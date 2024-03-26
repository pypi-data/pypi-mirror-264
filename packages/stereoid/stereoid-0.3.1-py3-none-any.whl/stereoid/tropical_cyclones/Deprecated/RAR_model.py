__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
import scipy as sp


# the scaling of the RAR spectrum should be checked rigorously
# FIXME: do not use this at the moment, it should be fixed and reconsidered
def RAR_spec(S, kx, ky, lambda_max, mu=0.5, theta=35, R=900E3, V=7000, L_A=3000,alpha=0):
    # L_A: antenna beamwidth
    # kx: wave number in the ground-range direction
    # ky: wave number perpendicular to the ground-range direction
    # alpha: bistatic angle

    # for a bistatic system kx must be pointing in the direction of the equivalent monostatic system (1/2 * bistatic angle)
    # this effectively means if you want to compare the RAR spectra of a monostatic system and a bistatic system, you
    # should rotate the input spectrum with 1/2* bistatic angle

    # angular frequency
    theta = np.deg2rad(theta)
    g = 9.81
    k = np.sqrt(kx ** 2 + ky ** 2)
    omega = np.sqrt(g * k)

    # RAR modulation per k_x
    if alpha==0:
        T_I = -1j * 4 * kx / (np.tan ( theta ) * (1 + np.sin ( theta ) ** 2)) - 1j * kx / np.tan (
            theta ) + 4.5 * omega * kx ** 2 * (omega - 1j * mu) / (k * (omega ** 2 + mu ** 2))
    if alpha!=0:
        kx=kx*np.cos(np.deg2rad(alpha)/2)
        T_I = -1j * 4 * kx / (np.tan ( theta ) * (1 + np.sin ( theta ) ** 2)) - 1j * kx / np.tan (
            theta ) + 4.5 * omega * kx ** 2 * (omega - 1j * mu) / (k * (omega ** 2 + mu ** 2))
    T_I[T_I != T_I] = 0

    # cross-spectral functions
    N_II_pos = 0.5 * T_I * np.conj ( T_I )
    S_neg = np.fft.fftshift ( S )
    S_neg = np.flipud ( np.fliplr ( S_neg ) )
    N_II_neg = np.fft.fftshift ( N_II_pos )
    N_II_neg = np.flipud ( np.fliplr ( N_II_neg ) )
    SN_II_neg = np.fft.ifftshift ( np.roll ( np.roll ( np.conj ( N_II_neg ) * S_neg, 1, axis=0 ), 1, axis=1 ) )


    # two dimensional spectrum
    S_RAR_2D =  np.real(N_II_pos * S + SN_II_neg)

    # I think we can simply assume that the waves come from a single direction
    S_RAR_1D = S_RAR_2D[0,:]
    # If that is the case we require some scaling
    # check for this in Jackson et al. (1985), A comparison of ...
    #S_RAR_1D = np.sqrt(2*np.pi)/L_A
    S_RAR_1D = S_RAR_1D/len(ky[0,:])

    # the previous function implies that we have SAR resolution in the along-track direction
    # let's generate a realization that leads
    #N = len ( ky )
    #s = np.real( np.fft.ifft2 ( np.sqrt( S_RAR_2D * N * N ) ) )
    #rho_s = np.real( np.fft.ifft2 ( S_RAR_2D)  )
    #plt.imshow(s)
    #plt.show()

    #plt.imshow(signal.correlate2d(s,s))
    #plt.show()

    # Gaussian antenna pattern with length L_A
    # FIXME: probably something is wrong with the scale and it can be more efficient
    #dy=lambda_max/N
    #y=np.arange(-lambda_max/2+0.5*dy,lambda_max/2,dy)
    #sigma_L=L_A/2
    #h=np.exp(-0.5*y**2/sigma_L**2)
    #h=h**2 # twice the antenna pattern
    #h=h/np.sum(h) # temporarily (if the size of the considered area is large enough not necessary)
    #h=np.convolve(h,h,'same')/N
    #plt.plot(h)
    #plt.show()

    # this can be faster, but I will do it with a for-loop for now (we filter with the antenna pattern)
    #s_1d=np.zeros((len(kx)))
    #rho_s1d=np.zeros((len(kx)))
    #for i in range(0,len(kx)):
        #s_1d[i]=np.sum(s[:,i]*h)
        #rho_s1d[i]=np.sum(rho_s[:,i]*h)

    #plt.plot(s_1d)
    #plt.show()

    #plt.plot(np.absolute(np.fft.fft(s_1d)))
    #plt.show()

    # get back 1D spectrum
    #S_RAR_1D=np.absolute(np.fft.fft(s_1d))**2/N
    #S_RAR_1D = np.absolute(np.fft.fft(rho_s1d))

    return S_RAR_2D, S_RAR_1D

if __name__ == '__main__':
    import os
    import numpy as np
    import scipy as sp
    from scipy import signal
    import SAR_model
    from matplotlib import pyplot as plt

    # wavelengths and wave numbers
    Nk = 128
    lambda_max = 5000
    kx = np.ones ( (1, Nk) )
    dk = 2 * np.pi / lambda_max  # fundamental frequency
    fs = lambda_max / Nk  # sampling rate
    kx[0, 0:int ( Nk / 2 )] = dk * np.arange ( 0, Nk / 2 )
    kx[0, int ( Nk / 2 ):] = dk * np.arange ( -Nk / 2, 0 )
    kx = np.dot ( np.ones ( (Nk, 1) ), kx )
    ky = np.transpose ( kx )
    k = np.sqrt(kx**2+ky**2)
    phi = np.arctan2 ( ky, kx )  # 0 is cross-track direction waves, 90 along-track

    ## monostatic input
    ###### let's put down a Gaussian swell wave spectrum
    phi_s = np.deg2rad ( -15 )  # swell direction
    f_p = 0.068  # peak frequency
    sigma_f = 0.01  # spread in frequency
    sigma_phi = np.deg2rad ( 5 )  # spreadk in direction
    Hs = 1  # significant wave height

    # frequency spectrum
    g = 9.81
    f = 0.5 / np.pi * np.sqrt ( g * k )
    fac_f = 0.25 / np.pi * np.sqrt ( g / k )
    amp = (Hs / 4) ** 2 / (sigma_f * np.sqrt ( 2 * np.pi ))
    Sp = (amp * np.exp ( -(f - f_p) ** 2 / (2 * sigma_f ** 2) ) + 1E-5) * fac_f

    # directional distribution
    dphi = (phi_s - phi + np.pi) % (2 * np.pi) - np.pi  # including unwrapping
    D = np.exp ( -dphi ** 2 / (2 * sigma_phi ** 2) ) / (2 * np.pi * sigma_phi ** 2) ** 0.5  # directional component
    S = Sp*D/k
    S[0,0]=0

    # RAR transform
    S_RAR_2D, S_RAR_1D=RAR_spec ( S, kx, ky, lambda_max, mu=0.5, theta=35, R=900E3, V=7000, L_A=3000 )

    plt.stem(kx[0,:],S_RAR_1D,'.')
    plt.show()

    ## bistatic input
    # bistatic angle
    alpha=32

    # directional distribution
    dphi = (phi_s+np.deg2rad(alpha/2) - phi + np.pi) % (2 * np.pi) - np.pi  # including unwrapping
    D = np.exp ( -dphi ** 2 / (2 * sigma_phi ** 2) ) / (2 * np.pi * sigma_phi ** 2) ** 0.5  # directional component
    S = Sp * D / k
    S[0, 0] = 0

    # RAR transform
    S_RAR_2D, S_RAR_1D = RAR_spec ( S, kx, ky, lambda_max, mu=0.5, theta=35, R=900E3, V=7000, L_A=3000 , alpha=alpha)

    plt.stem ( kx[0, :], S_RAR_1D, '.' )
    plt.show ()