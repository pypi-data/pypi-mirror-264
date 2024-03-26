__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

import numpy as np
import glob
import pickle
from stereoid.oceans.forward_models import SAR_spectra as SAR_model
from stereoid.oceans import ObsGeoAngles
from stereoid.oceans.forward_models.wrappers import interp_weights as griddata_step1
import stereoid.oceans.inversion.wave_spectra_inversion as wav_inv
import stereoid.oceans.tools.spectrum_tools as spectrum_tools

# this method converts the inverted parameters (for example k_s*np.cos(phi) and k_s*np.sin(phi)) to swell-wave parameters
def inversion2swellparameters(yhat,var,incs,ref_inc,Hs=0,sigma_Hs=0):
    """

    Parameters
    ----------
    yhat
    var
    incs
    ref_inc
    Hs
    sigma_Hs

    Returns
    -------
    k_s, phi_s, Hs_s, sigma_f, sigma_phi: swell-wave parameters

    """


    # the assumption is now that yhat looks like this:
    # y = [k_s * np.cos(phi_s), k_s * np.sin(phi_s), k_s * 1.0, np.cos(phi_s), np.sin(phi_s), sigma_f ** 2,
    #      sigma_phi ** 2, Hs_s ** 2]

    # get the closest incidence angle for which the model exists
    I3 = np.argmin(np.absolute(incs - ref_inc))

    ### wave number ###
    k1=np.sqrt(yhat[0]**2 + yhat[1]**2)
    var1=(yhat[0]/k1)**2*var[0][I3]+(yhat[1]/k1)**2*var[1][I3] # propagation of uncertainty
    k2=yhat[2]*1.0
    var2=var[2][I3]*1.0
    k_s=(k1*var1+k2*var2)/(var1+var2)

    ### wave direction ###
    phi1=np.arctan2(yhat[1],yhat[0])
    x=yhat[1]/yhat[0]
    varx=(x/yhat[1])**2*var[1][I3] + (x/yhat[0])**2*var[0][I3] # propagation of uncertainty
    var1=varx/(1+x**2) # propagation of uncertainty
    phi2=np.arctan2(yhat[4],yhat[3])
    x = yhat[4] / yhat[3]
    varx = (x / yhat[4]) ** 2 * var[4][I3] + (x / yhat[3]) ** 2 * var[3][I3]
    var2 = varx / (1 + x ** 2)
    phi_s=np.zeros(len(phi1))
    I = np.absolute(phi1-phi2) < np.pi
    phi_s[I]=(phi1[I]*var1[I]+phi2[I]*var2[I])/(var1[I]+var2[I])#phi2[I]*1.0
    I = phi1-phi2 < -np.pi
    phi_s[I] = (phi1[I] * var1[I] + (phi2[I]-2*np.pi) * var2[I]) / (var1[I] + var2[I])#phi2[I]*1.0
    I = phi2 - phi1 < -np.pi
    phi_s[I] = (phi1[I] * var1[I] + (phi2[I]+ 2*np.pi) * var2[I]) / (var1[I] + var2[I])#phi2[I]*1.0
    phi_s=np.mod(phi_s,2*np.pi)

    ### wave height ###
    if Hs == 0:
        Hs=np.sqrt(yhat[7][:])

    ### spectral width (frequency) ###
    sigma_f=np.sqrt(yhat[5][:])

    ### spectral width (angular) ###
    sigma_phi=np.sqrt(yhat[6][:])

    return k_s, phi_s, Hs, sigma_f, sigma_phi


