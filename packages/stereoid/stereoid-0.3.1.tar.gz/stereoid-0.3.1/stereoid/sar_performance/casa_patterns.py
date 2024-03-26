import numpy as np
#import scipy as sp
import scipy.io as spio
from scipy.io.idl import readsav
from scipy.constants import c
import os
from drama.performance.sar import pattern
import drama.utils as drtls

__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"


class casa_pattern(pattern):

    def __init__(self, matfile, b_at, f0,
                 squint=0, el0=0, tilt=0, el_offset=0, az_offset=0):
        """
        
        :param matfile: mat file with patterns 
        :param b_at: separation between phase centers
        :param f0: center frequency
        :param squint: Azimuth pointing, in degree. Defaults to 9.
        :param el0: Elevation pointing w.r.t. boresight, in degree.
                    Defaults to 0.
        :param tilt: Mechanical tilt, in degree, defaults to 0.
        :param el_offset: an offset w.r.t. to nominal phase center in (m).
                          This causes a linear phase in elevation.
        :param az_offset: same in azimuth
        """
        self.__read_ext_pattern(matfile)
        self.squint = np.radians(squint)
        self.rel0 = np.radians(el0) - np.radians(tilt)
        self.tilt = np.radians(tilt)
        self.az_offset = az_offset
        self.el_offset = el_offset
        self.du = self.pat_u[1] - self.pat_u[0]
        self.dv = self.pat_v[1] - self.pat_v[0]
        self.f0 = f0
        self.wl = c / f0
        self.k0 = 2 * np.pi / self.wl
        self.b_at = b_at

    def __read_ext_pattern(self, matfile):
        pats_as_dict = spio.loadmat(matfile)
        self.pat_fore = pats_as_dict['AF0_ref_fwd'].astype(np.complex64)
        self.pat_aft = pats_as_dict['AF0_ref_aft'].astype(np.complex64)
        self.xpat_fore = pats_as_dict['XF0_ref_fwd'].astype(np.complex64)
        self.xpat_aft = pats_as_dict['XF0_ref_aft'].astype(np.complex64)
        self.pat_u = pats_as_dict['u'].flatten().astype(np.float32)
        self.pat_v = pats_as_dict['v'].flatten().astype(np.float32)
        self.ind_vmid = int(self.pat_v.size / 2)
        self.ind_umid = int(self.pat_u.size / 2)
        # Normalize
        self.g0 = np.sqrt(np.nanmax(np.abs(self.pat_fore))**2 + np.nanmax(np.abs(self.pat_aft))**2)
        self.pat_fore /= (self.g0 * np.sqrt(2))
        self.pat_aft /= (self.g0 * np.sqrt(2))
        self.xpat_fore /= (self.g0 * np.sqrt(2))
        self.xpat_aft /= (self.g0 * np.sqrt(2))
        self.G0 = 20 * np.log10(self.g0)

    def elevation(self, ang, field=True):
        """ Returns elevation normalized pattern
            :param ang: angle in radians
            :param field: return field if True, intensity if False
        """
        sin_rang = np.sin(ang - self.tilt)
        vind = np.round((sin_rang - self.pat_v[0]) / self.dv).astype(np.int)
        elcut = self.pat_fore[vind, self.ind_umid] + self.pat_aft[vind, self.ind_umid]
        xelcut = self.xpat_fore[vind, self.ind_umid] + self.xpat_aft[vind, self.ind_umid]
        return elcut, xelcut

    def azimuth(self, ang, field=True, squint_rad=None):
        """ Returns azimuth normalized pattern
            :param ang: angle in radians
            :param field: return field if True, intensity if False
            :param squint_rad: overides init squint. If it is a vector then
                               it will be combined with ang, following numpy
                               rules. So, this could be sued to calculate a
                               stack of patterns with different squints, or
                               to compute the pattern seen by a target in
                               TOPS or Spotlight mode
        """
        if squint_rad is None:
            squint = self.squint
        else:
            squint = squint_rad
        sin_ang = np.sin(ang)
        uind = np.round((sin_ang - self.pat_u[0]) / self.du).astype(np.int)
        sina_s = sin_ang - np.sin(squint)
        ph = self.k0 * self.b_at * sina_s / 2
        azcut = (self.pat_fore[self.ind_vmid, uind] * np.exp(1j * ph) +
                 self.pat_aft[self.ind_vmid, uind] * np.exp(-1j * ph))
        xazcut = (self.xpat_fore[self.ind_vmid, uind] * np.exp(1j * ph) +
                  self.xpat_aft[self.ind_vmid, uind] * np.exp(-1j * ph))
        return azcut, xazcut

    def pat_2D(self, el_ang, az_ang, field=True, grid=True, squint_rad=None):
        """ Returns normalized pattern for (elevation, azimuth)
            :param el_ang: elevation angle in radians
            :param az_ang: azimuth angle in radians
            :param field: return field if True, intensity if False
            :param squint_rad: overides init squint. If it is a vector then
                               it will be combined with ang, following numpy
                               rules. So, this could be sued to calculate a
                               stack of patterns with different squints, or
                               to compute the pattern seen by a target in
                               TOPS or Spotlight mod
        """
        sin_rang = np.sin(el_ang - self.tilt)
        vind = np.round((sin_rang - self.pat_v[0]) / self.dv).astype(np.int)
        if squint_rad is None:
            squint = self.squint
        else:
            squint = squint_rad
        sin_ang = np.sin(az_ang)
        uind = np.round((sin_ang - self.pat_u[0]) / self.du).astype(np.int)
        sina_s = sin_ang - np.sin(squint)
        ph = self.k0 * self.b_at * sina_s / 2
        if grid:
            vind = vind.reshape((vind.size, 1))
            uind = uind.reshape((1, uind.size))
            ph = ph.reshape(uind.shape)
        pat = (self.pat_fore[vind, uind] * np.exp(1j * ph) +
               self.pat_aft[vind, uind] * np.exp(-1j * ph))
        xpat = (self.xpat_fore[vind, uind] * np.exp(1j * ph) +
                self.xpat_aft[vind, uind] * np.exp(-1j * ph))
        return pat, xpat


