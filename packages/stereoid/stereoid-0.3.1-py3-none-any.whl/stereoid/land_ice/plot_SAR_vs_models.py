
from stereoid.land_ice.coherence_model_SAR_stack import SARStackCoherence
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os


# First create the two year plots over East Greenland
stack_folder = '/Users/gertmulder/surfdrive/TU_Delft/STEREOID/Sentinel_1_Greenland/tiff_files'
processing_folder = '/Users/gertmulder/fast_datastacks'
master_date = '20191001'
study_area = 'east_greenland'
dirname = '/Users/gertmulder/Software/stereoid/Notebooks/land_ice'
# os.path.dirname(os.path.realpath('coherence_model.ipynb'))
data_file = os.path.join(dirname, 'study_cases', 'result_' + study_area + '.dat')

baselines = np.arange(50, 1500, 50)
penetration_depths = np.arange(20)
looks = [1, 10, 100]
hoas = np.arange(5, 100, 5)
# min/max EW (19-47), min/max IW (30, 46)
incidence_angles = np.arange(30, 46)
looks = [1, 10, 100]
percentiles = [5, 95]

d_t = 15        # 15 days
d_i = 1         # 1 degree
d_h = 200       # 200 meter

data = SARStackCoherence(stack_folder=stack_folder, processing_folder=processing_folder, result_file=data_file,
                         master_date=master_date, dat_types=['amplitude'])
data.load_data(load_from_file=True)

# data(d_t, d_i, d_h, baselines, penetration_depths, hoas, looks, mask_no=3)

d_t = True
d_h = True
d_i = False
plot_data = SARStackCoherence(stack_folder=stack_folder, processing_folder=processing_folder, master_date=master_date)
plots = plot_data.dynamic_plot(data, x_axis='time', baseline=500, pen_depth=10, hoa=50, t=20190727, h=100, i=40,
                               looks=[1, 10, 100], percentiles=[5, 95], d_t=d_t, d_h=d_h, d_i=d_i, use_hoa=False)

# First we try with a time interval of 90 days, a incidence interval of 1 degree and a height interval of 200 meter.
data(d_t=90, d_i=1, d_h=200)

# Apply the same thing for the NEGIS region
stack_folder = '/mnt/f7b747c7-594a-44bb-a62a-a3bf2371d931/radar_datastacks/RIPPL_v2.0/Sentinel_1/negis_greenland'
processing_folder = '/home/gert/fast_datastacks'
master_date = '20190210'

data = LoadTiffsStack(stack_folder=stack_folder, processing_folder=processing_folder, master_date=master_date)
data.load_data(resolution=[0.001, 0.0005])
data(6, 20, 100, mask_no=1)

SARModelPlots.plot_amplitude_coherence_movies(data)
SARModelPlots.plot_combined_amplitude_coherence_movies(data)

