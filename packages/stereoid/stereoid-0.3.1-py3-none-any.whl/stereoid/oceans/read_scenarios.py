__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

import os
from typing import Optional

import numpy as np
import scipy.io as spio
import xarray as xr
from matplotlib import pyplot as plt
from scipy import ndimage

from drama import constants as cnst
from drama import utils as drtls

def dummy_wind_adjustment(u_in, v_in):
    return 0.95 * u_in, 0.95 * v_in

def read_scenario_DALES_KNMI(ncfile, smp_out=500, wind_adjustment_func=dummy_wind_adjustment, SST0=292,
                             rot_angle: Optional[float] = 0, add_margin=22e3):
    swind = xr.open_dataset(ncfile)
    dx =1e3*(swind.cross_track.values[1] - swind.cross_track.values[0])
    u = np.flip(np.transpose(swind.U10.values), axis=1)
    v = np.flip(np.transpose(swind.V10.values), axis=1)
    z = np.flip(np.transpose(swind.Wind_height.values), axis=1)
    u, v = wind_adjustment_func(u, v)
    w = np.flip(np.transpose(swind.w10.values), axis=1)
    lat = np.flip(np.transpose(swind.latitude.values), axis=1)
    lon = np.flip(np.transpose(swind.longitude.values), axis=1)
    if int(np.floor(smp_out/dx)) > 1:
        dec = int(np.floor(smp_out/dx))
        smp_out = dec * dx
        smp0 = int(dec/2)
        u = drtls.smooth(u, dec)
        v = drtls.smooth(v, dec)
        w = drtls.smooth(w, dec)
        u=u[smp0:-1:dec, smp0:-1:dec]
        v=v[smp0:-1:dec, smp0:-1:dec]
        w=w[smp0:-1:dec, smp0:-1:dec]
        lat=lat[smp0:-1:dec, smp0:-1:dec]
        lon=lon[smp0:-1:dec, smp0:-1:dec]

    if int(add_margin/smp_out) > 0:
        shp = u.shape
        asmpl = int(add_margin/smp_out)
        shp_out = (shp[0] + 2 * asmpl,
                   shp[1]+  2 * asmpl)
        u_ = np.zeros(shp_out) + np.mean(u)
        u_[asmpl:asmpl+shp[0], asmpl:asmpl+shp[1]] = u
        u = u_
        v_ = np.zeros(shp_out) + np.mean(v)
        v_[asmpl:asmpl+shp[0], asmpl:asmpl+shp[1]] = v
        v = v_

        lat_ = np.arange(shp_out[0]) * (lat[1,0] - lat[0,0])
        lat = lat_.reshape((shp_out[0],1)) + np.zeros_like(u) - lat_[asmpl] + lat[0,0]
        lon_ = np.arange(shp_out[1]) * (lon[0,1] - lon[0,0])
        lon = lon_.reshape((1,shp_out[1])) + np.zeros_like(u) - lon_[asmpl] + lon[0,0]

    wind_v = np.stack([u,v], axis=-1)
    tsc_v = np.zeros_like(wind_v)
    sst = np.zeros_like(u) + SST0

    if rot_angle != 0:
        wind_v[np.isnan(wind_v)] = 0
        tsc_v[np.isnan(tsc_v)] = 0
        sst[np.isnan(sst)] = 25
        wind_v = np.stack([ndimage.rotate(wind_v[:, :, 0], rot_angle),
                           ndimage.rotate(wind_v[:, :, 1], rot_angle)], axis=-1)
        tsc_v = np.stack([ndimage.rotate(tsc_v[:, :, 0], rot_angle),
                          ndimage.rotate(tsc_v[:, :, 1], rot_angle)], axis=-1)
        sst = ndimage.rotate(sst, rot_angle)
        lat = ndimage.rotate(lat, rot_angle)
        lon = ndimage.rotate(lon, rot_angle)
        rot_m = np.array([[np.cos(np.radians(rot_angle)), np.sin(np.radians(rot_angle))],
                          [-np.sin(np.radians(rot_angle)), np.cos(np.radians(rot_angle))]])
        wind_v = np.einsum("lk,ijk->ijl", rot_m, wind_v)
        tsc_v = np.einsum("lk,ijk->ijl", rot_m, tsc_v)


    dic_out = {'tsc': tsc_v, 'wnd': wind_v, 'sst': sst,
               'lon': lon, 'lat': lat, 'grid_spacing': smp_out}
    return dic_out, smp_out


