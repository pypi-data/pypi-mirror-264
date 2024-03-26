__author__ = "Marcel Kleinherenbrink"
__email__ = "m.kleinherenbrink@tudelft.nl"

import numpy as np
import drama.utils as drtls
from drama.io import cfg as cfg
from drama import constants as const

class RetrievalModel( object ):
    def __init__( self, obs_geo_a, obs_geo_b, par_file ):
        self.par_file = par_file
        self.obs_geo_a = obs_geo_a
        self.obs_geo_b = obs_geo_b

    def sea_ice_drift(self, dopp_radar):#, s1_weight=1):

        # get some settings
        cfgdata = cfg.ConfigFile(drtls.get_par_file(self.par_file))

        # incident angles and wavelength
        wl = const.c / cfgdata.sar.f0
        inc_m = (self.obs_geo_a.inc_m)
        inc_b_a = (self.obs_geo_a.inc_b)
        inc_b_b = (self.obs_geo_b.inc_b)
        bist_ang_a = (self.obs_geo_a.bist_ang)
        bist_ang_b = (self.obs_geo_b.bist_ang)

        # vectors and unit vectors
        rthat = [np.sin(inc_m), 0, np.cos(inc_m)]
        rchat = [np.cos(bist_ang_a) * np.sin(inc_b_a), np.sin(bist_ang_a) * np.sin(inc_b_a), np.cos(inc_b_a)]
        rdhat = [np.cos(bist_ang_b) * np.sin(inc_b_b), np.sin(bist_ang_b) * np.sin(inc_b_b), np.cos(inc_b_b)]

        # design matrix
        a = np.zeros(inc_m.shape + (2, 2))
        #a[..., 0, 0] = 1 / wl * (rthat[0] + rthat[0]) * np.sqrt(s1_weight)
        #a[..., 0, 1] = 0
        a[..., 0, 0] = 1 / wl * (- rthat[0] - rchat[0])
        a[..., 0, 1] = 1 / wl * rchat[1]
        a[..., 1, 0] = 1 / wl * (- rthat[0] - rdhat[0])
        a[..., 1, 1] = 1 / wl * rdhat[1]

        # Pseudo inverse of a
        b = np.linalg.pinv(a)

        # compute sea-ice drift
        tscv = np.einsum("...ij,...j->...i", b, dopp_radar[:,:,1:])

        return tscv