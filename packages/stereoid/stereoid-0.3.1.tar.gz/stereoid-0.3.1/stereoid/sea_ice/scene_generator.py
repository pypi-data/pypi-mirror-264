__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
import drama.utils as drtls
from stereoid.sea_ice import read_nextsim as readsim
from matplotlib import path
from scipy import ndimage
from scipy.spatial import cKDTree
from scipy.interpolate.interpnd import _ndim_coords_from_arrays


class SceneGenerator(object):
    def __init__(self, fwdm, x_res, y_res, n_orbs=1):
        self.fwdm = fwdm
        self.x_res = x_res
        self.y_res = y_res
        self.n_orbs = n_orbs

    # get neXtSIM data within an overpass and reproject velocities
    def neXtSIM_inswath(self, datadir, fname, swth, lat_min=68):
        """

        :param datadir:
            path to neXtSIM file
        :param fname:
            filename of the '.npz' neXtSIM file
        :param swth:
            Drama bistatic swath [object] (sargeo.SingleSwathBistatic)
        :param lat_min:
            minimum latitude [deg] to be considered
        :return:
            lon: vector of neXtSIM longitudes [deg] within the swath
            lat: vector of neXtSIM latitudes [deg] within the swath
            u: vector of neXtSIM velocities [m/s] (cross) within the swath
            v: vector of neXtSIM velocities [m/s] (along) within the swath

        """

        # read data
        n = readsim.read_neXtSIM_npz(datadir, fname)

       # read some relevant data
        if self.n_orbs == 1:
            lat_s=swth.lats
            lon_s = swth.lons
            northing = swth.master_northing
        else:
            lat_s=swth.master_swath.lat
            lon_s = swth.master_swath.lon
            northing = swth.master_swath.Northing
        shp=lon_s.shape

        # make a polygon to read the data of interest
        lat_n = lat_s[:, 0];
        lat_f = lat_s[:, shp[1] - 1]
        lon_n = lon_s[:, 0];
        lon_f = lon_s[:, shp[1] - 1]
        lon_n = lon_n[lat_n > lat_min];
        lat_n = lat_n[lat_n > lat_min]
        lon_f = lon_f[lat_f > lat_min];
        lat_f = lat_f[lat_f > lat_min]
        lon_fi = lon_f[::-1];
        lat_fi = lat_f[::-1]  # invert

        # two polygons to avoid dateline issues
        lon_p1 = np.concatenate((lon_n[np.absolute(lon_n) < 90], lon_fi[np.absolute(lon_fi) < 90]));
        lat_p1 = np.concatenate((lat_n[np.absolute(lon_n) < 90], lat_fi[np.absolute(lon_fi) < 90]));
        if len(lon_p1) > 0:
            lon_p1 = np.append(lon_p1, lon_p1[0]);
            lat_p1 = np.append(lat_p1, lat_p1[0])
        if len(lon_p1) == 0:
            lon_p1 = np.zeros(5);
            lat_p1 = np.zeros(5)
        lon_p2 = np.concatenate((lon_n[np.absolute(lon_n) > 90], lon_fi[np.absolute(lon_fi) > 90]));
        lat_p2 = np.concatenate((lat_n[np.absolute(lon_n) > 90], lat_fi[np.absolute(lon_fi) > 90]));
        if len(lon_p2) > 0:
            lon_p2 = np.append(lon_p2, lon_p2[0]);
            lat_p2 = np.append(lat_p2, lat_p2[0])
            lon_p2[lon_p2 < 0] = lon_p2[lon_p2 < 0] + 360
        if len(lon_p2) == 0:
            lon_p2 = np.zeros(5);
            lat_p2 = np.zeros(5)

        # find interesting data
        lon_m = n['lon']
        lat_m = n['lat']
        p1 = path.Path(np.column_stack((lon_p1, lat_p1)))
        p2 = path.Path(np.column_stack((lon_p2, lat_p2)))
        in_poly1 = p1.contains_points(np.column_stack((lon_m, lat_m)))
        lon_m360 = np.zeros(len(lon_m));
        lon_m360[:] = lon_m[:];
        lon_m360[lon_m360 < 0] = lon_m360[lon_m360 < 0] + 360
        in_poly2 = p2.contains_points(np.column_stack((lon_m360, lat_m)))

        # get velocities (these are with respect the model orientation)
        u = n['u']
        v = n['v']

        # they are either in one or the other polygon
        I = np.logical_or(in_poly1, in_poly2)

        # convert velocities to north and east
        # FIXME: we have to check if it works like this
        v_e = u[I] * np.cos(np.deg2rad(lon_m[I] + 45)) + v[I] * np.sin(np.deg2rad(lon_m[I] + 45))
        v_n = -u[I] * np.sin(np.deg2rad(lon_m[I] + 45)) + v[I] * np.cos(np.deg2rad(lon_m[I] + 45))

        # convert velocities to cross-track (x) and along-track (y) velocities
        cosn = np.cos(northing.ravel())
        sinn = np.sin(northing.ravel())
        # FIXME: check issues with dateline
        cosn = griddata((lon_s.ravel(), lat_s.ravel()), cosn, (lon_m[I], lat_m[I]), method='nearest')
        sinn = griddata((lon_s.ravel(), lat_s.ravel()), sinn, (lon_m[I], lat_m[I]), method='nearest')
        v_x = v_e * cosn - v_n * sinn
        v_y = v_n * cosn + v_e * sinn

        return lon_m[I], lat_m[I], v_x, v_y

    # resamples the neXtSIM velocities to a 'regular' radar grid
    # it assume that the cross-track spacing is already set by 'gr_res' in the par-file
    # the along-track spacing will be upsampled
    def resample_neXtSIM(self, lon_m, lat_m, v_x, v_y, swth, t_res, y_res, x_res, lat_min=68, V=7200, thr=10E3):
        """

        Parameters
        ----------
        lon_m
        lat_m
        v_x
        v_y
        swth
        t_res
        y_res
        x_res
        lat_min
        V
        thr

        Returns
        -------
        lon_int, lat_int:
            interpolated longitude [deg] and latitude [deg]
        x_int, y_int:
            interpolated radar coordinates [m]
        vx_int, vy_int:
            interpolated ground velocities in radar reference frame [m/s]
        """

        # get lats and lons of the original swath
        if self.n_orbs == 1:
            lats = swth.lats
            lons = swth.lons
        else:
            lats = swth.master_swath.lat
            lons = swth.master_swath.lon

        # compute azimuth time t for each location of the original swath
        t = np.arange(lons.shape[0]) * t_res
        t = np.outer(t, np.ones(lons.shape[1]))

        # compute a cross-track index for the original swath
        # nx=np.arange(swth.lons.shape[1])
        # nx = np.outer(np.ones(swth.lons.shape[0]), nx)

        # remove all data below the minimum latitude to speed up the process
        I = lats[:, 0] > lat_min
        t = t[I, :]
        # nx=nx[I,:]
        lons = lons[I, :]
        lats = lats[I, :]

        # generate a high resolution grid
        dt = y_res / V
        t_int = np.arange(np.min(t), np.max(t), dt)

        # dateline
        if np.max(lons)-np.min(lons) > 270:
            lons[lons < 0]= lons[lons < 0] +  360
            lon_m[lon_m < 0]= lon_m[lon_m < 0] +  360

        # interpolate longitudes and latitudes
        # this assumes the cross-track already has sufficient grid points
        lon_int = np.zeros((len(t_int), lons.shape[1]))
        lat_int = np.zeros((len(t_int), lons.shape[1]))
        for i in range(lons.shape[1]):
            f = interp1d(t[:, i], lats[:, i])
            lat_int[:, i] = f(t_int)
            f = interp1d(t[:, i], lons[:, i])
            lon_int[:, i] = f(t_int)

        # radar coordinates
        x = np.arange(lon_int.shape[1]) * x_res
        x_int = np.outer(np.ones(lon_int.shape[0]), x)
        y = np.arange(lon_int.shape[0]) * y_res
        y_int = np.outer(y, np.ones(lon_int.shape[1]))

        # radar coordinates of neXtSIM (this is 'necessary' to use 'nearest neighbour' below)
        x_m = griddata((lon_int.ravel(), lat_int.ravel()), x_int.ravel(), (lon_m, lat_m), 'nearest')
        y_m = griddata((lon_int.ravel(), lat_int.ravel()), y_int.ravel(), (lon_m, lat_m), 'nearest')

        # radar coordinates of neXtSIM grid points
        vx_int = griddata((x_m, y_m), v_x, (x_int.ravel(), y_int.ravel()), 'nearest')
        vy_int = griddata((x_m, y_m), v_y, (x_int.ravel(), y_int.ravel()), 'nearest')
        vx_int = vx_int.reshape(x_int.shape)
        vy_int = vy_int.reshape(x_int.shape)

        # the grid will have irregular edges due to the triangular shape of the neXtSIM grid
        # we will clean this by a median filter
        vx_int = ndimage.median_filter(vx_int, 7)
        vy_int = ndimage.median_filter(vy_int, 7)

        # remove areas far away from points
        xy = np.zeros((len(x_m), 2))
        xy[:, 0] = x_m
        xy[:, 1] = y_m
        tree = cKDTree(xy)
        xi = _ndim_coords_from_arrays((x_int, y_int), ndim=2)
        dists, indexes = tree.query(xi)
        vx_int[dists > thr] = np.nan
        vy_int[dists > thr] = np.nan

        return lon_int, lat_int, x_int, y_int, vx_int, vy_int

    # calls forward model to compute dca, phase and nrcs (from t3, modelled drift input)
    def run_forward_model(self, ObsGeoTrio, pol, u, v, x1D, inc_m0):
        """

        Parameters
        ----------
        ObsGeoTrio:
            observation geometry (object) made with observations tools
        pol:
            expected output polarization
        u:
            cross-track velocity grid
        v:
            along-track velocity grid
        x1D:
            one-dimensional vector of cross-track distance
        inc_m0:
            transmitter incident angle at the near field

        Returns
        -------
        nrcs:
            three grids of cross-sections
        dca:
            three grids of Doppler centroid anomalies
        phase:
            three grids of ATI phases
        """

        # get geometry
        ObsGeoTrio.sentinel1.set_swath(inc_m0, x1D)
        ObsGeoTrio.concordia.set_swath(inc_m0, x1D)
        ObsGeoTrio.discordia.set_swath(inc_m0, x1D)
        inc_m = ObsGeoTrio.sentinel1._inc_m
        inc_bc = ObsGeoTrio.concordia.inc_b
        bist_c = ObsGeoTrio.concordia.bist_ang
        inc_bd = ObsGeoTrio.discordia.inc_b
        bist_d = ObsGeoTrio.discordia.bist_ang

        # set polarization (1=hh,2=vv,3=hv,4=vh)
        if pol == 'hh': x = 0
        if pol == 'vv': x = 1
        if pol == 'hv': x = 2
        if pol == 'vh': x = 3
        if pol == 'hh+hv': x = 4

        # get nrcs power
        nrcs_mono = self.fwdm.fwd_nrcs_monostatic(inc_m)
        nrcs_conc = self.fwdm.fwd_nrcs_bistatic(inc_m, inc_bc, bist_c)
        nrcs_disc = self.fwdm.fwd_nrcs_bistatic(inc_m, inc_bd, bist_d)

        # grid the nrcs
        nrcs = np.ones((u.shape[0], u.shape[1], 3))
        if x < 4:
            nrcs[:, :, 1] = nrcs[:, :, 1] * drtls.db(nrcs_conc[x])  # Harmony in front of Sentinel-1
            nrcs[:, :, 0] = nrcs[:, :, 0] * drtls.db(nrcs_mono[x])  # Sentinel-1
            nrcs[:, :, 2] = nrcs[:, :, 2] * drtls.db(nrcs_disc[x])  # Harmony behind Sentinel-1
        if x == 4:
            nrcs[:, :, 1] = nrcs[:, :, 1] * drtls.db(nrcs_conc[0] + nrcs_conc[2])  # Harmony in front of Sentinel-1
            nrcs[:, :, 0] = nrcs[:, :, 0] * drtls.db(nrcs_mono[0])  # Sentinel-1
            nrcs[:, :, 2] = nrcs[:, :, 2] * drtls.db(nrcs_disc[0] + nrcs_disc[2])  # Harmony behind Sentinel-1

        # forward model
        dopp = np.zeros(nrcs.shape)
        dopp[:, :, 1] = self.fwdm.fwd_ph_dca(u, v, inc_m, inc_bc, bist_c)
        dopp[:, :, 0] = self.fwdm.fwd_ph_dca(u, v, inc_m, inc_m, 0)
        dopp[:, :, 2] = self.fwdm.fwd_ph_dca(u, v, inc_m, inc_bd, bist_d)

        # return observed quantities + noise
        return nrcs, dopp