# this method estimates the spectral parameters from a set of SAR spectra with the same incident angle
def spectral_inversion(specfolder, modelfolder, obs_geo, ref_inc, kx, ky, Np, Nm, pols=[0,4,5],spec_type='test', cr_spec_batch=0,
                       inc_ind=0,phi_w=0,fetch=0,u10=0,n=25,kx_ku=0,ky_ku=0):
    '''

    Parameters
    ----------
    infolder: folder with spectra (only if spec_type == 'test', otherwise st a dummy)
    modelfolder: folder with input parameters for the model
    obs_geo: observation geometry (ObsGeoTrio type)
    ref_inc: incident angle of the spectra to be analyzed
    kx: spectra wave numbers
    ky: spectra wave numbers
    Np: numbers of spectra per location (three satellites x two polarizations = six)
    Nm: maximum order of moment arms
    pols: indices of polarizations to be used
    spec_type: 'test','swb': format that is being used
    if spec_tyep=='swb':
        cr_spec_batch: provide a set of spectra for the scene
        inc_ind: index to select the spectra with index 'inc_ind' belonging to ref_inc
        phi_w: wind directions at spectra locations
        fetch: estimated fetch at spectra locations
        u10: estimated u10 at spectra locations
        n: number of independent spectra averaged
        kx_ku: logaritmic spectrum wave numbers (to compute the backscatter/RAR)
        ky_ku: logaritmic spectrum wave numbers (to compute the backscatter/RAR)

    Returns
    -------

    '''

    # model data
    inc_file = modelfolder + 'incident_angles.pickle'
    I_file = modelfolder + 'parameter_indices.pickle'
    I2_file = modelfolder + 'parameter_indices_cutoff.pickle'
    xhat_file = modelfolder + 'parameters.pickle'
    with open(inc_file, 'rb') as handle:
        incs = pickle.load(handle)
    with open(I_file, 'rb') as handle:
        I = pickle.load(handle)
    with open(I2_file, 'rb') as handle:
        I2 = pickle.load(handle)
    with open(xhat_file, 'rb') as handle:
        xhat = pickle.load(handle)

    # number of spectra
    if spec_type == 'test':
        Ns = len(glob.glob1(specfolder, "crspec_wind*"))

    if spec_type == 'swb':
        shp=cr_spec_batch['S1']['V'].shape
        Ns = shp[0]

    # observation geometries
    vtx_h, wts_h, vtx_t, wts_t, HA_angles, HB_angles, S1_angles = obs_geo_aux(obs_geo, ref_inc, kx, ky)

    # spectral moments
    moments = ["K", "Kx", "Ky", "K_rel", "phi_rel", "var", "M", "Mx", "My"]
    spectral_moments = {"K": np.zeros((Np, Nm, Ns)), "Kx": np.zeros((Np, Nm, Ns)), "Ky": np.zeros((Np, Nm, Ns)),
                        "K_rel": np.zeros((Np, Nm, Ns)), "phi_rel": np.zeros((Np, Nm, Ns)), "var": np.zeros((Np, Ns)),
                        "M": np.zeros((Np, Nm, Ns)), "Mx": np.zeros((Np, Nm, Ns)), "My": np.zeros((Np, Nm, Ns))}
    cut_off = np.zeros((Np, Ns))

    for i in range(0, Ns):
        if np.mod(i, 50) == 0:
            print(int(i / Ns * 100))

        if spec_type == 'test':
            # read in data
            cr_spec, cr_spec_wind = read_spectra(specfolder, i)

        if spec_type == 'swb':
            # select the correct cr_spec
            polbase = ['m', 'M']
            cr_spec = {"S1": {}, "HA": {}, "HB": {}}
            for key in cr_spec.keys():
                if key == "S1":
                    # Here for now I chose to use H/V for S1, but we could also just stay with I (=H) and O (=V)
                    cr_spec[key] = {"H": cr_spec_batch["S1"]["H"][i,inc_ind,:,:],
                                    "V": cr_spec_batch["S1"]["H"][i,inc_ind,:,:]}
                else:
                    cr_spec[key] = {polbase[0]: cr_spec_batch[key][polbase[0]][i,inc_ind,:,:],
                                    polbase[1]: cr_spec_batch[key][polbase[1]][i,inc_ind,:,:]}

            # we have to compute a wind correction
            _, cr_spec_wind = wav_inv.wind_wave_correction(obs_geo, ref_inc, kx, ky, kx_ku, ky_ku, u10[i],
                                                                      phi_w[i], fetch[i], n, cross=True,
                                                                      noise=False, ord=4)

        # estimate cutoffs
        # FIXME: cutoff already computed for swb, so redundant
        cut_off[:, i] = compute_cutoffs(cr_spec, kx, ky, S1_angles, HA_angles, HB_angles, vtx_h, wts_h, vtx_t, wts_t)

        # compute spectral moments
        spec_mom_temp = spectral_preprocessing(cr_spec, cr_spec_wind, kx, ky, Nm)

        # store spectral moments
        for j in range(0, len(moments)):
            if moments[j] == 'var':
                spectral_moments[moments[j]][:, i] = spec_mom_temp[moments[j]][:]
            else:
                spectral_moments[moments[j]][:, :, i] = spec_mom_temp[moments[j]][:, :]

    # dummy variable y
    y = [np.ones(Ns), np.ones(Ns), np.ones(Ns), np.ones(Ns), np.ones(Ns), np.ones(Ns), np.ones(Ns), np.ones(Ns)]

    # apply model
    yhat, ehat, varN, dof = estimate_wave_parameters(y, moments, spectral_moments, cut_off, I, I2, xhat,
                                             incs, ref_inc, pols=pols, Nm=Nm)

    return yhat


