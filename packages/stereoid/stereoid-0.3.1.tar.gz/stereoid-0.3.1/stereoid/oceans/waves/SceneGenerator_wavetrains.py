__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import os
import numpy as np
import scipy as sp
# from scipy.stats import f
from scipy import interpolate
from matplotlib import pyplot as plt
import time
import stereoid.oceans.waves.wave_spectra as wave_spectra


class SceneGenerator_wavetrains(object):
    def __init__(self, shp, x_res, y_res, basin, hemisphere):
        self.shp = shp
        self.x_res = x_res
        self.y_res = y_res
        self.basin = basin
        self.hemisphere = hemisphere

    # compute instant TC eye direction from track
    def TC_eye_direction(self, path, code, year_i, month_i, day_i, t_i, heading):
        # path: path to track files
        # code: tropical storm code
        # year_i: year of S1 overpass
        # month_i: month of S1 overpass
        # day_i: day of S1 overpass
        # hour_i: decimal hour of S1 overpass
        # heading [deg]: satellite heading with respect to North

        # loads atcf tracks of ifremer
        filename = path + 'b' + self.basin + code + str(year_i) + '.dat'
        of = open(filename, 'r')  # We need to re-open the file
        data = of.read()
        of.close()
        lines = data.split('\n')

        # go through lines
        mon = np.zeros(len(lines) - 1)
        day = np.zeros(len(lines) - 1)
        hou = np.zeros(len(lines) - 1)
        lat = np.zeros(len(lines) - 1)
        lon = np.zeros(len(lines) - 1)
        for i in range(0, len(lines) - 1):
            spl = lines[i].split(',')

            # month, day, hour
            d = spl[2]
            mon[i] = float(d[5:7])
            day[i] = float(d[7:9])
            hou[i] = float(d[9:11])

            # coordinates
            lat[i] = float(spl[6][:-1]) / 10
            if spl[6][-1:] == 'S':
                lat[i] = -lat[i]
            lon[i] = float(spl[7][:-1]) / 10
            if spl[7][-1:] == 'W':
                lon[i] = -lon[i]

        # for some dark reason there are duplicates records, let's remove
        t = day * 24 * 60 * 60 + hou * 60 * 60  # time from start of the month
        t, ind = np.unique(t, return_index=True)
        lon = lon[ind]
        lat = lat[ind]

        # interpolate lon, lat's to the input time vector
        f = sp.interpolate.interp1d(t, lon, kind='cubic')
        lon = f(t_i)
        f = sp.interpolate.interp1d(t, lat, kind='cubic')
        lat = f(t_i)
        # lon=np.interp(t_i,t,lon)
        # lat=np.interp(t_i,t,lat)

        # convert to local x/y coordinate system
        Re = 6371E3;
        lon0 = np.min(lon)
        lat0 = np.min(lat)
        x = (lon - lon0) / 360 * 2 * np.pi * Re * np.cos(np.deg2rad(lat0))
        y = (lat - lat0) / 360 * 2 * np.pi * Re

        # rotate to radar coordinates
        heading = np.deg2rad(heading)
        xr = np.cos(heading) * x - np.sin(heading) * y
        yr = -np.sin(heading) * x + np.cos(heading) * y

        # eye velocity in radar reference frame
        dt = t_i[1:] - t_i[:-1]
        vx = (xr[1:] - xr[:-1]) / dt
        vy = (yr[1:] - yr[:-1]) / dt
        vx = np.append(vx, vx[-1:])
        vy = np.append(vy, vy[-1:])

        return vx, vy, lon, lat, xr, yr  # (vx,vy,xr,yr) in radar coordinates (x = cross-track)

    # generate parametric tropical cyclone wind in radar coordinates
    def parametric_TC_Holland(self, eye_loc, u_m, R_m, B, f, phi_in=0, v_eye=0, dir_eye=0):
        """

        Parameters
        ----------
        eye_loc
        u_m
        R_m
        B
        f
        phi_in
        v_eye
        dir_eye

        Returns
        -------

        """
        # based on Holland (1980), or Eq. 29 in Kudryavtsev et al. (2018)

        # make a grid
        x = np.linspace(0, self.x_res * self.shp[1], self.shp[1], endpoint=False)
        y = np.linspace(0, self.y_res * self.shp[0], self.shp[0], endpoint=False)
        x, y = np.meshgrid(x, y)

        # radial distance from eye wall
        r = np.sqrt((x - eye_loc[1]) ** 2 + (y - eye_loc[0]) ** 2)

        # rotational wind speed
        v = ((u_m ** 2 + u_m * r * f) * (R_m / r) ** B * np.exp(-(R_m / r) ** B + 1) + (
                r * f / 2) ** 2) ** 0.5 - r * f / 2

        # rotational wind direction
        vdir = -np.rad2deg(np.arctan2(y - eye_loc[0], x - eye_loc[1])) - phi_in

        # wind vectors to add the wind speed by hurricane translation
        vx = np.sin(np.deg2rad(vdir)) * v + np.sin(np.deg2rad(dir_eye)) * v_eye
        vy = np.cos(np.deg2rad(vdir)) * v + np.cos(np.deg2rad(dir_eye)) * v_eye

        # total wind speed
        # v=np.sqrt(vx**2+vy**2)

        # wind direction
        # vdir=np.rad2deg(np.arctan2(vx,vy))

        return x, y, vx, vy, r

    # generate parametric tropical cyclone wind in radar coordinates
    def parametric_TC_Holland_static(self, eye_loc, u_m, R_m, B, f, phi_in=0):
        """

        Parameters
        ----------
        eye_loc
        u_m
        R_m
        B
        f
        phi_in

        Returns
        -------

        """
        # based on Holland (1980), or Eq. 29 in Kudryavtsev et al. (2018)

        # make a grid
        x = np.linspace(0, self.x_res * self.shp[1], self.shp[1], endpoint=False)
        y = np.linspace(0, self.y_res * self.shp[0], self.shp[0], endpoint=False)
        x, y = np.meshgrid(x, y)

        # radial distance from eye wall
        r = np.sqrt((x - eye_loc[1]) ** 2 + (y - eye_loc[0]) ** 2)

        # rotational wind speed
        v = ((u_m ** 2 + u_m * r * f) * (R_m / r) ** B * np.exp(-(R_m / r) ** B + 1) + (
                r * f / 2) ** 2) ** 0.5 - r * f / 2

        # rotational wind direction
        vdir = -np.rad2deg(np.arctan2(y - eye_loc[0], x - eye_loc[1])) - phi_in

        # wind vectors
        vx = np.sin(np.deg2rad(vdir)) * v
        vy = np.cos(np.deg2rad(vdir)) * v

        return x, y, vx, vy, r

    # generate uniform wind field
    def uniform_wind(self, ws, wdir):
        """

        Parameters
        ----------
        ws
        wdir

        Returns
        -------

        """

        # make a grid
        x = np.linspace(0, self.x_res * self.shp[1], self.shp[1], endpoint=False)
        y = np.linspace(0, self.y_res * self.shp[0], self.shp[0], endpoint=False)
        x, y = np.meshgrid(x, y)

        # wind speed
        v = np.ones(self.shp) * ws

        # wind direction
        vdir = np.ones(self.shp) * wdir

        # wind vectors
        vx = np.sin(np.deg2rad(vdir)) * v
        vy = np.cos(np.deg2rad(vdir)) * v

        return x, y, vx, vy

    # generate wave rays (in TC) in the TC frame with constant TC direction
    def wave_field_constant(self, t, x_0, y_0, vx_eye, vy_eye, u_m, f, R_m, eye_loc, phi_in, B):
        # t [seconds]: time vector
        # x_0, y_0 [meters]: initial position of wave train (vector)
        # vx_eye [meters/second]: (vector)
        # vy_eye [meters/second]: (vector)
        # u_m [m/s], R_M [m] phi_in[deg], f: Coriolis parameter and TC properties
        # eye_loc [meters]: location of the eye

        # get some initial wind field
        r = np.sqrt((x_0 - eye_loc[1]) ** 2 + (y_0 - eye_loc[0]) ** 2)
        v = ((u_m ** 2 + u_m * r * f) * (R_m / r) ** B * np.exp(-(R_m / r) ** B + 1) + (
                r * f / 2) ** 2) ** 0.5 - r * f / 2
        vdir = -np.rad2deg(np.arctan2(y_0 - eye_loc[0], x_0 - eye_loc[1])) - phi_in
        vx_temp = np.sin(np.deg2rad(vdir)) * v + vx_eye[0]
        vy_temp = np.cos(np.deg2rad(vdir)) * v + vy_eye[0]
        u_int = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
        phi_w = np.arctan2(vx_temp, vy_temp)

        # some constants
        # b=0.06 # From 'Duncan' in Phillips (1985)
        q = -1 / 4  # (-0.33 - -0.23) Kudryavstev et al. (2015)
        p = 3 / 4  # (0.7 - 1.1) Kudryavstev et al. (2015)
        ph = 10  # p for the Heaviside function
        c_e = 1.2E-6  # (0.7E-7 - 18.9E-7) Badulin et al. (2007)
        c_alpha = 12  # (10.4 - 22.7) Badulin et al. (2007)
        C_e = 2.46E-4  # Chapron et al. (2020)
        C_alpha = -1.4  # Chapron et al. (2020)
        # c_beta=4E-2 # Chapron et al. (2020)
        cg_ratio = 4.6E-2  # this is Delta c_g / c_g from the JONSWAP spectrum
        C_phi = 1.8E-5  # constant from the JONSWAP spectrum
        g = 9.81
        eps_t = np.sqrt(0.135)  # threshold steepness (squared)
        r_g = 0.9
        n = 2 * q / (p + 4 * q)

        # set the initial conditions
        x = np.zeros((len(t), len(x_0)))
        y = np.zeros((len(t), len(x_0)))
        phi_p = np.zeros((len(t), len(x_0)))
        c_gp = np.zeros((len(t), len(x_0)))
        e = np.zeros((len(t), len(x_0)))
        Deltan_0 = 100.0
        Deltan = Deltan_0 * np.ones(len(x_0))
        Deltaphi_p = np.zeros(len(x_0))
        Deltaphi_w = np.zeros(len(x_0))
        phi_p[0, :] = phi_w
        omega_0 = 3
        c_gp[0, :] = g / omega_0 / 2
        c_p = c_gp[0, :] * 2
        alpha = u_int / c_p
        e[0, :] = u_int ** 4 / g ** 2 * c_e * (alpha / c_alpha) ** (p / q)
        x[0, :] = x_0
        y[0, :] = y_0
        WI = np.ones(x.shape)  # turns wind influence on and off

        # update equations
        for i in range(0, len(t) - 1):
            dt = t[i + 1] - t[i]

            # interpolate wind field
            phi_cross = phi_p[i, :] + np.pi / 2
            x_cr = Deltan * np.sin(phi_cross)
            y_cr = Deltan * np.cos(phi_cross)
            for j in range(0, len(x_0)):
                r = np.sqrt((x[i, j] - eye_loc[1]) ** 2 + (y[i, j] - eye_loc[0]) ** 2)
                v = ((u_m ** 2 + u_m * r * f) * (R_m / r) ** B * np.exp(-(R_m / r) ** B + 1) + (
                        r * f / 2) ** 2) ** 0.5 - r * f / 2
                vdir = -np.rad2deg(np.arctan2(y[i, j] - eye_loc[0], x[i, j] - eye_loc[1])) - phi_in
                vx_temp = np.sin(np.deg2rad(vdir)) * v + vx_eye[i]
                vy_temp = np.cos(np.deg2rad(vdir)) * v + vy_eye[i]
                u_int[j] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
                phi_w[j] = np.arctan2(vx_temp, vy_temp)  # watch out, this might be another reference than 'vdir'

                r = np.sqrt((x[i, j] + x_cr[j] - eye_loc[1]) ** 2 + (y[i, j] + y_cr[j] - eye_loc[0]) ** 2)
                v = ((u_m ** 2 + u_m * r * f) * (R_m / r) ** B * np.exp(-(R_m / r) ** B + 1) + (
                        r * f / 2) ** 2) ** 0.5 - r * f / 2
                vdir = -np.rad2deg(
                    np.arctan2(y[i, j] + y_cr[j] - eye_loc[0], x[i, j] + x_cr[j] - eye_loc[1])) - phi_in
                vx_temp = np.sin(np.deg2rad(vdir)) * v + vx_eye[i]
                vy_temp = np.cos(np.deg2rad(vdir)) * v + vy_eye[i]
                Deltaphi_w[j] = np.arctan2(vx_temp, vy_temp) - phi_w[j]

            # some equations for wave age, wavelength, etc.
            c_p = c_gp[i, :] * 2
            alpha = u_int / c_p
            cbar_g = r_g * c_gp[i, :]
            omega_p = g / c_p
            k_p = omega_p / c_p

            # wind input is switched off
            WI[i:, alpha * np.cos(phi_p[i, :] - phi_w) < 1] = 0

            # group velocity derivative
            Delta_p = 1 - 2 / np.cosh(10 * (alpha - 0.9)) ** 2
            dc_gp = -r_g * C_alpha / 2 * Delta_p * g * (k_p ** 2 * e[i, :]) ** 2  # c_gp in the presentation
            c_gp[i + 1, :] = c_gp[i, :] + dc_gp * dt

            # modified energy derivative
            H_p = 1 / 2 * (1 + np.tanh(ph * (np.cos(phi_p[i, :] - phi_w) * alpha - 1)))
            G_n = Deltaphi_p / Deltan_0 * (
                    Deltan / Deltan_0 / ((Deltan / Deltan_0) ** 2 + (0.5 * np.sqrt(cg_ratio)) ** 2)) * WI[i, :]
            Iw = C_e * H_p * alpha ** 2 * np.cos(phi_p[i, :] - phi_w) ** 2 * WI[i, :]
            D = (e[i, :] * k_p ** 2 / eps_t ** 2) ** n
            dlncge = -cbar_g * G_n + omega_p * (Iw - D)
            e[i + 1, :] = np.exp(np.log(cbar_g * e[i, :]) + dlncge * dt) / cbar_g

            # spectral peak direction derivative
            dphi_p = -C_phi * alpha ** 2 * omega_p * H_p * np.sin(2 * (phi_p[i, :] - phi_w)) * WI[i, :]
            phi_p[i + 1, :] = phi_p[i, :] + dphi_p * dt

            # wave train position derivatives (in the eye coordinate system)
            dx = np.sin(phi_p[i, :]) * cbar_g - vx_eye[i]  # phi_p is with respect to North
            dy = np.cos(phi_p[i, :]) * cbar_g - vy_eye[i]
            x[i + 1, :] = x[i, :] + dx * dt
            y[i + 1, :] = y[i, :] + dy * dt

            # update Deltan
            dDeltan = Deltaphi_p * cbar_g
            Deltan = Deltan + dDeltan * dt

            # spectral peak direction gradient
            Tinv = 2 * C_phi * H_p * alpha ** 2 * omega_p * np.cos(2 * (phi_p[i, :] - phi_w)) * WI[i, :]
            dDeltaphi_p = -Tinv * ((Deltaphi_p - Deltaphi_w))
            Deltaphi_p = Deltaphi_p + dDeltaphi_p * dt

        '''
        plt.plot(y[i, 0], omega_p[0]*Iw[0], 'r.', label='energy input')
        plt.plot(y[i, 0], omega_p[0]*D[0], 'g.', label='energy dissipation')
        plt.plot(y[i, 0], omega_p[0]*(Iw[0] - D[0]), 'b.', label='energy balance')
        plt.xlabel('fetch [km]')
        plt.ylabel('energy increase/descrease [-]')
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.show()
        '''

        return x, y, c_gp, e, np.rad2deg(phi_p), WI

    # generate wave rays (in TC) in an 'satellite' frame with a varying TC direction
    # FIXME: limited testing
    def wave_field_varying(self, t, x_0, y_0, vx_eye, vy_eye, u_m, f, R_m, eye_loc, phi_in, B, t_app=0):
        # t [seconds]: time vector
        # x_0, y_0 [meters]: initial position of wave train
        # vx_eye [meters/second]: (vector)
        # vy_eye [meters/second]: (vector)
        # u_m [m/s], R_M [m] phi_in[deg], f: Coriolis parameter and TC properties (vectors in this one)
        # eye_loc [meters]: locations of the eye at t=0
        # x_u, y_u [meters]: grid

        # get some initial wind field
        u_int = np.zeros((len(t), len(x_0)))  # wind speed
        phi_w = np.zeros((len(t), len(x_0)))  # wind direction
        r = np.sqrt((x_0 - eye_loc[1]) ** 2 + (y_0 - eye_loc[0]) ** 2)
        v = ((u_m[0] ** 2 + u_m[0] * r * f) * (R_m[0] / r) ** B * np.exp(-(R_m[0] / r) ** B + 1) + (
                r * f / 2) ** 2) ** 0.5 - r * f / 2
        vdir = -np.rad2deg(np.arctan2(y_0 - eye_loc[0], x_0 - eye_loc[1])) - phi_in[0]
        vx_temp = np.sin(np.deg2rad(vdir)) * v + vx_eye[0]
        vy_temp = np.cos(np.deg2rad(vdir)) * v + vy_eye[0]
        u_int[0, :] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
        phi_w[0, :] = np.arctan2(vx_temp, vy_temp)

        # some constants
        # b=0.06 # From 'Duncan' in Phillips (1985)
        q = -1 / 4  # (-0.33 - -0.23) Kudryavstev et al. (2015)
        p = 3 / 4  # (0.7 - 1.1) Kudryavstev et al. (2015)
        ph = 10  # p for the Heaviside function
        c_e = 1.2E-6  # (0.7E-7 - 18.9E-7) Badulin et al. (2007)
        c_alpha = 12  # (10.4 - 22.7) Badulin et al. (2007)
        C_e = 2.46E-4  # Chapron et al. (2020)
        C_alpha = -1.4  # Chapron et al. (2020)
        # c_beta=4E-2 # Chapron et al. (2020)
        cg_ratio = 4.6E-2  # this is Delta c_g / c_g from the JONSWAP spectrum
        C_phi = 1.8E-5  # constant from the JONSWAP spectrum
        g = 9.81
        eps_t = np.sqrt(0.135)  # threshold steepness (squared)
        r_g = 0.9
        n = 2 * q / (p + 4 * q)

        # set the initial conditions
        x = np.zeros((len(t), len(x_0)))
        y = np.zeros((len(t), len(x_0)))
        ex = np.zeros((len(t)))  # eye locations
        ey = np.zeros((len(t)))
        ex[0] = eye_loc[1]
        ey[0] = eye_loc[0]
        print(ex[0], ey[0])
        phi_p = np.zeros((len(t), len(x_0)))
        c_gp = np.zeros((len(t), len(x_0)))
        e = np.zeros((len(t), len(x_0)))
        Deltan_0 = 100.0
        Deltan = Deltan_0 * np.ones(len(x_0))
        Deltaphi_p = np.zeros(len(x_0))
        Deltaphi_w = np.zeros(len(x_0))
        phi_p[0, :] = phi_w[0, :]
        omega_0 = 3
        c_gp[0, :] = g / omega_0 / 2
        c_p = c_gp[0, :] * 2
        alpha = u_int[0, :] / c_p
        e[0, :] = u_int[0, :] ** 4 / g ** 2 * c_e * (alpha / c_alpha) ** (p / q)
        x[0, :] = x_0
        y[0, :] = y_0
        WI = np.ones(len(x_0))  # turns wind influence on and off

        # update equations
        for i in range(0, len(t) - 1):
            dt = t[i + 1] - t[i]

            # append a set of wave trains each t_app
            if t_app != 0 and np.floor(t[i + 1] / t_app) > np.floor(t[i] / t_app):
                phi_p = np.column_stack((phi_p, np.zeros((len(t), len(x_0)))))
                c_gp = np.column_stack((c_gp, np.zeros((len(t), len(x_0)))))
                e = np.column_stack((e, np.zeros((len(t), len(x_0)))))
                x = np.column_stack((x, np.zeros((len(t), len(x_0)))))
                y = np.column_stack((y, np.zeros((len(t), len(x_0)))))
                c_gp[i, -len(x_0):] = c_gp[100, 0:len(x_0)]
                phi_p[i, -len(x_0):] = phi_p[100, 0:len(
                    x_0)]  # probably close enough (check with rigorously varying wind field)
                e[i, -len(x_0):] = e[100, 0:len(x_0)]  # probably close enough
                x[i, -len(x_0):] = x[100, 0:len(x_0)] - eye_loc[1] + ex[i]
                y[i, -len(x_0):] = y[100, 0:len(x_0)] - eye_loc[0] + ey[i]
                Deltan = np.append(Deltan, Deltan_0 * np.ones(len(x_0)))
                u_int = np.column_stack((u_int, np.zeros((len(t), len(x_0)))))
                phi_w = np.column_stack((phi_w, np.zeros((len(t), len(x_0)))))
                Deltaphi_w = np.append(Deltaphi_w, np.zeros(len(x_0)))
                WI = np.append(WI, np.ones(len(x_0)))
                Deltaphi_p = np.append(Deltaphi_p, np.zeros(len(x_0)))

            # interpolate wind field
            phi_cross = phi_p[i, :] + np.pi / 2
            x_cr = Deltan * np.sin(phi_cross)
            y_cr = Deltan * np.cos(phi_cross)
            for j in range(0, len(Deltan)):
                r = np.sqrt((x[i, j] - ex[i]) ** 2 + (y[i, j] - ey[i]) ** 2)
                v = ((u_m[i] ** 2 + u_m[i] * r * f) * (R_m[i] / r) ** B * np.exp(-(R_m[i] / r) ** B + 1) + (
                        r * f / 2) ** 2) ** 0.5 - r * f / 2
                vdir = -np.rad2deg(np.arctan2(y[i, j] - ey[i], x[i, j] - ex[i])) - phi_in[i]
                vx_temp = np.sin(np.deg2rad(vdir)) * v + vx_eye[i]
                vy_temp = np.cos(np.deg2rad(vdir)) * v + vy_eye[i]
                u_int[i, j] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
                phi_w[i, j] = np.arctan2(vx_temp, vy_temp)

                r = np.sqrt((x[i, j] + x_cr[j] - ex[i]) ** 2 + (y[i, j] + y_cr[j] - ey[i]) ** 2)
                v = ((u_m[i] ** 2 + u_m[i] * r * f) * (R_m[i] / r) ** B * np.exp(-(R_m[i] / r) ** B + 1) + (
                        r * f / 2) ** 2) ** 0.5 - r * f / 2
                vdir2 = -np.rad2deg(np.arctan2(y[i, j] + y_cr[j] - ey[i], x[i, j] + x_cr[j] - ex[i])) - \
                        phi_in[i]
                vx_temp2 = np.sin(np.deg2rad(vdir2)) * v + vx_eye[i]
                vy_temp2 = np.cos(np.deg2rad(vdir2)) * v + vy_eye[i]
                Deltaphi_w[j] = np.arctan2(vx_temp2, vy_temp2) - phi_w[i, j]

            # some equations for wave age, wavelength, etc.
            c_p = c_gp[i, :] * 2
            alpha = u_int[i, :] / c_p
            cbar_g = r_g * c_gp[i, :]
            omega_p = g / c_p
            k_p = omega_p / c_p

            # wind input is switched off
            # print(alpha[2]*np.cos(phi_p[i,2]-phi_w[2]),alpha[2],phi_p[i,2],phi_w[2])
            WI[np.logical_and(alpha * np.cos(phi_p[i, :] - phi_w[i, :]) < 1, phi_w[i, :] > 5)] = 0

            # group velocity derivative
            Delta_p = 1 - 2 / np.cosh(10 * (alpha - 0.9)) ** 2
            dc_gp = -r_g * C_alpha / 2 * Delta_p * g * (k_p ** 2 * e[i, :]) ** 2  # c_gp in the presentation
            c_gp[i + 1, :] = c_gp[i, :] + dc_gp * dt

            # modified energy derivative
            H_p = 1 / 2 * (1 + np.tanh(ph * (np.cos(phi_p[i, :] - phi_w[i, :]) * alpha - 1)))
            G_n = Deltaphi_p / Deltan_0 * (
                    Deltan / Deltan_0 / ((Deltan / Deltan_0) ** 2 + (0.5 * np.sqrt(cg_ratio)) ** 2)) * WI
            Iw = C_e * H_p * alpha ** 2 * np.cos(phi_p[i, :] - phi_w[i, :]) ** 2 * WI
            D = (e[i, :] * k_p ** 2 / eps_t ** 2) ** n
            dlncge = -cbar_g * G_n + omega_p * (Iw - D)
            e[i + 1, :] = np.exp(np.log(cbar_g * e[i, :]) + dlncge * dt) / cbar_g

            # spectral peak direction derivative
            dphi_p = -C_phi * alpha ** 2 * omega_p * H_p * np.sin(2 * (phi_p[i, :] - phi_w[i, :])) * WI
            phi_p[i + 1, :] = phi_p[i, :] + dphi_p * dt

            # wave train position derivatives (in the eye coordinate system)
            dx = np.sin(phi_p[i, :]) * cbar_g
            dy = np.cos(phi_p[i, :]) * cbar_g
            x[i + 1, :] = x[i, :] + dx * dt
            y[i + 1, :] = y[i, :] + dy * dt

            # eye location
            ex[i + 1] = ex[i] + vx_eye[i] * dt
            ey[i + 1] = ey[i] + vy_eye[i] * dt

            # update Deltan
            dDeltan = Deltaphi_p * cbar_g
            Deltan = Deltan + dDeltan * dt

            # spectral peak direction gradient
            Tinv = 2 * C_phi * H_p * alpha ** 2 * omega_p * np.cos(2 * (phi_p[i, :] - phi_w[i, :])) * WI
            dDeltaphi_p = -Tinv * ((Deltaphi_p - Deltaphi_w))
            Deltaphi_p = Deltaphi_p + dDeltaphi_p * dt

        return x, y, c_gp, e, np.rad2deg(phi_p), ex, ey, u_int, np.rad2deg(phi_w)

    # generate (developed) wave rays with current interaction
    # this is based on Quilfen and Chapron (2019) with derivatives as in White and Fornberg (1998)
    def wave_field_currents(self, kx_0, ky_0, x_0, y_0, u, v, t):
        # kx_0, ky_0: initial peak wave numbers
        # x0, y0: initial locations

        # some constants
        g = 9.81

        # get the gradients
        dudx = np.gradient(u, self.x_res, axis=1)
        dudy = np.gradient(u, self.y_res, axis=0)
        dvdx = np.gradient(v, self.x_res, axis=1)
        dvdy = np.gradient(v, self.y_res, axis=0)

        # interpolate gradients and velocities
        shp = u.shape
        xg = np.arange(0, shp[1] * self.x_res, self.x_res)
        yg = np.arange(0, shp[0] * self.y_res, self.y_res)
        f_ux = interpolate.RectBivariateSpline(yg, xg, dudx)  # watch out, this thing flips the y and x axis
        f_uy = interpolate.RectBivariateSpline(yg, xg, dudy)
        f_vx = interpolate.RectBivariateSpline(yg, xg, dvdx)
        f_vy = interpolate.RectBivariateSpline(yg, xg, dvdy)
        f_u = interpolate.RectBivariateSpline(yg, xg, u)
        f_v = interpolate.RectBivariateSpline(yg, xg, v)

        kx = np.zeros((len(t), len(kx_0)))
        kx[0, :] = kx_0
        ky = np.zeros((len(t), len(kx_0)))
        ky[0, :] = ky_0
        x = np.zeros((len(t), len(kx_0)))
        x[0, :] = x_0
        y = np.zeros((len(t), len(kx_0)))
        y[0, :] = y_0
        dt = np.gradient(t)
        for i in range(0, len(t) - 1):
            # wavenumber
            k = np.sqrt(kx[i, :] ** 2 + ky[i, :] ** 2)

            # interpolate currents
            dudx_int = f_ux.ev(y[i, :], x[i, :])  # x and y should be flipped here as well
            dvdx_int = f_vx.ev(y[i, :], x[i, :])
            dudy_int = f_uy.ev(y[i, :], x[i, :])
            dvdy_int = f_vy.ev(y[i, :], x[i, :])
            u_int = f_u.ev(y[i, :], x[i, :])
            v_int = f_v.ev(y[i, :], x[i, :])

            # compute derivatives
            dkxdt = - (kx[i, :] * dudx_int + ky[i, :] * dvdx_int)
            dkydt = - (kx[i, :] * dudy_int + ky[i, :] * dvdy_int)
            dxdt = g ** 0.5 * kx[i, :] / (2 * k ** (3 / 2)) + u_int
            dydt = g ** 0.5 * ky[i, :] / (2 * k ** (3 / 2)) + v_int

            # update wave trains
            x[i + 1, :] = x[i, :] + dxdt * dt[i]
            y[i + 1, :] = y[i, :] + dydt * dt[i]
            kx[i + 1, :] = kx[i, :] + dkxdt * dt[i]
            ky[i + 1, :] = ky[i, :] + dkydt * dt[i]

        return kx, ky, x, y

    # this script is used to fit a spectrum to the wave trains collected in a box in a tropical cyclone
    # the wind-wave system will be modeled with a single Johnswap
    # the swell-wave system is modeled with multiple Gaussian to capture the spread
    # FIXME: this is not optimal, but it is the best we can do now
    def fit_spectrum_to_wavetrains(self, e_t, phi_t, la_t, WI_t, kx, ky, sigma_f=0.007, sigma_phi=np.deg2rad(5), phi_w=None):
        """

        Parameters
        ----------
        e_t: energy of wave train (one-dimensional)
        phi_t: peak direction [rad] of train (one-dimensional), in the Nautical system
        la_t: peak wavelength of train (one-dimensional)
        WI_t: if 1 = swell, if 0 = wind wave (one-dimensional)
        kx: spectral grid cross-track direction
        ky: spectral grid along-track direction

        Returns
        -------
        S_ww: wind-wave spectrum based on Johnswap
        S_sw: swell-wave spectrum based on a collection of Gaussian spectra
        """
        g = 9.81
        k = np.sqrt(kx ** 2 + ky ** 2)
        phi_k = np.arctan2(ky, kx)
        dks = (kx[0, 1] - kx[0, 0]) * (ky[1, 0] - ky[0, 0])
        f = 1 / (2 * np.pi) * np.sqrt(g * k)
        fac_f = 0.25 / np.pi * np.sqrt(g / k)

        # to Cartesian system
        phi_t=np.angle(np.exp(1j*(np.pi/2-phi_t)))
        phi_w=np.angle(np.exp(1j*(np.pi/2-phi_w)))

        # wind waves
        I = np.logical_and(WI_t == 1, 4*np.sqrt(e_t) > 2)
        e_temp, phi_temp, la_temp = e_t[I], phi_t[I], la_t[I]
        if len(e_temp) > 0:
            I2 = np.argmax(e_temp)
            Hs = 4 * np.sqrt(e_temp[I2])
            phi_p = phi_temp[I2]
            k_p = 2 * np.pi / la_temp[I2]
        else:
            print('Warning! No wind-wave-train found!')
            k_p = 2 * np.pi / 20
            Hs = 2
            phi_p = phi_w*1.0
        omega_p = np.sqrt(g * k_p)
        S_ww = wave_spectra.jonswap_hs(k, phi_k, omega_p, phi_p, Hs, dks, gamma=3.3, phi_w=phi_w)

        # swell waves
        if len(e_temp) > 0:
            I = np.logical_and(WI_t == 0, np.logical_or(np.absolute(la_t-la_temp[I2]) > 50, np.absolute(np.angle(np.exp(1j * (phi_p - phi_t)))) > np.pi/4))
        else:
            I = WI_t == 0
        e_temp, phi_temp, la_temp = e_t[I], phi_t[I], la_t[I]
        e_temp=e_temp/np.sum(e_temp) # normalized energy
        k_p = 2 * np.pi / la_temp
        f_p = 1 / ( 2 * np.pi ) * np.sqrt(g * k_p)
        S_sw = np.zeros(kx.shape)
        for i in range(0,len(e_temp)):
            # frequency spectrum

            amp = e_temp[i] / (sigma_f * np.sqrt(2 * np.pi))
            Sp = (amp * np.exp(-(f - f_p[i]) ** 2 / (2 * sigma_f ** 2)) + 1E-5) * fac_f

            # directional distribution
            dphi = np.angle(np.exp(1j * (phi_temp[i] - phi_k)))  # including unwrapping
            D = np.exp(-dphi ** 2 / (2 * sigma_phi ** 2)) / (
                    2 * np.pi * sigma_phi ** 2) ** 0.5  # directional component

            S_sw = S_sw + Sp * D / k

        return S_ww, S_sw

    '''
    # generate (developed) wave rays with current interaction
    # this is based on Quilfen and Chapron (2019) with derivatives as in White and Fornberg (1998)
    # we added a way to incorporate energy fluctuations as a function of wave-ray width
    # FIXME: this is not extensively tested
    def wave_field_currents_with_energy( self, kx_0, ky_0, x_0, y_0, u, v, t, Hs, phi_p0, Deltan_0 = 50 ):
        # kx_0, ky_0: initial peak wave numbers
        # x0, y0: initial locations
        # u, v: current velocity grid
        # Hs: initial significant wave height
        # phi_p0: initial wave direction with respect to East
        # Deltan_0: initial wave-ray width

        # some constants
        g = 9.81
        cg_ratio = 4.6E-2

        # get the gradients
        dudx = np.gradient( u, self.x_res, axis = 1 )
        dudy = np.gradient( u, self.y_res, axis = 0 )
        dvdx = np.gradient( v, self.x_res, axis = 1 )
        dvdy = np.gradient( v, self.y_res, axis = 0 )

        # interpolate gradients and velocities
        shp = u.shape
        xg = np.arange( 0, shp[ 1 ] * self.x_res, self.x_res )
        yg = np.arange( 0, shp[ 0 ] * self.y_res, self.y_res )
        f_ux = interpolate.RectBivariateSpline( yg, xg, dudx )  # watch out, this thing flips the y and x axis
        f_uy = interpolate.RectBivariateSpline( yg, xg, dudy )
        f_vx = interpolate.RectBivariateSpline( yg, xg, dvdx )
        f_vy = interpolate.RectBivariateSpline( yg, xg, dvdy )
        f_u = interpolate.RectBivariateSpline( yg, xg, u )
        f_v = interpolate.RectBivariateSpline( yg, xg, v )

        # initial direction
        k0 = np.sqrt( kx_0 ** 2 + ky_0 ** 2 )
        dxdt0 = g ** 0.5 * kx_0 / (2 * k0 ** (3 / 2)) + f_u.ev( y_0, x_0 )
        dydt0 = g ** 0.5 * ky_0 / (2 * k0 ** (3 / 2)) + f_v.ev( y_0, x_0 )
        phi_p = np.arctan2( dydt0, dxdt0 )

        # initialize wave-ray parameters
        kx = np.zeros( (len( t ), len( kx_0 )) )  # cross-track wave number
        kx[ 0, : ] = kx_0
        ky = np.zeros( (len( t ), len( kx_0 )) )  # along-track wave number
        ky[ 0, : ] = ky_0
        x = np.zeros( (len( t ), len( kx_0 )) )  # cross-track position
        x[ 0, : ] = x_0
        y = np.zeros( (len( t ), len( kx_0 )) )  # along-track position
        y[ 0, : ] = y_0
        Deltan = np.zeros( (len( t ), len( kx_0 )) )  # cross-ray width
        Deltan[ 0, : ] = Deltan_0
        e = np.zeros( (len( t ), len( kx_0 )) )  # relative energy
        e[ 0, : ] = Hs ** 2 / 16

        # integrate
        dt = np.gradient( t )
        for i in range( 0, len( t ) - 1 ):
            # wavenumber
            k = np.sqrt( kx[ i, : ] ** 2 + ky[ i, : ] ** 2 )

            # interpolate currents
            dudx_int1 = f_ux.ev( y[ i, : ], x[ i, : ] )  # x and y should be flipped here as well
            dvdx_int1 = f_vx.ev( y[ i, : ], x[ i, : ] )
            dudy_int1 = f_uy.ev( y[ i, : ], x[ i, : ] )
            dvdy_int1 = f_vy.ev( y[ i, : ], x[ i, : ] )
            u_int1 = f_u.ev( y[ i, : ], x[ i, : ] )
            v_int1 = f_v.ev( y[ i, : ], x[ i, : ] )

            # interpolate currents for the cross-ray widening
            x2 = x[ i, : ] + Deltan[ i, : ] * np.cos( phi_p + np.pi / 2 )
            y2 = y[ i, : ] + Deltan[ i, : ] * np.sin( phi_p + np.pi / 2 )
            # dudx_int2 = f_ux.ev( y2, x2 )
            # dvdx_int2 = f_vx.ev( y2, x2 )
            # dudy_int2 = f_uy.ev( y2, x2 )
            # dvdy_int2 = f_vy.ev( y2, x2 )
            u_int2 = f_u.ev( y2, x2 )
            v_int2 = f_v.ev( y2, x2 )

            # compute derivatives
            dkxdt1 = - (kx[ i, : ] * dudx_int1 + ky[ i, : ] * dvdx_int1)
            dkydt1 = - (kx[ i, : ] * dudy_int1 + ky[ i, : ] * dvdy_int1)
            dxdt1 = g ** 0.5 * kx[ i, : ] / (2 * k ** (3 / 2)) + u_int1
            dydt1 = g ** 0.5 * ky[ i, : ] / (2 * k ** (3 / 2)) + v_int1
            cbar1_g = np.sqrt( dxdt1 ** 2 + dydt1 ** 2 )
            phi_p = np.arctan2( dydt1, dxdt1 )

            # derivatives for cross-ray widening
            # dkxdt2 = - (kx[ i, : ] * dudx_int2 + ky[ i, : ] * dvdx_int2)
            # dkydt2 = - (kx[ i, : ] * dudy_int2 + ky[ i, : ] * dvdy_int2)
            dxdt2 = g ** 0.5 * kx[ i, : ] / (2 * k ** (3 / 2)) + u_int2
            dydt2 = g ** 0.5 * ky[ i, : ] / (2 * k ** (3 / 2)) + v_int2
            # cbar2_g = np.sqrt( dxdt2 ** 2 + dydt2 ** 2 )
            Deltaphi_p = np.arctan2( dydt2, dxdt2 ) - phi_p

            # distance change between ray and cross-ray
            dDeltandt = Deltaphi_p * cbar1_g  # direction difference * c_g

            # energy change
            G_n = Deltaphi_p / Deltan_0 * (
                    Deltan[ i, : ] / Deltan_0 / ((Deltan[ i, : ] / Deltan_0) ** 2 + (0.5 * np.sqrt( cg_ratio )) ** 2))
            dlncge = -cbar1_g * G_n

            # update wave trains
            x[ i + 1, : ] = x[ i, : ] + dxdt1 * dt[ i ]
            y[ i + 1, : ] = y[ i, : ] + dydt1 * dt[ i ]
            kx[ i + 1, : ] = kx[ i, : ] + dkxdt1 * dt[ i ]
            ky[ i + 1, : ] = ky[ i, : ] + dkydt1 * dt[ i ]
            Deltan[ i + 1, : ] = Deltan[ i, : ] + dDeltandt * dt[ i ]
            e[ i + 1, : ] = np.exp( np.log( cbar1_g * e[ i, : ] ) + dlncge * dt[ i ] ) / cbar1_g

        return kx, ky, x, y, e, Deltan

    # generate (developed) wave rays with current interaction
    # this is a combination of Quilfen and Chapron (2019) and Kudryavtsev et al. (2021)
    # FIXME: this should still be tested
    def wave_field_currents_and_wind( self, x_0, y_0, u, v, u_w, v_w, t, Hs_0, phi_p0, Deltan_0 = 50 ):
        # x0, y0: initial locations
        # u, v: current velocity grids
        # u_w, v_w: wind speed grids
        # Hs_0: initial significant wave height (not used at the moment)
        # phi_p0: initial wave direction with respect to East (not used at the moment)
        # Deltan_0: initial wave-ray width

        # some constants
        g = 9.81
        cg_ratio = 4.6E-2

        # get the gradients
        dudx = np.gradient( u, self.x_res, axis = 1 )
        dudy = np.gradient( u, self.y_res, axis = 0 )
        dvdx = np.gradient( v, self.x_res, axis = 1 )
        dvdy = np.gradient( v, self.y_res, axis = 0 )

        # interpolate gradients and velocities
        shp = u.shape
        xg = np.arange( 0, shp[ 1 ] * self.x_res, self.x_res )
        yg = np.arange( 0, shp[ 0 ] * self.y_res, self.y_res )
        f_ux = interpolate.RectBivariateSpline( yg, xg, dudx )  # watch out, this thing flips the y and x axis
        f_uy = interpolate.RectBivariateSpline( yg, xg, dudy )
        f_vx = interpolate.RectBivariateSpline( yg, xg, dvdx )
        f_vy = interpolate.RectBivariateSpline( yg, xg, dvdy )
        f_u = interpolate.RectBivariateSpline( yg, xg, u )
        f_v = interpolate.RectBivariateSpline( yg, xg, v )
        f_uw = interpolate.RectBivariateSpline( yg, xg, u_w )
        f_vw = interpolate.RectBivariateSpline( yg, xg, v_w )

        # initial wind input
        uw_int = f_uw.ev( y_0, x_0 )
        vw_int = f_vw.ev( y_0, x_0 )
        u_10 = np.sqrt( uw_int ** 2 + vw_int ** 2 )
        phi_w = np.arctan2( vw_int, uw_int )

        # some constants
        # b=0.06 # From 'Duncan' in Phillips (1985)
        q = -1 / 4  # (-0.33 - -0.23) Kudryavstev et al. (2015)
        p = 3 / 4  # (0.7 - 1.1) Kudryavstev et al. (2015)
        ph = 10  # p for the Heaviside function
        c_e = 1.2E-6  # (0.7E-7 - 18.9E-7) Badulin et al. (2007)
        c_alpha = 12  # (10.4 - 22.7) Badulin et al. (2007)
        C_e = 2.46E-4  # Chapron et al. (2020)
        C_alpha = -1.4  # Chapron et al. (2020)
        # c_beta=4E-2 # Chapron et al. (2020)
        cg_ratio = 4.6E-2  # this is Delta c_g / c_g from the JONSWAP spectrum
        C_phi = 1.8E-5  # constant from the JONSWAP spectrum
        g = 9.81
        eps_t = np.sqrt( 0.135 )  # threshold steepness (squared)
        r_g = 0.9
        n = 2 * q / (p + 4 * q)

        # set the initial conditions
        x = np.zeros( (len( t ), len( x_0 )) )
        y = np.zeros( (len( t ), len( x_0 )) )
        phi_p = np.zeros( (len( t ), len( x_0 )) )
        c_gp = np.zeros( (len( t ), len( x_0 )) )
        e = np.zeros( (len( t ), len( x_0 )) )
        Deltan = np.zeros( (len( t ), len( x_0 )) )
        Deltan[ 0, : ] = Deltan_0
        phi_p[ 0, : ] = np.deg2rad(phi_p0)#phi_w+np.random.rand(len(phi_w))*30/180*np.pi  # np.deg2rad(phi_p0)
        #omega_0 = 1.5
        #c_gp[ 0, : ] = g / omega_0 / 2
        #c_p = c_gp[ 0, : ] * 2
        #alpha = u_10 / c_p
        #e[ 0, : ] = u_10 ** 4 / g ** 2 * c_e * (alpha / c_alpha) ** (p / q)
        #e[ 0, : ] = u_mean ** 4 / g ** 2 * c_e * (alpha / c_alpha) ** (p / q)
        e[ 0, : ] = (Hs_0 / 4) ** 2
        alpha = (e [0, :] * g ** 2 / c_e / u_10 ** 4) ** (q / p) * c_alpha
        c_p = u_10 / alpha
        c_gp[0, :] = c_p / 2
        x[ 0, : ] = x_0
        y[ 0, : ] = y_0
        Deltaphi_p = np.zeros( len( x_0 ) )

        # update equations
        for i in range( 0, len( t ) - 1 ):
            dt = t[ i + 1 ] - t[ i ]

            #################### interpolate currents #####################
            # interpolate currents
            dudx_int1 = f_ux.ev( y[ i, : ], x[ i, : ] )  # x and y should be flipped here as well
            dvdx_int1 = f_vx.ev( y[ i, : ], x[ i, : ] )
            dudy_int1 = f_uy.ev( y[ i, : ], x[ i, : ] )
            dvdy_int1 = f_vy.ev( y[ i, : ], x[ i, : ] )
            u_int1 = f_u.ev( y[ i, : ], x[ i, : ] )
            v_int1 = f_v.ev( y[ i, : ], x[ i, : ] )

            # interpolate currents for the cross-ray widening
            x2 = x[ i, : ] - Deltan[ i, : ] * np.cos( phi_p[ i, : ] + np.pi / 2 )
            y2 = y[ i, : ] - Deltan[ i, : ] * np.sin( phi_p[ i, : ] + np.pi / 2 )
            dudx_int2 = f_ux.ev( y2, x2 )
            dvdx_int2 = f_vx.ev( y2, x2 )
            dudy_int2 = f_uy.ev( y2, x2 )
            dvdy_int2 = f_vy.ev( y2, x2 )
            # u_int2 = f_u.ev( y2, x2 )
            # v_int2 = f_v.ev( y2, x2 )

            #################### interpolate wind #####################
            # interpolate wind
            uw_int1 = f_uw.ev( y[ i, : ], x[ i, : ] )
            vw_int1 = f_vw.ev( y[ i, : ], x[ i, : ] )

            # interpolate wind for cross-ray widening
            uw_int2 = f_uw.ev( y2, x2 )
            vw_int2 = f_vw.ev( y2, x2 )

            #################### supporting equations #####################
            # some equations for wave age, wavelength, etc.
            u_10 = np.sqrt( uw_int1 ** 2 + vw_int1 ** 2 )
            phi_w = np.arctan2( vw_int1, uw_int1 )
            Deltaphi_w = phi_w - np.arctan2( vw_int2, uw_int2 )
            u_c = np.sqrt( u_int1 ** 2 + v_int1 ** 2 )
            phi_c = np.arctan2( v_int1, u_int1 )
            c_p = c_gp[ i, : ] * 2
            alpha = u_10 / c_p
            cbar_g = r_g * c_gp[ i, : ]
            k_p = g / 4 / (c_gp[ i, : ] - u_c * np.cos( phi_c )) ** 2
            omega_p = c_p * k_p
            kx = k_p * np.cos( phi_p[ i, : ] )
            ky = k_p * np.sin( phi_p[ i, : ] )

            # equations required for wind derivative
            Delta_p = 1 - 2 / np.cosh( 10 * (alpha - 0.9) ) ** 2
            H_p = 1 / 2 * (1 + np.tanh( ph * (np.cos( phi_p[ i, : ] - phi_w ) * alpha - 1) ))
            G_n = Deltaphi_p / Deltan_0 * (
                    Deltan[ i, : ] / Deltan_0 / ((Deltan[ i, : ] / Deltan_0) ** 2 + (0.5 * np.sqrt( cg_ratio )) ** 2))
            Iw = C_e * H_p * alpha ** 2 * np.cos( phi_p[ i, : ] - phi_w ) ** 2
            D = (e[ i, : ] * k_p ** 2 / eps_t ** 2) ** n
            Tinv = 2 * C_phi * H_p * alpha ** 2 * omega_p * np.cos( 2 * (phi_p[ i, : ] - phi_w) )

            # currents derivates
            # 
            #dkxdt = -(kx * dudx_int1 + ky * dvdx_int1)
            #dkydt = -(kx * dudy_int1 + ky * dvdy_int1)
            #dkpdt = 1/k_p * ( kx * dkxdt + ky * dkydt )
            #dphi_curr = 1 / k_p ** 2 * (kx * dkydt - ky * dkxdt)  # derivative of direction due to currents
            #dudt = dudx_int1 * c_gp[ i, : ] * np.cos( phi_p[ i, : ] ) + dudy_int1 * c_gp[ i, : ] * np.sin(
            #    phi_p[ i, : ] )
            #dAxdt = -1 / 4 * g ** 0.5 / k_p ** (3 / 2) * np.cos(
            #    phi_p[ i, : ] ) * dkpdt - 1 / 2 * g ** 0.5 / k_p ** 0.5 * np.sin(
            #    phi_p[ i, : ] ) * dphi_curr
            #dAydt = -1 / 4 * g ** 0.5 / k_p ** (3 / 2) * np.sin(
            #    phi_p[ i, : ] ) * dkpdt + 1 / 2 * g ** 0.5 / k_p ** 0.5 * np.cos(
            #    phi_p[ i, : ] ) * dphi_curr
            #dvdt = dvdx_int1 * c_gp[ i, : ] * np.cos( phi_p[ i, : ] ) + dvdy_int1 * c_gp[ i, : ] * np.sin(
            #    phi_p[ i, : ] )
            #dcxdt = dAxdt + dudt
            #dcydt = dAydt + dvdt
            #print(dAxdt[2],dAydt[2],dudt[2],dvdt[2])
            #print(dphi_curr[2])
            #dc_curr = np.cos( phi_p[ i, : ] ) * dcxdt + np.sin(
            #    phi_p[ i, : ] ) * dcydt  # derivative of group velocity due to currents
            #dkxdt = -(kx * dudx_int2 + ky * dvdx_int2)
            #dkydt = -(kx * dudy_int2 + ky * dvdy_int2)
            #dDeltaphi_curr = dphi_curr - 1 / k_p ** 2 * (
            #            kx * dkydt - ky * dkxdt)  # derivative of direction due to currents
            # 

            # group velocity derivative
            dc_gp = -r_g * C_alpha / 2 * Delta_p * g * (k_p ** 2 * e[ i, : ]) ** 2 + dc_curr
            c_gp[ i + 1, : ] = c_gp[ i, : ] + dc_gp * dt
            #print(-r_g * C_alpha / 2 * Delta_p[2] * g * (k_p[2] ** 2 * e[ i, 2 ]) ** 2)
            #print(dc_curr[2])

            # modified energy derivative
            dlncge = -cbar_g * G_n + omega_p * (Iw - D)
            e[ i + 1, : ] = np.exp( np.log( cbar_g * e[ i, : ] ) + dlncge * dt ) / cbar_g

            # spectral peak direction derivative
            dphi_p = -C_phi * alpha ** 2 * omega_p * H_p * np.sin( 2 * (phi_p[ i, : ] - phi_w) ) + dphi_curr
            phi_p[ i + 1, : ] = phi_p[ i, : ] + dphi_p * dt

            # wave train position derivatives (in the eye coordinate system)
            dx = np.cos( phi_p[ i, : ] ) * cbar_g  # phi_p is with respect to North
            dy = np.sin( phi_p[ i, : ] ) * cbar_g
            x[ i + 1, : ] = x[ i, : ] + dx * dt
            y[ i + 1, : ] = y[ i, : ] + dy * dt

            # update Deltan
            dDeltan = Deltaphi_p * cbar_g
            Deltan[ i + 1, : ] = Deltan[ i, : ] + dDeltan * dt

            # spectral peak direction gradient
            dDeltaphi_p = -Tinv * ((Deltaphi_p - Deltaphi_w)) + dDeltaphi_curr
            Deltaphi_p = Deltaphi_p + dDeltaphi_p * dt

        return x, y, c_gp, e, np.rad2deg( phi_p ), Deltan



    # get wave train fluxes
    # FIXME: this does not really work
    def get_flux( self, x_t, y_t, xs, ys, dr ):
        # x_t,y_t: wave train coordinates
        # xs,ys: grid coordinates
        # dr: box size (one-dimensional)

        SHP = xs.shape

        N = np.zeros( SHP )
        for i in range( 0, SHP[ 0 ] ):
            if np.mod( i, 100 ) == 0:
                print( i / SHP[ 0 ] * 100 )
            for j in range( 0, SHP[ 1 ] ):
                I = np.zeros( x_t.shape )
                dx_t = np.absolute( x_t - xs[ j ] )
                dy_t = np.absolute( y_t - ys[ i ] )
                I[ np.logical_and( dx_t < dr, dy_t < dr ) ] = 1
                N[ i, j ] = np.count_nonzero( np.sum( I, axis = 0 ) )  # the number of wave trains passing through a box

        return N

    # this script detects nearby wave trains, like in 'get_flux'
    # then it selects the wave train with the largest Hs as the dominant one, or interpolates with a Gaussian
    # then it fits a JONSWAP, or Gaussian, etc.
    # FIXME: this does not really work
    def fit_spectrum_o( self, x_t, y_t, Hs_t, kx_t, ky_t, x_s, y_s, dr, k=None, phi=None, dks=None, method = 'maximum', fit = 'nofit' ):
        # x_t,y_t: wave train coordinates
        # Hs_t: significant wave height
        # xs,ys: a single set of grid coordinates
        # dr: box size (one-dimensional)
        # k: two-dimensional Cartesian grid of wave numbers
        # phi: two-dimensional Cartesian grid of wave number directions
        # dks: two-dimensional (dk*dk) Cartesian grid size for normalization
        # method: 'maximum' use wave train with maximum wave energy
        #         'Gaussian' interpolate using Gaussian radial basis function
        # fit: 'nofit' does not fit any wave spectrum
        #      'JONSWAP' fits a JONSWAP

        g = 9.81

        # get indices of wave trains near
        dx_t = np.absolute( x_t.ravel() - x_s )
        dy_t = np.absolute( y_t.ravel() - y_s )
        I = np.where( np.logical_and( dx_t < dr, dy_t < dr ) )[ 0 ]
        Hs_t = Hs_t.ravel()

        # get the 'maximum'
        if method == 'maximum':
            if np.any( I ):
                Jmax = np.argmax( Hs_t[ I ] )
                Imax = I[ Jmax ]
            if np.any( I ) == False:
                d_t = np.sqrt( dx_t ** 2 + dy_t ** 2 )
                Imax = np.argmin( d_t )

            # input variables for wave spectrum
            ky_t = ky_t.ravel()
            kx_t = kx_t.ravel()
            phi_p = np.arctan2(ky_t[Imax], kx_t[Imax])
            k_p = np.sqrt(kx_t[Imax] ** 2 + ky_t[Imax] ** 2)
            omega_p = np.sqrt(g * k_p)  # FIXME: do we have correct currents here?
            Hs = Hs_t[Imax]

        if method == 'Gaussian':
            # Radial basis functions
            d_t = np.sqrt(dx_t[I] ** 2 + dy_t[I] ** 2)
            G=np.exp(-d_t**2/(dr/2)**2) # simple G over two
            G=G/np.sum(G)
            kx = np.sum(np.ravel(kx_t)[I] * G)
            ky = np.sum(np.ravel(ky_t)[I] * G)
            phi_p = np.arctan2(ky, kx)
            k_p = np.sqrt(kx ** 2 + ky ** 2)
            omega_p = np.sqrt(g * k_p)
            Hs = np.sum(np.ravel(Hs_t)[I] * G)

        # fit a jonswap spectrum
        if fit == 'JONSWAP':
            S = wave_spectra.jonswap_hs( k, phi, omega_p, phi_p, Hs, dks, gamma = 3.3 )

            return S, k_p, phi_p, Hs

        if fit == 'nofit':
            return k_p, phi_p, Hs
    '''


