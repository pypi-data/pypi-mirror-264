#%%
import os

import numpy as np
import scipy as sp
from scipy import ndimage
import scipy.io as spio
import scipy.io
from scipy.interpolate import griddata
from scipy.integrate import cumtrapz, trapz
from matplotlib import pyplot as plt
from drama import constants as cnst
from drama import utils as drtls

from pylab import cm
from typing import Tuple, Optional

#  to ignore the warnings by nan
import warnings

#warnings.simplefilter(action="ignore", category=RuntimeWarning)

def tc_wake_kudry19(input_file, show_plots=False):
    """ Generate cold wake of a tropical cyclone
    
    This is an implemetation of the theory in
    [1] V. Kudryavtsev, A. Monzikova, C. Combot, B. Chapron, and N. Reul, 
    “A Simplified Model for the Baroclinic and Barotropic Ocean Response to Moving Tropical Cyclones: 2. 
    Model and Simulations,” 
    Journal of Geophysical Research: Oceans, vol. 0, no. 0, Apr. 2019, doi: 10.1029/2018JC014747.
    [2] V. Kudryavtsev, A. Monzikova, C. Combot, B. Chapron, N. Reul, and Y. Quilfen, “
    A Simplified Model for the Baroclinic and Barotropic Ocean Response to Moving Tropical Cyclones: 1. 
    Satellite Observations,” 
    Journal of Geophysical Research: Oceans, vol. 0, no. 0, Apr. 2019, doi: 10.1029/2018JC014746.
    The initial matlab code was written by Anya Monzikova. This python version is based on matlab code
    provided by Clement Combot. Translation to Python and by Paco Lopez-Dekker and ChatGPT.

    Args:
        input_file (_type_): _description_
        show_plots (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    #read data
    mat = sp.io.loadmat(input_file)
    argo_pressure = mat['argo_Press'].flatten()
    argo_temp = mat['argo_Temp'].flatten()
    argo_psal = mat['argo_Psal'].flatten()
    valind = np.argwhere(~np.isnan(argo_pressure + argo_temp +argo_psal))
    if  show_plots:
        plt.figure()
        plt.plot(argo_temp[valind], -argo_pressure[valind])
        plt.figure()
        plt.plot(argo_psal[valind], -argo_pressure[valind])
    depth = argo_pressure[valind].flatten()
    Tz_in =  argo_temp[valind].flatten()
    Sz_in= argo_psal[valind].flatten()

    # INPUT PARAMETERS
    lat = mat['lat'][0,0]
    print(lat)
    R_m = mat['R_m'][0,0]
    V_m = mat['V_m'][0,0]
    print(R_m)
    U = mat['U'][0,0]
    # CONSTANTS
    g = 9.8
    al = 2.5e-4
    OMEGA = 7.29e-5
    B = 1.5
    da = np.pi/8
    ch = 0.63
    h0 = 0
    NM = 6
    H = 5e3 #np.max(depth)
    C0 = np.sqrt(g*H)

    f = 2 * np.sin(lat/180*np.pi) * OMEGA
    fr = np.zeros_like(f)

    # GRID
    dx = R_m/10
    dy = dx
    sf = 10
    ymax = sf*R_m
    ymin = -sf*R_m
    xmin = -5*R_m
    xmax = 2*sf*R_m
    Ny = int(np.floor((ymax-ymin)/dy)+1)
    Nx = int(np.floor((xmax-xmin)/dx)+1)
    y = np.linspace(ymin, ymax, Ny)
    x = np.linspace(xmin, xmax, Nx)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    R = np.where(R>0, R, 1e-3)


    # FOURIER SPACE

    Kx = 2*np.pi*np.fft.fftfreq(Nx, dx)
    Ky = 2*np.pi*np.fft.fftfreq(Ny, dy)
    KX, KY = np.meshgrid(Kx, Ky)

    # VERTICAL DOMAIN
    zmin = 0.1
    zmax = min(H, np.round(np.max(depth)))
    #zmax=3e3
    dz = 1
    Nz = int(np.floor((zmax-zmin)/dz)+1)
    z = np.linspace(zmin, zmax, Nz)

    # STRATIFICATION: 3-layer-N_MODEL, (N1,N2)>f, Omega<(N1,N2)
    Tz = np.interp(z, depth, Tz_in)
    Sz = np.interp(z, depth, Sz_in)
    GT = np.gradient(Tz, dz)
    GT = np.minimum(0, GT)

    rho = 1.0235 * (1 - 2.7e-4 * (Tz-27) + 7.6e-4 * (Sz-36)) - 1
    Grho = np.gradient(rho, dz)
    Grho = np.maximum(0, Grho)
    Grho.shape

    T1 = rho
    # Calculate gradients and second derivatives
    GT1 = -1 * np.gradient(T1, dz)
    G2T1 = np.gradient(drtls.smooth(GT1,5), dz)
    indh1 = np.argmin(G2T1)
    h1 = z[indh1]
    indH = np.argmin(np.abs(cumtrapz(GT1, z, initial=0) - 0.95*np.trapz(GT1, z)))

    # Calculate values for t2
    t3 = T1[indH]
    t1 = T1[indh1]
    zD = z[indh1+1:indH-1] - h1
    z1 = z[indh1:indH] - h1
    H1 = z[indH] - h1
    T = T1[indh1:indH]
    TD = T1[indh1+1:indH-1]
    cumD = cumtrapz(TD, zD, initial=0) + np.trapz(T[:2], z1[:2])
    cumDH = np.trapz(T, z1) - cumD #[-1]
    cumzD = cumtrapz(TD*zD, zD, initial=0) + np.trapz(T[:2]*z1[:2], z1[:2])
    # cumzDH = np.trapz(T*z1, z1-h1) - cumzD[-1] - zD[-1]*cumDH
    cumzDH = np.trapz(T*z1, z1) - cumzD - zD*cumDH
    t2 = 3/H1 * (1/zD*cumzD - 1/(H1-zD)*cumzDH + cumDH) - 0.5*(t1*zD/H1 + t3*(H1-zD)/H1)

    # Calculate values for F1 and F2
    F1 = -2*t1*cumD - 2*(t2-t1)/zD*cumzD + (t1*t2 + 1/3*(t2-t1)**2)*zD
    F2 = -2*t2*cumDH - 2*(t3-t2)/(H1-zD)*cumzDH + (t3*t2 + 1/3*(t3-t2)**2)*(H1-zD)

    # Calculate value for tD
    F = F1 + F2
    indD = np.argmin(F)
    tD = t2[indD]
    d1 = zD[indD] + h1
    d2 = z[indH]

    # Calculate values for GradT_upper and N1, N2
    GradT_upper = (tD-t1)/(d1-h1)/2.7e-4
    N1 = np.sqrt(g*(tD-t1)/(d1-h1))
    N2 = np.sqrt(g*(t3-tD)/(d2-d1))

    # Plot results
    if show_plots:
        plt.figure(22)
        plt.plot(rho, -z)
        plt.figure(23)
        plt.plot(Tz, -z)
        plt.figure(24)
        plt.plot(Sz, -z)
        plt.show()

    # Holland [1980] profile
    # V = np.sqrt((V_m**2 + V_m*R_m*f) * (R_m/R)**B * np.exp(-(R_m/R)**B)/np.exp(-1) + (R**2)* (f**2) /4) - R*f/2;
    V = np.sqrt((V_m**2 + V_m*R_m*f) * (R_m/R)**B * np.exp(-(R_m/R)**B)/np.exp(-1) + (R**2) * (f**2)/4) - R*f/2

    coswd = -Y / (R+1e-3)
    sinwd = X / (R+1e-3)

    # da = np.pi/2
    Vu = (coswd*np.cos(da) - sinwd*np.sin(da)) * V
    Vv = (sinwd*np.cos(da) + coswd*np.sin(da)) * V

    # Surface stress in the water
    z0 = 0.012*(1.5e-3*V**2/g)
    C_d1 = (0.41/np.log(10/z0))**2
    tau0 = C_d1 * V**2
    n = 2
    tauf = 2.5
    tao0 = ((1/tau0)**n + (1/tauf)**n)**(-1/n) * 1.3e-3
    C_d = tao0 / V**2 / 1.3e-3

    tao_x = (coswd*np.cos(da) - sinwd*np.sin(da)) * tao0
    tao_y = (sinwd*np.cos(da) + coswd*np.sin(da)) * tao0
    T = tao_x + 1j * tao_y
    dtxy, dtxx = np.gradient(tao_x, dx, dy)
    dtyy, dtyx = np.gradient(tao_y, dx, dy)
    rotT = dtyx - dtxy
 
    #
    # Baroclinic response
    print("Computing Baroclinic response")
    D0 = d2
    d2 = d2 - d1

    N = np.where(z < d1, N1, np.where((z >= d1) & (z < D0), N2, 0))
    SNh = N1 * d1 + N2 * d2
    DNh = N1 * d1 - N2 * d2
    r = (N1 - N2) / (N1 + N2)

    # IW phase velocity
    cj = np.linspace(0.2, 10, 50000)
    phi_H = np.arcsin((N2*(H-D0)/cj)/np.sqrt(1 + (N2*(H-D0)/cj)**2))
    phi = np.sin(SNh/cj+phi_H) - r*np.sin(DNh/cj-phi_H)
    msk = np.logical_and(phi > -0.01, phi < 0.01)
    cc = cj * msk
    c = np.zeros(NM)
    for nm in range(NM):
        xx = np.max(cc)
        mskt = cc > (0.9 * xx)
        ind = np.where(mskt)[0]
        c[nm] = np.mean(cc[ind])
        cc *= (1 - mskt)

    wz = np.zeros((NM, z.size))
    w0 = np.zeros((NM, Ny, Nx))
    d0 = np.zeros((NM, Ny, Nx))
    E = np.zeros(NM)
    E1 = np.zeros(NM)
    w01 = np.zeros(NM)
    w02 = np.zeros(NM)
    for nm in range(NM):
        C = c[nm]
        alf = f/C
        par = (U/C)**2 - 1

        w2 = np.zeros((Ny, Nx), dtype=complex)
        w = np.zeros((Ny, Nx), dtype=complex)
        RTfy = np.zeros((Ny, Nx))
        phi_H = np.arcsin((N2*(H-D0)/C) / np.sqrt(1 + (N2*(H-D0)/C)**2))
        # phi_H = np.pi/2
        # Vertical profile
        w01[nm] = 2*C/SNh*(np.cos(SNh/C+phi_H) - r*np.cos(DNh/C-phi_H)) / \
            (np.cos(SNh/C+phi_H) - r*np.cos(DNh/C-phi_H)*DNh/SNh)
        w02[nm] = 2*C/SNh*2*N1/(N1+N2)/(np.cos(SNh/C+phi_H) - r*np.cos(DNh/C-phi_H)*DNh/SNh)
        wz[nm,:] = (-1 * w01[nm]*np.sin(-N1*z/C)*(z<d1) - w02[nm]*np.sin(N2*(D0-z)/C+phi_H)*((z>=d1) & (z<D0)) - 
                    w02[nm]*np.sin(phi_H)*(H-z)/(max(1e-3,H-D0))*(z>=D0))

        if abs(U) > C:
            Kx0 = np.sqrt(Ky**2 + alf**2) / np.sqrt(par)

            for ix in range(Nx):
                x1 = x[ix]
                for ixx in range(ix):
                    x2 = x[ixx]
                    RTfy = np.fft.fft(rotT[:,ixx])
                    fint = RTfy*np.sin(Kx0.flatten()*(x1-x2))/Kx0.flatten()
                    w2[:,ixx] = np.fft.ifft(fint)
                w[:,ix] = np.trapz(w2, axis=1)*dx
            w = f / (C**2) / par * w
            wr = np.real(w)
            w0[nm,:,:] = np.real(w)
            aa = np.squeeze(w0[nm,:,:])
            d0[nm,:,:] = -cumtrapz(aa, axis=1, initial=0)/U*dx

        else:
            Rot_f = np.fft.fft2(rotT)
            fint = Rot_f / (-par*KX**2 + KY**2 + alf**2) * (f/C**2)
            w = np.fft.ifft2(fint)
            wr = np.real(w)
            w0[nm,:,:] = np.real(w)
            aa = np.squeeze(w0[nm,:,:])
            d0[nm,:,:] = -cumtrapz(aa, axis=1, initial=0)/U*dx

        E[nm] = trapz(N**2*wz[nm,:]**2)*dz*np.max(d0[nm,:,:])**2
        E1[nm] = trapz(N**2*wz[nm,:]**2)*dz*np.std(d0[nm,:,:])**2

    # Thermocline depth
    iD1 = np.argmin(abs(z-d1))
    iD2 = np.argmin(abs(z-D0))
    D1 = np.zeros((NM, Ny, Nx))
    D2 = np.zeros((NM, Ny, Nx))
    D1[0, :, :] = wz[0, iD1]*d0[0, :, :]
    D2[0, :, :] = wz[0, iD2]*d0[0, :, :]

    for nm in range(NM):
        D1[nm, :, :] = wz[nm, iD1]*d0[nm, :, :] + D1[nm-1, :, :]
        D2[nm, :, :] = wz[nm, iD2]*d0[nm, :, :] + D2[nm-1, :, :]

    D1 = -d1 + D1  # Depth of seasonal thermocline
    D2 = -D0 + D2  # Depth of main thermocline

    from scipy.integrate import cumulative_trapezoid

    L0 = U / (f - 1j * fr)
    Mstark = -np.exp(1j * X / L0) * cumulative_trapezoid(T / U * np.exp(-1j * X / L0), dx=dx, initial=0, axis=1)
    Mstar = np.abs(Mstark)

    # Depth caused by mixing
    # h = np.sqrt(ch * np.sqrt(2) * Mstar / f / np.sqrt(1 + np.sqrt(1 + ch ** 2 * N1 ** 4 / f ** 4)))
    # h[h == 0] = 0.001

    hh = np.zeros_like(Mstar)
    We = np.zeros_like(Mstar)
    G = np.zeros_like(Mstar)
    h = np.zeros_like(Mstar)
    ih = np.zeros_like(Mstar)
    print(Mstar.shape)
    SST = np.zeros_like(Mstar)

    rp = ch * Mstar ** 2
    sum_rho = 1 / z * cumulative_trapezoid(z * Grho, x=z, initial=0)

    dh = -np.abs(cumulative_trapezoid(w0[0], dx=dx, axis=1)) / U * dx

    for jy in range(Ny):
        for jx in range(Nx):
            lp = z ** 3 * ((-g * sum_rho) ** 2 + 1 * (Mstar[jy, jx] * f / z) ** 2) ** 0.5
            dif = (lp - rp[jy, jx]) > 0
            ih[jy, jx] = np.argmax(dif, axis=0)
            h[jy, jx] = z[int(ih[jy, jx])]

            ih[jy, jx] = np.argmin(np.abs(z - h[jy, int(np.max([0, jx - 1]))]), axis=0)
            wh = wz[0, int(ih[jy, jx])] * w0[0, jy, jx]

            if h[jy, jx] > hh[jy, max(0, jx - 1)]:
                hh[jy, jx] = h[jy, jx]
                We[jy, jx] = -U * (h[jy, jx] - h[jy, max(0, jx - 1)]) / dx + wh
                G[jy, jx] = 2 / (hh[jy, jx]) ** 2 * np.trapz(-z[z <= hh[jy, jx]] * GT[z <= hh[jy, jx]], z[z <= hh[jy, jx]])
                SST[jy, jx] = SST[jy, max(0, jx - 1)] + dx / 2 / U * G[jy, jx] * We[jy, jx]
            else:
                hh[jy, jx] = hh[jy, max(0, jx - 1)] + wh * dx / U
                We[jy, jx] = 0
                G[jy, jx] = G[jy, max(0, jx - 1)]
                SST[jy, jx] = SST[jy, max(0, jx - 1)]

    Y1 = Y - 1 / U * cumtrapz(np.imag(Mstark) / hh, axis=1, initial=0) * dx
    SST = griddata((X.flatten(), Y1.flatten()), SST.flatten(), (X, Y))

    #
    h_bc_s = np.zeros((NM,Ny,Nx))
    h_bc_s[0,:,:] = -w01[0]*d0[0,:,:]*N1*c[0]/g
    Es = np.zeros((NM,))
    Es[0] = np.max(np.abs(h_bc_s[0,:,:]))
    for nm in range(1, NM):
        h_bc_s[nm,:,:] = -w01[nm]*d0[nm,:,:]*N1*c[nm]/g + h_bc_s[nm-1,:,:]
        Es[nm] = np.max(np.abs(h_bc_s[nm,:,:]-h_bc_s[nm-1,:,:]))
    hs_bc = h_bc_s[NM-1,:,:]

    # Compute the barotropic mode
    Rot_f = np.fft.fft2(rotT)
    Rot_f[0,0] = 0
    fint1 = -Rot_f/(1e-80+KX**2+KY**2)*(f/C0**2)
    w = np.fft.ifft2(fint1)
    wr_bt = np.real(w)
    hs_bt = -1/U*cumtrapz(wr_bt, None, 2,initial=0)*dx #BRT Surface

    # Compute the barotropic stream function
    fint = -Rot_f/(1e-80+KX**2+KY**2)
    dphit = np.fft.ifft2(fint)
    dphit = np.real(dphit)
    phi = -1/U*cumtrapz(dphit, None, 2,initial=0)*dx/H
    gphix,gphiy = np.gradient(phi, dx, dy)
    W_bt = -gphiy + 1j*gphix #BRT complex velocity

    # Compute the full solution for surface elevation
    hs = hs_bt + hs_bc
    # Surface currents
    [dhsy,dhsx] = np.gradient(hs);
    dhs = dhsx/dx + 1j * dhsy/dy;
    FT = -g * hh * dhs + T

    L0=U/(f - 1j * fr);
    Mtk = -np.exp(1j * X/L0) * cumtrapz(FT / U * np.exp(-1j*X/L0), initial=0, axis=1) * dx;
    u_total = Mtk/hh
    sc_u = np.real(u_total)
    sc_v = np.imag(u_total)
    sc = np.stack([sc_u, sc_v], axis=-1)
    res = {'x': X,  'y': Y, 'SC': sc, 'U': np.stack([Vu, Vv], axis=-1), 
           'SSHA': hs,
           'SSHA_bc': hs_bc,
           'SSHA_bt': hs_bt,
           'SST': SST,
           'lat0': lat}
    return res


def tc_wake_scene(tc_wake_dct: dict, 
                  smp_out: Optional[float] = None,
                  tc_heading: Optional[float] = -90,
                  orb_heading: Optional[float] = -8,
                  lon0: Optional[float] = -60
                  ) -> Tuple[dict, float]:
    """
    Take tc_wake output and return scene for Harmony simulation
    :param matfile:
    :return: dic
    """

    tsc_v = tc_wake_dct['SC']
    wind_v = tc_wake_dct['U']

    # convert wind stress to wind speed with Cd=1e-3, air_density = 1.22 kg/m^3

    dx = tc_wake_dct['x'][0,1] - tc_wake_dct['x'][0,0]
    dy = tc_wake_dct['y'][1,0] - tc_wake_dct['y'][0,0]
    # print(dx)
    # print(dy)
    lat0 = tc_wake_dct['lat0']
    # We can potentially rotate x and y
    x = tc_wake_dct['x'] 
    y = tc_wake_dct['y']
    scn_rot = np.radians(tc_heading + 90)
    xr = x * np.cos(scn_rot) + y * np.sin(scn_rot)
    yr = y * np.cos(scn_rot) - x * np.sin(scn_rot)
    lon = lon0 + np.degrees(xr / (cnst.r_earth * np.cos(np.radians(lat0))))
    lat = lat0 + np.degrees(yr /cnst.r_earth)
    sst = tc_wake_dct['SST']
    ssha = tc_wake_dct['SSHA']
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
        sst = drtls.linresample(drtls.linresample(sst, xo, axis=1, extrapolate=True),
                                yo, axis=0, extrapolate=True)
        ssha = drtls.linresample(drtls.linresample(ssha, xo, axis=1, extrapolate=True),
                                yo, axis=0, extrapolate=True)
        lon = drtls.linresample(drtls.linresample(lon, xo, axis=1, extrapolate=True),
                                yo, axis=0, extrapolate=True)
        lat = drtls.linresample(drtls.linresample(lat, xo, axis=1, extrapolate=True),
                                yo, axis=0, extrapolate=True)
    # wind_v = np.transpose(wind_v, axes=[1, 0, 2])
    # tsc_v = np.transpose(tsc_v, axes=[1, 0, 2])
    # sst = np.transpose(sst)
    # lat = np.transpose(lat)
    # lon = np.transpose(lon)
    rot_angle = -orb_heading + np.degrees(scn_rot)
    if rot_angle != 0:
        wind_v[np.isnan(wind_v)] = 0
        tsc_v[np.isnan(tsc_v)] = 0
        sst[np.isnan(sst)] = 25
        ssha[np.isnan(ssha)] = -999
        wind_v = np.stack([ndimage.rotate(wind_v[:, :, 0], rot_angle),
                           ndimage.rotate(wind_v[:, :, 1], rot_angle)], axis=-1)
        tsc_v = np.stack([ndimage.rotate(tsc_v[:, :, 0], rot_angle),
                          ndimage.rotate(tsc_v[:, :, 1], rot_angle)], axis=-1)
        sst = ndimage.rotate(sst, rot_angle)
        ssha = ndimage.rotate(ssha, rot_angle)
        xn = np.arange(sst.shape[1])[np.newaxis,:] * smp_out
        yn = np.arange(sst.shape[0])[:, np.newaxis] * smp_out
        xr = xn * np.cos(np.radians(orb_heading)) + yn * np.sin(np.radians(orb_heading))
        yr = yn * np.cos(np.radians(orb_heading)) - xn * np.sin(np.radians(orb_heading))
        lonn = np.degrees(xr / (cnst.r_earth * np.cos(np.radians(lat0))))
        latn = np.degrees(yr /cnst.r_earth)
        lat_ = ndimage.rotate(lat, rot_angle, cval=-999)
        lon_ = ndimage.rotate(lon, rot_angle, cval=-999)
        indorg = np.unravel_index(np.argmin((lat_ - lat0)**2 + (lon_ - lon0)**2), lat_.shape)
        lat = latn - latn[indorg[0], indorg[1]] + lat0
        lon = lonn - lonn[indorg[0], indorg[1]] + lon0
        rot_m = np.array([[np.cos(np.radians(rot_angle)), np.sin(np.radians(rot_angle))],
                          [-np.sin(np.radians(rot_angle)), np.cos(np.radians(rot_angle))]])
        wind_v = np.einsum("lk,ijk->ijl", rot_m, wind_v)
        tsc_v = np.einsum("lk,ijk->ijl", rot_m, tsc_v)
    dic_out = {'tsc': tsc_v, 'wnd': wind_v, 'sst': sst, 'ssha': ssha,
               'lon': lon, 'lat': lat, 'grid_spacing': smp_out}
    return dic_out, smp_out

#%%
if __name__ == '__main__':
    tc = 'jimena'
    if tc == 'hector':
        tc_name = 'hector2018'
        input_file = '/Users/plopezdekker/Documents/WORK/Harmony/DATA/TCs/hector2018/hector2018_10082018_input.mat'
    else:
        tc_name = 'jimena2015'
        input_file = '/Users/plopezdekker/Documents/WORK/Harmony/DATA/TCs/jimena2017/jimena2015_03092015_input.mat'
    mat = sp.io.loadmat(input_file)
    ref_output_file = '/Users/plopezdekker/Documents/WORK/Harmony/DATA/TCs/hector2018/hector2018_10082018_output.mat'
    #ref_output_file = '/Users/plopezdekker/Documents/WORK/Harmony/DATA/TCs/jimena2017/jimena2015_03092015_output.mat'
    # tc_dict = tc_wake_kudry19(input_file)

    tc_scn, smp_out = tc_wake_scene(tc_dict, smp_out=2e3, orb_heading=-10, tc_heading=-80)
    print(tc_scn['wnd'].shape)
    print(tc_scn['tsc'].shape)  

    mtsc = np.linalg.norm(tc_scn['tsc'], axis=-1)
    # mtsc = np.sqrt(scn['usfc']**2 + scn['vsfc']**2)
    mwind = np.linalg.norm(tc_scn['wnd'], axis=-1)
    xs = np.arange(tc_scn['tsc'].shape[1]) * smp_out
    ys = np.arange(tc_scn['tsc'].shape[0]) * smp_out
    plt.figure()
    strm_wind = plt.streamplot(xs / 1e3, ys/ 1e3,
                                tc_scn['wnd'][:, :, 0], tc_scn['wnd'][:, :, 1],
                                color=mwind, cmap='viridis_r')
    plt.colorbar(strm_wind.lines)
    plt.figure()
    strm_wind = plt.streamplot(xs / 1e3, ys/ 1e3,
                                tc_scn['tsc'][:, :, 0], tc_scn['tsc'][:, :, 1],
                                color=mtsc, cmap='viridis_r')
    plt.colorbar(strm_wind.lines)
    # plt.figure()
    # plt.imshow(tc_scn['wnd'][:,:,0], origin='lower')
    # plt.figure()
    # plt.imshow(tc_scn['lon'], origin='lower')
    # plt.colorbar()
    # plt.figure()
    # plt.imshow(tc_scn['lat'], origin='lower')
    # plt.colorbar()