# this method generates the full model with incidence angle dependence for the wave-spectra inversion
def wave_spectra_model(spec_folder, ref_inc, incs, obs_geo, Nm=3, Np=6, scene_size=5000, dx=5, dy=16,
                       ref_inc_only=True, pols = [0, 4, 5], NoM=8, NoM_co=4, Na = 200):

    """

    Parameters
    ----------
    spec_folder
    ref_inc
    incs
    obs_geo
    Nm
    Np
    scene_size
    dx
    dy
    ref_inc_only: boolean, if it is true, we will compute the model only for one incident angle
    pols: indexes of channels (sats, polarization) to be used
    NoM: number of moments in the model
    NoM: number of moments weighted by the cutoff in the model
    Na: number of attemps to find the best model

    Returns
    -------
    xhat_inc: list of model parameters for each model incident for all incident angles
    var_inc: list of variances of residuals for each model incident for all incident angles
    """

    # get reference incident angle files
    infolder = spec_folder + str(int(np.degrees(ref_inc))) + '/'
    Ns = len(glob.glob1(infolder, "crspec_wind*"))

    # create a spectral grid
    spec_grid = spectrum_tools.wave_number_grids_sar(scene_size, dx=dx, dy=dy)
    kx=spec_grid['k_x']
    ky=spec_grid['k_y']

    # observation geometries and auxiliary information
    vtx_h, wts_h, vtx_t, wts_t, HA_angles, HB_angles, S1_angles = obs_geo_aux(obs_geo, ref_inc, kx, ky)

    # wave parameter vectors
    g = 9.81
    phi_w = np.zeros(Ns)
    u10 = np.zeros(Ns)
    IWA = np.zeros(Ns)
    Hs_s = np.zeros(Ns)
    phi_s = np.zeros(Ns)
    k_s = np.zeros(Ns)
    sigma_phi = np.zeros(Ns)
    sigma_f = np.zeros(Ns)

    # spectral parameters and cut_offs
    moments = ["K", "Kx", "Ky", "K_rel", "phi_rel", "var", "M", "Mx", "My"]
    spectral_moments = {"K": np.zeros((Np, Nm, Ns)), "Kx": np.zeros((Np, Nm, Ns)), "Ky": np.zeros((Np, Nm, Ns)),
                        "K_rel": np.zeros((Np, Nm, Ns)), "phi_rel": np.zeros((Np, Nm, Ns)),
                        "var": np.zeros((Np, Ns)),
                        "M": np.zeros((Np, Nm, Ns)), "Mx": np.zeros((Np, Nm, Ns)), "My": np.zeros((Np, Nm, Ns))}
    cut_off = np.zeros((Np, Ns))

    ########### step 1: generate the model for a reference incident angle ###########
    for i in range(0, Ns):
        # k = k + 1
        if np.mod(i, 50) == 0:
            print(int(i / Ns * 100))

        # read in data
        cr_spec, cr_spec_wind = read_spectra(infolder, i)
        phi_w[i], u10[i], IWA[i], Hs_s[i], phi_s[i], k_s[i], sigma_phi[i], sigma_f[i] = read_wavespectrum_params(
            infolder, i)

        # estimate cutoffs
        cut_off[:, i] = compute_cutoffs(cr_spec, kx, ky, S1_angles, HA_angles, HB_angles, vtx_h, wts_h,
                                        vtx_t, wts_t)

        # compute spectral moments
        #print(i)
        spec_mom_temp = spectral_preprocessing(cr_spec, cr_spec_wind, kx, ky, Nm)

        # store spectral moments
        for j in range(0, len(moments)):
            if moments[j] == 'var':
                spectral_moments[moments[j]][:, i] = spec_mom_temp[moments[j]][:]
            else:
                spectral_moments[moments[j]][:, :, i] = spec_mom_temp[moments[j]][:, :]

    # FIXME: this stuff is now hardcoded, but should be changed
    y = [k_s * np.cos(phi_s), k_s * np.sin(phi_s), k_s * 1.0, np.cos(phi_s), np.sin(phi_s), sigma_f ** 2,
         sigma_phi ** 2, Hs_s ** 2]

    # get the model for the reference spectra
    xhat, yhat, ehat, varN, dof, I, I2, Ival = get_model(y, spectral_moments, cut_off, pols=pols, Nm=Nm,
                                                   NoM=NoM, NoM_co=NoM_co, Na=Na)

    # save the model and the normalized variance to a list
    xhat_inc = np.empty(shape=len(y)).tolist()
    var_inc = np.empty(shape=len(y)).tolist()
    #y_inc = np.empty(shape=len(y)).tolist()
    #yhat_inc = np.empty(shape=len(y)).tolist()
    for i in range(0, len(xhat)):
        xhat_inc[i] = xhat[i][0]
        var_inc[i] = varN[i] / dof[i]
        #y_inc[i] = y[i]
        #yhat_inc[i] = yhat[i]

    ########### step 2: expand the model for other incident angles ###########
    # FIXME: this second part, not rigorously checked
    # """
    if ref_inc_only == False:
        for l in range(0, len(incs)):

            # observation geometries and auxiliary information
            vtx_h, wts_h, vtx_t, wts_t, HA_angles, HB_angles, S1_angles = obs_geo_aux(obs_geo, incs[l], kx, ky)

            # folder with spectra at incidence angle incs[l]
            infolder = spec_folder + str(int(np.degrees(incs[l]))) + '/' + '/'
            Ns = len(glob.glob1(infolder, "crspec_wind*"))
            for i in range(0, Ns):
                # k = k + 1
                if np.mod(i, 50) == 0:
                    print(int(i / Ns * 100))

                # read in data
                cr_spec, cr_spec_wind = read_spectra(infolder, i)
                phi_w[i], u10[i], IWA[i], Hs_s[i], phi_s[i], k_s[i], sigma_phi[i], sigma_f[
                    i] = read_wavespectrum_params(infolder, i)

                # estimate cutoffs
                cut_off[:, i] = compute_cutoffs(cr_spec, kx, ky, S1_angles, HA_angles, HB_angles, vtx_h, wts_h,
                                                vtx_t, wts_t)

                # compute spectral moments
                spec_mom_temp = spectral_preprocessing(cr_spec, cr_spec_wind, kx, ky, Nm)

                # store spectral moments
                for j in range(0, len(moments)):
                    if moments[j] == 'var':
                        spectral_moments[moments[j]][:, i] = spec_mom_temp[moments[j]][:]
                    else:
                        spectral_moments[moments[j]][:, :, i] = spec_mom_temp[moments[j]][:, :]

            # get the model for the reference spectra
            y = [k_s * np.cos(phi_s), k_s * np.sin(phi_s), k_s * 1.0, np.cos(phi_s), np.sin(phi_s), sigma_f ** 2,
                 sigma_phi ** 2, Hs_s ** 2]
            xhat, yhat, ehat, varN, dof, Ival = get_model_parameters(y, moments, spectral_moments, cut_off, I, I2, pols=pols,
                                                               Nm=Nm)

            # save the model and the normalized variance to a list
            for i in range(0, len(xhat)):
                xhat_inc[i] = np.column_stack((xhat_inc[i], xhat[i][0]))
                var_inc[i] = np.append(var_inc[i], varN[i] / dof[i])
                #y_inc[i] = np.column_stack((y_inc[i], y[i]))
                #yhat_inc[i] = np.column_stack((yhat_inc[i], yhat[i]))

    # """

    return xhat_inc, var_inc, I, I2