class tasi_pattern(casa_pattern):

    def __init__(self, matfile, b_at, f0,
                 squint=0, el0=0, tilt=0, el_offset=0, az_offset=0):
        """

        :param matfile: mat file with patterns 
        :param b_at: separation between phase centers
        :param f0: center frequency
        :param squint: Azimuth pointing, in degree. Defaults to 9.
        :param el0: Elevation pointing w.r.t. boresight, in degree.
                    Defaults to 0.
        :param tilt: Mechanical tilt, in degree, defaults to 0.
        :param el_offset: an offset w.r.t. to nominal phase center in (m).
                          This causes a linear phase in elevation.
        :param az_offset: same in azimuth
        """
        self.__read_ext_pattern(matfile)
        self.squint = np.radians(squint)
        self.rel0 = np.radians(el0) - np.radians(tilt)
        self.tilt = np.radians(tilt)
        self.az_offset = az_offset
        self.el_offset = el_offset
        self.du = self.pat_u[1] - self.pat_u[0]
        self.dv = self.pat_v[1] - self.pat_v[0]
        self.f0 = f0
        self.wl = c / f0
        self.k0 = 2 * np.pi / self.wl
        self.b_at = b_at

    def __read_ext_pattern(self, file):
        pats_as_dict = readsav(file)
        self.pat_fore = drtls.lincongrid(pats_as_dict.patt_eco.astype(np.complex64),(1000,1000))
        self.pat_aft = np.fliplr(self.pat_fore).copy()
        self.xpat_fore = drtls.lincongrid(pats_as_dict.patt_ex.astype(np.complex64),(1000,1000))
        self.xpat_aft = np.fliplr(self.xpat_fore).copy()
        self.pat_u = drtls.lincongrid(pats_as_dict.ucord.astype(np.float32), (1000))
        self.pat_v = drtls.lincongrid(pats_as_dict.vcord.flatten().astype(np.float32), (1000))
        self.ind_vmid = int(self.pat_v.size / 2)
        self.ind_umid = int(self.pat_u.size / 2)
        # Normalize
        self.g0 = np.sqrt(np.nanmax(np.abs(self.pat_fore))**2 + np.nanmax(np.abs(self.pat_aft))**2)
        self.pat_fore /= (self.g0 * np.sqrt(2))
        self.pat_aft /= (self.g0 * np.sqrt(2))
        self.xpat_fore /= (self.g0 * np.sqrt(2))
        self.xpat_aft /= (self.g0 * np.sqrt(2))
        self.G0 = 20 * np.log10(self.g0)


if __name__ == '__main__':
    SESAME_dir = "/Users/plopezdekker/Documents/WORK/SESAME"
    datadir = os.path.join(SESAME_dir, 'DATA')
    patterdir = os.path.join(datadir, 'PATTERNS')
    patfile = os.path.join(os.path.join(patterdir,'CASA'), 'pattern_sesame_mom2.mat')
    patfile2 = os.path.join(os.path.join(patterdir, 'TASI'), 'FF_reflector.sav')
    casa_pat = casa_pattern(patfile, 4.5, 5.4e9)
    tasi_pat = tasi_pattern(patfile2, 4.5, 5.4e9)
    #theta, rad = np.meshgrid(theta.flatten(), phi.flatten())