def read_tsc_wind_from_mat(matfile, smp_out=None):
    """
    Read tsc and wind from mat file (in Claudia Pasquero's format)
    :param matfile:
    :return:
    """
    scn = spio.loadmat(matfile)
    tsc_v = np.zeros(scn['usfc'].shape + (2,))
    wind_v = np.zeros_like(tsc_v)
    tsc_v[:, :, 0] = scn['usfc']
    tsc_v[:, :, 1] = scn['vsfc']
    wind_v[:, :, 0] = scn['uwind']
    wind_v[:, :, 1] = scn['vwind']
    lat = scn['lat']
    lon = scn['lon']
    dx = np.radians(lon[0,1] - lon[0,0]) * cnst.r_earth
    dy = np.radians(lat[1, 0] - lat[0, 0]) * cnst.r_earth
    if smp_out is None:
        smp_out = dx
    else:
        # Resample
        nxo = int(np.floor(tsc_v.shape[1] * dx / smp_out))
        nyo = int(np.floor(tsc_v.shape[0] * dy / smp_out))
        xo = np.arange(nxo) * smp_out / dx
        yo = np.arange(nyo) * smp_out / dy
        wind_v = drtls.linresample(drtls.linresample(wind_v, xo, axis=1, extrapolate=True),
                                   yo, axis=0, extrapolate=True)
        tsc_v = drtls.linresample(drtls.linresample(tsc_v, xo, axis=1, extrapolate=True),
                                  yo, axis=0, extrapolate=True)



    return tsc_v, wind_v, smp_out

#%%

if __name__ == '__main__':

    surfwinds = '/Users/plopezdekker/Documents/WORK/STEREOID/DATA/TIR/DALES/DALES_HR_model/Dales_36_hrs_12_01_00_surface_winds.nc'
    surfwinds_130 = '/Users/plopezdekker/Documents/WORK/STEREOID/DATA/TIR/DALES/DALES_HR_model/Dales_36_hrs_12_03_10_surface_winds.nc'
    swind = xr.open_dataset(surfwinds)
    swind_130  = xr.open_dataset(surfwinds_130)
    dls, dx = read_scenario_DALES_KNMI(surfwinds, smp_out=300,
                                   rot_angle= 11)
    dls
    5/7500
    plt.figure()
    plt.imshow(np.linalg.norm(dls['wnd'], axis=-1), origin='lower', cmap='gray')
    plt.figure()
    plt.imshow(dls['lon'], origin='lower', cmap='gray')

    #np.sin(np.radians(11))*100e3
    #%%
    main_dir = "/Users/plopezdekker/Documents/WORK/STEREOID"
    pardir = os.path.join(main_dir, 'PAR')
    datadir = '/Users/plopezdekker/Documents/WORK/STEREOID/DATA/Ocean/Scenarios'
    # scn_file = 'sample_sfc_velocity_wind.mat
    scn_file = 'sample_indian'
    tsc, wind, dx = read_tsc_wind_from_mat(os.path.join(datadir, scn_file), smp_out=1e3)
    # scn = spio.loadmat(os.path.join(datadir, scn_file))
    mtsc = np.linalg.norm(tsc, axis=-1)
    # mtsc = np.sqrt(scn['usfc']**2 + scn['vsfc']**2)
    mwind = np.linalg.norm(wind, axis=-1)
    # mwind = np.sqrt(scn['uwind'] ** 2 + scn['vwind'] ** 2)
    # vorticity
    # rough
    dy = dx
    xs = dx * np.arange(tsc.shape[1])
    ys = dy * np.arange(tsc.shape[0])
    dvtsc_dy, dvtsc_dx = np.gradient(tsc[:, :, 1], dy, dx)
    dutsc_dy, dutsc_dx = np.gradient(tsc[:, :, 0], dy, dx)
    vort_tsc = dvtsc_dx - dutsc_dy
    div_tsc = dutsc_dx + dvtsc_dy

    plt.figure()
    strm_tsc = plt.streamplot(xs / 1e3, ys / 1e3,
                              tsc[:, :, 0], tsc[:, :, 1],
                              color=mtsc, cmap='viridis_r')
    plt.colorbar(strm_tsc.lines)
    plt.figure()

    strm_wind = plt.streamplot(xs / 1e3, ys / 1e3,
                               wind[:, :, 0], wind[:, :, 1],
                               color=mwind, cmap='viridis_r')
    plt.colorbar(strm_wind.lines)

    plt.figure()
    plt.imshow(vort_tsc, origin='lower',
               extent=[xs[0] / 1e3, xs[-1]/1e3, ys[0] / 1e3, ys[-1] / 1e3],
               vmin=-np.max(np.abs(vort_tsc)), vmax=np.max(np.abs(vort_tsc)),
               cmap='bwr')
    plt.title("TSC vorticity")
    plt.colorbar()

    plt.figure()
    plt.imshow(div_tsc, origin='lower',
               extent=[xs[0] / 1e3, xs[-1]/1e3, ys[0] / 1e3, ys[-1] / 1e3],
               vmin=-np.max(np.abs(div_tsc)), vmax=np.max(np.abs(div_tsc)),
               cmap='bwr')
    plt.title("TSC divergence")
    plt.colorbar()