def read_spectra(infolder, i):
    """

    Parameters
    ----------
    infolder: assumes that the spectra and the 'wind-correction' spectrum are in the same folder
    i: file number

    Returns
    -------

    """
    # read in data
    fn = infolder + 'crspec_' + f"{i + 1:03d}" + '.npy'
    file1 = open(fn, 'rb')
    cr_spec = pickle.load(file1)
    file1.close()
    fn = infolder + 'crspec_wind_' + f"{i + 1:03d}" + '.npy'
    file2 = open(fn, 'rb')
    cr_spec_wind = pickle.load(file2)
    file2.close()

    return cr_spec, cr_spec_wind


def read_wavespectrum_params(infolder, i):
    """

    Parameters
    ----------
    infolder
    i

    Returns
    -------
    phi_w,u10,IWA: wind-wave parameters
    Hs_s,phi_s,k_s,sigma_phi,sigma_f: swell parameters
    """
    fn = infolder + 'wavespec_' + f"{i + 1:03d}" + '.npy'
    with open(fn) as f:
        specprops = f.read().split(' ')

    # swell and wind-wave properties
    g = 9.81
    phi_w = float(specprops[0])
    u10 = float(specprops[1])
    IWA = float(specprops[2])
    Hs_s = float(specprops[3])
    phi_s = float(specprops[4])
    k_s = (float(specprops[5]) * 2 * np.pi) ** 2 / g
    sigma_phi = float(specprops[7])
    sigma_f = float(specprops[6])

    return phi_w, u10, IWA, Hs_s, phi_s, k_s, sigma_phi, sigma_f


