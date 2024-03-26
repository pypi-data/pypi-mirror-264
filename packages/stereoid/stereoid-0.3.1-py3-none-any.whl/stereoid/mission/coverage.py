# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:40:58 2015

@author: lope_fr
"""

import numpy as np
import os
from drama import coverage as cov
from drama import utils as trutls
from drama.utils.misc import (save_object, load_object)

savedirr = "D:\\WORK\\SESAME\\RESULTS\\COVERAGE\\FIXED_TIMING"
pardir = "D:\\WORK\\SESAME\\PAR"

do_swathInterp = False
sm_inc = np.array([19.99, 26.31, 23.45, 29.50, 29.33, 34.85,
                   34.71, 39.72, 39.62, 44.12, 42.53, 46.73]).reshape((6, 2))
iws_inc = np.array([29.1, 46.0])
iws_sbs_inc = np.array([30.86, 36.69, 36.47, 41.85,
                        41.75, 46.00]).reshape((3, 2))
parFile = os.path.join(pardir, 'SESAME_NoDrift_A.par')
# parFile = trutls.get_parFile()
oneorb = cov.single_swath(look='right', parFile=parFile,
                          inc_angle=[16, 47])
if do_swathInterp:
    swathInterp = cov.swath_interpol(oneorb,  dlat=0.25, dlon=0.1,
                                     maxlat_value=90.)
    os.makedirs(savedirr, exist_ok=True)
    save_object(swathInterp, os.path.join(savedirr,'swath_interp.pkl'))
else:
    swathInterp = load_object(os.path.join(savedirr,'swath_interp.pkl'))
sw = 0
#cov_multiplier = 365./s1cov.repeat_cycle
cov_multiplier = 1
discrete = True
max_cb = 6
#for sw in range(6):
#    s1cov = cov.coverage_analysis(swathInterp, inc_angle_range=sm_inc[sw],
#                                  lon_width=360,
#                                  echo_window='ref_equator')
#    savedir = os.path.join(savedirr, 'SM%i' % sw)
#    cov.coverage_plot(s1cov, continents=True,
#                      cov_multiplier=cov_multiplier,
#                      lat_min=-85, lat_max=85,
#                      max_cb=max_cb, savepath=savedir, discrete=discrete,
#                      grid_spacing=30)
#    cov.coverage_plot(s1cov, continents=True,
#                      cov_multiplier=cov_multiplier,
#                      lat_min=60, projection='npstere',
#                      max_cb=max_cb, savepath=savedir, discrete=discrete,
#                      grid_spacing=30)
#    cov.coverage_plot(s1cov, continents=True,
#                      cov_multiplier=cov_multiplier,
#                      lat_max=-60, projection='spstere',
#                      max_cb=max_cb, savepath=savedir, discrete=discrete,
#                      grid_spacing=30)
#    del s1cov

# IWS for each subswath
IWS_cov = ()
for sw in range(3):
    s1cov = cov.coverage_analysis(swathInterp, inc_angle_range=iws_sbs_inc[sw],
                                  lon_width=360,
                                  echo_window='ref_equator')
    IWS_cov = IWS_cov + (s1cov,)
    savedir = os.path.join(savedirr, 'IWS%i' % sw)
    cov.coverage_plot(s1cov, continents=True,
                      cov_multiplier=cov_multiplier,
                      lat_min=-85, lat_max=85,
                      max_cb=max_cb, savepath=savedir, discrete=discrete,
                      grid_spacing=30)
    cov.coverage_plot(s1cov, continents=True,
                      cov_multiplier=cov_multiplier,
                      lat_min=60, projection='npstere',
                      max_cb=max_cb, savepath=savedir, discrete=discrete,
                      grid_spacing=30)
    cov.coverage_plot(s1cov, continents=True,
                      cov_multiplier=cov_multiplier,
                      lat_max=-60, projection='spstere',
                      max_cb=max_cb, savepath=savedir, discrete=discrete,
                      grid_spacing=30)
    #del s1cov

iws_12 = cov.coverage_add(IWS_cov[0], IWS_cov[1])
savedir = os.path.join(savedirr, 'IWS1-2')
cov.coverage_plot(iws_12, continents=True,
                  cov_multiplier=cov_multiplier,
                  lat_min=-85, lat_max=85,
                  max_cb=max_cb, savepath=savedir, discrete=discrete,
                  grid_spacing=30)
cov.coverage_plot(iws_12, continents=True,
                  cov_multiplier=cov_multiplier,
                  lat_min=60, projection='npstere',
                  max_cb=max_cb, savepath=savedir, discrete=discrete)
cov.coverage_plot(iws_12, continents=True,
                  cov_multiplier=cov_multiplier,
                  lat_max=-60, projection='spstere',
                  max_cb=max_cb, savepath=savedir, discrete=discrete)
del iws_12
iws_13 = cov.coverage_add(IWS_cov[0], IWS_cov[2])
savedir = os.path.join(savedirr, 'IWS1-3')
cov.coverage_plot(iws_13, continents=True,
                  cov_multiplier=cov_multiplier,
                  lat_min=-85, lat_max=85,
                  max_cb=max_cb, savepath=savedir, discrete=discrete,
                  grid_spacing=30)
cov.coverage_plot(iws_13, continents=True,
                  cov_multiplier=cov_multiplier,
                  lat_min=60, projection='npstere',
                  max_cb=max_cb, savepath=savedir, discrete=discrete)
cov.coverage_plot(iws_13, continents=True,
                  cov_multiplier=cov_multiplier,
                  lat_max=-60, projection='spstere',
                  max_cb=max_cb, savepath=savedir, discrete=discrete)
del iws_13
#s1cov = cov.coverage_analysis(swathInterp, inc_angle_range=iws_inc,
#                              lon_width=360,
#                              echo_window='ref_equator')
#savedir = os.path.join(savedirr, 'IWS')
#cov.coverage_plot(s1cov, continents=True,
#                  cov_multiplier=cov_multiplier,
#                  lat_min=-85, lat_max=85,
#                  max_cb=max_cb, savepath=savedir, discrete=discrete,
#                  grid_spacing=30)
#cov.coverage_plot(s1cov, continents=True,
#                  cov_multiplier=cov_multiplier,
#                  lat_min=60, projection='npstere',
#                  max_cb=max_cb, savepath=savedir, discrete=discrete)
#cov.coverage_plot(s1cov, continents=True,
#                  cov_multiplier=cov_multiplier,
#                  lat_max=-60, projection='spstere',
#                  max_cb=max_cb, savepath=savedir, discrete=discrete)