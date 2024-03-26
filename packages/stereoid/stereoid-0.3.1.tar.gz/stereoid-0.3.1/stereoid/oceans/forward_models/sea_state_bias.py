__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

from stereoid.oceans.waves.wave_spectra import elfouhaily
from stereoid.oceans.waves.wave_spectra import elfouhaily_spread




# Two scale model of sea-state bias for monostatic equivalent
def seastatebias_twoscale(S, kx, ky, dk):
    # S: long-wave two-dimensional spectrum
    # kx,ky: wave numbers
    # dk: wave-number resolution

    # some computations
    g=9.81
    k=( kx ** 2 + ky ** 2) ** 0.5
    omega_k = np.sqrt( k * g )

    # modulation transfer function (Schulz-Stellenfleth et al. (2005))
    mu=0.5
    M_k = 4.5 * omega_k * kx ** 2 / k * omega_k / (omega_k ** 2 + mu ** 2)

    # sea state bias
    # FIXME: intuitively I would say, single-sided spectrum, we have to argue why
    # FIXME: carefully check if scaling is correct
    I=np.logical_and(k>0, k < 2*np.pi/0.3)
    ssb=np.sum(S[I]*M_k[I]*dk*dk)

    return ssb

if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt

    # wave numbers
    Nk = 1024
    lambda_max = 250  # maximum wavelength (size of image)
    kx = np.ones( (1, Nk) )
    dk = 2 * np.pi / lambda_max  # fundamental frequency
    fs = lambda_max / Nk  # sampling rate
    kx[ 0, 0:int( Nk / 2 ) ] = dk * np.arange( 0, Nk / 2 )
    kx[ 0, int( Nk / 2 ): ] = dk * np.arange( -Nk / 2, 0 )
    kx = np.dot( np.ones( (Nk, 1) ), kx )
    ky = np.transpose( kx )
    k = np.sqrt( kx ** 2 + ky ** 2 )
    dk = kx[0,1]-kx[0,0]
    dks=dk*dk*np.ones(k.shape)
    phi = np.arctan2( ky, kx )

    # wave spectrum using KMC14
    fetch = 100E3
    phi_w = 0
    u_10=np.arange(5,17,2)
    ssb=np.zeros(len(u_10))
    for i in range(0,len(u_10)):
        #B = Kudry_spec( kx, ky, u_10[i], fetch, phi_w, dks )
        #S = np.where( k > 0, B * k ** -4, 0 )

        # wave-number spectrum
        Sp = elfouhaily( k, u_10[i], fetch )
        dphi = (np.deg2rad( phi_w ) - phi + np.pi) % (2 * np.pi) - np.pi  # including unwrapping
        D = elfouhaily_spread( k, dphi, u_10[i], fetch )
        S = Sp * D / k
        S[ 0, 0 ] = 0


        # sea state bias
        ssb[i]=seastatebias_twoscale( S, kx, ky, dk)

    plt.plot(u_10,ssb)
    plt.xlabel('u_10 [m/s]')
    plt.ylabel('sea-state bias [m]')
    plt.show()

    print('minimum wavelength')
    print('should be close to 4 * radar wavelength')
    print(str(2*np.pi/np.max(k)) + 'm')