# some auxiliary information w.r.t. observation geometry
def obs_geo_aux(obs_geo, inc_m, kx, ky):
    # observation geometries
    (obs_geo_concordia, obs_geo_discordia, obs_geo_sentinel1) = (
        obs_geo.concordia,
        obs_geo.discordia,
        obs_geo.sentinel1,
    )

    inc_b_c = obs_geo_concordia.swth_geo.inc2slave_inc(inc_m)
    bist_ang_c = obs_geo_concordia.swth_geo.inc2bistatic_angle_az(inc_m)
    alpha_rot_c = np.arctan2(np.sin(bist_ang_c) * np.sin(inc_b_c),
                             (np.sin(inc_m) + np.cos(bist_ang_c) * np.sin(inc_b_c)))

    inc_b_d = obs_geo_discordia.swth_geo.inc2slave_inc(inc_m)
    bist_ang_d = obs_geo_discordia.swth_geo.inc2bistatic_angle_az(inc_m)
    alpha_rot_d = np.arctan2(np.sin(bist_ang_d) * np.sin(inc_b_d),
                             (np.sin(inc_m) + np.cos(bist_ang_d) * np.sin(inc_b_d)))

    # we use the griddata interpolator to rotate the spectrum
    # in azimuth this is always the same, so we can use the same indices
    kx_h = kx * np.cos(alpha_rot_c) - ky * np.sin(alpha_rot_c)
    ky_h = ky * np.cos(alpha_rot_c) + kx * np.sin(alpha_rot_c)
    xy = np.column_stack((kx.flatten(), ky.flatten()))
    uv = np.column_stack((kx_h.flatten(), ky_h.flatten()))
    vtx_h, wts_h = griddata_step1(uv, xy)

    kx_t = kx * np.cos(alpha_rot_d) - ky * np.sin(alpha_rot_d)
    ky_t = ky * np.cos(alpha_rot_d) + kx * np.sin(alpha_rot_d)
    xy = np.column_stack((kx.flatten(), ky.flatten()))
    uv = np.column_stack((kx_t.flatten(), ky_t.flatten()))
    vtx_t, wts_t = griddata_step1(uv, xy)

    # some test
    HA_angles = ObsGeoAngles(inc_m, inc_b_c, bist_ang_c)
    HB_angles = ObsGeoAngles(inc_m, inc_b_d, bist_ang_d)
    S1_angles = ObsGeoAngles(inc_m, inc_m, 0)

    return vtx_h, wts_h, vtx_t, wts_t, HA_angles, HB_angles, S1_angles