if __name__ == '__main__':
    import os
    import numpy as np
    from matplotlib import pyplot as plt

    # Note that I just use the 'lon'-direction as the x-direction and 'lat'-direction as the y-direction,
    # so they are not radar coordinates
    # '''
    # Marcel's model
    shp = (100, 20)
    y_res = 2000  # meter
    x_res = 2000  # meter
    basin = 'Atlantic'
    hemisphere = 'Northern'

    # '''
    # Create a wind field
    ws = 20.0  # meter/second: this is a scaling parameter, but not the maximum
    wdir = 0.0  # North is 0 deg, clockwise positive
    scene = SceneGenerator(shp, x_res, y_res, basin, hemisphere)
    x1, y1, vx1, vy1 = scene.uniform_wind(ws, wdir)

    # Compute the waves
    n = np.arange(0, 1000)
    dt = 1.01 ** n;
    dt[dt > 500] = 500
    t = np.cumsum(dt);
    t = t - t[0]
    x_0 = np.array([0.0E3, 15.0E3])  # initial position wave train
    y_0 = np.array([0.0E3, 10.0E3])  # initial position wave train
    x_wt, y_wt, c_gp, e, phi_p = scene.wave_field(t, x_0, y_0, vx1, vy1, x1, y1)

    # print energy
    g = 9.81
    c_e = 1.2E-6  # (0.7E-7 - 18.9E-7) Badulin et al. (2007)
    c_alpha = 12  # (10.4 - 22.7) Badulin et al. (2007)
    q = -1 / 4  # (-0.33 - -0.23) Kudryavstev et al. (2015)
    p = 3 / 4  # (0.7 - 1.1) Kudryavstev et al. (2015)
    x_tilde = np.sqrt((x_wt - x_0) ** 2 + (y_wt - y_0) ** 2) * g / ws ** 2  # dimensionless fetch
    e_tilde = c_e * x_tilde ** p  # dimensionless energy
    c_p = c_gp * 2
    alpha = ws / c_p
    alpha_tilde = c_alpha * x_tilde ** q
    e_tilde2 = c_e * (alpha / c_alpha) ** (p / q)

    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x_tilde, alpha, 'b', label='u/c_p')
    plt.plot(x_tilde, alpha_tilde, 'r', label='c_alpha*x_tilde^q')
    plt.xlabel('dimensionless fetch')
    plt.ylabel('dimensionless wave age/frequency')
    # plt.xlim(10 ** 3, 10 ** 5.5)
    # plt.ylim(0, 3)
    # plt.xscale('log')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x_tilde, e * g ** 2 / ws ** 4, 'b', label='from integration')
    plt.plot(x_tilde, e_tilde, 'r', label='c_e * x_tilde^p')
    plt.plot(x_tilde, e_tilde2, 'g--', label='c_e * (alpha / c_alpha)^(p/q)')
    plt.xlabel('dimensionless fetch')
    plt.ylabel('dimensionless energy')
    # plt.xlim(10 ** 3, 10 ** 5.5)
    # plt.ylim(10**-4, 10**-1)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    # '''
