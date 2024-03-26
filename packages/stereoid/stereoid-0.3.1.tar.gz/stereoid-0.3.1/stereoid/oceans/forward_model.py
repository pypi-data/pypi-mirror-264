__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

import os

import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from scipy.ndimage.interpolation import map_coordinates as spmp

import drama.utils as drtls
from stereoid.oceans import ObsGeo


def ind_clip(ind, n):
    if type(ind) is np.ndarray:
        ind = np.where(ind > 0, ind, 0)
        ind = np.where(ind > (n - 1), n - 1, ind)
        return ind
    else:
        if ind < 0:
            return 0
        elif ind > (n - 1):
            return n - 1
        else:
            return ind


class FwdModelRIM(object):
    def __init__(
        self,
        nrcs_data,
        dop_data,
        imacs_data,
        cutoff_data,
        f_isv,
        daz=2,
        dinc=0.5,
        dspd=0.5,
        stereo=True,
        sigma_nrcs_db=0.1,
        sigma_isv=0.025e-3,
        sigma_dca=1,
        pol_hack=1,
        duvec=0.25,
        model="RIM",
        normalise_imacs=False,
    ):
        """

        :param filename:
        :param daz: Azimuth resolution of LUT
        :param dinc: Incident angle resolution of LUT
        """
        self.fwdm_type = "RIM"
        if type(nrcs_data) is xr.core.dataset.Dataset:
            # This is already a data set
            self.fwd_ds = nrcs_data
        else:
            # Assume it is a directory
            print("Input is not xarray")
            return False
        if type(dop_data) is xr.core.dataset.Dataset:
            # This is already a data set
            self.fwd_dop_ds = dop_data
        else:
            # Assume it is a directory
            print("Input is not xarray")
            return False
            
        self.fwd_imacs = imacs_data  
        self.fwd_cut_off = cutoff_data  
              
        self.stereo = stereo
        # dimensions
        # shp = self.fwd_ds.WindSpeed.values.shape

        self.wspeedv = self.fwd_ds.wind_norm.values
        self.wdirv = self.fwd_ds.wind_direction.values
        self.incv = self.fwd_ds.incidence.values
        self.wspd_min = self.wspeedv.min()
        self.wspd_step = self.wspeedv[1] - self.wspeedv[0]
        self.wdir_min = self.wdirv.min()
        self.wdir_step = self.wdirv[1] - self.wdirv[0]
        self.inc_min = self.incv.min()
        self.inc_step = self.incv[1] - self.incv[0]
        self.waveagev = self.fwd_ds.wave_age.values
        #self.at_distance_v = self.fwd_ds.at_distance.values

        # data
        # self.nrcsm = self.fwd_ds.nrcs_KAlin.values * pol_hack
        #nrcs_crt[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]
        nrcs_shp = self.fwd_ds.nrcs_S1_H.values.shape
        self.nrcsm = np.zeros((3, nrcs_shp[3], 2, nrcs_shp[2], nrcs_shp[1], nrcs_shp[0]))
        self.nrcsm[0,:, 0, :, :, :] = np.transpose(self.fwd_ds.nrcs_S1_H.values, (3, 2, 1, 0))
        self.nrcsm[0,:, 1, :, :, :] = np.transpose(self.fwd_ds.nrcs_S1_V.values, (3, 2, 1, 0))
        self.nrcsm[1,:, 0, :, :, :] = np.transpose(self.fwd_ds.nrcs_HA_m.values, (3, 2, 1, 0))
        self.nrcsm[1,:, 1, :, :, :] = np.transpose(self.fwd_ds.nrcs_HA_M.values, (3, 2, 1, 0))
        self.nrcsm[2,:, 0, :, :, :] = np.transpose(self.fwd_ds.nrcs_HB_m.values, (3, 2, 1, 0))
        self.nrcsm[2,:, 1, :, :, :] = np.transpose(self.fwd_ds.nrcs_HB_M.values, (3, 2, 1, 0))

        self.dop_wspeedv = self.fwd_dop_ds.wind_norm.values
        self.dop_wdirv = self.fwd_dop_ds.wind_direction.values
        self.dop_incv = self.fwd_dop_ds.incidence.values
        self.dop_wspd_min = self.dop_wspeedv.min()
        self.dop_wspd_step = self.dop_wspeedv[1] - self.dop_wspeedv[0]
        self.dop_wdir_min = self.dop_wdirv.min()
        self.dop_wdir_step = self.dop_wdirv[1] - self.dop_wdirv[0]
        self.dop_inc_min = self.dop_incv.min()
        self.dop_inc_step = self.dop_incv[1] - self.incv[0]
        self.dop_waveagev = self.fwd_dop_ds.wave_age.values
        dop_shp = self.fwd_dop_ds.dop_S1_H.values.shape
        self.dcam = np.zeros((3, dop_shp[3], 2, dop_shp[2], dop_shp[1], dop_shp[0]))
        self.dcam[0,:, 0, :, :, :] = np.transpose(self.fwd_dop_ds.dop_S1_H.values, (3, 2, 1, 0))
        self.dcam[0,:, 1, :, :, :] = np.transpose(self.fwd_dop_ds.dop_S1_V.values, (3, 2, 1, 0))
        self.dcam[1,:, 0, :, :, :] = np.transpose(self.fwd_dop_ds.dop_HA_m.values, (3, 2, 1, 0))
        self.dcam[1,:, 1, :, :, :] = np.transpose(self.fwd_dop_ds.dop_HA_M.values, (3, 2, 1, 0))
        self.dcam[2,:, 0, :, :, :] = np.transpose(self.fwd_dop_ds.dop_HB_m.values, (3, 2, 1, 0))
        self.dcam[2,:, 1, :, :, :] = np.transpose(self.fwd_dop_ds.dop_HB_M.values, (3, 2, 1, 0))
        # self.dca_stdm = np.array(self.ncfile.variables["DCA_stdev"])
        # FIXME: since this is absent I just make it up, assuming 1 m/s std
        self.dca_stdm = np.zeros_like(self.dcam) + 2 / 0.054

        self.imacs_wspeedv = self.fwd_imacs.wind_norm.values
        self.imacs_wdirv = self.fwd_imacs.wind_direction.values
        self.imacs_incv = self.fwd_imacs.incidence.values
        self.imacs_wspd_min = self.imacs_wspeedv.min()
        self.imacs_wspd_step = self.imacs_wspeedv[1] - self.imacs_wspeedv[0]
        self.imacs_wdir_min = self.imacs_wdirv.min()
        self.imacs_wdir_step = self.imacs_wdirv[1] - self.imacs_wdirv[0]
        self.imacs_inc_min = self.imacs_incv.min()
        self.imacs_inc_step = self.imacs_incv[1] - self.incv[0]
        self.imacs_waveagev = self.fwd_imacs.wave_age.values
        imacs_shp = self.fwd_imacs.imag_macs_S1_H.values.shape
        self.imacsm = np.zeros((3, imacs_shp[3], 2, imacs_shp[2], imacs_shp[1], imacs_shp[0]))
        if normalise_imacs == False:
            self.imacsm[0,:, 0, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_S1_H.values, (3, 2, 1, 0))
            self.imacsm[0,:, 1, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_S1_V.values, (3, 2, 1, 0))
            self.imacsm[1,:, 0, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HA_m.values, (3, 2, 1, 0))
            self.imacsm[1,:, 1, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HA_M.values, (3, 2, 1, 0))
            self.imacsm[2,:, 0, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HB_m.values, (3, 2, 1, 0))
            self.imacsm[2,:, 1, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HB_M.values, (3, 2, 1, 0))
        else:
            self.imacsm[0, :, 0, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_S1_H.values/self.fwd_imacs.imag_macs_S1_H.values, (3, 2, 1, 0))
            self.imacsm[0, :, 1, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_S1_V.values/self.fwd_imacs.imag_macs_S1_V.values, (3, 2, 1, 0))
            self.imacsm[1, :, 0, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HA_m.values/self.fwd_imacs.imag_macs_HA_m.values, (3, 2, 1, 0))
            self.imacsm[1, :, 1, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HA_M.values/self.fwd_imacs.imag_macs_HA_M.values, (3, 2, 1, 0))
            self.imacsm[2, :, 0, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HB_m.values/self.fwd_imacs.imag_macs_HB_m.values, (3, 2, 1, 0))
            self.imacsm[2, :, 1, :, :, :] = np.transpose(self.fwd_imacs.imag_macs_HB_M.values/self.fwd_imacs.imag_macs_HB_M.values, (3, 2, 1, 0))

        self.cut_off_wspeedv = self.fwd_cut_off.wind_norm.values
        self.cut_off_wdirv = self.fwd_cut_off.wind_direction.values
        self.cut_off_incv = self.fwd_cut_off.incidence.values
        self.cut_off_wspd_min = self.cut_off_wspeedv.min()
        self.cut_off_wspd_step = self.cut_off_wspeedv[1] - self.cut_off_wspeedv[0]
        self.cut_off_wdir_min = self.cut_off_wdirv.min()
        self.cut_off_wdir_step = self.cut_off_wdirv[1] - self.cut_off_wdirv[0]
        self.cut_off_inc_min = self.cut_off_incv.min()
        self.cut_off_inc_step = self.cut_off_incv[1] - self.incv[0]
        self.cut_off_waveagev = self.fwd_cut_off.wave_age.values
        cut_off_shp = self.fwd_cut_off.cut_off_S1_H.values.shape
        self.cutoffm = np.zeros((3, cut_off_shp[3], 2, cut_off_shp[2], cut_off_shp[1], cut_off_shp[0]))
        self.cutoffm[0,:, 0, :, :, :] = np.transpose(self.fwd_cut_off.cut_off_S1_H.values, (3, 2, 1, 0))
        self.cutoffm[0,:, 1, :, :, :] = np.transpose(self.fwd_cut_off.cut_off_S1_V.values, (3, 2, 1, 0))
        self.cutoffm[1,:, 0, :, :, :] = np.transpose(self.fwd_cut_off.cut_off_HA_m.values, (3, 2, 1, 0))
        self.cutoffm[1,:, 1, :, :, :] = np.transpose(self.fwd_cut_off.cut_off_HA_M.values, (3, 2, 1, 0))
        self.cutoffm[2,:, 0, :, :, :] = np.transpose(self.fwd_cut_off.cut_off_HB_m.values, (3, 2, 1, 0))
        self.cutoffm[2,:, 1, :, :, :] = np.transpose(self.fwd_cut_off.cut_off_HB_M.values, (3, 2, 1, 0))

        # Geophysical noise model
        self.sigma_nrcs_db = sigma_nrcs_db
        self.sigma_isv = sigma_isv
        self.sigma_dca = sigma_dca
        # Make cartesian
        self.wcrt_step = duvec
        self.__lut_pol2cart(dinc, order=3)
        # Resample
        self.__lut_resample(daz, dinc, dspd)
        # Init isv
        #self.__init_isv(f_isv, daz, dinc, dspd)
        #self.__isv_lut_pol2cart(dinc, order=3)
        #self.__isv_lut_resample(daz, dinc, dspd)
        # Set inc to smallest in LUT
        self.inc = 0
        # Set wave age to the mean value in LUT
        self.waveage = self.waveagev.mean()
        #self.at_distance = 300e3
        self.at_distance_c1_ind = 1
        self.at_distance_c2_ind = 2
        self.monostatic_ind = 0

    def __init_isv(self, f_isv, daz, dinc, dspd):
        self.ncisv = Dataset(f_isv)
        # dimensions
        # shp = self.ncfile.variables["windspeed"].shape
        self.isv_wspeedv = np.array(self.ncisv.variables["windspeed"])
        self.isv_wdirv = np.array(self.ncisv.variables["winddirection"])
        self.isv_incv = np.array(self.ncisv.variables["incangle"])
        self.isv_wspd_min = self.isv_wspeedv.min()
        self.isv_wspd_step = self.isv_wspeedv[1] - self.isv_wspeedv[0]
        self.isv_wdir_min = self.isv_wdirv.min()
        self.isv_wdir_step = self.isv_wdirv[1] - self.isv_wdirv[0]
        self.isv_inc_min = self.isv_incv.min()
        self.isv_inc_step = self.isv_incv[1] - self.isv_incv[0]
        self.isv_waveagev = np.array(self.ncisv.variables["waveage"])

        # data
        # FIXME: here I assume that there is only one element in first dimension
        self.isv_im = np.transpose(
            np.array(self.ncisv.variables["isvIm"])[0], (0, 1, 4, 2, 3)
        )
        self.isv_re = np.transpose(
            np.array(self.ncisv.variables["isvRe"])[0], (0, 1, 4, 2, 3)
        )

    def __lut_pol2cart(self, dinc, order=3):
        u_max = self.wspeedv.max()
        nu = int(2 * np.ceil(u_max / self.wcrt_step))
        self.w_u = np.linspace(-u_max, u_max, nu)
        self.w_v = self.w_u.copy()
        # "x" and "y" are numpy arrays with the desired cartesian coordinates
        # we make a meshgrid with them
        ug, vg = np.meshgrid(self.w_u, self.w_v)

        # Now that we have the ug and vg coordinates of each point in the output plane
        # we can calculate their corresponding theta and range
        wdir = np.degrees(np.arctan2(vg, ug)).ravel()
        wspd = (np.sqrt(vg ** 2 + ug ** 2)).ravel()

        # Negative angles are corrected
        wdir[wdir < 0] = 360 + wdir[wdir < 0]

        # Using the known theta and range steps, the coordinates are mapped to
        # those of the data grid
        nrcs_wdir = wdir / self.wdir_step + 2
        nrcs_wspd = (wspd - self.wspd_min) / self.wspd_step
        dop_wdir = wdir / self.dop_wdir_step + 2
        dop_wspd = (wspd - self.dop_wspd_min) / self.dop_wspd_step
        imacs_wdir = wdir / self.imacs_wdir_step + 2
        imacs_wspd = (wspd - self.imacs_wspd_min) / self.imacs_wspd_step
        cut_off_wdir = wdir / self.cut_off_wdir_step + 2
        cut_off_wspd = (wspd - self.cut_off_wspd_min) / self.cut_off_wspd_step



        # An array of polar coordinates is created stacking the previous arrays
        nrcs_coords = np.vstack((nrcs_wdir, nrcs_wspd))
        dop_coords = np.vstack((dop_wdir, dop_wspd))
        imacs_coords = np.vstack((nrcs_wdir, imacs_wspd))
        cut_off_coords = np.vstack((cut_off_wdir, cut_off_wspd))
        
        shpin = self.nrcsm.shape
        shpout = (shpin[0], shpin[1], shpin[2], shpin[3], nu, nu)
        self.nrcs_crt = np.zeros(shpout)
        self.dca_crt = np.zeros(shpout)
        self.imacs_crt = np.zeros(shpout)
        self.cut_off_crt = np.zeros(shpout)
        
        for i0 in range(shpin[0]):
            for i1 in range(shpin[1]):
                for i2 in range(shpin[2]):
                    for i3 in range(shpin[3]):
                        # To avoid holes in the 360º - 0º boundary, the last column of the data
                        # copied in the begining
                        polar_nrcs = np.vstack(
                            (
                                self.nrcsm[i0, i1, i2, i3, -3:-1, :],
                                self.nrcsm[i0, i1, i2, i3, :, :],
                                self.nrcsm[i0, i1, i2, i3, 1:3, :],
                            )
                        )
                        tmp = spmp(
                            polar_nrcs,
                            nrcs_coords,
                            order=order,
                            mode="constant",
                            cval=np.nan,
                        )
                        self.nrcs_crt[i0, i1, i2, i3, :, :] = tmp.reshape((nu, nu))
                        polar_dca = np.vstack(
                            (
                                self.dcam[i0, i1, i2, i3, -3:-1, :],
                                self.dcam[i0, i1, i2, i3, :, :],
                                self.dcam[i0, i1, i2, i3, 1:3, :],
                            )
                        )
                        tmp = spmp(
                            polar_dca, dop_coords, order=order, mode="constant", cval=np.nan
                        )
                        self.dca_crt[i0, i1, i2, i3, :, :] = tmp.reshape((nu, nu))
                        polar_imacs = np.vstack(
                            (
                                self.imacsm[i0, i1, i2, i3, -3:-1, :],
                                self.imacsm[i0, i1, i2, i3, :, :],
                                self.imacsm[i0, i1, i2, i3, 1:3, :],
                            )
                        )
                        tmp = spmp(
                            polar_imacs, imacs_coords, order=order, mode="constant", cval=np.nan
                        )
                        self.imacs_crt[i0, i1, i2, i3, :, :] = tmp.reshape((nu, nu))
                        polar_cut_off = np.vstack(
                            (
                                self.cutoffm[i0, i1, i2, i3, -3:-1, :],
                                self.cutoffm[i0, i1, i2, i3, :, :],
                                self.cutoffm[i0, i1, i2, i3, 1:3, :],
                            )
                        )
                        tmp = spmp(
                            polar_cut_off, cut_off_coords, order=order, mode="constant", cval=np.nan
                        )
                        self.cut_off_crt[i0, i1, i2, i3, :, :] = tmp.reshape((nu, nu))
                        
        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.incv[0]) / self.inc_step
        self.nrcs_crt = drtls.linresample(self.nrcs_crt, indout, axis=3)
        self.dca_crt = drtls.linresample(self.dca_crt, indout, axis=3)
        self.imacs_crt = drtls.linresample(self.imacs_crt, indout, axis=3)
        self.cut_off_crt = drtls.linresample(self.cut_off_crt, indout, axis=3)
        # self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=3)

    def __isv_lut_pol2cart(self, dinc, order=3):
        u_max = self.wspeedv.max()
        nu = int(2 * np.ceil(u_max / self.wcrt_step))
        # self.w_u = np.linspace(-u_max, u_max, nu)
        # self.w_v = self.w_u.copy()
        # "x" and "y" are numpy arrays with the desired cartesian coordinates
        # we make a meshgrid with them
        ug, vg = np.meshgrid(self.w_u, self.w_v)

        # Now that we have the ug and vg coordinates of each point in the output plane
        # we can calculate their corresponding theta and range
        wdir = np.degrees(np.arctan2(vg, ug)).ravel()
        wspd = (np.sqrt(vg ** 2 + ug ** 2)).ravel()

        # Negative angles are corrected
        wdir[wdir < 0] = 360 + wdir[wdir < 0]

        # Using the known theta and range steps, the coordinates are mapped to
        # those of the data grid
        wdir = wdir / self.isv_wdir_step + 2
        wspd = (wspd - self.isv_wspd_min) / self.isv_wspd_step

        # An array of polar coordinates is created stacking the previous arrays
        coords = np.vstack((wdir, wspd))
        shpin = self.isv_im.shape
        shpout = (shpin[0], shpin[1], shpin[2], nu, nu)
        self.isv_re_crt = np.zeros(shpout)
        self.isv_im_crt = np.zeros(shpout)
        for i0 in range(shpin[0]):
            for i1 in range(shpin[1]):
                for i2 in range(shpin[2]):
                    # To avoid holes in the 360º - 0º boundary, the last column of the data
                    # copied in the begining
                    polar_isvr = np.vstack(
                        (
                            self.isv_re[i0, i1, i2, -3:-1, :],
                            self.isv_re[i0, i1, i2, :, :],
                            self.isv_re[i0, i1, i2, 1:4, :],
                        )
                    )
                    tmp = spmp(
                        polar_isvr, coords, order=order, mode="constant", cval=np.nan
                    )
                    self.isv_re_crt[i0, i1, i2, :, :] = tmp.reshape((nu, nu))
                    polar_isvi = np.vstack(
                        (
                            self.isv_im[i0, i1, i2, -3:-1, :],
                            self.isv_im[i0, i1, i2, :, :],
                            self.isv_im[i0, i1, i2, 1:4, :],
                        )
                    )
                    tmp = spmp(
                        polar_isvi, coords, order=order, mode="constant", cval=np.nan
                    )
                    self.isv_im_crt[i0, i1, i2, :, :] = tmp.reshape((nu, nu))
        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.isv_incv[0]) / self.isv_inc_step
        self.isv_im_crt = drtls.linresample(
            self.isv_im_crt, indout, axis=2, circular=False, extrapolate=True
        )
        self.isv_re_crt = drtls.linresample(
            self.isv_re_crt, indout, axis=2, circular=False, extrapolate=True
        )

    def __lut_resample(self, daz, dinc, dspd):
        """
        Upsample LUT in winddir, windspd and inc dimensions.

        :param data:
        :param daz: azimuth resolution
        :return:
        """
        naz = int(np.floor(360 / daz))
        daz = 360 / naz
        nwdirv = np.arange(naz) * daz
        indout = nwdirv / self.wdir_step
        indout_dop = nwdirv / self.dop_wdir_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=4, circular=True)
        self.dcam = drtls.linresample(self.dcam, indout_dop, axis=4, circular=True)
        # self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=2, circular=True)
        self.wdirv = nwdirv
        self.wdir_step = daz

        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.incv[0]) / self.inc_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=3)
        self.dcam = drtls.linresample(self.dcam, indout, axis=3)
        self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=3)
        self.incv = nincv
        self.inc_step = dinc

        # Wind vector interpolation
        nspd = int(np.ceil((self.wspeedv.max() - self.wspeedv.min()) / dspd))
        nwspeedv = np.linspace(self.wspeedv.min(), self.wspeedv.max(), nspd + 1)
        dwspeed = nwspeedv[1] - nwspeedv[0]
        indout = (nwspeedv - self.wspeedv[0]) / self.wspd_step
        dop_indout = (nwspeedv - self.dop_wspeedv[0]) / self.dop_wspd_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=5)
        self.dcam = drtls.linresample(self.dcam, dop_indout, axis=5)
        self.dca_stdm = drtls.linresample(self.dca_stdm, dop_indout, axis=5)
        self.wspeedv = nwspeedv
        self.wspd_step = dwspeed

    def __isv_lut_resample(self, daz, dinc, dspd):
        """
        Upsample LUT in winddir, windspd and inc dimensions.

        :param data:
        :param daz: azimuth resolution
        :return:
        """
        naz = int(np.floor(360 / daz))
        daz = 360 / naz
        nwdirv = np.arange(naz) * daz
        indout = nwdirv / self.isv_wdir_step
        self.isv_im = drtls.linresample(self.isv_im, indout, axis=3, circular=True)
        self.isv_re = drtls.linresample(self.isv_re, indout, axis=3, circular=True)
        self.isv_wdirv = nwdirv
        self.isv_wdir_step = daz

        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.isv_incv[0]) / self.isv_inc_step
        self.isv_im = drtls.linresample(
            self.isv_im, indout, axis=2, circular=False, extrapolate=True
        )
        self.isv_re = drtls.linresample(
            self.isv_re, indout, axis=2, circular=False, extrapolate=True
        )
        self.isv_incv = nincv
        self.isv_inc_step = dinc

        # Wind vector interpolation
        nspd = int(np.ceil((self.wspeedv.max() - self.wspeedv.min()) / dspd))
        nwspeedv = np.linspace(self.wspeedv.min(), self.wspeedv.max(), nspd + 1)
        dwspeed = nwspeedv[1] - nwspeedv[0]
        indout = (nwspeedv - self.isv_wspeedv[0]) / self.isv_wspd_step
        self.isv_im = drtls.linresample(
            self.isv_im, indout, axis=4, circular=False, extrapolate=True
        )
        self.isv_re = drtls.linresample(
            self.isv_re, indout, axis=4, circular=False, extrapolate=True
        )
        self.isv_wspeedv = nwspeedv
        self.isv_wspd_step = dwspeed

    # @property
    # def at_distance(self):
    #     if self.stereo:
    #         return (self.__at_distance_c1, self.__at_distance_c2)
    #     else:
    #         return self.__at_distance_c1
    #
    # @at_distance.setter
    # def at_distance(self, at_distance):
    #     if type(at_distance) in [list, tuple]:
    #         self.at_distance_c1_ind = np.argmin(
    #             np.abs(np.abs(at_distance[0]) / 1e3 - self.at_distance_v)
    #         )
    #         self.at_distance_c2_ind = np.argmin(
    #             np.abs(-np.abs(at_distance[1]) / 1e3 - self.at_distance_v)
    #         )
    #     else:
    #         self.at_distance_c1_ind = np.argmin(
    #             np.abs(np.abs(at_distance) / 1e3 - self.at_distance_v)
    #         )
    #         self.at_distance_c2_ind = np.argmin(
    #             np.abs(-np.abs(at_distance) / 1e3 - self.at_distance_v)
    #         )
    #     self.monostatic_ind = np.argmin(np.abs(self.at_distance_v))
    #     self.__at_distance_c1 = self.at_distance_v[self.at_distance_c1_ind] * 1e3
    #     self.__at_distance_c2 = self.at_distance_v[self.at_distance_c2_ind] * 1e3

    @property
    def inc(self):
        return self.__inc

    @inc.setter
    def inc(self, inc):
        self.__inc = inc
        self.inc_ind = np.abs(self.incv - inc).argmin()

    @property
    def waveage(self):
        return self.__waveage

    @waveage.setter
    def waveage(self, waveage):
        self.__waveage = waveage
        self.waveage_ind = np.abs(self.waveagev - waveage).argmin()
        #self.isv_waveage_ind = np.abs(self.isv_waveagev - waveage).argmin()

    def nrcs_lut(self, pol_ind, cart=False):
        """Return NRCS LUT for polarization indicated.

        The waveage, along-track separation and incident angle already set.

        Parameters
        ----------
        pol_ind : type
            Description of parameter `pol_ind`.
        cart : type
            Description of parameter `cart`.

        Returns
        -------
        type
            Description of returned object.

        """
        if cart:
            nrcs = self.nrcs_crt[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]

        else:
            nrcs = self.nrcsm[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]
        if self.stereo:
            return nrcs
        else:
            return nrcs[0:2]

    def dca_lut(self, pol_ind, cart=False):
        """Return DCA LUT for polarization indicated.

        The waveage, along-track separation and incident angle already set.

        Parameters
        ----------
        pol_ind : type
            Description of parameter `pol_ind`.
        cart : type
            Description of parameter `cart`.

        Returns
        -------
        type
            Description of returned object.
        """
        if cart:
            dca = self.dca_crt[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]
        else:
            dca = self.dcam[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]
        if self.stereo:
            return dca
        else:
            return dca[0:2]

    def isv_im_lut(self, pol_ind, cart=False):
        if cart:
            return self.isv_im_crt[self.waveage_ind, pol_ind, self.inc_ind, :, :]
        else:
            return self.isv_im[self.waveage_ind, pol_ind, self.inc_ind, :, :]

    def isv_re_lut(self, pol_ind, cart=False):
        if cart:
            return self.isv_re_crt[self.waveage_ind, pol_ind, self.inc_ind, :, :]
        else:
            return self.isv_re[self.waveage_ind, pol_ind, self.inc_ind, :, :]

    def nrcs_dca(self, pol_ind, wspd, wdir, inc, sat="mono"):
        """
        :param pol_ind:
        :param wspd:
        :param wdir:
        :param inc:
        :return:
        """
        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        inc_ind = ind_clip(
            np.round((inc - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )

        wdir_ind = np.mod(
            np.round((wdir - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        if sat == "cs1":
            at_ind = self.at_distance_c1_ind
        elif sat == "cs2":
            at_ind = self.at_distance_c2_ind
        else:
            at_ind = self.monostatic_ind

        nrcs_o = self.nrcsm[
            at_ind, self.waveage_ind, pol_ind, inc_ind, wdir_ind, wspd_ind
        ]
        dca_o = self.dcam[
            at_ind, self.waveage_ind, pol_ind, inc_ind, wdir_ind, wspd_ind
        ]
        # dca_std_o = self.dca_stdm[self.monostatic_ind, :, self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        return nrcs_o, dca_o  # , dca_std_o

    def isv_bist(self, pol_ind, wspd, wdir0, inc1, inc2, bist_ang_az):
        """
        :param pol_ind: 0 is VV and 1 is HH, for now
        :param wspd:
        :param wdir0: wind direction w.r.t. to nonostatic reference
        :param inc1: Reference, monostatic incident angle
        :param inc2: receive incident angle
        :param bist_ang_az: azimuth bistatic angle
        :return:
        """
        # We assume equivalent incident angle is the mean
        inc = (inc1 + inc2) / 2
        # We assume that things are as if we where looking monostatically from a slightly different direction
        wdir = wdir0 - bist_ang_az / 2
        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        inc_ind = ind_clip(
            np.round((inc - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )

        wdir_ind = np.mod(
            np.round((wdir - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )

        isv_re_o = self.isv_re[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        isv_im_o = self.isv_im[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        return isv_re_o, isv_im_o

    def fwd(self, pol_ind, wspd, wdir0, incm, incb, bist_ang_az):
        incbeq = (incm + incb) / 2
        # wdirb1 = np.mod(wdir0 + bist_ang_az/2, 360)
        # wdirb2 = np.mod(wdir0 - bist_ang_az/2, 360)
        wdir0 = np.mod(wdir0, 360)
        # In this case the LUT already considers the bistatic angle
        wdirb1 = wdir0
        wdirb2 = wdir0

        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        incm_ind = ind_clip(
            np.round((incm - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        incb_ind = ind_clip(
            np.round((incbeq - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        wdir0_ind = np.mod(
            np.round((wdir0 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        wdirb1_ind = np.mod(
            np.round((wdirb1 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        wdirb2_ind = np.mod(
            np.round((wdirb2 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        nrcs_o = [
            self.nrcsm[
                0,
                self.waveage_ind,
                pol_ind,
                wdir0_ind,
                wspd_ind,
                incm_ind,
            ]
        ]
        nrcs_o.append(
            self.nrcsm[
                1,
                self.waveage_ind,
                pol_ind,
                wdir0_ind,
                wspd_ind,
                incm_ind,
            ]
        )
        dca_o = [
            self.dcam[
                0,
                self.waveage_ind,
                pol_ind,
                wdir0_ind,
                wspd_ind,
                incm_ind,
            ]
        ]
        dca_o.append(
            self.dcam[
                1,
                self.waveage_ind,
                pol_ind,
                wdirb1_ind,
                wspd_ind,
                incm_ind,
            ]
        )
        # isv_im_o = [
        #     self.isv_im[self.isv_waveage_ind, pol_ind, wdir0_ind, wspd_ind, incm_ind]
        # ]
        # isv_im_o.append(
        #     self.isv_im[self.isv_waveage_ind, pol_ind, wdirb1_ind, wspd_ind, incb_ind]
        # )
        if self.stereo:
            nrcs_o.append(
                self.nrcsm[
                    2,
                    self.waveage_ind,
                    pol_ind,
                    wdirb2_ind,
                    wspd_ind,
                    incm_ind,
                ]
            )
            dca_o.append(
                self.dcam[
                    2,
                    self.waveage_ind,
                    pol_ind,
                    wdirb2_ind,
                    wspd_ind,
                    incm_ind,
                ]
            )
            # isv_im_o.append(
            #     self.isv_im[
            #         self.isv_waveage_ind, pol_ind, wdirb2_ind, wspd_ind, incb_ind
            #     ]
            # )
        return (
            np.stack(nrcs_o, axis=-1),
            np.stack(dca_o, axis=-1),
            False,
        )

    def fwd_jacobian(self, incm):
        """Compute jacobian of fwd model for given monostatic incident angle.

        Parameters
        ----------
        incm : type
            Incident angle.

        Returns
        -------
        type
            Description of returned object.

        """
        incm_ind = ind_clip(
            np.round((incm - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        nrcs = self.nrcs_crt[:, self.waveage_ind, :, incm_ind, :, :]
        if self.stereo:
            nrcs = nrcs
        else:
            nrcs = nrcs[0:2]
        dca = self.dca_crt[:, self.waveage_ind, :, incm_ind, :, :]
        if self.stereo:
            dca = dca
        else:
            dca = dca[0:2]
        shpin = nrcs.shape
        shpout = (shpin[0], shpin[1], 2, shpin[2], shpin[3])
        jcn = np.zeros(shpout)
        jcd = np.zeros(shpout)
        jcn[:, :, 0, :, :], jcn[:, :, 1, :, :] = np.gradient(
            nrcs, self.wcrt_step, axis=(3, 2)  # self.wcrt_step,
        )
        jcd[:, :, 0, :, :], jcd[:, :, 1, :, :] = np.gradient(
            dca, self.wcrt_step, axis=(3, 2)  # self.wcrt_step,
        )
        return jcn, jcd

    def fwd_crt(self, pol_ind, u, v, incm, incb, bist_ang_az, what="nrcs"):
        """Short summary.

        Parameters
        ----------
        pol_ind : type
            Description of parameter `pol_ind`.
        u : type
            Description of parameter `u`.
        v : type
            Description of parameter `v`.
        incm : type
            Description of parameter `incm`.
        incb : type
            Description of parameter `incb`.
        bist_ang_az : type
            Description of parameter `bist_ang_az`.
        what : type
            this can be 'nrcs', 'dca', 'isv_im'. It will fall back to 'nrcs'

        Returns
        -------
        type
            Description of returned object.

        """
        du = self.w_u[1] - self.w_u[0]
        dv = self.w_v[1] - self.w_v[0]
        um = self.w_u[0]
        vm = self.w_v[0]
        u_ind = (np.round((u - um) / du)).astype(np.int)
        v_ind = (np.round((v - vm) / dv)).astype(np.int)
        incm_ind = ind_clip(
            np.round((incm - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        if what.lower() == "dca":
            data = self.dca_crt
        elif what.lower() == "isv_im":
            data = self.isv_im_crt
        elif what.lower() == "isv_re":
            data = self.isv_re_crt
        elif what.lower() == "imacs":
            data = self.imacs_crt
        elif what.lower() == "cut_off":
            data = self.cut_off_crt
        else:
            data = self.nrcs_crt

        data_o = [
            data[0, self.waveage_ind, pol_ind, incm_ind, v_ind, u_ind]
        ]
        data_o.append(
            data[
                1,
                self.waveage_ind,
                pol_ind,
                incm_ind,
                v_ind,
                u_ind,
            ]
        )

        if self.stereo:
            data_o.append(
                data[
                    2,
                    self.waveage_ind,
                    pol_ind,
                    incm_ind,
                    v_ind,
                    u_ind,
                ]
            )

        return np.stack(data_o, axis=-1)




class FwdModel(object):
    def __init__(
        self,
        nrcs_dop_data,
        f_isv,
        daz=2,
        dinc=0.5,
        dspd=0.5,
        stereo=True,
        sigma_nrcs_db=0.1,
        sigma_isv=0.025e-3,
        sigma_dca=1,
        pol_hack=1,
        duvec=0.25,
        model="KAlin",
    ):
        """

        :param filename:
        :param daz: Azimuth resolution of LUT
        :param dinc: Incident angle resolution of LUT
        """
        self.fwdm_type = model
        if type(nrcs_dop_data) is xr.core.dataset.Dataset:
            # This is already a data set
            self.fwd_ds = nrcs_dop_data
        else:
            # Assume it is a directory
            from stereoid.oceans.read_fwd import merge_luts

            self.fwd_ds = merge_luts(nrcs_dop_data, model=model)
        self.stereo = stereo
        # dimensions
        # shp = self.fwd_ds.WindSpeed.values.shape

        self.wspeedv = self.fwd_ds.wind_sp.values
        self.wdirv = self.fwd_ds.wind_dr.values
        self.incv = self.fwd_ds.inc_Tx.values
        self.wspd_min = self.wspeedv.min()
        self.wspd_step = self.wspeedv[1] - self.wspeedv[0]
        self.wdir_min = self.wdirv.min()
        self.wdir_step = self.wdirv[1] - self.wdirv[0]
        self.inc_min = self.incv.min()
        self.inc_step = self.incv[1] - self.incv[0]
        self.waveagev = self.fwd_ds.iwa.values
        self.at_distance_v = self.fwd_ds.at_distance.values

        # data
        # self.nrcsm = self.fwd_ds.nrcs_KAlin.values * pol_hack
        self.nrcsm = getattr(self.fwd_ds, "nrcs_%s" % model).values
        # self.dcam = self.fwd_ds.mean_doppler_KAlin.values
        self.dcam = getattr(self.fwd_ds, "mean_doppler_%s" % model).values
        # self.dca_stdm = np.array(self.ncfile.variables["DCA_stdev"])
        # FIXME: since this is absent I just make it up, assuming 1 m/s std
        self.dca_stdm = np.zeros_like(self.dcam) + 2 / 0.054

        # Geophysical noise model
        self.sigma_nrcs_db = sigma_nrcs_db
        self.sigma_isv = sigma_isv
        self.sigma_dca = sigma_dca
        # Make cartesian
        self.wcrt_step = duvec
        self.__lut_pol2cart(dinc, order=3)
        # Resample
        self.__lut_resample(daz, dinc, dspd)
        # Init isv
        self.__init_isv(f_isv, daz, dinc, dspd)
        self.__isv_lut_pol2cart(dinc, order=3)
        self.__isv_lut_resample(daz, dinc, dspd)
        # Set inc to smallest in LUT
        self.inc = 0
        # Set wave age to the mean value in LUT
        self.waveage = self.waveagev.mean()
        self.at_distance = 300e3

    def __init_isv(self, f_isv, daz, dinc, dspd):
        self.ncisv = Dataset(f_isv)
        # dimensions
        # shp = self.ncfile.variables["windspeed"].shape
        self.isv_wspeedv = np.array(self.ncisv.variables["windspeed"])
        self.isv_wdirv = np.array(self.ncisv.variables["winddirection"])
        self.isv_incv = np.array(self.ncisv.variables["incangle"])
        self.isv_wspd_min = self.isv_wspeedv.min()
        self.isv_wspd_step = self.isv_wspeedv[1] - self.isv_wspeedv[0]
        self.isv_wdir_min = self.isv_wdirv.min()
        self.isv_wdir_step = self.isv_wdirv[1] - self.isv_wdirv[0]
        self.isv_inc_min = self.isv_incv.min()
        self.isv_inc_step = self.isv_incv[1] - self.isv_incv[0]
        self.isv_waveagev = np.array(self.ncisv.variables["waveage"])

        # data
        # FIXME: here I assume that there is only one element in first dimension
        self.isv_im = np.transpose(
            np.array(self.ncisv.variables["isvIm"])[0], (0, 1, 4, 2, 3)
        )
        self.isv_re = np.transpose(
            np.array(self.ncisv.variables["isvRe"])[0], (0, 1, 4, 2, 3)
        )

    def __lut_pol2cart(self, dinc, order=3):
        u_max = self.wspeedv.max()
        nu = int(2 * np.ceil(u_max / self.wcrt_step))
        self.w_u = np.linspace(-u_max, u_max, nu)
        self.w_v = self.w_u.copy()
        # "x" and "y" are numpy arrays with the desired cartesian coordinates
        # we make a meshgrid with them
        ug, vg = np.meshgrid(self.w_u, self.w_v)

        # Now that we have the ug and vg coordinates of each point in the output plane
        # we can calculate their corresponding theta and range
        wdir = np.degrees(np.arctan2(vg, ug)).ravel()
        wspd = (np.sqrt(vg ** 2 + ug ** 2)).ravel()

        # Negative angles are corrected
        wdir[wdir < 0] = 360 + wdir[wdir < 0]

        # Using the known theta and range steps, the coordinates are mapped to
        # those of the data grid
        wdir = wdir / self.wdir_step + 2
        wspd = (wspd - self.wspd_min) / self.wspd_step

        # An array of polar coordinates is created stacking the previous arrays
        coords = np.vstack((wdir, wspd))
        shpin = self.nrcsm.shape
        shpout = (shpin[0], shpin[1], shpin[2], shpin[3], nu, nu)
        self.nrcs_crt = np.zeros(shpout)
        self.dca_crt = np.zeros(shpout)
        for i0 in range(shpin[0]):
            for i1 in range(shpin[1]):
                for i2 in range(shpin[2]):
                    for i3 in range(shpin[3]):
                        # To avoid holes in the 360º - 0º boundary, the last column of the data
                        # copied in the begining
                        polar_nrcs = np.vstack(
                            (
                                self.nrcsm[i0, i1, i2, i3, -2:, :],
                                self.nrcsm[i0, i1, i2, i3, :, :],
                                self.nrcsm[i0, i1, i2, i3, 0:3, :],
                            )
                        )
                        tmp = spmp(
                            polar_nrcs,
                            coords,
                            order=order,
                            mode="constant",
                            cval=np.nan,
                        )
                        self.nrcs_crt[i0, i1, i2, i3, :, :] = tmp.reshape((nu, nu))
                        polar_dca = np.vstack(
                            (
                                self.dcam[i0, i1, i2, i3, -2:, :],
                                self.dcam[i0, i1, i2, i3, :, :],
                                self.dcam[i0, i1, i2, i3, 0:3, :],
                            )
                        )
                        tmp = spmp(
                            polar_dca, coords, order=order, mode="constant", cval=np.nan
                        )
                        self.dca_crt[i0, i1, i2, i3, :, :] = tmp.reshape((nu, nu))
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.incv[0]) / self.inc_step
        self.nrcs_crt = drtls.linresample(self.nrcs_crt, indout, axis=3)
        self.dca_crt = drtls.linresample(self.dca_crt, indout, axis=3)
        # self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=3)

    def __isv_lut_pol2cart(self, dinc, order=3):
        u_max = self.wspeedv.max()
        nu = int(2 * np.ceil(u_max / self.wcrt_step))
        # self.w_u = np.linspace(-u_max, u_max, nu)
        # self.w_v = self.w_u.copy()
        # "x" and "y" are numpy arrays with the desired cartesian coordinates
        # we make a meshgrid with them
        ug, vg = np.meshgrid(self.w_u, self.w_v)

        # Now that we have the ug and vg coordinates of each point in the output plane
        # we can calculate their corresponding theta and range
        wdir = np.degrees(np.arctan2(vg, ug)).ravel()
        wspd = (np.sqrt(vg ** 2 + ug ** 2)).ravel()

        # Negative angles are corrected
        wdir[wdir < 0] = 360 + wdir[wdir < 0]

        # Using the known theta and range steps, the coordinates are mapped to
        # those of the data grid
        wdir = wdir / self.isv_wdir_step + 2
        wspd = (wspd - self.isv_wspd_min) / self.isv_wspd_step

        # An array of polar coordinates is created stacking the previous arrays
        coords = np.vstack((wdir, wspd))
        shpin = self.isv_im.shape
        shpout = (shpin[0], shpin[1], shpin[2], nu, nu)
        self.isv_re_crt = np.zeros(shpout)
        self.isv_im_crt = np.zeros(shpout)
        for i0 in range(shpin[0]):
            for i1 in range(shpin[1]):
                for i2 in range(shpin[2]):
                    # To avoid holes in the 360º - 0º boundary, the last column of the data
                    # copied in the begining
                    polar_isvr = np.vstack(
                        (
                            self.isv_re[i0, i1, i2, -2:, :],
                            self.isv_re[i0, i1, i2, :, :],
                            self.isv_re[i0, i1, i2, 0:3, :],
                        )
                    )
                    tmp = spmp(
                        polar_isvr, coords, order=order, mode="constant", cval=np.nan
                    )
                    self.isv_re_crt[i0, i1, i2, :, :] = tmp.reshape((nu, nu))
                    polar_isvi = np.vstack(
                        (
                            self.isv_im[i0, i1, i2, -2:, :],
                            self.isv_im[i0, i1, i2, :, :],
                            self.isv_im[i0, i1, i2, 0:3, :],
                        )
                    )
                    tmp = spmp(
                        polar_isvi, coords, order=order, mode="constant", cval=np.nan
                    )
                    self.isv_im_crt[i0, i1, i2, :, :] = tmp.reshape((nu, nu))
        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.isv_incv[0]) / self.isv_inc_step
        self.isv_im_crt = drtls.linresample(
            self.isv_im_crt, indout, axis=2, circular=False, extrapolate=True
        )
        self.isv_re_crt = drtls.linresample(
            self.isv_re_crt, indout, axis=2, circular=False, extrapolate=True
        )

    def __lut_resample(self, daz, dinc, dspd):
        """
        Upsample LUT in winddir, windspd and inc dimensions.

        :param data:
        :param daz: azimuth resolution
        :return:
        """
        naz = int(np.floor(360 / daz))
        daz = 360 / naz
        nwdirv = np.arange(naz) * daz
        indout = nwdirv / self.wdir_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=4, circular=True)
        self.dcam = drtls.linresample(self.dcam, indout, axis=4, circular=True)
        # self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=2, circular=True)
        self.wdirv = nwdirv
        self.wdir_step = daz

        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.incv[0]) / self.inc_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=3)
        self.dcam = drtls.linresample(self.dcam, indout, axis=3)
        self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=3)
        self.incv = nincv
        self.inc_step = dinc

        # Wind vector interpolation
        nspd = int(np.ceil((self.wspeedv.max() - self.wspeedv.min()) / dspd))
        nwspeedv = np.linspace(self.wspeedv.min(), self.wspeedv.max(), nspd + 1)
        dwspeed = nwspeedv[1] - nwspeedv[0]
        indout = (nwspeedv - self.wspeedv[0]) / self.wspd_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=5)
        self.dcam = drtls.linresample(self.dcam, indout, axis=5)
        self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=5)
        self.wspeedv = nwspeedv
        self.wspd_step = dwspeed

    def __isv_lut_resample(self, daz, dinc, dspd):
        """
        Upsample LUT in winddir, windspd and inc dimensions.

        :param data:
        :param daz: azimuth resolution
        :return:
        """
        naz = int(np.floor(360 / daz))
        daz = 360 / naz
        nwdirv = np.arange(naz) * daz
        indout = nwdirv / self.isv_wdir_step
        self.isv_im = drtls.linresample(self.isv_im, indout, axis=3, circular=True)
        self.isv_re = drtls.linresample(self.isv_re, indout, axis=3, circular=True)
        self.isv_wdirv = nwdirv
        self.isv_wdir_step = daz

        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.isv_incv[0]) / self.isv_inc_step
        self.isv_im = drtls.linresample(
            self.isv_im, indout, axis=2, circular=False, extrapolate=True
        )
        self.isv_re = drtls.linresample(
            self.isv_re, indout, axis=2, circular=False, extrapolate=True
        )
        self.isv_incv = nincv
        self.isv_inc_step = dinc

        # Wind vector interpolation
        nspd = int(np.ceil((self.wspeedv.max() - self.wspeedv.min()) / dspd))
        nwspeedv = np.linspace(self.wspeedv.min(), self.wspeedv.max(), nspd + 1)
        dwspeed = nwspeedv[1] - nwspeedv[0]
        indout = (nwspeedv - self.isv_wspeedv[0]) / self.isv_wspd_step
        self.isv_im = drtls.linresample(
            self.isv_im, indout, axis=4, circular=False, extrapolate=True
        )
        self.isv_re = drtls.linresample(
            self.isv_re, indout, axis=4, circular=False, extrapolate=True
        )
        self.isv_wspeedv = nwspeedv
        self.isv_wspd_step = dwspeed

    @property
    def at_distance(self):
        if self.stereo:
            return (self.__at_distance_c1, self.__at_distance_c2)
        else:
            return self.__at_distance_c1

    @at_distance.setter
    def at_distance(self, at_distance):
        if type(at_distance) in [list, tuple]:
            self.at_distance_c1_ind = np.argmin(
                np.abs(np.abs(at_distance[0]) / 1e3 - self.at_distance_v)
            )
            self.at_distance_c2_ind = np.argmin(
                np.abs(-np.abs(at_distance[1]) / 1e3 - self.at_distance_v)
            )
        else:
            self.at_distance_c1_ind = np.argmin(
                np.abs(np.abs(at_distance) / 1e3 - self.at_distance_v)
            )
            self.at_distance_c2_ind = np.argmin(
                np.abs(-np.abs(at_distance) / 1e3 - self.at_distance_v)
            )
        self.monostatic_ind = np.argmin(np.abs(self.at_distance_v))
        self.__at_distance_c1 = self.at_distance_v[self.at_distance_c1_ind] * 1e3
        self.__at_distance_c2 = self.at_distance_v[self.at_distance_c2_ind] * 1e3

    @property
    def inc(self):
        return self.__inc

    @inc.setter
    def inc(self, inc):
        self.__inc = inc
        self.inc_ind = np.abs(self.incv - inc).argmin()

    @property
    def waveage(self):
        return self.__waveage

    @waveage.setter
    def waveage(self, waveage):
        self.__waveage = waveage
        self.waveage_ind = np.abs(self.waveagev - waveage).argmin()
        self.isv_waveage_ind = np.abs(self.isv_waveagev - waveage).argmin()

    def nrcs_lut(self, pol_ind, cart=False):
        """Return NRCS LUT for polarization indicated.

        The waveage, along-track separation and incident angle already set.

        Parameters
        ----------
        pol_ind : type
            Description of parameter `pol_ind`.
        cart : type
            Description of parameter `cart`.

        Returns
        -------
        type
            Description of returned object.

        """
        if cart:
            nrcs = self.nrcs_crt[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]

        else:
            nrcs = self.nrcsm[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]
        if self.stereo:
            return nrcs[
                [self.monostatic_ind, self.at_distance_c1_ind, self.at_distance_c2_ind]
            ]
        else:
            return nrcs[[self.monostatic_ind, self.at_distance_c1_ind]]

    def dca_lut(self, pol_ind, cart=False):
        """Return DCA LUT for polarization indicated.

        The waveage, along-track separation and incident angle already set.

        Parameters
        ----------
        pol_ind : type
            Description of parameter `pol_ind`.
        cart : type
            Description of parameter `cart`.

        Returns
        -------
        type
            Description of returned object.
        """
        if cart:
            dca = self.dca_crt[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]
        else:
            dca = self.dcam[:, self.waveage_ind, pol_ind, self.inc_ind, :, :]
        if self.stereo:
            return dca[
                [self.monostatic_ind, self.at_distance_c1_ind, self.at_distance_c2_ind]
            ]
        else:
            return dca[[self.monostatic_ind, self.at_distance_c1_ind]]

    def isv_im_lut(self, pol_ind, cart=False):
        if cart:
            return self.isv_im_crt[self.waveage_ind, pol_ind, self.inc_ind, :, :]
        else:
            return self.isv_im[self.waveage_ind, pol_ind, self.inc_ind, :, :]

    def isv_re_lut(self, pol_ind, cart=False):
        if cart:
            return self.isv_re_crt[self.waveage_ind, pol_ind, self.inc_ind, :, :]
        else:
            return self.isv_re[self.waveage_ind, pol_ind, self.inc_ind, :, :]

    def nrcs_dca(self, pol_ind, wspd, wdir, inc, sat="mono"):
        """
        :param pol_ind:
        :param wspd:
        :param wdir:
        :param inc:
        :return:
        """
        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        inc_ind = ind_clip(
            np.round((inc - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )

        wdir_ind = np.mod(
            np.round((wdir - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        if sat == "cs1":
            at_ind = self.at_distance_c1_ind
        elif sat == "cs2":
            at_ind = self.at_distance_c2_ind
        else:
            at_ind = self.monostatic_ind

        nrcs_o = self.nrcsm[
            at_ind, self.waveage_ind, pol_ind, inc_ind, wdir_ind, wspd_ind
        ]
        dca_o = self.dcam[
            at_ind, self.waveage_ind, pol_ind, inc_ind, wdir_ind, wspd_ind
        ]
        # dca_std_o = self.dca_stdm[self.monostatic_ind, :, self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        return nrcs_o, dca_o  # , dca_std_o

    def isv_bist(self, pol_ind, wspd, wdir0, inc1, inc2, bist_ang_az):
        """
        :param pol_ind: 0 is VV and 1 is HH, for now
        :param wspd:
        :param wdir0: wind direction w.r.t. to nonostatic reference
        :param inc1: Reference, monostatic incident angle
        :param inc2: receive incident angle
        :param bist_ang_az: azimuth bistatic angle
        :return:
        """
        # We assume equivalent incident angle is the mean
        inc = (inc1 + inc2) / 2
        # We assume that things are as if we where looking monostatically from a slightly different direction
        wdir = wdir0 - bist_ang_az / 2
        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        inc_ind = ind_clip(
            np.round((inc - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )

        wdir_ind = np.mod(
            np.round((wdir - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )

        isv_re_o = self.isv_re[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        isv_im_o = self.isv_im[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        return isv_re_o, isv_im_o

    def fwd(self, pol_ind, wspd, wdir0, incm, incb, bist_ang_az):
        incbeq = (incm + incb) / 2
        # wdirb1 = np.mod(wdir0 + bist_ang_az/2, 360)
        # wdirb2 = np.mod(wdir0 - bist_ang_az/2, 360)
        wdir0 = np.mod(wdir0, 360)
        # In this case the LUT already considers the bistatic angle
        wdirb1 = wdir0
        wdirb2 = wdir0

        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        incm_ind = ind_clip(
            np.round((incm - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        incb_ind = ind_clip(
            np.round((incbeq - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        wdir0_ind = np.mod(
            np.round((wdir0 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        wdirb1_ind = np.mod(
            np.round((wdirb1 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        wdirb2_ind = np.mod(
            np.round((wdirb2 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        nrcs_o = [
            self.nrcsm[
                self.monostatic_ind,
                self.waveage_ind,
                pol_ind,
                wdir0_ind,
                wspd_ind,
                incm_ind,
            ]
        ]
        nrcs_o.append(
            self.nrcsm[
                self.at_distance_c1_ind,
                self.waveage_ind,
                pol_ind,
                wdir0_ind,
                wspd_ind,
                incm_ind,
            ]
        )
        dca_o = [
            self.dcam[
                self.monostatic_ind,
                self.waveage_ind,
                pol_ind,
                wdir0_ind,
                wspd_ind,
                incm_ind,
            ]
        ]
        dca_o.append(
            self.dcam[
                self.at_distance_c1_ind,
                self.waveage_ind,
                pol_ind,
                wdirb1_ind,
                wspd_ind,
                incm_ind,
            ]
        )
        isv_im_o = [
            self.isv_im[self.isv_waveage_ind, pol_ind, wdir0_ind, wspd_ind, incm_ind]
        ]
        isv_im_o.append(
            self.isv_im[self.isv_waveage_ind, pol_ind, wdirb1_ind, wspd_ind, incb_ind]
        )
        if self.stereo:
            nrcs_o.append(
                self.nrcsm[
                    self.at_distance_c2_ind,
                    self.waveage_ind,
                    pol_ind,
                    wdirb2_ind,
                    wspd_ind,
                    incm_ind,
                ]
            )
            dca_o.append(
                self.dcam[
                    self.at_distance_c2_ind,
                    self.waveage_ind,
                    pol_ind,
                    wdirb2_ind,
                    wspd_ind,
                    incm_ind,
                ]
            )
            isv_im_o.append(
                self.isv_im[
                    self.isv_waveage_ind, pol_ind, wdirb2_ind, wspd_ind, incb_ind
                ]
            )
        return (
            np.stack(nrcs_o, axis=-1),
            np.stack(dca_o, axis=-1),
            np.stack(isv_im_o, axis=-1),
        )

    def fwd_jacobian(self, incm):
        """Compute jacobian of fwd model for given monostatic incident angle.

        Parameters
        ----------
        incm : type
            Incident angle.

        Returns
        -------
        type
            Description of returned object.

        """
        incm_ind = ind_clip(
            np.round((incm - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        nrcs = self.nrcs_crt[:, self.waveage_ind, :, incm_ind, :, :]
        if self.stereo:
            nrcs = nrcs[
                [self.monostatic_ind, self.at_distance_c1_ind, self.at_distance_c2_ind]
            ]
        else:
            nrcs = nrcs[[self.monostatic_ind, self.at_distance_c1_ind]]
        dca = self.dca_crt[:, self.waveage_ind, :, incm_ind, :, :]
        if self.stereo:
            dca = dca[
                [self.monostatic_ind, self.at_distance_c1_ind, self.at_distance_c2_ind]
            ]
        else:
            dca = dca[[self.monostatic_ind, self.at_distance_c1_ind]]
        shpin = nrcs.shape
        shpout = (shpin[0], shpin[1], 2, shpin[2], shpin[3])
        jcn = np.zeros(shpout)
        jcd = np.zeros(shpout)
        jcn[:, :, 0, :, :], jcn[:, :, 1, :, :] = np.gradient(
            nrcs, self.wcrt_step, axis=(3, 2)  # self.wcrt_step,
        )
        jcd[:, :, 0, :, :], jcd[:, :, 1, :, :] = np.gradient(
            dca, self.wcrt_step, axis=(3, 2)  # self.wcrt_step,
        )
        return jcn, jcd

    def fwd_crt(self, pol_ind, u, v, incm, incb, bist_ang_az, what="nrcs"):
        """Short summary.

        Parameters
        ----------
        pol_ind : type
            Description of parameter `pol_ind`.
        u : type
            Description of parameter `u`.
        v : type
            Description of parameter `v`.
        incm : type
            Description of parameter `incm`.
        incb : type
            Description of parameter `incb`.
        bist_ang_az : type
            Description of parameter `bist_ang_az`.
        what : type
            this can be 'nrcs', 'dca', 'isv_im'. It will fall back to 'nrcs'

        Returns
        -------
        type
            Description of returned object.

        """
        du = self.w_u[1] - self.w_u[0]
        dv = self.w_v[1] - self.w_v[0]
        um = self.w_u[0]
        vm = self.w_v[0]
        u_ind = (np.round((u - um) / du)).astype(np.int)
        v_ind = (np.round((v - vm) / dv)).astype(np.int)
        incm_ind = ind_clip(
            np.round((incm - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        if what.lower() == "dca":
            data = self.dca_crt
        elif what.lower() == "isv_im":
            data = self.isv_im_crt
        elif what.lower() == "isv_re":
            data = self.isv_re_crt
        else:
            data = self.nrcs_crt

        data_o = [
            data[self.monostatic_ind, self.waveage_ind, pol_ind, incm_ind, v_ind, u_ind]
        ]
        data_o.append(
            data[
                self.at_distance_c1_ind,
                self.waveage_ind,
                pol_ind,
                incm_ind,
                v_ind,
                u_ind,
            ]
        )

        if self.stereo:
            data_o.append(
                data[
                    self.at_distance_c2_ind,
                    self.waveage_ind,
                    pol_ind,
                    incm_ind,
                    v_ind,
                    u_ind,
                ]
            )

        return np.stack(data_o, axis=-1)


# %%


class FwdModelMonostaticProxy(FwdModel):
    def __init__(
        self,
        f_nrcs_dop,
        f_isv,
        daz=2,
        dinc=0.5,
        dspd=0.5,
        stereo=True,
        sigma_nrcs_db=0.1,
        sigma_isv=0.025e-3,
        sigma_dca=1,
    ):
        """

        :param filename:
        :param daz: Azimuth resolution of LUT
        :param dinc: Incident angle resolution of LUT
        """
        self.fwdm_type = "monostatic_proxy"
        self.ncfile = Dataset(f_nrcs_dop)
        self.stereo = stereo
        # dimensions
        shp = self.ncfile.variables["windspeed"].shape

        self.wspeedv = np.array(self.ncfile.variables["windspeed"])
        self.wdirv = np.array(self.ncfile.variables["winddirection"])
        self.incv = np.array(self.ncfile.variables["incangle"])
        self.wspd_min = self.wspeedv.min()
        self.wspd_step = self.wspeedv[1] - self.wspeedv[0]
        self.wdir_min = self.wdirv.min()
        self.wdir_step = self.wdirv[1] - self.wdirv[0]
        self.inc_min = self.incv.min()
        self.inc_step = self.incv[1] - self.incv[0]
        self.waveagev = np.array(self.ncfile.variables["waveage"])

        # data
        self.nrcsm = np.array(self.ncfile.variables["NRCS"])
        self.dcam = np.array(self.ncfile.variables["DCA"])
        self.dca_stdm = np.array(self.ncfile.variables["DCA_stdev"])

        # Geophysical noise model
        self.sigma_nrcs_db = sigma_nrcs_db
        self.sigma_isv = sigma_isv
        self.sigma_dca = sigma_dca
        # Resample
        self.__lut_resample(daz, dinc, dspd)
        # Init isv
        self.__init_isv(f_isv, daz, dinc, dspd)
        # Set inc to smallest in LUT
        self.inc = 0
        # Set wave age to the mean value in LUT
        self.waveage = self.waveagev.mean()

    def __init_isv(self, f_isv, daz, dinc, dspd):
        self.ncisv = Dataset(f_isv)
        # dimensions
        shp = self.ncfile.variables["windspeed"].shape
        self.isv_wspeedv = np.array(self.ncisv.variables["windspeed"])
        self.isv_wdirv = np.array(self.ncisv.variables["winddirection"])
        self.isv_incv = np.array(self.ncisv.variables["incangle"])
        self.isv_wspd_min = self.isv_wspeedv.min()
        self.isv_wspd_step = self.isv_wspeedv[1] - self.isv_wspeedv[0]
        self.isv_wdir_min = self.isv_wdirv.min()
        self.isv_wdir_step = self.isv_wdirv[1] - self.isv_wdirv[0]
        self.isv_inc_min = self.isv_incv.min()
        self.isv_inc_step = self.isv_incv[1] - self.isv_incv[0]
        self.isv_waveagev = np.array(self.ncfile.variables["waveage"])

        # data
        # FIXME: here I assume that there is only one element in first dimension
        self.isv_im = np.array(self.ncisv.variables["isvIm"])[0]
        self.isv_re = np.array(self.ncisv.variables["isvRe"])[0]
        # Resample
        self.__isv_lut_resample(daz, dinc, dspd)

    def __lut_resample(self, daz, dinc, dspd):
        """
        Upsample LUT in winddir, windspd and inc dimensions
        :param data:
        :param daz: azimuth resolution
        :return:
        """
        naz = int(np.floor(360 / daz))
        daz = 360 / naz
        nwdirv = np.arange(naz) * daz
        indout = nwdirv / self.wdir_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=2, circular=True)
        self.dcam = drtls.linresample(self.dcam, indout, axis=2, circular=True)
        self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=2, circular=True)
        self.wdirv = nwdirv
        self.wdir_step = daz

        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.incv[0]) / self.inc_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=4)
        self.dcam = drtls.linresample(self.dcam, indout, axis=4)
        self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=4)
        self.incv = nincv
        self.inc_step = dinc

        # Wind vector interpolation
        nspd = int(np.ceil((self.wspeedv.max() - self.wspeedv.min()) / dspd))
        nwspeedv = np.linspace(self.wspeedv.min(), self.wspeedv.max(), nspd + 1)
        dwspeed = nwspeedv[1] - nwspeedv[0]
        indout = (nwspeedv - self.wspeedv[0]) / self.wspd_step
        self.nrcsm = drtls.linresample(self.nrcsm, indout, axis=3)
        self.dcam = drtls.linresample(self.dcam, indout, axis=3)
        self.dca_stdm = drtls.linresample(self.dca_stdm, indout, axis=3)
        self.wspeedv = nwspeedv
        self.wspd_step = dwspeed

    def __isv_lut_resample(self, daz, dinc, dspd):
        """
        Upsample LUT in winddir, windspd and inc dimensions
        :param data:
        :param daz: azimuth resolution
        :return:
        """
        naz = int(np.floor(360 / daz))
        daz = 360 / naz
        nwdirv = np.arange(naz) * daz
        indout = nwdirv / self.isv_wdir_step
        self.isv_im = drtls.linresample(self.isv_im, indout, axis=2, circular=True)
        self.isv_re = drtls.linresample(self.isv_re, indout, axis=2, circular=True)
        self.isv_wdirv = nwdirv
        self.isv_wdir_step = daz

        # Incident angle interpolation
        ninc = int(np.ceil((self.incv.max() - self.incv.min()) / dinc))
        nincv = np.linspace(self.incv.min(), self.incv.max(), ninc + 1)
        dinc = nincv[1] - nincv[0]
        indout = (nincv - self.isv_incv[0]) / self.isv_inc_step
        self.isv_im = drtls.linresample(
            self.isv_im, indout, axis=4, circular=False, extrapolate=True
        )
        self.isv_re = drtls.linresample(
            self.isv_re, indout, axis=4, circular=False, extrapolate=True
        )
        self.isv_incv = nincv
        self.isv_inc_step = dinc

        # Wind vector interpolation
        nspd = int(np.ceil((self.wspeedv.max() - self.wspeedv.min()) / dspd))
        nwspeedv = np.linspace(self.wspeedv.min(), self.wspeedv.max(), nspd + 1)
        dwspeed = nwspeedv[1] - nwspeedv[0]
        indout = (nwspeedv - self.isv_wspeedv[0]) / self.isv_wspd_step
        self.isv_im = drtls.linresample(
            self.isv_im, indout, axis=3, circular=False, extrapolate=True
        )
        self.isv_re = drtls.linresample(
            self.isv_re, indout, axis=3, circular=False, extrapolate=True
        )
        self.isv_wspeedv = nwspeedv
        self.isv_wspd_step = dwspeed

    @property
    def inc(self):
        return self.__inc

    @inc.setter
    def inc(self, inc):
        self.__inc = inc
        self.inc_ind = np.abs(self.incv - inc).argmin()

    @property
    def waveage(self):
        return self.__waveage

    @waveage.setter
    def waveage(self, waveage):
        self.__waveage = waveage
        self.waveage_ind = np.abs(self.waveagev - waveage).argmin()

    def nrcs_lut(self, pol_ind):
        return self.nrcsm[self.waveage_ind, pol_ind, :, :, self.inc_ind]

    def dca_lut(self, pol_ind):
        return self.dcam[self.waveage_ind, pol_ind, :, :, self.inc_ind]

    def dca_std_lut(self, pol_ind):
        return self.dca_stdm[self.waveage_ind, pol_ind, :, :, self.inc_ind]

    def isv_im_lut(self, pol_ind):
        return self.isv_im[self.waveage_ind, pol_ind, :, :, self.inc_ind]

    def isv_re_lut(self, pol_ind):
        return self.isv_re[self.waveage_ind, pol_ind, :, :, self.inc_ind]

    def nrcs_dca(self, pol_ind, wspd, wdir, inc):
        """
        :param pol_ind:
        :param wspd:
        :param wdir:
        :param inc:
        :return:
        """
        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        inc_ind = ind_clip(
            np.round((inc - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )

        wdir_ind = np.mod(
            np.round((wdir - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )

        nrcs_o = self.nrcsm[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        dca_o = self.dcam[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        dca_std_o = self.dca_stdm[
            self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind
        ]
        return nrcs_o, dca_o, dca_std_o

    # Now a hack for the bistatic
    # FIXME please
    def nrcs_dca_bist(self, pol_ind, wspd, wdir0, inc1, inc2, bist_ang_az):
        """
        :param pol_ind: 0 is VV and 1 is HH, for now
        :param wspd:
        :param wdir0: wind direction w.r.t. to nonostatic reference
        :param inc1: Reference, monostatic incident angle
        :param inc2: receive incident angle
        :param bist_ang_az: azimuth bistatic angle
        :return:
        """
        # We assume equivalent incident angle is the mean
        inc = (inc1 + inc2) / 2
        # We assume that things are as if we where looking monostatically from a slightly different direction
        wdir = wdir0 - bist_ang_az / 2
        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        inc_ind = ind_clip(
            np.round((inc - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )

        wdir_ind = np.mod(
            np.round((wdir - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )

        nrcs_o = self.nrcsm[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        dca_o = self.dcam[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        dca_std_o = self.dca_stdm[
            self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind
        ]
        return nrcs_o, dca_o, dca_std_o

    def isv_bist(self, pol_ind, wspd, wdir0, inc1, inc2, bist_ang_az):
        """
        :param pol_ind: 0 is VV and 1 is HH, for now
        :param wspd:
        :param wdir0: wind direction w.r.t. to nonostatic reference
        :param inc1: Reference, monostatic incident angle
        :param inc2: receive incident angle
        :param bist_ang_az: azimuth bistatic angle
        :return:
        """
        # We assume equivalent incident angle is the mean
        inc = (inc1 + inc2) / 2
        # We assume that things are as if we where looking monostatically from a slightly different direction
        wdir = wdir0 - bist_ang_az / 2
        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        inc_ind = ind_clip(
            np.round((inc - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )

        wdir_ind = np.mod(
            np.round((wdir - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )

        isv_re_o = self.isv_re[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        isv_im_o = self.isv_im[self.waveage_ind, pol_ind, wdir_ind, wspd_ind, inc_ind]
        return isv_re_o, isv_im_o

    def fwd(self, pol_ind, wspd, wdir0, incm, incb, bist_ang_az):
        incbeq = (incm + incb) / 2
        wdirb1 = np.mod(wdir0 + bist_ang_az / 2, 360)
        wdirb2 = np.mod(wdir0 - bist_ang_az / 2, 360)
        wdir0 = np.mod(wdir0, 360)

        wspd_ind = ind_clip(
            np.round((wspd - self.wspd_min) / self.wspd_step).astype(np.int),
            self.wspeedv.size,
        )
        incm_ind = ind_clip(
            np.round((incm - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        incb_ind = ind_clip(
            np.round((incbeq - self.inc_min) / self.inc_step).astype(np.int),
            self.incv.size,
        )
        wdir0_ind = np.mod(
            np.round((wdir0 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        wdirb1_ind = np.mod(
            np.round((wdirb1 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        wdirb2_ind = np.mod(
            np.round((wdirb2 - self.wdir_min) / self.wdir_step).astype(np.int),
            self.wdirv.size,
        )
        nrcs_o = [self.nrcsm[self.waveage_ind, pol_ind, wdir0_ind, wspd_ind, incm_ind]]
        nrcs_o.append(
            self.nrcsm[self.waveage_ind, pol_ind, wdirb1_ind, wspd_ind, incb_ind]
        )
        dca_o = [self.dcam[self.waveage_ind, pol_ind, wdir0_ind, wspd_ind, incm_ind]]
        dca_o.append(
            self.dcam[self.waveage_ind, pol_ind, wdirb1_ind, wspd_ind, incb_ind]
        )
        isv_im_o = [
            self.isv_im[self.waveage_ind, pol_ind, wdir0_ind, wspd_ind, incm_ind]
        ]
        isv_im_o.append(
            self.isv_im[self.waveage_ind, pol_ind, wdirb1_ind, wspd_ind, incb_ind]
        )
        if self.stereo:
            nrcs_o.append(
                self.nrcsm[self.waveage_ind, pol_ind, wdirb2_ind, wspd_ind, incb_ind]
            )
            dca_o.append(
                self.dcam[self.waveage_ind, pol_ind, wdirb2_ind, wspd_ind, incb_ind]
            )
            isv_im_o.append(
                self.isv_im[self.waveage_ind, pol_ind, wdirb2_ind, wspd_ind, incb_ind]
            )
        return (
            np.stack(nrcs_o, axis=-1),
            np.stack(dca_o, axis=-1),
            np.stack(isv_im_o, axis=-1),
        )


if __name__ == "__main__":
    # %%
    from stereoid.oceans import RetrievalModel

    datadir = "/Users/plopezdekker/Documents/WORK/STEREOID/DATA/Ocean"
    fname = "C_band_nrcs_dop_ocean_simulation.nc"
    fnameisv = "C_band_isv_ocean_simulation.nc"
    fname_s1 = "S1_VV.nc"
    fname_c1 = "s1_cs1_HH_200km"
    fold = Dataset(os.path.join(datadir, fname))
    fs1 = Dataset(os.path.join(datadir, fname_s1))
    # fisv = Dataset(os.path.join(datadir, fnameisv))
    # %%
    fwdm = FwdModel(
        datadir, os.path.join(datadir, fnameisv), dspd=2, duvec=0.5, model="SSAlin"
    )
    fwdm.nrcs_crt.shape
    fwdm.at_distance = 200e3
    fwdm.at_distance
    # %%
    plt.figure(figsize=(6, 6))
    plt.imshow(10 * np.log10(fwdm.nrcs_lut(0, cart=True)[0]), origin="lower")
    plt.colorbar()
    plt.figure(figsize=(6, 6))
    plt.imshow(10 * np.log10(fwdm.nrcs_lut(0, cart=True)[1]), origin="lower")
    plt.colorbar()
    # plt.figure()
    # plt.plot(fwdm.nrcs_crt[0, 1, 1, 10, :, 120])
    # plt.plot(fwdm.nrcs_crt[-1, 1, 1, 10, :, 120])
    # plt.figure()
    # plt.plot(fwdm.nrcsm[5, 1, 1, 10, :, 1])
    # fwdm.wspd_min
    # plt.figure()
    # plt.imshow(fwdm.isv_im_crt[1, 1, 0, :, :], origin='lower')
    # plt.colorbar()
    # %%
    jac_n, jac_d = fwdm.fwd_jacobian(35)
    jac_n.shape
    plt.figure(figsize=(6, 6))
    plt.imshow(jac_n[1, 0, 1, :, :], origin="lower")
    plt.colorbar()
    plt.figure(figsize=(6, 6))
    plt.imshow(jac_n[2, 0, 1, :, :], origin="lower")
    plt.colorbar()
    # %%
    fwdm.waveagev
    fwdm.isv_im
    # Now test
    incm = 35
    incb = 36
    bang = 40
    obsgeo = ObsGeo(incm, incb, bang)
    ret = RetrievalModel(fwdm, obsgeo)

    U = np.array([8, 7])
    Udir = np.array([90, 80])
    U = 8
    Udir = 20
    tnrcs, tdca, tisv = fwdm.fwd(0, U, Udir, incm, incb, bang)
    wspd, dca, j1a, j1b = ret.retrieval_1(
        tnrcs, tisv, dir0=None, sigma_nrcs_db=0.1, debug=True
    )
    plt.figure()
    plt.plot(j1a[:, 20], label="j1a")
    plt.plot(j1b[:, 20], label="j1b")
    plt.plot(j1a[:, 20] + j1b[:, 20], label="j1")
    plt.legend(loc=0)

    for ind in range(3):
        plt.figure()
        plt.imshow(ret.isv_im_lut[0, :, :, ind])

    kk = (1, 2)
    type(kk) in (list, tuple)