# this method calls the pre-processing methods in wave_spectra_inversion in the right order to get spectral moments for the peaks
def spectral_preprocessing(cr_spec, cr_spec_wind, kx, ky, Nm, swell_lim=2 * np.pi / 150, filt_abs=[3, 5, 2, 2],
                           filt_comp=[3, 3, 3, 3]):
    """

    Parameters
    ----------
    cr_spec: cross-spectra
    cr_spec_wind: model wind correction (cross-)spectra
    kx: cross-track wave number
    ky: along-track wave number
    Nm: order of
    swell_lim: maximum swell wave number
    filt_abs: filtering setting for absolute cross-spectra (for peak detection) [sigma_x,sigma_y,nx,ny]
    filt_comp: filtering setting for complex cross-spectra (for peak detection) [sigma_x,sigma_y,nx,ny]

    Returns
    -------
    spectral_moments: dictionary of moments, variances and moment arms for the six spectra
    """

    # apply wind-wave correction
    spec_corr = wav_inv.apply_wind_wave_correction(cr_spec, cr_spec_wind)

    # crop the wave spectra
    spec_crop, kx_sh, ky_sh = wav_inv.crop_spec(spec_corr, kx, ky, kx_lim=swell_lim * 2, ky_lim=swell_lim * 2)

    # filter the spectra
    spec_filt = wav_inv.filter_Gauss(spec_crop, filt_abs[0], filt_abs[1], nx=filt_abs[2], ny=filt_abs[2])
    #from matplotlib import pyplot as plt
    #plt.imshow(spec_filt['S1']['V'])
    #plt.show()

    # crop cross-spectra, but keep complex values
    cr_spec_crop, kx_sh, ky_sh = wav_inv.crop_spec(cr_spec, kx, ky, kx_lim=swell_lim * 2, ky_lim=swell_lim * 2,
                                                   abso=0)

    # filter cross-spectra, but keep complex values
    cr_spec_filt = wav_inv.filter_Gauss(cr_spec_crop, filt_comp[0], filt_comp[1], nx=filt_comp[2], ny=filt_comp[3],
                                        abso=0)
    #from matplotlib import pyplot as plt
    #plt.imshow(np.imag(cr_spec_filt['S1']['V']))
    #plt.show()

    # find swell peaks
    spec_peaks, swell_flag = wav_inv.swell_peaks_rough(spec_filt, cr_spec_filt, kx_sh, ky_sh, 7)

    # mask spec
    spec_mask = wav_inv.spec_mask(spec_filt, spec_peaks, kx_sh, ky_sh, kmax=swell_lim)

    # compute spectral moments
    spectral_moments = wav_inv.compute_spectral_moments(spec_mask, spec_peaks, kx_sh, ky_sh, ord=Nm)

    return spectral_moments


