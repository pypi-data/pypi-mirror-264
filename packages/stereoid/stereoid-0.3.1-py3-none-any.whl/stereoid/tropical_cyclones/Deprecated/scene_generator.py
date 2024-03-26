__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import os
import numpy as np
import scipy as sp
#from scipy.stats import f
from scipy import interpolate
from matplotlib import pyplot as plt
import time

class SceneGenerator(object):
    def __init__(self, shp, x_res, y_res, basin, hemisphere):
        self.shp = shp
        self.x_res = x_res
        self.y_res = y_res
        self.basin = basin
        self.hemisphere = hemisphere

    # compute instant TC eye direction from track
    def TC_eye_direction(self,path,code,year_i,month_i,day_i,t_i,heading):
        # path: path to track files
        # code: tropical storm code
        # year_i: year of S1 overpass
        # month_i: month of S1 overpass
        # day_i: day of S1 overpass
        # hour_i: decimal hour of S1 overpass
        # heading [deg]: satellite heading with respect to North

        # loads atcf tracks of ifremer
        filename=path + 'b' + self.basin + code + str(year_i) + '.dat'
        of = open(filename, 'r')  # We need to re-open the file
        data = of.read()
        of.close()
        lines=data.split('\n')

        # go through lines
        mon=np.zeros(len(lines)-1)
        day = np.zeros(len(lines)-1)
        hou = np.zeros(len(lines)-1)
        lat = np.zeros(len(lines)-1)
        lon = np.zeros(len(lines)-1)
        for i in range(0,len(lines)-1):
            spl=lines[i].split(',')

            # month, day, hour
            d=spl[2]
            mon[i]=float(d[5:7])
            day[i]=float(d[7:9])
            hou[i]=float(d[9:11])

            # coordinates
            lat[i]=float(spl[6][:-1])/10
            if spl[6][-1:] == 'S':
                lat[i]=-lat[i]
            lon[i]=float(spl[7][:-1])/10
            if spl[7][-1:] == 'W':
                lon[i]=-lon[i]


        # for some dark reason there are duplicates records, let's remove
        t=day*24*60*60+hou*60*60 # time from start of the month
        t, ind =np.unique(t, return_index=True)
        lon=lon[ind]
        lat=lat[ind]

        # interpolate lon, lat's to the input time vector
        f=sp.interpolate.interp1d(t,lon,kind='cubic')
        lon=f(t_i)
        f = sp.interpolate.interp1d(t, lat,kind='cubic')
        lat = f(t_i)
        #lon=np.interp(t_i,t,lon)
        #lat=np.interp(t_i,t,lat)

        # convert to local x/y coordinate system
        Re=6371E3;
        lon0=np.min(lon)
        lat0=np.min(lat)
        x=(lon-lon0)/360*2*np.pi*Re*np.cos(np.deg2rad(lat0))
        y=(lat-lat0)/360*2*np.pi*Re

        # rotate to radar coordinates
        heading=np.deg2rad(heading)
        xr=np.cos(heading)*x-np.sin(heading)*y
        yr=-np.sin(heading)*x+np.cos(heading)*y

        # eye velocity in radar reference frame
        dt=t_i[1:]-t_i[:-1]
        vx=(xr[1:]-xr[:-1])/dt
        vy=(yr[1:]-yr[:-1])/dt
        vx=np.append(vx,vx[-1:])
        vy=np.append(vy,vy[-1:])

        return vx, vy, lon, lat, xr, yr #(vx,vy,xr,yr) in radar coordinates (x = cross-track)

    # generate parametric tropical cyclone wind in radar coordinates
    def parametric_TC_Holland(self,eye_loc,u_m,R_m,B,f,phi_in=0,v_eye=0,dir_eye=0):
        # based on Holland (1980), or Eq. 29 in Kudryavtsev et al. (2018)

        # make a grid
        x = np.linspace(0, self.x_res * self.shp[1], self.shp[1],endpoint=False)
        y = np.linspace(0, self.y_res * self.shp[0], self.shp[0],endpoint=False)
        x,y = np.meshgrid(x,y)

        # radial distance from eye wall
        r=np.sqrt((x-eye_loc[1])**2+(y-eye_loc[0])**2)

        # rotational wind speed
        v=((u_m ** 2 + u_m*r*f) * (R_m/r) ** B * np.exp(-(R_m/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2

        # rotational wind direction
        vdir = -np.rad2deg(np.arctan2(y - eye_loc[0], x - eye_loc[1]))-phi_in

        # wind vectors to add the wind speed by hurricane translation
        vx = np.sin(np.deg2rad(vdir))*v+np.sin(np.deg2rad(dir_eye))*v_eye
        vy = np.cos(np.deg2rad(vdir))*v+np.cos(np.deg2rad(dir_eye))*v_eye

        # total wind speed
        #v=np.sqrt(vx**2+vy**2)

        # wind direction
        #vdir=np.rad2deg(np.arctan2(vx,vy))

        return x,y,vx,vy,r

    # generate parametric tropical cyclone wind in radar coordinates
    def parametric_TC_Holland_static(self,eye_loc,u_m,R_m,B,f,phi_in=0):
        # based on Holland (1980), or Eq. 29 in Kudryavtsev et al. (2018)

        # make a grid
        x = np.linspace(0, self.x_res * self.shp[1], self.shp[1],endpoint=False)
        y = np.linspace(0, self.y_res * self.shp[0], self.shp[0],endpoint=False)
        x,y = np.meshgrid(x,y)

        # radial distance from eye wall
        r=np.sqrt((x-eye_loc[1])**2+(y-eye_loc[0])**2)

        # rotational wind speed
        v=((u_m ** 2 + u_m*r*f) * (R_m/r) ** B * np.exp(-(R_m/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2

        # rotational wind direction
        vdir = -np.rad2deg(np.arctan2(y - eye_loc[0], x - eye_loc[1]))-phi_in

        # wind vectors
        vx = np.sin(np.deg2rad(vdir))*v
        vy = np.cos(np.deg2rad(vdir))*v

        return x,y,vx,vy,r

    # generate uniform wind field
    def uniform_wind(self, ws, wdir):

        # make a grid
        x = np.linspace(0, self.x_res * self.shp[1], self.shp[1],endpoint=False)
        y = np.linspace(0, self.y_res * self.shp[0], self.shp[0],endpoint=False)
        x,y = np.meshgrid(x,y)

        # wind speed
        v=np.ones(self.shp)*ws

        # wind direction
        vdir=np.ones(self.shp)*wdir

        # wind vectors
        vx = np.sin(np.deg2rad(vdir))*v
        vy = np.cos(np.deg2rad(vdir))*v

        return x, y, vx, vy

    # generate wave rays (in TC) old version [deprecated]
    def wave_field(self,t,x_0,y_0,vx,vy,x_u,y_u,v_eye=0,dir_eye=0):
        # t [seconds]: time vector
        # x_0, y_0 [meters]: initial position of wave train
        # vx [meters/second]:
        # vy [meters/second]:
        # u_10 [m/s]: wind speed field --- REPLACED
        # eye_loc [meters]: locations of the eye --- REPLACED
        # x_u, y_u [meters]: grid
        # v_eye [meters]: hurricane eye displacement velocity
        # dir_eye [meters]: direction of eye displacement (clockwise positive from North)

        # interpolate wind field
        fvx = sp.interpolate.bisplrep(x_u, y_u, vx)
        fvy = sp.interpolate.bisplrep(x_u, y_u, vy)
        u_int=np.zeros(len(x_0))
        phi_w=np.zeros(len(x_0))
        for i in range(0,len(x_0)):
            vx_temp = sp.interpolate.bisplev(x_0[i], y_0[i],fvx)
            vy_temp = sp.interpolate.bisplev(x_0[i], y_0[i], fvy)
            u_int[i] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
            phi_w[i] = np.arctan2(vx_temp, vy_temp)

        # some constants
        #b=0.06 # From 'Duncan' in Phillips (1985)
        q = -1 / 4 # (-0.33 - -0.23) Kudryavstev et al. (2015)
        p = 3 / 4 # (0.7 - 1.1) Kudryavstev et al. (2015)
        ph= 10 # p for the Heaviside function
        c_e = 1.2E-6 # (0.7E-7 - 18.9E-7) Badulin et al. (2007)
        c_alpha = 12 # (10.4 - 22.7) Badulin et al. (2007)
        C_e=2.46E-4 # Chapron et al. (2020)
        C_alpha=-1.4 # Chapron et al. (2020)
        #c_beta=4E-2 # Chapron et al. (2020)
        cg_ratio = 4.6E-2  # this is Delta c_g / c_g from the JONSWAP spectrum
        C_phi = 1.8E-5  # constant from the JONSWAP spectrum
        g = 9.81
        eps_t = np.sqrt(0.135) # threshold steepness (squared)
        r_g = 0.9
        n = 2 * q / (p + 4 * q)

        # some computation on the wind field and some additional parameters
        # phi_in=np.deg2rad(20) # inward wind
        #r = np.sqrt((x_u - eye_loc[1]) ** 2 + (y_u - eye_loc[0]) ** 2)
        #G_w=1/r
        #Gn_w=-np.absolute(G_w)*np.sin(phi_in) #wind direction gradient (Shea & Gray, 1973)


        # set the initial conditions
        x = np.zeros((len(t),len(x_0)))
        y = np.zeros((len(t),len(x_0)))
        phi_p = np.zeros((len(t),len(x_0)))
        c_gp = np.zeros((len(t),len(x_0)))
        e = np.zeros((len(t),len(x_0)))
        Deltan_0=100.0
        Deltan=Deltan_0*np.ones(len(x_0))
        Deltaphi_p=np.zeros(len(x_0))
        Deltaphi_w = np.zeros(len(x_0))
        phi_p[0,:]= phi_w
        omega_0= 3
        c_gp[0,:]= g / omega_0 / 2
        c_p = c_gp[0,:] * 2
        alpha = u_int / c_p
        e[0,:]=u_int**4/g**2*c_e*(alpha/c_alpha)**(p/q)
        x[0,:]=x_0
        y[0,:]=y_0
        WI=np.ones(len(x_0)) # turns wind influence on and off

        # update equations
        for i in range(0,len(t)-1):
            dt=t[i+1]-t[i]

            # interpolate wind field
            phi_cross=phi_p[i,:]+np.pi/2
            x_cr =  Deltan * np.sin(phi_cross)
            y_cr = Deltan * np.cos(phi_cross)
            for j in range(0, len(x_0)):
                vx_temp = sp.interpolate.bisplev(x[i, j], y[i, j], fvx)
                vy_temp = sp.interpolate.bisplev(x[i, j], y[i, j], fvy)
                u_int[j] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
                phi_w[j] = np.arctan2(vx_temp, vy_temp)
                vx_temp = sp.interpolate.bisplev(x[i, j] + x_cr[j], y[i, j] + y_cr[j], fvx)
                vy_temp = sp.interpolate.bisplev(x[i, j] + x_cr[j], y[i, j] + y_cr[j], fvy)
                Deltaphi_w[j] = np.arctan2(vx_temp, vy_temp) - phi_w[j]

            # some equations for wave age, wavelength, etc.
            c_p = c_gp[i, :] * 2
            alpha = u_int / c_p
            cbar_g = r_g * c_gp[i,:]
            omega_p = g / c_p
            k_p = omega_p / c_p

            # wind input is switched off
            #print(alpha[2]*np.cos(phi_p[i,2]-phi_w[2]),alpha[2],phi_p[i,2],phi_w[2])
            WI[alpha*np.cos(phi_p[i,:]-phi_w) < 1]=0

            # group velocity derivative
            Delta_p = 1 - 2/np.cosh(10*(alpha - 0.9)) ** 2
            dc_gp=-r_g*C_alpha/2*Delta_p*g*(k_p**2*e[i,:])**2 # c_gp in the presentation
            c_gp[i+1,:]=c_gp[i,:]+ dc_gp*dt

            # modified energy derivative
            H_p = 1/2 * (1 + np.tanh( ph * ( np.cos(phi_p[i, :] - phi_w)*alpha - 1) ) )
            G_n=Deltaphi_p/Deltan_0 * (Deltan/Deltan_0 / ((Deltan/Deltan_0)**2 +(0.5*np.sqrt(cg_ratio))**2)) * WI
            Iw = C_e * H_p * alpha ** 2 * np.cos(phi_p[i, :] - phi_w) ** 2 * WI
            D = (e[i, :]*k_p ** 2/eps_t ** 2) ** n
            dlncge = -cbar_g * G_n + omega_p * (Iw-D)
            e[i + 1,:]=np.exp(np.log(cbar_g*e[i,:])+ dlncge * dt) / cbar_g
            #de= e[i,:]*(-dc_gp*r_g/cbar_g-cbar_g * G_n + omega_p * (Iw-D))
            #e[i + 1, :] = e[i,:]+de*dt
            #print('dt:',dt)
            #print('energy:',e[i,:])
            #print('G_n:',G_n)
            #print('x_wt:', x[i,:])
            #print('y_wt:', y[i, :])
            #print('Deltaphi_p:', Deltaphi_p)
            #print('Deltan:', Deltan)
            #print('Deltaphi_w:',Deltaphi_w)
            #print(u_int[0], c_p[0], c_gp[i, 0], alpha[0], omega_p[0], k_p[0],H_p[0])

            #plt.plot(y[i,0], omega_p[0] * Iw[0],'r.')
            #plt.plot(y[i,0], omega_p[0] * D[0], 'g.')
            #plt.plot(y[i, 0], omega_p[0]*(Iw[0]-D[0]),'b.')

            # spectral peak direction derivative
            dphi_p=-C_phi * alpha ** 2 * omega_p * H_p * np.sin(2 * (phi_p[i,:]-phi_w) ) * WI
            phi_p[i+1,:]=phi_p[i,:]+dphi_p*dt

            # wave train position derivatives
            dx = np.sin(phi_p[i,:]) * cbar_g - v_eye*np.sin(np.deg2rad(dir_eye))
            dy = np.cos(phi_p[i,:]) * cbar_g - v_eye*np.cos(np.deg2rad(dir_eye))
            x[i+1,:]=x[i,:]+dx*dt
            y[i+1,:]=y[i,:]+dy*dt

            # update Deltan
            dDeltan=Deltaphi_p*cbar_g
            Deltan=Deltan+dDeltan*dt

            # spectral peak direction gradient
            Tinv = 2 * C_phi * H_p * alpha ** 2 * omega_p * np.cos(2 * (phi_p[i,:] - phi_w)) * WI
            dDeltaphi_p=-Tinv*((Deltaphi_p-Deltaphi_w))
            Deltaphi_p=Deltaphi_p+dDeltaphi_p*dt

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

        return x, y, c_gp, e, np.rad2deg(phi_p)

    # generate wave rays (in TC) in the TC frame with constant TC direction
    def wave_field_constant(self,t,x_0,y_0,vx_eye,vy_eye,u_m,f,R_m,eye_loc,phi_in,B):
        # t [seconds]: time vector
        # x_0, y_0 [meters]: initial position of wave train (vector)
        # vx_eye [meters/second]: (vector)
        # vy_eye [meters/second]: (vector)
        # u_m [m/s], R_M [m] phi_in[deg], f: Coriolis parameter and TC properties
        # eye_loc [meters]: location of the eye

        # get some initial wind field
        r = np.sqrt((x_0 - eye_loc[1]) ** 2 + (y_0 - eye_loc[0]) ** 2)
        v = ((u_m ** 2 + u_m*r*f)*(R_m/r) ** B*np.exp(-(R_m/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2
        vdir = -np.rad2deg(np.arctan2(y_0 - eye_loc[0], x_0 - eye_loc[1])) - phi_in
        vx_temp = np.sin(np.deg2rad(vdir))*v+vx_eye[0]
        vy_temp = np.cos(np.deg2rad(vdir))*v+vy_eye[0]
        u_int = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
        phi_w = np.arctan2(vx_temp, vy_temp)

        # some constants
        #b=0.06 # From 'Duncan' in Phillips (1985)
        q = -1 / 4 # (-0.33 - -0.23) Kudryavstev et al. (2015)
        p = 3 / 4 # (0.7 - 1.1) Kudryavstev et al. (2015)
        ph= 10 # p for the Heaviside function
        c_e = 1.2E-6 # (0.7E-7 - 18.9E-7) Badulin et al. (2007)
        c_alpha = 12 # (10.4 - 22.7) Badulin et al. (2007)
        C_e=2.46E-4 # Chapron et al. (2020)
        C_alpha=-1.4 # Chapron et al. (2020)
        #c_beta=4E-2 # Chapron et al. (2020)
        cg_ratio = 4.6E-2  # this is Delta c_g / c_g from the JONSWAP spectrum
        C_phi = 1.8E-5  # constant from the JONSWAP spectrum
        g = 9.81
        eps_t = np.sqrt(0.135) # threshold steepness (squared)
        r_g = 0.9
        n = 2 * q / (p + 4 * q)

        # set the initial conditions
        x = np.zeros((len(t),len(x_0)))
        y = np.zeros((len(t),len(x_0)))
        phi_p = np.zeros((len(t),len(x_0)))
        c_gp = np.zeros((len(t),len(x_0)))
        e = np.zeros((len(t),len(x_0)))
        Deltan_0=100.0
        Deltan=Deltan_0*np.ones(len(x_0))
        Deltaphi_p=np.zeros(len(x_0))
        Deltaphi_w = np.zeros(len(x_0))
        phi_p[0,:]= phi_w
        omega_0= 3
        c_gp[0,:]= g / omega_0 / 2
        c_p = c_gp[0,:] * 2
        alpha = u_int / c_p
        e[0,:]=u_int**4/g**2*c_e*(alpha/c_alpha)**(p/q)
        x[0,:]=x_0
        y[0,:]=y_0
        WI=np.ones(len(x_0)) # turns wind influence on and off

        # update equations
        for i in range(0,len(t)-1):
            dt=t[i+1]-t[i]

            # interpolate wind field
            phi_cross=phi_p[i,:]+np.pi/2
            x_cr =  Deltan * np.sin(phi_cross)
            y_cr = Deltan * np.cos(phi_cross)
            for j in range(0, len(x_0)):
                r = np.sqrt((x[i, j] - eye_loc[1]) ** 2 + (y[i, j] - eye_loc[0]) ** 2)
                v = ((u_m ** 2 + u_m*r*f)*(R_m/r) ** B*np.exp(-(R_m/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2
                vdir = -np.rad2deg(np.arctan2(y[i, j] - eye_loc[0], x[i, j] - eye_loc[1])) - phi_in
                vx_temp = np.sin(np.deg2rad(vdir))*v + vx_eye[i]
                vy_temp = np.cos(np.deg2rad(vdir))*v + vy_eye[i]
                u_int[j] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
                phi_w[j] = np.arctan2(vx_temp, vy_temp) # watch out, this might be another reference than 'vdir'

                r = np.sqrt((x[i, j] + x_cr[j] - eye_loc[1]) ** 2 + (y[i, j] + y_cr[j] - eye_loc[0]) ** 2)
                v = ((u_m ** 2 + u_m*r*f)*(R_m/r) ** B*np.exp(-(R_m/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2
                vdir = -np.rad2deg(np.arctan2(y[i, j] + y_cr[j] - eye_loc[0], x[i, j] + x_cr[j] - eye_loc[1])) - phi_in
                vx_temp = np.sin(np.deg2rad(vdir))*v + vx_eye[i]
                vy_temp = np.cos(np.deg2rad(vdir))*v + vy_eye[i]
                Deltaphi_w[j] = np.arctan2(vx_temp, vy_temp) - phi_w[j]

            # some equations for wave age, wavelength, etc.
            c_p = c_gp[i, :] * 2
            alpha = u_int / c_p
            cbar_g = r_g * c_gp[i,:]
            omega_p = g / c_p
            k_p = omega_p / c_p

            # wind input is switched off
            WI[alpha*np.cos(phi_p[i,:]-phi_w) < 1]=0

            # group velocity derivative
            Delta_p = 1 - 2/np.cosh(10*(alpha - 0.9)) ** 2
            dc_gp=-r_g*C_alpha/2*Delta_p*g*(k_p**2*e[i,:])**2 # c_gp in the presentation
            c_gp[i+1,:]=c_gp[i,:]+ dc_gp*dt

            # modified energy derivative
            H_p = 1/2 * (1 + np.tanh( ph * ( np.cos(phi_p[i, :] - phi_w)*alpha - 1) ) )
            G_n=Deltaphi_p/Deltan_0 * (Deltan/Deltan_0 / ((Deltan/Deltan_0)**2 +(0.5*np.sqrt(cg_ratio))**2)) * WI
            Iw = C_e * H_p * alpha ** 2 * np.cos(phi_p[i, :] - phi_w) ** 2 * WI
            D = (e[i, :]*k_p ** 2/eps_t ** 2) ** n
            dlncge = -cbar_g * G_n + omega_p * (Iw-D)
            e[i + 1,:]=np.exp(np.log(cbar_g*e[i,:])+ dlncge * dt) / cbar_g

            # spectral peak direction derivative
            dphi_p=-C_phi * alpha ** 2 * omega_p * H_p * np.sin(2 * (phi_p[i,:]-phi_w) ) * WI
            phi_p[i+1,:]=phi_p[i,:]+dphi_p*dt

            # wave train position derivatives (in the eye coordinate system)
            dx = np.sin(phi_p[i,:]) * cbar_g - vx_eye[i]
            dy = np.cos(phi_p[i,:]) * cbar_g - vy_eye[i]
            x[i+1,:]=x[i,:]+dx*dt
            y[i+1,:]=y[i,:]+dy*dt

            # update Deltan
            dDeltan=Deltaphi_p*cbar_g
            Deltan=Deltan+dDeltan*dt

            # spectral peak direction gradient
            Tinv = 2 * C_phi * H_p * alpha ** 2 * omega_p * np.cos(2 * (phi_p[i,:] - phi_w)) * WI
            dDeltaphi_p=-Tinv*((Deltaphi_p-Deltaphi_w))
            Deltaphi_p=Deltaphi_p+dDeltaphi_p*dt

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

        return x, y, c_gp, e, np.rad2deg(phi_p)

# generate wave rays (in TC) in an 'satellite' frame with a varying TC direction
    def wave_field_varying(self,t,x_0,y_0,vx_eye,vy_eye,u_m,f,R_m,eye_loc,phi_in,B,t_app=0):
        # t [seconds]: time vector
        # x_0, y_0 [meters]: initial position of wave train
        # vx_eye [meters/second]: (vector)
        # vy_eye [meters/second]: (vector)
        # u_m [m/s], R_M [m] phi_in[deg], f: Coriolis parameter and TC properties (vectors in this one)
        # eye_loc [meters]: locations of the eye at t=0
        # x_u, y_u [meters]: grid

        # get some initial wind field
        u_int = np.zeros((len(t),len(x_0))) # wind speed
        phi_w = np.zeros((len(t),len(x_0))) # wind direction
        r = np.sqrt((x_0 - eye_loc[1]) ** 2 + (y_0 - eye_loc[0]) ** 2)
        v = ((u_m[0] ** 2 + u_m[0]*r*f)*(R_m[0]/r) ** B*np.exp(-(R_m[0]/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2
        vdir = -np.rad2deg(np.arctan2(y_0 - eye_loc[0], x_0 - eye_loc[1])) - phi_in[0]
        vx_temp = np.sin(np.deg2rad(vdir))*v+vx_eye[0]
        vy_temp = np.cos(np.deg2rad(vdir))*v+vy_eye[0]
        u_int[0,:] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
        phi_w[0,:] = np.arctan2(vx_temp, vy_temp)

        # some constants
        #b=0.06 # From 'Duncan' in Phillips (1985)
        q = -1 / 4 # (-0.33 - -0.23) Kudryavstev et al. (2015)
        p = 3 / 4 # (0.7 - 1.1) Kudryavstev et al. (2015)
        ph= 10 # p for the Heaviside function
        c_e = 1.2E-6 # (0.7E-7 - 18.9E-7) Badulin et al. (2007)
        c_alpha = 12 # (10.4 - 22.7) Badulin et al. (2007)
        C_e=2.46E-4 # Chapron et al. (2020)
        C_alpha=-1.4 # Chapron et al. (2020)
        #c_beta=4E-2 # Chapron et al. (2020)
        cg_ratio = 4.6E-2  # this is Delta c_g / c_g from the JONSWAP spectrum
        C_phi = 1.8E-5  # constant from the JONSWAP spectrum
        g = 9.81
        eps_t = np.sqrt(0.135) # threshold steepness (squared)
        r_g = 0.9
        n = 2 * q / (p + 4 * q)

        # set the initial conditions
        x = np.zeros((len(t),len(x_0)))
        y = np.zeros((len(t),len(x_0)))
        ex = np.zeros((len(t))) # eye locations
        ey = np.zeros((len(t)))
        ex[0]=eye_loc[1]
        ey[0]=eye_loc[0]
        print(ex[0],ey[0])
        phi_p = np.zeros((len(t),len(x_0)))
        c_gp = np.zeros((len(t),len(x_0)))
        e = np.zeros((len(t),len(x_0)))
        Deltan_0=100.0
        Deltan=Deltan_0*np.ones(len(x_0))
        Deltaphi_p=np.zeros(len(x_0))
        Deltaphi_w = np.zeros(len(x_0))
        phi_p[0,:]= phi_w[0,:]
        omega_0=3
        c_gp[0,:]= g / omega_0 / 2
        c_p = c_gp[0,:] * 2
        alpha = u_int[0,:] / c_p
        e[0,:]=u_int[0,:]**4/g**2*c_e*(alpha/c_alpha)**(p/q)
        x[0,:]=x_0
        y[0,:]=y_0
        WI=np.ones(len(x_0)) # turns wind influence on and off

        # update equations
        for i in range(0,len(t)-1):
            dt=t[i+1]-t[i]

            # append a set of wave trains each t_app
            if t_app != 0 and np.floor(t[i+1]/t_app) > np.floor(t[i]/t_app):
                phi_p = np.column_stack((phi_p,np.zeros((len(t), len(x_0)))))
                c_gp = np.column_stack((c_gp,np.zeros((len(t), len(x_0)))))
                e = np.column_stack((e,np.zeros((len(t), len(x_0)))))
                x = np.column_stack((x,np.zeros((len(t), len(x_0)))))
                y = np.column_stack((y,np.zeros((len(t), len(x_0)))))
                c_gp[i, -len(x_0):]=c_gp[100, 0:len(x_0)]
                phi_p[i, -len(x_0):] = phi_p[100, 0:len(x_0)] # probably close enough (check with rigorously varying wind field)
                e[i, -len(x_0):] = e[100, 0:len(x_0)] # probably close enough
                x[i, -len(x_0):] = x[100, 0:len(x_0)] - eye_loc[1] + ex[i]
                y[i, -len(x_0):] = y[100, 0:len(x_0)] - eye_loc[0] + ey[i]
                Deltan=np.append(Deltan,Deltan_0*np.ones(len(x_0)))
                u_int = np.column_stack((u_int,np.zeros((len(t), len(x_0)))))
                phi_w = np.column_stack((phi_w, np.zeros((len(t), len(x_0)))))
                Deltaphi_w=np.append(Deltaphi_w,np.zeros(len(x_0)))
                WI=np.append(WI,np.ones(len(x_0)))
                Deltaphi_p=np.append(Deltaphi_p,np.zeros(len(x_0)))

            # interpolate wind field
            phi_cross=phi_p[i,:]+np.pi/2
            x_cr =  Deltan * np.sin(phi_cross)
            y_cr = Deltan * np.cos(phi_cross)
            for j in range(0, len(Deltan)):
                r = np.sqrt((x[i, j] - ex[i]) ** 2 + (y[i, j] - ey[i]) ** 2)
                v = ((u_m[i] ** 2 + u_m[i]*r*f)*(R_m[i]/r) ** B*np.exp(-(R_m[i]/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2
                vdir = -np.rad2deg(np.arctan2(y[i, j] - ey[i], x[i, j] - ex[i])) - phi_in[i]
                vx_temp = np.sin(np.deg2rad(vdir))*v + vx_eye[i]
                vy_temp = np.cos(np.deg2rad(vdir))*v + vy_eye[i]
                u_int[i,j] = np.sqrt(vx_temp ** 2 + vy_temp ** 2)
                phi_w[i,j] = np.arctan2(vx_temp, vy_temp)

                r = np.sqrt((x[i, j] + x_cr[j] - ex[i]) ** 2 + (y[i, j] + y_cr[j] - ey[i]) ** 2)
                v = ((u_m[i] ** 2 + u_m[i]*r*f)*(R_m[i]/r) ** B*np.exp(-(R_m[i]/r) ** B + 1) + (r*f/2) ** 2) ** 0.5 - r*f/2
                vdir2 = -np.rad2deg(np.arctan2(y[i, j] + y_cr[j] - ey[i], x[i, j] + x_cr[j] - ex[i])) - phi_in[i]
                vx_temp2 = np.sin(np.deg2rad(vdir2))*v + vx_eye[i]
                vy_temp2 = np.cos(np.deg2rad(vdir2))*v + vy_eye[i]
                Deltaphi_w[j] = np.arctan2(vx_temp2, vy_temp2) - phi_w[i,j]

            # some equations for wave age, wavelength, etc.
            c_p = c_gp[i, :] * 2
            alpha = u_int[i,:] / c_p
            cbar_g = r_g * c_gp[i,:]
            omega_p = g / c_p
            k_p = omega_p / c_p

            # wind input is switched off
            #print(alpha[2]*np.cos(phi_p[i,2]-phi_w[2]),alpha[2],phi_p[i,2],phi_w[2])
            WI[np.logical_and(alpha*np.cos(phi_p[i,:]-phi_w[i,:]) < 1,phi_w[i,:] > 5)]=0

            # group velocity derivative
            Delta_p = 1 - 2/np.cosh(10*(alpha - 0.9)) ** 2
            dc_gp=-r_g*C_alpha/2*Delta_p*g*(k_p**2*e[i,:])**2 # c_gp in the presentation
            c_gp[i+1,:]=c_gp[i,:]+ dc_gp*dt

            # modified energy derivative
            H_p = 1/2 * (1 + np.tanh( ph * ( np.cos(phi_p[i, :] - phi_w[i,:])*alpha - 1) ) )
            G_n=Deltaphi_p/Deltan_0 * (Deltan/Deltan_0 / ((Deltan/Deltan_0)**2 +(0.5*np.sqrt(cg_ratio))**2)) * WI
            Iw = C_e * H_p * alpha ** 2 * np.cos(phi_p[i, :] - phi_w[i,:]) ** 2 * WI
            D = (e[i, :]*k_p ** 2/eps_t ** 2) ** n
            dlncge = -cbar_g * G_n + omega_p * (Iw-D)
            e[i + 1,:]=np.exp(np.log(cbar_g*e[i,:])+ dlncge * dt) / cbar_g

            # spectral peak direction derivative
            dphi_p=-C_phi * alpha ** 2 * omega_p * H_p * np.sin(2 * (phi_p[i,:]-phi_w[i,:]) ) * WI
            phi_p[i+1,:]=phi_p[i,:]+dphi_p*dt

            # wave train position derivatives (in the eye coordinate system)
            dx = np.sin(phi_p[i,:]) * cbar_g
            dy = np.cos(phi_p[i,:]) * cbar_g
            x[i+1,:]=x[i,:]+dx*dt
            y[i+1,:]=y[i,:]+dy*dt

            # eye location
            ex[i+1]=ex[i] + vx_eye[i]*dt
            ey[i+1]=ey[i] + vy_eye[i]*dt

            # update Deltan
            dDeltan=Deltaphi_p*cbar_g
            Deltan=Deltan+dDeltan*dt

            # spectral peak direction gradient
            Tinv = 2 * C_phi * H_p * alpha ** 2 * omega_p * np.cos(2 * (phi_p[i,:] - phi_w[i,:])) * WI
            dDeltaphi_p=-Tinv*((Deltaphi_p-Deltaphi_w))
            Deltaphi_p=Deltaphi_p+dDeltaphi_p*dt

        return x, y, c_gp, e, np.rad2deg(phi_p), ex, ey, u_int, np.rad2deg(phi_w)

if __name__ == '__main__':
    import os
    import numpy as np
    from matplotlib import pyplot as plt

    # Note that I just use the 'lon'-direction as the x-direction and 'lat'-direction as the y-direction,
    # so they are not radar coordinates
    #'''
    # Marcel's model
    shp = (100, 20)
    y_res = 2000  # meter
    x_res = 2000  # meter
    basin = 'Atlantic'
    hemisphere = 'Northern'

    #'''
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
    q = -1/4  # (-0.33 - -0.23) Kudryavstev et al. (2015)
    p = 3/4  # (0.7 - 1.1) Kudryavstev et al. (2015)
    x_tilde = np.sqrt((x_wt - x_0) ** 2 + (y_wt - y_0) ** 2)*g/ws ** 2   # dimensionless fetch
    e_tilde = c_e*x_tilde ** p  # dimensionless energy
    c_p=c_gp*2
    alpha=ws/c_p
    alpha_tilde = c_alpha*x_tilde ** q
    e_tilde2 = c_e*( alpha / c_alpha ) ** (p/q)

    plt.figure(figsize=(15, 5))
    plt.subplot(1,2,1)
    plt.plot(x_tilde, alpha , 'b',label='u/c_p')
    plt.plot(x_tilde, alpha_tilde, 'r',label='c_alpha*x_tilde^q')
    plt.xlabel('dimensionless fetch')
    plt.ylabel('dimensionless wave age/frequency')
    #plt.xlim(10 ** 3, 10 ** 5.5)
    #plt.ylim(0, 3)
    #plt.xscale('log')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x_tilde, e*g ** 2/ws ** 4, 'b', label='from integration')
    plt.plot(x_tilde, e_tilde, 'r', label='c_e * x_tilde^p')
    plt.plot(x_tilde, e_tilde2, 'g--', label='c_e * (alpha / c_alpha)^(p/q)')
    plt.xlabel('dimensionless fetch')
    plt.ylabel('dimensionless energy')
    #plt.xlim(10 ** 3, 10 ** 5.5)
    #plt.ylim(10**-4, 10**-1)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    #'''

