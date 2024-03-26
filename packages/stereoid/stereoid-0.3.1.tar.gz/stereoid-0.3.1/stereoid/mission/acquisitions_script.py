# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:05:46 2016

@author: lope_fr
"""

import numpy as np
from matplotlib import pyplot as plt
import os
from drama.utils.misc import (save_object, load_object)
from drama.utils.read_masks import read_mask
from drama.io import cfg
from drama.performance.sar import SARModeFromCfg
import drama.geo as sargeo
from drama.coverage.activation import (RoI_in_view, GS_in_view,
                                       contact_plot, DailyLatMask,
                                       CompositeOrbTimeline,
                                       GlobalCompositeOrbTimeline)
import drama.coverage as cov
from drama.mission.timeline import (FormationTimeline, LatLonTimeline)
from stereoid.mission.activation_analysis import (
    activation_temp_prof, memory_profile)
import copy

STEREOID_dir = "/home/atheodosiou/Code/stereoid/"
runid = '2019_1'
pardir = os.path.join(STEREOID_dir, 'PAR')
savedirr = os.path.join(os.path.join(
    os.path.join(STEREOID_dir, 'RESULTS'), 'DUTY'), runid)
pltdirr = os.path.join(os.path.join(os.path.join(
    STEREOID_dir, 'RESULTS'), 'Activation'), runid)
parfile = os.path.join(pardir, ("Hrmny_%s.cfg" % runid))

conf = cfg.ConfigFile(parfile)
swth = 0
maskpath = os.path.join(os.path.join(STEREOID_dir, 'DATA'), 'Masks')
Svalbard = [78, 15, 460]
Matera = [40.6, 16.5, 400]
Troll = [-72, 2.5, 1298]
Neustrelitz = [53 + 19.7/60, 13 + 4/60]
Inuvik = [68 + 24/60, -133 - 30/60]
OHiggins = [-63 - 19/60, -57 - 54/60]

h_amb_range = (15, 100)

do_swathInterp = True
do_calculate_masks = True
do_plot_GSs = True
do_memory_profile = True
do_activation_profile = True
do_activation_masks = True
do_acqtimeline = True

# forest_mask_name = 'Boreal'  # Or just "Forest"
modename = 'IWS'
mode = SARModeFromCfg(conf, modename)

nmodes = mode.prfs.size
# SolidEarthViews = ()
# ForestViews = ()
# PermafrostViews = ()

if do_calculate_masks:
    for swth in range(3):
        SolidEarthView = RoI_in_view(parfile,
                                     inc_range=[mode.incs[swth, 0],
                                                mode.incs[swth, 1]],
                                     echo_window='ref_equator',
                                     mask_path=maskpath,
                                     mask_name=('mountain', 'cryo_boundary'))
        PermafrostView = RoI_in_view(parfile,
                                     inc_range=[mode.incs[swth, 0],
                                                mode.incs[swth, 1]],
                                     echo_window='ref_equator',
                                     mask_path=maskpath,
                                     mask_name='permafrost')

        os.makedirs(savedirr, exist_ok=True)
        file = ('SolidEarthView_%i.pkl' % int(swth))
        save_object(SolidEarthView, os.path.join(savedirr, file))
        # save_object(SolidEarthView2, os.path.join(savedirr, 'SolidEarthView2.pkl'))
        file = ('PermafrostView_%i.pkl' % int(swth))
        save_object(PermafrostView, os.path.join(savedirr, file))
        print("Removing SolidEarthView from PermafrostView")
        PermafrostView.inRoI[:, :] = np.logical_and(PermafrostView.inRoI,
                                                    np.logical_not(SolidEarthView.inRoI))

        if swth == 0:
            SolidEarthViews = SolidEarthView
            PermafrostViews = PermafrostView
        else:
            SolidEarthViews.or_mask(SolidEarthView)
            PermafrostViews.or_mask(PermafrostView)
else:
    for swth in range(3):
        file = ('SolidEarthView_%i.pkl' % int(swth))
        SolidEarthView = load_object(os.path.join(savedirr, file))
        file = ('PermafrostView_%i.pkl' % int(swth))
        PermafrostView = load_object(os.path.join(savedirr, file))
        print("Removing SolidEarthView from PermafrostView")
        PermafrostView.inRoI[:, :] = np.logical_and(PermafrostView.inRoI,
                                                    np.logical_not(SolidEarthView.
                                                                   inRoI))
        if swth == 0:
            SolidEarthViews = SolidEarthView
            PermafrostViews = PermafrostView
        else:
            SolidEarthViews.or_mask(SolidEarthView)
            PermafrostViews.or_mask(PermafrostView)

# Ground statinons contacts
Svalbard_view = GS_in_view(parfile, Svalbard[0], Svalbard[1],
                           elev_min=5)
Inuvik_view = GS_in_view(parfile, Inuvik[0], Inuvik[1],
                         elev_min=5)
OHiggins_view = GS_in_view(parfile, OHiggins[0], OHiggins[1],
                           elev_min=5)
Troll_view = GS_in_view(parfile, Troll[0], Troll[1],
                        elev_min=5)
# Formation timeline
ftl = FormationTimeline(parfile, secondary=True)
# Acquisitions masks based on baseline

# Height of ambiguity mask adapted to height profile
# Increases h_amb allowed between 20S and 40N

# for swth in range(nmodes):
inc_ref = (mode.incs[0, 0] + mode.incs[-1, 1])/2
DopMaskIWSasc = ftl.acquisition_mask(inc_ref, dDoppler_max=120,
                                     ascending=True,
                                     h_amb_range=h_amb_range)
# DopMaskIWSasc = DopMaskIWSasc + (DopMaskIWS_,)
DopMaskIWSdsc = ftl.acquisition_mask(inc_ref, dDoppler_max=120,
                                     ascending=False,
                                     h_amb_range=h_amb_range)
# DopMaskIWSdsc = DopMaskIWSdsc + (DopMaskIWS_,)

# Daily latlon mask according to phasing
LatDayPhaseMask = np.ones(DopMaskIWSasc.shape, dtype='bool')
# First 72 days, exclude Acquistions below 50S
LatDayPhaseMask[0:90 + 45, 0:72] = False
# Eliminate all swath 2 acquisitions above 70N
LatDayPolarMask = np.empty_like(LatDayPhaseMask)

# Copy phase mask into Polar-specific mask
LatDayPolarMask[:, :] = LatDayPhaseMask[:, :]
# Limit to polarphases
LatDayPolarMask[:, 72:180] = False
LatDayPolarMask[:, 252:-1] = False

# Same between day 180 and 252, for acquisitions above 50N
LatDayPhaseMask[55:, 204:252] = False

LatDayPermafrostPhaseMask = np.ones(DopMaskIWSasc.shape,
                                    dtype='bool')

LatDayPermafrostMask = np.ones_like(LatDayPhaseMask, dtype='bool')
LatDayPermafrostMask[:, 120:204] = False
# Eliminate all swath 2 acquisitions above 70N
LatDayPermafrostMask[90+70:, :] = False
# Eliminate all swath 3 acquisitions between 30N and 60N
LatDayPermafrostMask[90 + 30:90 + 70, :] = False
# Eliminate all swath 3 acquisitions between 30S and 45S

#LatDayForestPhaseMask[:, 0:72] = False
#LatDayForestPhaseMask[:, 180:252] = False
# Merge Phase mask with formation masks
# TODO
SolidEarthPlan = ()
ForestPlan = ()
PermafrostPlan = ()
for swth in range(nmodes):
    LatDayMaskIWSasc = np.logical_and(DopMaskIWSasc[swth],
                                      LatDayPhaseMask[swth])
    LatDayMaskIWSdsc = np.logical_and(DopMaskIWSdsc[swth],
                                      LatDayPhaseMask[swth])
    inc_ref = (mode.incs[swth, 0] + mode.incs[swth, 1])/2
# BUG: DailyLatMask expects mask_asc and mask_dsc to be 2d arrays
# where the first dimension spans latitudes between -90 and 90 degrees
# and the second is a time index. LatDayMaskIWSasc and
# LatDayMaskIWSdsc have shape (360,)
    SolidEarthPlan_ = DailyLatMask(parfile,
                                   LatDayMaskIWSasc,
                                   LatDayMaskIWSdsc,
                                   (0, 29), inc_ref,
                                   echo_window='ref_equator')
    SolidEarthPlan_.and_mask(SolidEarthViews[swth])
    SolidEarthPlan = SolidEarthPlan + (SolidEarthPlan_,)
    # Permafrost
    # Not applying any restriction here!
    # Forest
    LatDayMaskIWSasc = np.logical_and(DopMaskIWSasc[swth],
                                      LatDayPermafrostMask[swth])
    LatDayMaskIWSdsc = np.logical_and(DopMaskIWSdsc[swth],
                                      LatDayPermafrostMask[swth])
    PermafrostPlan_ = DailyLatMask(parfile,
                                   LatDayMaskIWSasc,
                                   LatDayMaskIWSdsc,
                                   (0, 29), inc_ref,
                                   echo_window='ref_equator')
    PermafrostPlan_.and_mask(PermafrostViews[swth])
    PermafrostPlan = PermafrostPlan + (PermafrostPlan_,)

# Generate vector relating orbit number to subswath
# In this case a totally idiotic cyclic mode
cyclic_mode = np.zeros(30, dtype=np.int)
# Alternate between subswath 1 and 3 in first 6 cycles and the
# 6 polar cycles starting at cycle 15
cyclic_mode[0:6] = 2 * np.mod(np.arange(6, dtype=np.int), 2) + 1
cyclic_mode[15:21] = 2 * np.mod(np.arange(6, dtype=np.int), 2) + 1
# Cycle over subswathes 1-3 the rest of the time
cyclic_mode = np.where(cyclic_mode == 0,
                       np.mod(np.arange(30, dtype=np.int), 3) + 1,
                       cyclic_mode)
# cyclic_mode[18] = 1
cyclic_mode[16] = 1
Norb = SolidEarthPlan[0].inMask.shape[1]
cyclic_mode = cyclic_mode.reshape((30, 1)) + np.zeros((1, Norb), dtype=np.int)
sec = cyclic_mode[6:15, :] + np.arange(Norb, dtype=np.int).reshape((1, Norb))
sec = np.mod(sec - 1, 3) + 1
cyclic_mode[6:15, :] = sec
cyclic_mode[21:30, :] = sec
cyclic_mode = cyclic_mode.reshape((30, Norb, 1))
SolidEarthPlan_all = CompositeOrbTimeline(SolidEarthPlan, cyclic_mode)
PermafrostPlan_all = CompositeOrbTimeline(PermafrostPlan, cyclic_mode)
GlobalPlan = GlobalCompositeOrbTimeline(ForestPlan, cyclic_mode,
                                        SolidEarthPlan,
                                        PermafrostPlan)

# Down link scenario
Svalbard_use = np.zeros(30, dtype='bool')
Svalbard_use[:] = True
Svalbard_use = Svalbard_use.reshape((30, 1))
OHiggins_use = np.logical_not(Svalbard_use)
#OHiggins_use[0:15] = True
#OHiggins_use = OHiggins_use.reshape((30, 1))
Troll_use = OHiggins_use
OHiggins_or_Troll = (OHiggins_view.contact_length >= Troll_view.contact_length)
# OHiggins_or_Troll[:] = False
OHiggins_or_Troll = OHiggins_or_Troll.reshape((1,
                                               OHiggins_view.contact.shape[0]))
OHiggins_use = np.logical_and(OHiggins_use, OHiggins_or_Troll)
Troll_use = np.logical_and(Troll_use, np.logical_not(OHiggins_or_Troll))
gs_sel_mask = (Svalbard_use, OHiggins_use, Troll_use)
gs_contact = (Svalbard_view, OHiggins_view, Troll_view)
os.makedirs(pltdirr, exist_ok=True)
if do_plot_GSs:
    OHiggins_or_Troll = OHiggins_or_Troll.reshape((OHiggins_or_Troll.size, 1))
    contact_plot(parfile, (Svalbard_view.contact,
                           np.logical_and(OHiggins_view.contact,
                                          OHiggins_or_Troll),
                           np.logical_and(Troll_view.contact,
                                          np.logical_not(OHiggins_or_Troll))),
                 fontsize=10)
    plt.savefig(os.path.join(pltdirr, 'SvalbardOHigginsTroll'),
                bbox_inches='tight', dpi=150)
if do_swathInterp:
    track_grid = cov.swath_interpol(ftl.track,  dlat=0.25, dlon=0.1,
                                    maxlat_value=90.)
    track_grid_prim = cov.swath_interpol(ftl.track_prim,
                                         dlat=0.25, dlon=0.1,
                                         maxlat_value=90.)
    os.makedirs(savedirr, exist_ok=True)
    save_object(track_grid, os.path.join(savedirr, 'track_grid.pkl'))
    save_object(track_grid_prim, os.path.join(savedirr, 'track_grid_prim.pkl'))
else:
    track_grid = load_object(os.path.join(savedirr, 'track_grid.pkl'))
    track_grid_prim = load_object(os.path.join(savedirr,
                                               'track_grid_prim.pkl'))
if do_memory_profile:
    memory_profile(SolidEarthPlan_all.mode +
                   PermafrostPlan_all.mode, 1,
                   track_grid.Torb, gs_contact, gs_sel_mask,
                   memlimit=[256, 512], down_link_rate=400)

if do_activation_profile:
    activation_temp_prof((SolidEarthPlan_all,
                          PermafrostPlan_all), 1, 24*3600,
                         title="Daily",
                         plan_names=('Solid Earth', 'Permafrost'))

if do_activation_masks:
    for swth in range(3):
        contact_plot(parfile, (SolidEarthViews[swth].inRoI,
                               PermafrostViews[swth].inRoI,
                               ForestViews[swth].inRoI),
                     colors=('m', 'teal', 'olive'), fontsize=10)
        file = ("RoI_view_sw%i.png" % int(swth))
        plt.savefig(os.path.join(pltdirr, file), bbox_inches='tight', dpi=150)
        plt.close()
    for c in range(30):
        contact_plot(parfile, (SolidEarthPlan_all.inMask[c],
                               PermafrostPlan_all.inMask[c]),
                     colors=('m', 'teal', 'olive'), fontsize=10)
        file = ("AcqPlan_cyc%i.png" % int(1000 + c))
        plt.savefig(os.path.join(pltdirr, file), bbox_inches='tight', dpi=150)
        plt.close()

if do_acqtimeline:
    # Compute the slant ranges defining the echo windows, hopefully at
    # equator
    mode_echo_windows = sargeo.inc_to_sr(
        np.radians(mode.incs), track_grid.Horb)
    lats_ = np.linspace(-80, 80, 321)
    lats = lats_.reshape((321, 1)) + np.zeros((1, 720))
    lons_ = np.linspace(-180, 179, 720)
    lons = lons_.reshape((1, 720)) + np.zeros((321, 1))
    landmask = read_mask(lats_, lons_, maskpath)
    mlats = lats[np.where(landmask)]
    mlons = lons[np.where(landmask)]
    # The timeline goes fast because the track_grid and track_grid_prim
    # Have been precalculated
    tl = LatLonTimeline(parfile, mlats, mlons, form=ftl,
                        inc_angle_range=[mode.incs[0, 0] -
                                         5, mode.incs[-1, 1] + 5],
                        track_grid=track_grid,
                        track_grid_prim=track_grid_prim)
    # Merge acquisition timeline with tl
    tl.OrbTimeline_merge(GlobalPlan, mode_echo_windows, 'echo_window')
#    tl.OrbTimeline_merge(SolidEarthPlan, mode_echo_windows, 'echo_window')
#    tl_forest = copy.deepcopy(tl)
#    tl_forest.OrbTimeline_merge(ForestPlan, mode_echo_windows, 'echo_window')
    save_object(tl, os.path.join(savedirr, 'acquisition_timeline.pkl'))