# compute all six cut-offs
def compute_cutoffs(cr_spec, kx, ky, S1_angles, HA_angles, HB_angles, vtx_h, wts_h, vtx_t, wts_t):
    """

    Parameters
    ----------
    cr_spec
    kx
    ky
    S1_angles
    HA_angles
    HB_angles
    vtx_h
    wts_h
    vtx_t
    wts_t

    Returns
    -------
    cut_off: dictionary with six cut-offs
    """

    #sats = ["S1", "HA", "HB", "S1", "HA", "HB"]
    #pols = ["V", "m", "m", "H", "M", "M"]

    cut_off = np.zeros(6)
    spec_par = {"S": cr_spec['S1']['V'],"k_x": kx,"k_y": ky}
    cut_off[0], macs_temp = SAR_model.cutoff_and_macs(spec_par, S1_angles)
    spec_par = {"S": cr_spec['S1']['H'], "k_x": kx, "k_y": ky}
    cut_off[3], macs_temp = SAR_model.cutoff_and_macs(spec_par, S1_angles)
    spec_par = {"S": cr_spec['HA']['M'], "k_x": kx, "k_y": ky}
    cut_off[4], macs_temp = SAR_model.cutoff_and_macs(spec_par, HA_angles, vtx=vtx_h,wts=wts_h)
    spec_par = {"S": cr_spec['HA']['m'], "k_x": kx, "k_y": ky}
    cut_off[1], macs_temp = SAR_model.cutoff_and_macs(spec_par, HA_angles, vtx=vtx_h,wts=wts_h)
    spec_par = {"S": cr_spec['HB']['M'], "k_x": kx, "k_y": ky}
    cut_off[5], macs_temp = SAR_model.cutoff_and_macs(spec_par, HB_angles, vtx=vtx_t,wts=wts_t)
    spec_par = {"S": cr_spec['HB']['m'], "k_x": kx, "k_y": ky}
    cut_off[2], macs_temp = SAR_model.cutoff_and_macs(spec_par, HB_angles, vtx=vtx_t,wts=wts_t)

    return cut_off


# this method fits a model that connects spectral moments to swell parameters
# it used Na iterations to find the 'best' set of spectral moments to be used
# the idea is that we run this method for a set of spectra at one incident angle
# after that we estimate models using the same spectral moments for other incident angles
# this can be done with the function 'get_model_parameters'
# FIXME: NoM, Na and NoM_co should become vectors
def get_model(y, spectral_moments, cut_off, pols=[0, 4, 5], Nm=3, NoM=4, NoM_co=3, Na=50):
    """

    Parameters
    ----------
    y: swell parameters
    spectral_moments: dictionary of spectral moments
    cut_off: set of cut_offs
    pols: polarizations (sats,pols per sat) to be used (indices)
    Nm: maximum order of the moments
    NoM: number of unweighted moments
    NoM_co: number of moments weighted with the cut-off
    Na: attempts to fit a model

    Returns
    -------
    xhat
    yhat
    ehat
    varN: rms**2 of residuals * N
    dof
    I: indices of moments to be used
    I2: indices of moments weighted by the cut-off to be used
    Ival: used values after outlier removal
    """

    # create some lists for output
    I = np.empty(shape=len(y)).tolist()
    I2 = np.empty(shape=len(y)).tolist()
    Ival = np.empty(shape=len(y)).tolist()
    xhat = np.empty(shape=len(y)).tolist()
    yhat = np.empty(shape=len(y)).tolist()
    ehat = np.empty(shape=len(y)).tolist()
    dof = np.zeros(len(y), dtype=int)
    varN = np.zeros(len(y))

    for i in range(0, len(y)):
        xhat[i], yhat[i], ehat[i], varN[i], dof[i], I[i], I2[i], Ival[i] = wav_inv.find_best_fit(y[i],
                                                                                        spectral_moments,
                                                                                        cut_off,
                                                                                        pols=pols,
                                                                                        Nm=Nm,
                                                                                        NoM=NoM,
                                                                                        NoM_co=NoM_co,
                                                                                        Na=Na)

    return xhat, yhat, ehat, varN, dof, I, I2, Ival


