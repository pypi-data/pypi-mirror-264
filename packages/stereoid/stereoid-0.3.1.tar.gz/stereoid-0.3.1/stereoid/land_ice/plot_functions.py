import os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
from stereoid.land_ice.coherence_model_SAR_stack import SARStackCoherence
from stereoid.land_ice.deterministic_data import DeterministicData

"""
Test script.
data.stack_folder = '/mnt/f7b747c7-594a-44bb-a62a-a3bf2371d931/radar_datastacks/RIPPL_v2.0/Sentinel_1/east_greenland'
processing_folder = '/home/gert/fast_datastacks'
master_date = '20191001'

data = SARStackCoherence(stack_folder=data.stack_folder, processing_folder=processing_folder, master_date=master_date)
data.stack_calculations(6, 20, 100)

"""


class PlotData():

    @staticmethod
    def get_baseline_plot_data(data, use_hoa=False, x_axis='dist', i_no=0, pd_no=0, dist_no=0):
        """

        :param SARStackCoherence data:
        :return:
        """

        if use_hoa:
            dict_str = 'hoa'
            dist_vals = data.hoa
        else:
            dict_str = 'baseline'
            dist_vals = data.baselines

        pen_depth = data.pen_depths[0]
        incidence_angle = data.i_bins[0]

        looks = data.looks

        if x_axis == 'dist':
            hoa = data.hoa_vals[dict_str][i_no, :, pd_no]
            coh_baseline = data.coh_baseline[dict_str][i_no, :, pd_no]
            coh_vol = data.coh_vol[dict_str][i_no, :, pd_no]
        elif x_axis == 'incidence':
            hoa = data.hoa_vals[dict_str][:, dist_no, pd_no]
            coh_baseline = data.coh_baseline[dict_str][:, dist_no, pd_no]
            coh_vol = data.coh_vol[dict_str][:, dist_no, pd_no]
        elif x_axis == 'volume':
            hoa = data.hoa_vals[dict_str][i_no, dist_no, :]
            coh_baseline = data.coh_baseline[dict_str][i_no, dist_no, :]
            coh_vol = data.coh_vol[dict_str][i_no, dist_no, :]

        std_degrees_list = []
        std_meters_list = []

        for look in looks:
            std_degrees, std_meters = data.calc_std_from_total_coh(coh_vol * coh_baseline, hoa, look)
            std_degrees_list.append(std_degrees)
            std_meters_list.append(std_meters)

        return std_meters_list, std_degrees_list, coh_baseline, coh_vol, hoa

    @staticmethod
    def get_enveo_data(plot_data):
        """
        Get data from ENVEO experiments for plotting

        :param plot_data:
        :return:
        """

        enveo_val = dict()
        ice_types = ['glacier_ice', 'percolation_zone', 'dry_snow_zone', 'wet_snow']
        ice_markers = ["o", "v", "X", 'D']
        ice_styles = ["-", "--", "dotted", '-.']
        pol_enveo = ['VV', 'VH']
        pol_colors = ['black']

        # Get the values from ENVEO for the four zones
        enveo_poly = DeterministicData.load_ENVEO_poly()

        for ice_type in ice_types:
            for pol in pol_enveo:
                enveo_val[ice_type + '_' + pol] = enveo_poly[ice_type][pol][0] * plot_data['mean_inc']**3 + \
                                                  enveo_poly[ice_type][pol][1] * plot_data['mean_inc']**2 + \
                                                  enveo_poly[ice_type][pol][2] * plot_data['mean_inc']**1 + \
                                                  enveo_poly[ice_type][pol][3]

        return enveo_val, ice_types, ice_markers, ice_styles, pol_enveo, pol_colors

    @staticmethod
    def height_vs_incidence_angle(data):

        if not isinstance(data, SARStackCoherence):
            return

        # Check mid-winter amplitude vs incidence angle.
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('height (m)')
        ax1.set_ylabel('amplitude (db)', color=color)
        ax1.plot(data.height, data.median_values['amplitude_HH'][0, :], color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_title('incidence angle vs amplitude')

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('incidence angle (degree)', color=color)  # we already handled the x-label with ax1
        ax2.plot(data.height, data.incidence, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        fig.savefig(os.path.join(data.stack_folder, 'fig', 'amplitude vs incidence angle in winter'))
        plt.show()

    @staticmethod
    def ENVEO_vs_backscatter_plots(data):

        if not isinstance(data, SARStackCoherence):
            return

        # For blocks of three months we compare the ENVEO results with bins of 200 meter height of the glacier.
        # Most likely this only works for a small range of incidence angles.
        # Cutoff for the bins is 50 pixels.

        cut_off_num = 50

        # Load ENVEO data
        enveo_poly = DeterministicData.load_ENVEO_poly()

        time_slot = 0
        i_bins = np.array(data.i_bins) / 180 * np.pi
        plt.figure()

        # Plot the different functions
        for key in enveo_poly.keys():
            for pol in enveo_poly[key].keys():
                if 'std' not in pol and 'VV' in pol:
                    ENVEO_curve = enveo_poly[key][pol][0] * i_bins**3 + enveo_poly[key][pol][1] * i_bins**2 + \
                                  enveo_poly[key][pol][2] * i_bins**1 + enveo_poly[key][pol][3]
                    plt.plot(data.i_bins, ENVEO_curve, label=key + '_' + pol)
        plt.legend()

        plt.figure()

        for h_n, h in enumerate(data.h_bins):
            count = data.bin_sizes['amplitude_HH'][time_slot, :, h_n] > 50

            plt.plot(i_bins[count] * 180 / np.pi, data.median_values['amplitude_HH'][time_slot, :, h_n][count], label=str(int(h)))

        plt.legend()



class MidpointNormalize(mpl.colors.Normalize):
    def __init__(self, vmin, vmax, midpoint=0, clip=False):
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        normalized_min = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) / (self.midpoint - self.vmax))))
        normalized_max = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) / (self.midpoint - self.vmin))))
        normalized_mid = 0.5
        x, y = [self.vmin, self.midpoint, self.vmax], [normalized_min, normalized_mid, normalized_max]
        return sp.ma.masked_array(sp.interp(value, x, y))