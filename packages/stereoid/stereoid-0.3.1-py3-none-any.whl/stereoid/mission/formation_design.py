# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 23:25:50 2016

@author: lope_fr
"""

import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import drama.constants as cnst
from drama.mission.timeline import FormationTimeline
from drama.io import cfg


STEREOID_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
runid = '2019_1'
pardir = os.path.join(STEREOID_dir, 'PAR')
#pltdirr = os.path.join(os.path.join(os.path.join(STEREOID_dir, 'RESULTS'), 'Activation'), runid)
parfile = os.path.join(pardir, ("Hrmny_%s.cfg" % runid))
conf = cfg.ConfigFile(parfile)
form_id = conf.formation.id
savedirr = os.path.join(os.path.join(os.path.join(STEREOID_dir, 'RESULTS'), 'FORMATION'), runid)
savedirr = os.path.join(savedirr, form_id)
wl = cnst.c / 5.4e9
Rnear = 790e3
La = 10
Lsar = wl / La * Rnear
Lburst = Lsar / 4
# Maximum allowed distance
Bw_loss = 0.2 # 20%
# There is a factor 2 due to the bistatic geometry
Bat_max = Bw_loss * Lburst * 2

u = np.linspace(-np.pi, np.pi, 360)
i = np.radians(98)
lat = np.degrees(np.arcsin(np.sin(i) * np.sin(u)))

Bv = np.arange(400, 1800, 200)
du0 = 1200
Bat = 2 * Bv.reshape((Bv.size,1)) * np.cos(u.reshape(1,360)) + du0

# plt.figure()
# for ind in range(Bv.size):
#     plt.plot(Bat[ind], lat, label=("$B_v$ = %4.0f" % Bv[ind]))
# plt.legend()
# plt.ylim(-90, 90)
# plt.grid(b=True, which='major', color='b', linestyle='-')

ftl = FormationTimeline(parfile, secondary=True)
# Plot formation configuration
fontsize = 18
fontweight = 'normal'
matplotlib.rcParams.update({'font.size': fontsize,
                            'font.weight': fontweight})
plt.figure()
lw = 2
plt.plot(ftl.t, ftl.dae, '-', label=r"$a\cdot\Delta e$",
         lw=lw)
plt.plot(ftl.t, np.radians(ftl.domega) * ftl.a, '--',
         label=r"$a\cdot\Delta \Omega$",
         lw=lw)
plt.plot(ftl.t, np.radians(ftl.du * ftl.a), 'k:', label=r"$a\cdot\Delta u$",
         lw=lw)
plt.plot(ftl.t, np.radians(ftl.di * ftl.a), 'r--', label=r"$a\cdot\Delta i$",
         lw=lw)
plt.xlabel('Time [days]', fontsize=fontsize)
plt.ylabel('Formation parameters [m]', fontsize=fontsize)
plt.legend(loc='best', fontsize=fontsize)
plt.xlim((0,365))
plt.grid(True)
plt.tight_layout()
os.makedirs(savedirr, exist_ok=True)
plt.savefig(os.path.join(savedirr, 'Hrmny_formation_conf.png'))
#ftl.reload()
doplevels = [50, 100, 150, 200, 250, 300]
ftl.view_baseline('Doppler', inc=30, ascending=True, vmax=350, clevels=doplevels,
                  savefile=os.path.join(savedirr, 'dDop_IWS_near_asc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS near")
plt.close()
ftl.view_baseline('Doppler', inc=30, ascending=False, vmax=350, clevels=doplevels,
                  savefile=os.path.join(savedirr, 'dDop_IWS_near_dsc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS near")
plt.close()
ftl.view_baseline('Doppler', inc=45, ascending=True, vmax=350, clevels=doplevels,
                  savefile=os.path.join(savedirr, 'dDop_IWS_far_asc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS far")
#plt.close()
ftl.view_baseline('Doppler', inc=45, ascending=False, vmax=350, clevels=doplevels,
                  savefile=os.path.join(savedirr, 'dDop_IWS_far_dsc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS far")
#plt.close()
cmap_hamb = 'plasma_r' #''autumn_r'
hlevels = np.array([30, 40, 60, 70, 80, 90])*4
ftl.view_baseline('h_amb', inc=30, ascending=True, vmin=25, vmax=300,
                  savefile=os.path.join(savedirr, 'h_amb_IWS_near_asc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS near", cmap=cmap_hamb, clevels=hlevels)
ftl.view_baseline('h_amb', inc=30, ascending=False, vmin=25, vmax=100,
                  savefile=os.path.join(savedirr, 'h_amb_IWS_near_dsc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS near", cmap=cmap_hamb, clevels=hlevels)
ftl.view_baseline('h_amb', inc=39, ascending=True, vmin=25, vmax=100,
                  savefile=os.path.join(savedirr, 'h_amb_IWS_mid_asc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS2", cmap=cmap_hamb, clevels=hlevels)
ftl.view_baseline('h_amb', inc=39, ascending=False, vmin=25, vmax=100,
                  savefile=os.path.join(savedirr, 'h_amb_IWS_mid_dsc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS2", cmap=cmap_hamb, clevels=hlevels)
ftl.view_baseline('h_amb', inc=45, ascending=True, vmin=25, vmax=100,
                  savefile=os.path.join(savedirr, 'h_amb_IWS_far_asc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS far", cmap=cmap_hamb, clevels=hlevels)
ftl.view_baseline('h_amb', inc=45, ascending=False, vmin=25, vmax=100,
                  savefile=os.path.join(savedirr, 'h_amb_IWS_far_dsc.png'),
                  contour=True, fontsize=fontsize, titlesufix=", IWS3", cmap=cmap_hamb, clevels=hlevels)

kzlevels = [0.025, 0.05, 0.075, 0.1, 0.125, 0.150, 0.175, 0.2, 0.225, 0.25, 0.275]
ftl.view_baseline('k_z', inc=33, ascending=True, vmin=0, vmax=0.3, clevels=kzlevels,
                  savefile=os.path.join(savedirr, 'k_z_IWS1_asc.png'),
                  cmap='plasma', contour=True, fontsize=fontsize, titlesufix=", IWS1")
ftl.view_baseline('k_z', inc=33, ascending=False, vmin=0, vmax=0.3, clevels=kzlevels,
                  savefile=os.path.join(savedirr, 'k_z_IWS1_dsc.png'),
                  cmap='plasma', contour=True, fontsize=fontsize, titlesufix=", IWS1")
ftl.view_baseline('k_z', inc=39, ascending=True, vmin=0, vmax=0.3, clevels=kzlevels,
                  savefile=os.path.join(savedirr, 'k_z_IWS2_asc.png'),
                  cmap='plasma', contour=True, fontsize=fontsize, titlesufix=", IWS2")
ftl.view_baseline('k_z', inc=39, ascending=False, vmin=0, vmax=0.3, clevels=kzlevels,
                  savefile=os.path.join(savedirr, 'k_z_IWS2_dsc.png'),
                  cmap='plasma', contour=True, fontsize=fontsize, titlesufix=", IWS2")
ftl.view_baseline('df', inc=33, ascending=True, vmax=10, fontsize=fontsize,
                  savefile=os.path.join(savedirr, 'df_asc.png'), contour=True, titlesufix=", IWS1")
ftl.view_baseline('df', inc=33, ascending=False, vmax=10, fontsize=fontsize,
                  savefile=os.path.join(savedirr, 'df_dsc.png'), contour=True, titlesufix=", IWS1")
ftl.view_delta_v(savefile=os.path.join(savedirr, 'delta_v.png'))

# Plot acquisition mask based on delta Doppler and allowing 100 Hz
DopMaskIWS1asc = ftl.acquisition_mask(33, dDoppler_max=100, ascending=True)
DopMaskIWS1dsc = ftl.acquisition_mask(33, dDoppler_max=100, ascending=False)
DopMaskIWS2asc = ftl.acquisition_mask(38, dDoppler_max=100, ascending=True)
DopMaskIWS2dsc = ftl.acquisition_mask(38, dDoppler_max=100, ascending=False)
DopMaskIWS3asc = ftl.acquisition_mask(43, dDoppler_max=100, ascending=True)
DopMaskIWS3dsc = ftl.acquisition_mask(43, dDoppler_max=100, ascending=False)

corners = [0, DopMaskIWS1asc.shape[1] - 1, -90, 90]
plt.figure()
plt.imshow(DopMaskIWS1asc, origin='lower', extent=corners, cmap='winter')
plt.xlabel('Time [days]', fontsize=18)
plt.ylabel('Latitude [deg]', fontsize=18)
plt.title('Ascending acquisition mask, IWS1')
plt.grid(True)
plt.savefig(os.path.join(savedirr, 'Dop100Mask_IWS1_asc'), bbox_inches='tight')
plt.figure()
plt.imshow(DopMaskIWS1dsc, origin='lower', extent=corners, cmap='winter')
plt.xlabel('Time [days]', fontsize=18)
plt.ylabel('Latitude [deg]', fontsize=18)
plt.title('Descending acquisition mask, IWS1')
plt.grid(True)
plt.savefig(os.path.join(savedirr, 'Dop100Mask_IWS1_dsc'), bbox_inches='tight')
plt.figure()
plt.imshow(DopMaskIWS2asc, origin='lower', extent=corners, cmap='winter')
plt.xlabel('Time [days]', fontsize=18)
plt.ylabel('Latitude [deg]', fontsize=18)
plt.title('Ascending acquisition mask, IWS2')
plt.grid(True)
plt.savefig(os.path.join(savedirr, 'Dop100Mask_IWS2_asc'), bbox_inches='tight')
plt.figure()
plt.imshow(DopMaskIWS2dsc, origin='lower', extent=corners, cmap='winter')
plt.xlabel('Time [days]', fontsize=18)
plt.ylabel('Latitude [deg]', fontsize=18)
plt.title('Descending acquisition mask, IWS2')
plt.grid(True)
plt.savefig(os.path.join(savedirr, 'Dop100Mask_IWS2_dsc'), bbox_inches='tight')

# Plot acquisition mask based on delta Doppler and allowing 100 Hz
# DopMaskIWS1asc_str = ftl.acquisition_mask(33, dDoppler_max=750, ascending=True)
# DopMaskIWS1dsc_str = ftl.acquisition_mask(33, dDoppler_max=750, ascending=False)
# plt.figure()
# plt.imshow(DopMaskIWS1asc_str, origin='lower', extent=corners, cmap='winter')
# plt.xlabel('Time [days]', fontsize=18)
# plt.ylabel('Latitude [deg]', fontsize=18)
# plt.title('Ascending acquisition mask, IWS1')
# plt.grid(True)
# plt.savefig(os.path.join(savedirr, 'Dop750Mask_IWS1_asc'), bbox_inches='tight')
# plt.figure()
# plt.imshow(DopMaskIWS1dsc_str, origin='lower', extent=corners, cmap='winter')
# plt.xlabel('Time [days]', fontsize=18)
# plt.ylabel('Latitude [deg]', fontsize=18)
# plt.title('Descending acquisition mask, IWS1')
# plt.grid(True)
# plt.savefig(os.path.join(savedirr, 'Dop750Mask_IWS1_dsc'), bbox_inches='tight')
# plt.close('all')