# if the spectral moments to be used are already known ('get_model'), you can regress with this function
def get_model_parameters(y, moments, spectral_moments, cut_off, I, I2, pols=[0, 4, 5], Nm=3):
    """

    Parameters
    ----------
    y: these are the wave parameters, if they are known from other sources, otherwise just enter a dummy
    moments: list of moment names
    spectral_moments
    cut_off
    I
    I2
    xhat
    pols
    Nm

    Returns
    -------
    yhat: the estimated wave parameters
    ehat: residuals (only if 'y' is not a dummy)
    varN: rms**2 of residuals * N
    dof: degrees-of-freedom
    """

    Ns = len(y[0])
    yhat = np.empty(shape=len(y)).tolist()
    xhat = np.empty(shape=len(y)).tolist()
    ehat = np.empty(shape=len(y)).tolist()
    Ival = np.empty(shape=len(y)).tolist()
    dof = np.zeros(len(y), dtype=int)
    varN = np.zeros(len(y))
    for i in range(0, len(y)):
        A = wav_inv.construct_model(moments, spectral_moments, cut_off, pols, Nm, Ns, I[i], I2[i])

        # regression, which alsoe handles outliers
        Ival_temp = range(0, len(y[i]))
        emax = 10
        std_e = 3
        while emax > 3 * std_e:
            xhat[i], yhat[i], ehat[i], varN[i], dof[i] = wav_inv.estimate_model_parameters(y[i][Ival_temp], A[Ival_temp,:])
            emax = np.max(np.absolute(ehat[i]))
            std_e = np.sqrt(varN[i]/dof[i])
            if emax > 3 * std_e:
                Ival_temp = np.delete(Ival_temp, np.argmax(np.absolute(ehat[i])))

        Ival[i]=Ival_temp

    return xhat, yhat, ehat, varN, dof, Ival


# this is the forward application of the model to estmimate the wave parameters
def estimate_wave_parameters(y, moments, spectral_moments, cut_off, I, I2, xhat, incs, inc_m, pols=[0, 4, 5], Nm=3):
    """

    Parameters
    ----------
    y: these are the wave parameters, if they are known from other sources, otherwise just enter a dummy (with correct length)
    moments: list of moment names
    spectral_moments
    cut_off
    I
    I2
    xhat
    incs: incident angles for which we have parameters xhat
    inc_m: incident angle of observations (at which the spectral moments are computed)
    pols
    Nm

    Returns
    -------
    yhat: the estimated wave parameters
    ehat: residuals (only if 'y' is not a dummy)
    varN: rms**2 of residuals * N
    dof: degrees-of-freedom
    """

    # find the parameters xhat for incident angle nearest to inc_m
    I3 = np.argmin(np.absolute(incs - inc_m))

    Ns = len(y[0])
    yhat = np.empty(shape=len(y)).tolist()
    ehat = np.empty(shape=len(y)).tolist()
    dof = np.zeros(len(y), dtype=int)
    varN = np.zeros(len(y))
    for i in range(0, len(y)):
        A = wav_inv.construct_model(moments, spectral_moments, cut_off, pols, Nm, Ns, I[i], I2[i])
        yhat[i], ehat[i], varN[i], dof[i] = wav_inv.apply_model(A, xhat[i][:, I3], y[i])

    return yhat, ehat, varN, dof
