from osgeo import gdal
import os
import numpy as np
import datetime
import pickle

from stereoid.land_ice.phase_model import PhaseModel
from stereoid.land_ice.deterministic_data import DeterministicData


class BaselineVolumeCoherence():

    def __init__(self, baselines, hoas, incidence_angles, penetration_depths, looks):

        # First set all parameters
        self.set_orbit_settings(baselines, penetration_depths, hoas)
        self.set_incidence_bins(incidence_angles)

        self.set_ice_characteristics()
        self.set_satellite_characteristics()
        self.phase_model = PhaseModel(101, 101)
        self.set_looks(looks)

        # Then do the calculations
        self.calc_baseline_volume_coherence()

    def calc_baseline_volume_coherence(self):

        geo_hoa_size = (len(self.i_bins), len(self.hoa), len(self.pen_depths))
        geo_baseline_size = (len(self.i_bins), len(self.baselines), len(self.pen_depths))

        # Calculations for the height of ambiguity, volume and baseline decorrelation.
        self.coh_baseline = dict()
        self.coh_vol = dict()
        self.hoa_vals = dict()
        self.coh_baseline['hoa'] = np.zeros(geo_hoa_size)
        self.coh_vol['hoa'] = np.zeros(geo_hoa_size)
        self.hoa_vals['hoa'] = np.zeros(geo_hoa_size)
        self.coh_baseline['baseline'] = np.zeros(geo_baseline_size)
        self.coh_vol['baseline'] = np.zeros(geo_baseline_size)
        self.hoa_vals['baseline'] = np.zeros(geo_baseline_size)

        for n_i, i in enumerate(self.i_bins):
            for dist_type in ['hoa', 'baseline']:
                if dist_type == 'hoa':
                    sat_dists = self.hoa
                elif dist_type == 'baseline':
                    sat_dists = self.baselines

                for n_d, sat_dist in enumerate(sat_dists):

                    r0 = 693000 / np.cos(np.deg2rad(i))

                    # Calculate height of ambiguity as a function of incidence angles.
                    if dist_type == 'hoa':
                        hoa = sat_dist
                        baseline = r0 * self.wavelength * np.sin(np.radians(i)) / hoa
                    elif dist_type == 'baseline':
                        baseline = sat_dist
                        hoa = r0 * self.wavelength * np.sin(np.radians(i)) / baseline

                    critical_baseline = r0 * self.wavelength * np.tan(np.radians(i)) * (self.BW / self.c)
                    coh_baseline = 1 - (baseline / critical_baseline)

                    for n_pd, pen_depth in enumerate(self.pen_depths):
                        coh_vol = 1 / np.sqrt(1 + (
                                (2 * np.pi * np.sqrt(self.permittivity_H) * pen_depth * baseline) / (
                                r0 * self.wavelength * np.tan(np.radians(i)))))

                        self.coh_baseline[dist_type][n_i, n_d, n_pd] = coh_baseline
                        self.coh_vol[dist_type][n_i, n_d, n_pd] = coh_vol
                        self.hoa_vals[dist_type][n_i, n_d, n_pd] = hoa

    def set_orbit_settings(self,
                           baselines=[10, 50, 100, 200, 300, 500, 700, 1000],
                           pen_depths=[0, 1, 2, 5, 10, 15, 20],
                           hoa=[5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]):

        self.baselines = baselines
        self.pen_depths = pen_depths
        self.hoa = hoa

    def set_incidence_bins(self, incidence):
        self.i_bins = incidence

    def set_satellite_characteristics(self, wavelength=0.05546576, r0=850000):
        """


        :return:
        """

        self.wavelength = wavelength
        self.BW = 55000000
        self.c = 299792458
        # This value is variable over the swath, but for now we assume that it is the same over the whole image.
        self.r0 = r0

    def set_ice_characteristics(self, ice_density=0.4):
        """
        Set the characteristics of the ice. For now we assume one value for the whole area, but this can be changed
        if we have further information. For now it is only the ice or snow density.

        :param ice_density:
        :return:
        """

        self.ice_density = ice_density

        ice_density *= 1000
        permittivity = DeterministicData.density2transmissivity('horizontal')
        self.permittivity_H = (permittivity[2] + permittivity[1] * ice_density + permittivity[0] * ice_density ** 2)
        permittivity = DeterministicData.density2transmissivity('vertical')
        self.permittivity_V = (permittivity[2] + permittivity[1] * ice_density + permittivity[0] * ice_density ** 2)

    def set_looks(self, looks=[1, 5, 10, 20, 50, 100, 200]):
        self.looks = looks

        for L in self.looks:
            self.phase_model.create_lookup_table(L)

    def calc_std_from_total_coh(self, dat, hoa, looks):
        """

        :return:
        """

        std = self.phase_model.interp_coh_real(looks, dat)
        std_degrees = std / np.pi * 180
        std_meters = (std / 2 / np.pi) * hoa

        return std_degrees, std_meters

    def get_baseline_plot_data(self, use_hoa=False, x_axis='dist', i_val=None, pd_val=None, dist_val=None, looks=[1, 10, 100]):
        """

        :return:
        """

        if use_hoa:
            dict_str = 'hoa'
            dist_vals = self.hoa
        else:
            dict_str = 'baseline'
            dist_vals = self.baselines

        try:
            if i_val != None:
                i_no = np.where(self.i_bins == i_val)[0][0]
            else:
                i_no = 0
            if pd_val != None:
                pd_no = np.where(self.pen_depths == pd_val)[0][0]
            else:
                pd_no = 0
            if dist_val != None:
                dist_no = np.where(dist_vals == dist_val)[0][0]
            else:
                dist_no = 0
        except:
            raise ValueError('Incidence angle, penetration depth, baseline or height of ambiguity value does not exist!')

        if x_axis in ['dist', 'baseline', 'height of ambiguity']:
            hoa = self.hoa_vals[dict_str][i_no, :, pd_no]
            coh_baseline = self.coh_baseline[dict_str][i_no, :, pd_no]
            coh_vol = self.coh_vol[dict_str][i_no, :, pd_no]
        elif x_axis == 'incidence angle':
            hoa = self.hoa_vals[dict_str][:, dist_no, pd_no]
            coh_baseline = self.coh_baseline[dict_str][:, dist_no, pd_no]
            coh_vol = self.coh_vol[dict_str][:, dist_no, pd_no]
        elif x_axis == 'penetration depth':
            hoa = self.hoa_vals[dict_str][i_no, dist_no, :]
            coh_baseline = self.coh_baseline[dict_str][i_no, dist_no, :]
            coh_vol = self.coh_vol[dict_str][i_no, dist_no, :]
        else:
            raise ValueError('x-axis should be dist/baseline/height of ambiguity/incidence angle/penetration depth not ' + x_axis)

        std_degrees_list = []
        std_meters_list = []

        for look in looks:
            std_degrees, std_meters = self.calc_std_from_total_coh(coh_vol * coh_baseline, hoa, look)
            std_degrees_list.append(std_degrees)
            std_meters_list.append(std_meters)

        return std_meters_list, std_degrees_list, coh_baseline, coh_vol, hoa
