"""
Script to create a few images of the study areas we are looking at.

Test:
stack_folder = '/mnt/f7b747c7-594a-44bb-a62a-a3bf2371d931/radar_datastacks/RIPPL_v2.0/Sentinel_1/east_greenland'
processing_folder = '/home/gert/fast_datastacks'
master_date = '20191001'

shpfile = '/mnt/fcf5fddd-48eb-445a-a9a6-bbbb3400ba42/Data/GIS/shapes/Stereoid_cases/Ice_mask_east_greenland.shp'

Test mac:

import os
from stereoid.land_ice.study_area_plots import StudyAreaPlots

stack_folder = '/Users/gertmulder/surfdrive/TU_Delft/STEREOID/Sentinel_1_Greenland/tiff_files'
processing_folder = '/Users/gertmulder/fast_datastacks'
master_date = '20191001'
study_area = 'east_greenland'
dirname = '/Users/gertmulder/software/stereoid/Notebooks/land_ice'
# os.path.dirname(os.path.realpath('coherence_model.ipynb'))
data_file = os.path.join(dirname, 'study_cases', study_area, 'result.dat')

shapefile = '/Users/gertmulder/surfdrive/TU_Delft/STEREOID/GIS/East_greenland_extend_ice_radar.shp'

plots = StudyAreaPlots(stack_folder, processing_folder, data_file, master_date, shapefile)
plots.plot_NESZ_SNR_Amplitude()
plots.plot_coverage_DEM()

self = plots

"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from shapely.geometry.polygon import LinearRing
from stereoid.land_ice.plot_functions import MidpointNormalize
from stereoid.land_ice.coherence_model_SAR_stack import SARStackCoherence

class StudyAreaPlots():

    def __init__(self, stack_folder, processing_folder, data_file, master_date, shapefile):
        # Load a stack to be able to analyze and plot the data.
        self.data = SARStackCoherence(stack_folder=stack_folder, processing_folder=processing_folder, result_file=data_file,
                                 master_date=master_date, dat_types=['amplitude'])
        self.result_folder = os.path.dirname(data_file)
        self.data.load_data(load_from_file=True)

        self.amplitude = dict()
        self.amplitude['HH'] = self.data.input_data['amplitude_HH']
        self.amplitude['HV'] = self.data.input_data['amplitude_HV']
        self.nesz = self.data.nesz_dual
        self.dem = self.data.height
        self.shape = self.dem.shape
        self.geo_info = self.data.geo_info

        # Define the borders of the image.
        self.dlat = self.geo_info[5]
        self.dlon = self.geo_info[1]
        self.lat_lim = [self.geo_info[3], self.geo_info[3] + self.shape[0] * self.dlat]
        self.lon_lim = [self.geo_info[0], self.geo_info[0] + self.shape[1] * self.dlon]
        # And the latitudes/longitudes
        self.lats = self.lat_lim[0] + np.arange(self.shape[0]) * self.dlat
        self.lons = self.lon_lim[0] + np.arange(self.shape[1]) * self.dlon
        self.lon_grid, self.lat_grid = np.meshgrid(self.lons, self.lats)
        self.lat_shift = np.diff(self.lat_lim)[0] * 0.1
        self.lon_shift = np.diff(self.lon_lim)[0] * 0.1
        self.image_limits = [self.lon_lim[0] - self.lon_shift, self.lon_lim[1] + self.lon_shift,
                             self.lat_lim[0] - self.lat_shift, self.lat_lim[1] + self.lat_shift]

        # Information from shapefile
        self.shapefile = shapefile

    def plot_NESZ_SNR_Amplitude(self, low_percentage=10, correct_empty=False):
        """
        Plot a number

        :param low_percentage:
        :return:
        """

        # Plot for NESZ
        self.nesz[self.nesz == 0] = np.nan
        fig, ax_nesz = self.create_base_image()
        ax_nesz.set_title('NESZ for Harmony XTI')
        data = ax_nesz.pcolormesh(self.lon_grid, self.lat_grid, np.flipud(self.nesz), cmap='Greys_r',
                                  zorder=6, transform=ccrs.PlateCarree())
        cbar = plt.colorbar(data, ax=ax_nesz, shrink=0.6)
        cbar.set_label('NESZ XTI Harmony (dB)')
        self.add_inset(fig, ax_nesz, ccrs.Mercator())
        fig.savefig(os.path.join(self.result_folder, 'plot_nesz_ATI.png'), bbox_inches='tight', pad_inches=0.2)

        for amplitude_type in ['HH', 'HV']:
            # First detect the empty slices
            amplitude = self.amplitude[amplitude_type]

            # Next step only needed if you expect a lot of empty layers
            if correct_empty:
                zero_layers = len(np.where(np.sum(np.sum(amplitude, axis=2), axis=1) == 0)[0])
            else:
                zero_layers = 0

            # select which nth value we need.
            low_percentile = low_percentage + int(np.round(zero_layers / amplitude.shape[0] * 100))

            # Get the amplitude
            scaled_amplitude = np.percentile(amplitude, low_percentile, axis=0)
            median_amplitude = np.median(amplitude, axis=0)

            # Finally create the plots.
            # max_val = np.maximum(np.max(scaled_amplitude), np.max(self.nesz))
            # min_val = np.minimum(np.min(scaled_amplitude), np.min(self.nesz))

            # Plot for median amplitude
            median_amplitude[median_amplitude == 0] = np.nan
            fig, ax_amp = self.create_base_image()
            ax_amp.set_title('Median amplitude of Sentinel-1 stack for ' + amplitude_type)
            data = ax_amp.pcolormesh(self.lon_grid, self.lat_grid, median_amplitude, cmap='Greys_r',
                                      zorder=6, transform=ccrs.PlateCarree(),
                                     vmin=np.nanpercentile(median_amplitude, 1), vmax=np.nanpercentile(median_amplitude, 99))
            cbar = plt.colorbar(data, shrink=0.6)
            cbar.set_label('Amplitude (dB)')
            self.add_inset(fig, ax_amp, ccrs.Mercator())
            fig.savefig(os.path.join(self.result_folder, 'plot_median_amplitude_' + amplitude_type + '.png'), bbox_inches='tight', pad_inches=0.2)

            # Plot for scaled amplitude
            scaled_amplitude[scaled_amplitude == 0] = np.nan
            fig, ax_amp = self.create_base_image()
            ax_amp.set_title('Amplitude of ' + str(low_percentile) + 'th percentile for ' + amplitude_type)
            data = ax_amp.pcolormesh(self.lon_grid, self.lat_grid, scaled_amplitude, cmap='Greys_r',
                                      zorder=6, transform=ccrs.PlateCarree(),
                                     vmin=np.nanpercentile(scaled_amplitude, 1), vmax=np.nanpercentile(scaled_amplitude, 99))
            cbar = plt.colorbar(data, shrink=0.6)
            cbar.set_label('Amplitude (dB)')
            self.add_inset(fig, ax_amp, ccrs.Mercator())
            fig.savefig(os.path.join(self.result_folder, 'plot_amplitude_' + str(low_percentile) + 'th_percentile_' + amplitude_type + '.png'), bbox_inches='tight', pad_inches=0.2)

            scaled_SNR = scaled_amplitude - np.flipud(self.nesz)
            norm = MidpointNormalize(vmin=np.nanpercentile(scaled_SNR, 2), vmax=np.nanpercentile(scaled_SNR, 98))
            norm.clip = True

            fig, ax_snr = self.create_base_image()
            ax_snr.set_title('SNR of ' + str(low_percentile) + 'th percentile for ' + amplitude_type)
            data = ax_snr.pcolormesh(self.lon_grid, self.lat_grid, scaled_SNR, cmap='RdBu', norm=norm,
                                      zorder=6, transform=ccrs.PlateCarree())
            data.cmap.set_under(color='black', alpha=0)
            cbar = plt.colorbar(data, shrink=0.6)
            cbar.set_label('SNR (dB)')
            self.add_inset(fig, ax_snr, ccrs.Mercator())
            fig.savefig(os.path.join(self.result_folder, 'plot_SNR_' + str(low_percentile) + 'th_percentile_' + amplitude_type + '.png'), bbox_inches='tight', pad_inches=0.2)

    def plot_coverage_DEM(self):
        """
        This script will create an image of the area with the covering DEM and shapefiles.

        :return:
        """

        fig, ax_dem = self.create_base_image(False)
        ax_dem.set_title('DEM and glacier coverage of region')
        data = ax_dem.pcolormesh(self.lon_grid, self.lat_grid, self.dem, cmap='terrain',
                                  zorder=2, transform=ccrs.PlateCarree())
        cbar = plt.colorbar(data, shrink=0.8)
        cbar.set_label('DEM height (m)')

        # Now add the glacier coverage
        shapes = [shape for shape in shpreader.Reader(self.shapefile).geometries()]

        ax_dem.add_geometries([shapes[0]], edgecolor='black', facecolor="none", zorder=20,
                              linewidth=1, crs=ccrs.PlateCarree())
        ax_dem.add_geometries([shapes[1]], edgecolor='red', facecolor="none", zorder=21, linewidth=1, crs=ccrs.PlateCarree())
        self.add_inset(fig, ax_dem, ccrs.Mercator())
        fig.savefig(os.path.join(self.result_folder, 'DEM_glacier_extend.png'), bbox_inches='tight', pad_inches=0.2)

    def create_base_image(self, margins=False):
        """
        Create base image, which is used as a base for the other images.

        :parameter bool margins: Turn on or off added margins of 0.1 the size of the full image

        :return:
        """

        ocean_10m = cfeature.NaturalEarthFeature('physical', 'ocean', '10m',
                                                edgecolor='face',
                                                facecolor=cfeature.COLORS['water'])
        land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                                edgecolor='face',
                                                facecolor=cfeature.COLORS['land'])
        crs = ccrs.Mercator()

        fig = plt.figure(figsize=(6, 8))
        ax = fig.add_subplot(111, projection=crs)
        ax.coastlines(resolution='10m', zorder=10, alpha=0.5)
        ax.add_feature(ocean_10m, zorder=5)
        ax.add_feature(land_10m, zorder=1)
        if margins:
            ax.set_extent(self.image_limits)
        else:
            ax.set_extent([self.lon_lim[0], self.lon_lim[1], self.lat_lim[0], self.lat_lim[1]])
        self.add_coor_ticks(ax, crs=ccrs.PlateCarree())

        return fig, ax

    def add_inset(self, fig, ax, crs):
        """

        :param fig:
        :param ax:
        :param crs:
        :return:
        """

        ax2 = fig.add_axes([0.8, 0.8, 0.2, 0.2], projection=crs)
        ax2.set_extent([self.lon_lim[0] - 30,
                        self.lon_lim[1] + 30,
                        np.maximum(self.lat_lim[0] - 20, -90),
                        np.minimum(self.lat_lim[1] + 20, 90)])
        lat_shift = np.diff(self.lat_lim)[0] * 0.05
        lon_shift = np.diff(self.lon_lim)[0] * 0.05
        ring = LinearRing(list(zip(
            [self.lon_lim[0] - lon_shift, self.lon_lim[0] - lon_shift, self.lon_lim[1] + lon_shift,
             self.lon_lim[1] + lon_shift],
            [self.lat_lim[0] - lat_shift, self.lat_lim[1] + lat_shift, self.lat_lim[1] + lat_shift,
             self.lat_lim[0] - lat_shift])))
        ax2.add_geometries([ring], ccrs.PlateCarree(), facecolor='none', edgecolor='red', linewidth=0.75)
        ax2.coastlines()
        ax2.stock_img()

        p1 = ax.get_position()
        p2 = ax2.get_position()
        ax2.set_position([p1.x0, p1.y1 - p2.height, p2.width, p2.height])

        return ax2

    def add_coor_ticks(self, ax, crs):
        """

        :param ax:
        :param crs:
        :return:
        """

        gl = ax.gridlines(crs=crs, draw_labels=True, alpha=0.5)
        gl.xlabels_top = None
        gl.ylabels_right = None
        xgrid = np.arange(np.floor(self.lon_lim[0]) - 10, np.ceil(self.lon_lim[1]) + 10, 2)
        ygrid = np.arange(np.floor(np.min(self.lat_lim)) - 10, np.ceil(np.max(self.lat_lim)) + 10, 1)
        gl.xlocator = mticker.FixedLocator(xgrid.tolist())
        gl.ylocator = mticker.FixedLocator(ygrid.tolist())
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 11, 'color': 'black'}
        gl.ylabel_style = {'size': 11, 'color': 'black'}
