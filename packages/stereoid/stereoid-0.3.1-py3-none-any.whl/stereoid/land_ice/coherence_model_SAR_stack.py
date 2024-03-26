from osgeo import gdal
import os
import numpy as np
import datetime
import pickle

from stereoid.land_ice.phase_model import PhaseModel
from stereoid.land_ice.coherence_model_baseline_volume import BaselineVolumeCoherence

"""
Test

stack_folder = '/mnt/f7b747c7-594a-44bb-a62a-a3bf2371d931/radar_datastacks/RIPPL_v2.0/Sentinel_1/east_stack'
processing_folder = '/home/gert/fast_datastacks'

"""


class SARStackCoherence(BaselineVolumeCoherence):
    
    
    def __init__(self, stack_folder='', processing_folder='', master_date='', pol=None, dat_types=None, result_file=''):
        """

        :param stack_folder:
        :param processing_folder:
        :param master_date:
        :param pol:
        :param dat_types:
        """

        if dat_types is None:
            dat_types = ['amplitude', 'coherence', 'ratios']
        if pol is None:
            pol = ['HH', 'HV']

        if os.path.exists(result_file):
            if os.path.getsize(result_file) == 0:
                print('File you want to load is empty')
                return

            with open(result_file, 'rb') as data_file:
                self.__dict__ = pickle.load(data_file)
        else:
            if result_file:
                if os.path.exists(os.path.dirname(result_file)):
                    self.result_file = result_file
                else:
                    print('Folder for result file does not exist')
            else:
                self.result_file = os.path.join(self.stack_folder, 'bin_calculations.dat')

            self.stack_folder = stack_folder
            self.processing_folder = processing_folder
            self.files = []
            self.pol = pol
            self.dat_types = dat_types
            self.master_date = master_date
            self.dates = dict()
            self.height_bins = []
            self.date_bins = []
            self.incidence_bins = []
            self.phase_model = PhaseModel(101, 101)

            # The data itself.
            self.input_data = dict()
            self.mask = []
            self.incidence = []
            self.height = []

            # Intervals
            self.d_t = []
            self.d_i = []
            self.d_h = []
            self.percentiles = []
            self.mask_no = 2

            # The output data
            self.median_values = dict()
            self.percentiles_values = dict()
            self.bin_sizes = dict()
            self.coh_snr = dict()
            self.coh_vol = dict()
            self.coh_baseline = dict()
            self.coh_total = dict()
            self.std_degrees = dict()
            self.std_meters = dict()
            self.coh_percentiles = dict()
            self.average_dem = dict()
            self.average_inc = dict()

    def __call__(self, d_t, d_i, d_h, baselines, penetration_depths, hoas, looks=None, percentiles=None, mask_no=2):

        if percentiles is None:
            percentiles = [5, 25, 75, 95]
        if looks is None:
            looks = [1, 10, 100]

        self.d_t = d_t
        self.d_i = d_i
        self.d_h = d_h

        self.define_time_bins(d_t)          # 6 day intervals
        self.define_incidence_bins(d_i)     # 1 degree incidence angle intervals
        self.define_height_bins(d_h)        # 100 meter height bins
        self.set_looks(looks)
        self.set_percentiles(percentiles)

        self.set_ice_characteristics()
        self.set_satellite_characteristics()
        self.set_orbit_settings(baselines, penetration_depths, hoas)
        self.calc_baseline_volume_coherence()
        self.calc_bins(mask_no=mask_no)

    def load_data(self, resolution=None, load_from_file=False):

        # Resolution string
        if resolution is None:
            resolution = [0.001, 0.001]
        res_str = '@geo_WGS84_' + str(int(resolution[0] * 3600)) + '_' + str(int(resolution[1] * 3600))

        # Read geotiff information
        self.files = dict()
        if 'amplitude' in self.dat_types:
            if 'HH' in self.pol:
                self.files['amplitude_HH'] = [file for file in os.listdir(self.stack_folder) if 'calibrated_amplitude_db_HH' + res_str in file]
            if 'HV' in self.pol:
                self.files['amplitude_HV'] = [file for file in os.listdir(self.stack_folder) if 'calibrated_amplitude_db_HV' + res_str in file]

        # Only 6 day intervals
        if 'coherence' in self.dat_types:
            if 'HH' in self.pol:
                self.files['coherence_HH'] = [file for file in os.listdir(self.stack_folder) if 'coherence_HH' + res_str in file and int(file[9:17]) - int(file[:8]) == 6]
            if 'HV' in self.pol:
                self.files['coherence_HV'] = [file for file in os.listdir(self.stack_folder) if 'coherence_HV' + res_str in file and int(file[9:17]) - int(file[:8]) == 6]

        for key in self.files.keys():
            self.files[key].sort()
            self.dates[key] = np.array([int(file[:8]) for file in self.files[key]])

        ds = gdal.Open(os.path.join(self.stack_folder, self.files['amplitude_HH'][0]))
        band = ds.GetRasterBand(1)
        amp_arr = band.ReadAsArray()
        self.geo_info = ds.GetGeoTransform()

        self.image_shape = amp_arr.shape
        self.input_data = dict()

        # Load the ice mask
        mask_file = os.path.join(self.stack_folder, 'glaciers_rasterized.tif')
        ds = gdal.Open(mask_file)
        band = ds.GetRasterBand(1)
        self.mask = band.ReadAsArray()
        self.mask[amp_arr == 0] = 0

        # Load the height file
        h_file = [file for file in os.listdir(self.stack_folder) if self.master_date + '_dem'  + res_str in file][0]
        height_file = os.path.join(self.stack_folder, h_file)
        ds = gdal.Open(height_file)
        band = ds.GetRasterBand(1)
        self.height = band.ReadAsArray()

        # Load the incidence angles
        incidence_file = os.path.join(self.stack_folder, self.master_date + '_incidence_angle'  + res_str + '.tiff')
        ds = gdal.Open(incidence_file)
        band = ds.GetRasterBand(1)
        self.incidence_angle = band.ReadAsArray()

        # Load the NESZ values
        nesz_ati = os.path.join(self.stack_folder, self.master_date + '_nesz_harmony_ati'  + res_str + '_in_coor_radar.tiff')
        ds = gdal.Open(nesz_ati)
        band = ds.GetRasterBand(1)
        self.nesz_single = band.ReadAsArray()

        nesz_dual = os.path.join(self.stack_folder, self.master_date + '_nesz_harmony_dual'  + res_str + '_in_coor_radar.tiff')
        ds = gdal.Open(nesz_dual)
        band = ds.GetRasterBand(1)
        self.nesz_dual = band.ReadAsArray()

        nesz_sentinel = os.path.join(self.stack_folder, self.master_date + '_nesz_sentinel' + res_str + '_in_coor_radar.tiff')
        ds = gdal.Open(nesz_sentinel)
        band = ds.GetRasterBand(1)
        self.nesz_sentinel = band.ReadAsArray()

        for key in self.files.keys():

            if load_from_file:
                try:
                    self.input_data[key] = np.memmap(os.path.join(self.processing_folder, key + '.raw'), 'float32',
                                                     'r+', shape=(len(self.files[key]), self.image_shape[0], self.image_shape[1]))
                    loaded = True
                except:
                    loaded = False

            if not load_from_file or not loaded:
                self.input_data[key] = np.memmap(os.path.join(self.processing_folder, key + '.raw'), 'float32', 'w+', shape=(len(self.files[key]), self.image_shape[0], self.image_shape[1]))

                # Load all data self.files to one variable
                for no, file in enumerate(self.files[key]):
                    print('loading ' + file)
                    ds = gdal.Open(os.path.join(self.stack_folder, file))
                    band = ds.GetRasterBand(1)
                    arr = band.ReadAsArray()

                    self.input_data[key][no, :, :] = arr

        # Also calculate the ratio between amplitudes and difference in coherence.
        if 'amplitude' in self.dat_types and 'ratios' in self.dat_types and self.pol == ['HH', 'HV']:

            if load_from_file:
                try:
                    self.input_data['amplitude_ratio'] = np.memmap(
                        os.path.join(self.processing_folder, 'amplitude_ratio.raw'), 'float32', 'r+',
                        shape=(len(self.files['amplitude_HH']), self.image_shape[0], self.image_shape[1]))
                    loaded = True
                except:
                    loaded = False

            if not load_from_file or not loaded:

                self.input_data['amplitude_ratio'] = np.memmap(os.path.join(self.processing_folder, 'amplitude_ratio.raw'), 'float32', 'w+',
                                                 shape=(len(self.files['amplitude_HH']), self.image_shape[0], self.image_shape[1]))
                for n in range(len(self.files['amplitude_HH'])):
                    self.input_data['amplitude_ratio'][n, :, :] = self.input_data['amplitude_HH'][n, :, :] - self.input_data['amplitude_HV'][n, :, :]
                    print('Calculating amplitude ratio of ' + self.files['amplitude_HH'][n][:8])
        if 'coherence' in self.dat_types and 'ratios' in self.dat_types and self.pol == ['HH', 'HV']:

            if load_from_file:
                try:
                    self.input_data['coherence_difference'] = np.memmap(
                        os.path.join(self.processing_folder, 'coherence_difference.raw'), 'float32', 'r+',
                        shape=(len(self.files['coherence_HH']), self.image_shape[0], self.image_shape[1]))
                    loaded = True
                except:
                    loaded = False

            if not load_from_file or not loaded:

                self.input_data['coherence_difference'] = np.memmap(os.path.join(self.processing_folder, 'coherence_difference.raw'), 'float32', 'w+',
                                                 shape=(len(self.files['coherence_HH']), self.image_shape[0], self.image_shape[1]))
                for n in range(len(self.files['coherence_HH'])):
                    self.input_data['coherence_difference'][n, :, :] = self.input_data['coherence_HH'][n, :, :] - self.input_data['coherence_HV'][n, :, :]
                    print('Calculating coherence difference of ' + self.files['coherence_HH'][n][:8])

    def define_height_bins(self, d_h=100, heights=[]):
        """
        Define binning in height. If not defined everything will be binned as one.

        :param int d_h: Interval for regular binning
        :param heights: Pairs of min/max heights for irregular binning
        :return:
        """

        if heights != []:
            self.height_bins = heights
            return

        # Calculate regular bins
        min_val = np.maximum(np.min(self.height[self.mask != 0]), 0)
        min_height = np.floor(min_val / d_h) * d_h - (0.5 * d_h)
        max_height = np.max(self.height[self.mask != 0])

        self.d_h = d_h
        bins = np.ceil((max_height - min_height) / d_h)
        self.height_bins = [[min_height + n * d_h, min_height + (n+1) * d_h] for n in np.arange(bins)]
        self.h_bins = [int((i[0] + i[1]) / 2) for i in self.height_bins]

    def define_time_bins(self, d_t=30, date_bins=[]):
        """
        Define binning in time. If not defined data will be binned per date.
        For ifgs we use the first date as a reference

        :param int d_t: interval in days for regular binning
        :param date_bins: pairs of min/max dates in specific days. Format > ([yyyymmdd, yyyymmdd])
        :return:
        """

        if date_bins != []:
            self.date_bins = date_bins
            return

        all_dates = []
        for key in self.dates.keys():
            all_dates.extend(list(self.dates[key]))

        min_date = datetime.datetime.strptime(str(np.min(all_dates)), '%Y%m%d')
        min_date = min_date - datetime.timedelta(days=min_date.day - 1)
        max_date = datetime.datetime.strptime(str(np.max(all_dates)), '%Y%m%d')

        interval = datetime.timedelta(days=d_t)
        n_intervals = np.ceil((max_date - min_date).days / d_t)

        self.d_t = d_t
        self.date_bins = [[int((min_date + interval * n).strftime('%Y%m%d')),
                           int((min_date + interval * (n+1)).strftime('%Y%m%d'))] for n in np.arange(n_intervals)]
        self.d_bins = [i[0] for i in self.date_bins]
        self.d_datetime = [datetime.datetime.strptime(str(d), '%Y%m%d') for d in self.d_bins]

    def define_incidence_bins(self, d_inc=1, incidence_angles=[]):
        """
        Define binning of incidence angles. If not, everything will be binned in one single bin.

        :param d_inc:
        :param incidence_angles:
        :return:
        """

        if incidence_angles != []:
            self.incidence_bins = incidence_angles
            return

        # Calculate regular bins
        min_val = np.min(self.incidence_angle[self.mask != 0])
        min_inc = np.floor(min_val / d_inc) * d_inc - (0.5 * d_inc)
        max_inc = np.max(self.incidence_angle[self.mask != 0])

        bins = np.ceil((max_inc - min_inc) / d_inc)
        self.d_inc = d_inc
        self.incidence_bins = [[min_inc + n * d_inc, min_inc + (n + 1) * d_inc] for n in np.arange(bins)]
        self.i_bins = [int((i[0] + i[1]) / 2) for i in self.incidence_bins]

    def set_percentiles(self, percentiles=None):
        if percentiles is None:
            percentiles = [5, 10, 25, 75, 90, 95]

        self.percentiles = percentiles


    def calc_bins(self, mask_no=2, harmony_types=None):
        """
        Calculate different bins. Returning values have on the first axis time, the second axis incidence angles and
        the last axis height.

        :param list(int) percentiles: Apart from mean also the percentiles in this list are calculated.

        :return:
        """

        if harmony_types is None:
            harmony_types = ['dual', 'ati', 'sentinel']

        mask_size = self.image_shape[0] * self.image_shape[1]

        data_size = (len(self.d_bins), len(self.h_bins), len(self.i_bins))
        data_percentiles_size = (len(self.d_bins), len(self.h_bins), len(self.i_bins), len(self.percentiles))

        # Average values and percentiles.
        self.bin_sizes = np.zeros(data_size)
        self.median_values = dict()
        self.percentiles_values = dict()

        # Calculations for the SNR values
        self.coh_snr = dict()
        self.coh_snr_percentiles = dict()

        nesz_mask = self.nesz_sentinel != 0

        # Prepare output datasets
        for key in self.input_data.keys():

            self.median_values[key] = np.zeros(data_size)
            self.percentiles_values[key] = np.zeros(data_percentiles_size)

            if key in ['amplitude_HH', 'amplitude_HV']:

                self.coh_snr[key] = dict()
                self.coh_snr_percentiles[key] = dict()

                for n_type, harmony_type in enumerate(harmony_types):
                    self.coh_snr[key][harmony_type] = np.zeros(data_size)
                    self.coh_snr_percentiles[key][harmony_type] = np.zeros(data_percentiles_size)

            total_size = self.median_values[key].size
            processed = 0

        sum_input = np.sum(self.input_data['amplitude_HH'], axis=0)

        for n_i, i in enumerate(self.incidence_bins):
            for n_h, h in enumerate(self.height_bins):

                mask_data = np.ravel_multi_index(np.where((self.mask == mask_no) * nesz_mask *
                                                          (self.height > h[0]) * (self.height < h[1]) *
                                                          (self.incidence_angle > i[0]) * (self.incidence_angle < i[1]) *
                                                          (sum_input != 0)), self.image_shape)

                inc = np.ravel(self.incidence_angle)[mask_data]

                dem_data = np.ravel(self.height)[mask_data]

                if len(mask_data) < 50:
                    continue

                for n_t, t in enumerate(self.date_bins):
                    processed += 1
                    print('executed ' + str(processed / total_size * 100)[:4] + ' % of calculation')

                    if key == 'amplitude_ratio':
                        date_key = 'amplitude_HH'
                    elif key == 'coherence_difference':
                        date_key = 'coherence_HH'
                    else:
                        date_key = key

                    date_num = np.where((self.dates[date_key] >= t[0]) * (self.dates[date_key] < t[1]))[0]
                    if len(date_num) == 0:
                        continue

                    # Calculate the affected indices.
                    ids = np.ravel(date_num[:, None] * mask_size + mask_data[None, :])

                    self.bin_sizes[n_t, n_h, n_i] = len(ids)

                    for key in self.input_data.keys():

                        input_data = np.ravel(self.input_data[key])

                        self.median_values[key][n_t, n_h, n_i] = np.median(input_data[ids])
                        for n_per, percentile in enumerate(self.percentiles):
                            self.percentiles_values[key][n_t, n_h, n_i, n_per] = np.percentile(input_data[ids], percentile)

                        if key in ['amplitude_HH', 'amplitude_HV']:

                            for n_type, harmony_type in enumerate(harmony_types):
                                # First prepare SNR and SNR coherence.
                                if harmony_type == 'dual':
                                    nesz_data = self.nesz_dual
                                elif harmony_type == 'ati':
                                    nesz_data = self.nesz_single
                                else:
                                    nesz_data = self.nesz_sentinel

                                nesz = np.ravel(nesz_data)[mask_data]
                                snr = 10 ** ((input_data[ids] - np.tile(nesz, len(date_num))) / 10)
                                coh_snr = 1 / np.sqrt(1 + 1 / snr)

                                self.coh_snr[key][harmony_type][n_t, n_h, n_i] = np.median(coh_snr)

                                for n_per, percentile in enumerate(self.percentiles):
                                    self.coh_snr_percentiles[key][harmony_type][n_t, n_h, n_i, n_per] = np.percentile(coh_snr, percentile)

        # Save calculation using python
        data_file = open(self.result_file, 'wb')
        self.input_data = dict()
        self.nesz_dual = []
        self.nesz_sentinel = []
        self.nesz_single = []
        self.mask = []
        self.height = []
        self.incidence_angle = []

        pickle.dump(self.__dict__, data_file)
        data_file.close()
        self.load_data(load_from_file=True)

    def load_plot_data(self, x_axis='time', harmony_type='dual', select_date=True, select_height=True, select_incidence=False, use_hoa=False,
                       percentiles=None, baseline=100, hoa=100, pen_depth=10, t=20190727, h=100, i=40, min_pix_num=100):
        """
        This function loads the needed data to make a plot.

        :return:
        """

        if percentiles is None:
            percentiles = [5, 95]

        axis_nos = {'time': 0, 'height': 1, 'incidence angle': 2, 'baseline': 3, 'height of ambiguity': 3,
                    'penetration depth': 4}
        axis_vals = {'time': self.d_datetime,
                     'height': self.h_bins,
                     'incidence angle': self.i_bins,
                     'baseline': self.baselines,
                     'height of ambiguity': self.hoa,
                     'penetration depth': self.pen_depths}
        axis_labels = {'time': 'date', 'height': 'height (m)', 'incidence angle': 'incidence angle (degrees)', 'baseline': 'baseline (m)', 'height of ambiguity': 'height of ambiguity (m)',
                    'penetration depth': 'penetration depth (m)'}

        per_1_id = np.where(np.array(self.percentiles) == percentiles[0])[0][0]
        per_2_id = np.where(np.array(self.percentiles) == percentiles[1])[0][0]

        axis_no = axis_nos[x_axis]
        # Only add the percentiles already here.
        s_per_1 = slice(per_1_id, per_1_id + 1)
        s_per_2 = slice(per_2_id, per_2_id + 1)
        s_select = []
        val_names = list(axis_vals.keys())
        if use_hoa:
            dist_type = 'hoa'
            dist = hoa
            d_bins = self.hoa
            val_names.remove('baseline')
        else:
            dist_type = 'baseline'
            dist = baseline
            d_bins = self.baselines
            val_names.remove('height of ambiguity')
        self.axis_lengths = [len(self.date_bins), len(self.h_bins), len(self.i_bins), len(d_bins), len(self.pen_depths)]

        full = slice(None)
        for n_s, [select_data, input_data, val_name, use_vals] in enumerate(zip([t, h, i, dist, pen_depth], [self.date_bins, self.h_bins, self.i_bins, d_bins, self.pen_depths], val_names, [select_date, select_height, select_incidence, True, True])):

            if n_s == axis_no or not use_vals:
                s_select.append(full)        # Meaning all data over this axis.
            else:
                loc = np.where(np.array(input_data) == select_data)[0]
                if len(loc) == 0:
                    raise LookupError(str(select_data) + ' for ' + val_name + ' does not exist. Aborting.')
                else:
                    n = loc[0]
                s_select.append(slice(n, n+1))

        if not select_incidence:
            self.i_weights = (np.sum(self.bin_sizes, axis=(0, 1)) / np.sum(self.bin_sizes))[None, None, :, None, None]
        else:
            self.i_weights = np.array([1])
        if not select_height:
            self.h_weights = (np.sum(self.bin_sizes, axis=(0, 2)) / np.sum(self.bin_sizes))[None, :, None, None, None]
        else:
            self.h_weights = np.array([1])
        if not select_date:
            self.d_weights = (np.sum(self.bin_sizes, axis=(1, 2)) / np.sum(self.bin_sizes))[:, None, None, None, None]
        else:
            self.d_weights = np.array([1])

        dat_select = [s_select[0], s_select[1], s_select[2]]
        percentile_select_1 = [s_select[0], s_select[1], s_select[2], s_per_1]
        percentile_select_2 = [s_select[0], s_select[1], s_select[2], s_per_2]
        coh_select = [s_select[2], s_select[3], s_select[4]]

        # Get the bin sizes of the output values.
        sum_axes = []
        for ax_n in range(3):
            if ax_n != axis_no:
                sum_axes.append(ax_n)
        out_bin_sizes = np.sum(self.bin_sizes, axis=tuple(sum_axes))

        data = dict()
        for pol in ['HH', 'HV']:
        # First get the amplitude

            median_data = self.median_values['amplitude_' + pol][tuple(dat_select)][:, :, :, None, None]
            data['median_' + pol] = self.weighting_values(median_data, axis_no)

            # Select the percentiles
            data['percentiles_1_' + pol] = self.weighting_values(self.percentiles_values['amplitude_' + pol][tuple(percentile_select_1)][:, :, :, :, None], axis_no)
            data['percentiles_2_' + pol] = self.weighting_values(self.percentiles_values['amplitude_' + pol][tuple(percentile_select_2)][:, :, :, :, None], axis_no)

            # Now select the baseline and volume coherences.
            coh_baseline = self.coh_baseline[dist_type][tuple(coh_select)][None, None, :, :, :]
            coh_volume = self.coh_vol[dist_type][tuple(coh_select)][None, None, :, :, :]
            hoa_vals = self.hoa_vals[dist_type][tuple(coh_select)][None, None, :, :, :] * np.ones(median_data.shape)

            # And the SNR and possible the AASR/RASR values
            coh_snr = self.coh_snr['amplitude_' + pol][harmony_type][tuple(dat_select)][:, :, :, None, None]

            # Select the coherence data percentiles
            coh_snr_per_1 = self.coh_snr_percentiles['amplitude_' + pol][harmony_type][tuple(percentile_select_1)][:, :, :, :, None]
            coh_snr_per_2 = self.coh_snr_percentiles['amplitude_' + pol][harmony_type][tuple(percentile_select_2)][:, :, :, :, None]

            # Apply the final calculations and averaging to get the output values
            tot_coh = coh_baseline * coh_volume * coh_snr
            data['coherence_baseline_' + pol] = self.weighting_values(coh_baseline, axis_no)
            data['coherence_vol_' + pol] = self.weighting_values(coh_volume, axis_no)
            data['coherence_snr_' + pol] = self.weighting_values(coh_snr, axis_no)
            data['coherence_' + pol] = self.weighting_values(tot_coh, axis_no)
            data['coh_percentiles_1_' + pol] = self.weighting_values(coh_baseline * coh_volume * coh_snr_per_1, axis_no)
            data['coh_percentiles_2_' + pol] = self.weighting_values(coh_baseline * coh_volume * coh_snr_per_2, axis_no)
            data['hoa_vals'] = self.weighting_values(hoa_vals, axis_no)

            # Based on final found coherences and number of looks, calculate the std in degrees and meters.
            for looks in self.looks:
                std_degrees, std_meters = self.calc_std_from_total_coh(tot_coh, hoa_vals, looks)

                data['std_degrees_' + pol + '_' + str(looks)] = self.weighting_values(std_degrees, axis_no)
                data['std_meters_' + pol + '_' + str(looks)] = self.weighting_values(std_meters, axis_no)

        # Finally replace values with nans where we have zeros or a weight below the minimal weight.
        use_vals = ((data['median_' + pol] != 0) * (out_bin_sizes > min_pix_num))
        for key in data.keys():
            data[key] = data[key][use_vals]

        return data, axis_labels[x_axis], list(np.array(axis_vals[x_axis])[use_vals]), [axis_vals[x_axis][0], axis_vals[x_axis][-1]]

    def weighting_values(self, in_data, axis_no):
        """
        Apply weighting over 3 axis for input values.
        Algorithm always assumes it is the first 3 axes that will be averaged over.

        :return:
        """

        # First weighting of the date, height and incidence axis
        if not axis_no == 0 and in_data.shape[0] > 1:
            in_data = in_data * self.d_weights
        if not axis_no == 1 and in_data.shape[1] > 1:
            in_data = in_data * self.h_weights
        if not axis_no == 2 and in_data.shape[2] > 1:
            in_data = in_data * self.i_weights

        # Then sum over needed axes
        sum_axes = []
        for ax_n in range(5):
            if ax_n != axis_no:
                sum_axes.append(ax_n)

        out_data = np.sum(in_data, axis=tuple(sum_axes))

        # Finally multiply by ones if needed.
        if out_data.size == 1:
            out_data = out_data * np.ones(self.axis_lengths[axis_no])

        return out_data
