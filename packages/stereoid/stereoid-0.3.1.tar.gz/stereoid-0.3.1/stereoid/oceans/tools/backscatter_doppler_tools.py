import logging
from collections import namedtuple
from typing import Tuple, Optional

import numpy
import stereoid.oceans.waves.wave_spectra as swave_spectra
import stereoid.oceans.waves.spectral_conversions as spectral_conv
import stereoid.utils.tools as tools
import stereoid.oceans.forward_models.wrappers as wrappers
from stereoid.oceans import ObsGeoAngles, RadarModel
from stereoid.polarimetry import pol_rotations as polrot
import stereoid.oceans.tools.observation_tools as obs_tools
import stereoid.oceans.tools.spectrum_tools as spec_tools

# Define logger level for debug purposes
logger = logging.getLogger(__name__)
ObsGeoTrio = namedtuple("ObsGeoTrio", ["concordia", "discordia", "sentinel1"])


def rotation_companion(obs_geo, inc_tx: float, ws: dict
                       ) -> Tuple[float, numpy.ndarray, numpy.ndarray]:
    """ Compute rotation vector for Companion
    Parameters:
    -----------
    obs_geo: Obsgeo
        Geometry object
    inc_tx: float
        incidence angle
    ws: dict
        Wavelength dictionary
    Return:
    ------
    float, array, array
    bistatic angle, vtx, wts
    """
    bist_ang = obs_geo.swth_geo.inc2bistatic_angle_az(inc_tx)
    inc_rx = obs_geo.swth_geo.inc2slave_inc(inc_tx)
    bistatic_angle_me=numpy.arctan2(numpy.sin(bist_ang) * numpy.sin(inc_rx),
                             (numpy.sin(inc_tx) + numpy.cos(bist_ang) * numpy.sin(inc_rx)))

    xy, uv = obs_tools.compute_rotation(bistatic_angle_me, ws)
    vtx, wts = wrappers.interp_weights(xy, uv)
    # kr_c = k0 * obs_geo_concordia.swth_geo.inc2me_k_scaling(inc_tx)
    return bistatic_angle_me, vtx, wts


def backscatter_doppler(
    ws,
    model: dict,
    obs_geo_trio: ObsGeoTrio,
    mod_transfer: dict,
    wn: dict,
    pol: Optional[str] = "V",
    rxpol: Optional[str] = "mM",
    swell: Optional[bool] = False,
    spec_type: Optional[str] = "SWAN_noneq",
    short_wave_spec_type: Optional[str] = 'polar',
    progress_bar: Optional[bool] = True,
    fetch: Optional[float] = 100e3,
    k_l: Optional[float] = None,
    f0: Optional[float] = 5.4e9,
    add_current_Doppler = False,
):
    """Polarimetric bistatic backscatter and Doppler
    Parameters:
    -----------
    ws: wavespectra
        Wave spectra object from SWAN or None
    Model data: dict
        Model dict that contains tsc_u, tsc_v, wnd_u, wnd_v, wnd_norm, wnd_dir
                                 sst, anomalies,
    obs_geo: ObsGeo
        Geometry of Sentinel1, Companions
    mod_transfer: dict
        Modulation transfer function
    wn: dict
        Wave number
    pol = 'V': str
        polarization of Sentinel1
    rxpol = 'mM': str
        polarization of companions
    swell = True: bool
        Compute swell
    spec_type = "SWAN": str
        Spectrum type, SWAN or LUT
    progress_bar = True: bool
        Activate / deactivate progress bar
    fetch = 100e3: float
        Fetch length in m
    k_l = None: float
        Separating wave number for merging the long and short wave spectra.
    f0 = 5.4e9: float
        Electronic wave number?
    """
    # TODO: also this needs to be refactored, California should not be
    # in name of file, also wrappers is questionable probably the wrappers
    # should go to the forward_models directory, as they are part of the
    # RIM
    # AT: REVIEW (moved to oceans.forward_models.wrappers)

    # polarimetry for rotations
    # pol='V'
    SHP = model["wnd_norm"].shape
    rxpol, polbase = obs_tools.set_polarization(rxpol)
    # monostatic
    nrcs_mono, dop_mono, q = wrappers.make_grids_mono(SHP)

    # bistatic (heading)
    nrcs_me1, dop_me1, qb1 = wrappers.make_grids_bistatic(SHP)
    # Products as specified in Product Specification Document. xarrays would be better
    nrcsd = {"S1": {}, "HA": {}, "HB": {}}
    dopd = {"S1": {}, "HA": {}, "HB": {}}
    geom = {"S1": {}, "HA": {}, "HB": {}}
    covd = {
        "S1": numpy.zeros(SHP, dtype=complex),
        "HA": numpy.zeros(SHP, dtype=complex),
        "HB": numpy.zeros(SHP, dtype=complex),
    }
    for key in nrcsd.keys():
        geom[key] = {"incidence": numpy.zeros((SHP[0])), "other": numpy.zeros((SHP[0]))}
        if key == "S1":
            # Here for now I chose to use H/V for S1, but we could also just stay with I (=H) and O (=V)
            nrcsd[key] = {"H": numpy.zeros(SHP), "V": numpy.zeros(SHP)}
            dopd[key] = {"H": numpy.zeros(SHP), "V": numpy.zeros(SHP)}
        else:
            nrcsd[key] = {polbase[0]: numpy.zeros(SHP), polbase[1]: numpy.zeros(SHP)}
            dopd[key] = {polbase[0]: numpy.zeros(SHP), polbase[1]: numpy.zeros(SHP)}

    # bistatic (trailing)
    nrcs_me2, dop_me2, qb2 = wrappers.make_grids_bistatic(SHP)


    # Change reference for direction of waves from SWAN:
    nwnd_mean = numpy.mean(model["wnd_norm"])
    tools.print_info_spec(spec_type)
    (obs_geo_concordia, obs_geo_discordia) = (
        obs_geo_trio.concordia,
        obs_geo_trio.discordia,
    )
    inc_out = numpy.zeros((SHP[1]))
    # loop over all pixels
    # goes over each column (x-direction)
    k0 = numpy.pi * 2 * f0 / 3e8
    for j in tools.progress(0, SHP[1], step=1, progress_bar=progress_bar):

        # we use the griddata interpolator to rotate the spectrum
        # in azimuth this is always more-or-less the same, so we can use the same indices

        # read transmitter and receivers incident and bistatic angles
        (
            obs_geo_c_angles_j,
            obs_geo_d_angles_j,
        ) = obs_geo_trio.concordia.get_angles_at_index(
            [0, j]
        ), obs_geo_trio.discordia.get_angles_at_index(
            [0, j]
        )

        # for both the trailing and heading satellite we compute the monostatic equivalent geometry
        # this is required for the correct computation of backscatter and Doppler (which includes a rotation of the spectrum)
        # relevant variables are:
        # - 'bistatic_angle_me(_d)': wrongly named, it is the angle between the ground-range direction and 'cross-track'
        # - 'in_me(_d)': monostatic equivalent incident angle
        # - 'kr_c/d': the effective range-projected wavelength (will not change too much)
        inc_tx = obs_geo_c_angles_j.inc_m
        inc_me = obs_geo_concordia.swth_geo.inc2me_inc(
            inc_tx
        )
        if short_wave_spec_type != 'polar':
            bistatic_angle_me, vtx_h, wts_h = rotation_companion(obs_geo_concordia, inc_tx,  wn)
        else:
            inc_rx = obs_geo_c_angles_j.inc_b
            bist_ang = obs_geo_c_angles_j.bist_ang
            bistatic_angle_me = numpy.arctan2(numpy.sin(bist_ang) * numpy.sin(inc_rx),
                                              (numpy.sin(inc_tx) + numpy.cos(bist_ang) * numpy.sin(inc_rx)))
        obs_geo_me_angles = ObsGeoAngles(inc_me, None, bistatic_angle_me)
        kr_c = k0 * obs_geo_concordia.swth_geo.inc2me_k_scaling(inc_tx)
        inc_me_d = obs_geo_discordia.swth_geo.inc2me_inc(inc_tx)
        if short_wave_spec_type != 'polar':
            bistatic_angle_me_d, vtx_t, wts_t = rotation_companion(obs_geo_discordia, inc_tx,  wn)
        else:
            inc_rx = obs_geo_d_angles_j.inc_b
            bist_ang = obs_geo_d_angles_j.bist_ang
            bistatic_angle_me_d = numpy.arctan2(numpy.sin(bist_ang) * numpy.sin(inc_rx),
                                              (numpy.sin(inc_tx) + numpy.cos(bist_ang) * numpy.sin(inc_rx)))
        obs_geo_me_angles_d = ObsGeoAngles(inc_me_d, None, bistatic_angle_me_d)
        kr_d = k0 * obs_geo_discordia.swth_geo.inc2me_k_scaling(inc_tx)

        for i in range(0, SHP[0]):  # goes over each row (y-direction)

            # computes a wind-wave spectrum (or what we refer to as short waves) for each pixel on a non-linear wavenumber grid
            # we have now the option to do this Cartesian and polar, polar is recommended for numerical purposes
            B, S = spec_tools.compute_spec(ws, wn, model, SHP, spec_type,
                                           mod_transfer, (i, j), fetch=fetch, k_l=k_l,short_wave_spec_type=short_wave_spec_type)

            # - monostatic - #
            # the monostatic wrapper computes monostatic backscatter, Doppler and the wave breaking fraction
            # backscatter and Doppler are subdivided in specular, breaking, Bragg and 'cross' contributions
            # the sum of all contributions is taken later
            # we input two times the local wind, which is a bit of a legacy issue, but leave it in for now, it will give use some flexibility
            wnd_dir = model["wnd_dir"][i, j]
            nwnd_local = model["wnd_norm"][i, j]

            # call the monostatic wrapper
            if short_wave_spec_type == 'polar':
                bkscatt = wrappers.backscatter_Doppler_mono_polar
                ij_smono, ij_dmono, qij = bkscatt(
                    S,
                    wn["k"],
                    wn["phi"],
                    wnd_dir,
                    obs_geo_c_angles_j,
                    nwnd_local,
                    fetch,
                    degrees=False,
                    u10_local=nwnd_local,
                )
            else:
                print("Warning! Using Cartesian spectrum might give numerical issues!")
                bkscatt = wrappers.backscatter_Doppler_mono
                ij_smono, ij_dmono, qij = bkscatt(
                    S,
                    wn["k_x"],
                    wn["k_y"],
                    wn["dks"],
                    wnd_dir,
                    obs_geo_c_angles_j,
                    nwnd_local,
                    fetch,
                    degrees=False,
                    u10_local=nwnd_local,
                )
            for key in nrcs_mono.keys():
                nrcs_mono[key][i, j] = ij_smono[key]
                dop_mono[key][i, j] = ij_dmono[key]
            q[i, j] = qij


            # - bistatic heading - #
            # The bistatic scattering is computing by rotating the input spectrum into the ground-range direction
            # Note that the associated wind direction should also be rotated
            # Input into the wrapper requires the monostatic equivalent geometry and the projected/scaled radar wave number
            # Note also that inside the monostatic equivalent wrapper the multiplication with wave breaking fraction q is already done
            # rotate the spectrum
            if short_wave_spec_type == 'polar':
                wn["S"] = S
                Sb=obs_tools.compute_rotation_polar(bistatic_angle_me, wn)
                # call the bistatic wrapper
                # bkscatt = wrappers.backscatter_Doppler_bistatic
                bkscatt = wrappers.backscatter_Doppler_monoeq_polar
                # TODO: here we will need to pass the actual monostatic equivalent
                # angle of incidence
                # AT: REVIEW passing the monostatic equivalent inc angle
                ij_sbi, ij_dbi = bkscatt(
                    Sb,
                    wn["k"],
                    wn["phi"],
                    wnd_dir + bistatic_angle_me,
                    obs_geo_me_angles,
                    obs_geo_c_angles_j,
                    nwnd_local,
                    fetch,
                    'V',
                    degrees=False,
                    k_r=kr_c,
                    u10_local=nwnd_local,
                )
            else:
                print("Warning! Using Cartesian spectrum might give numerical issues!")
                Sb = wrappers.interpolate(S.flatten(), vtx_h, wts_h)
                Sb = Sb.reshape(wn["k"].shape)
                # call the bistatic wrapper
                # bkscatt = wrappers.backscatter_Doppler_bistatic
                bkscatt = wrappers.backscatter_Doppler_monoeq
                # TODO: here we will need to pass the actual monostatic equivalent
                # angle of incidence
                # AT: REVIEW passing the monostatic equivalent inc angle
                ij_sbi, ij_dbi = bkscatt(
                    Sb,
                    wn["k_x"],
                    wn["k_y"],
                    wn["dks"],
                    wnd_dir + bistatic_angle_me,
                    obs_geo_me_angles,
                    obs_geo_c_angles_j,
                    nwnd_local,
                    fetch,
                    'V',
                    degrees=False,
                    k_r=kr_c,
                    u10_local=nwnd_local,
                )


            for key in nrcs_me1.keys():
                nrcs_me1[key][i, j] = ij_sbi[key]
            for key in dop_me1.keys():
                dop_me1[key][i, j] = ij_dbi[key]

            # - bistatic trailing - #
            # Analog to the bistatic heading scatter and Doppler
            # rotate the spectrum
            if short_wave_spec_type == 'polar':
                #wn["S"] = S
                Sb=obs_tools.compute_rotation_polar(bistatic_angle_me_d, wn)
                # call the bistatic wrapper
                # bkscatt = wrappers.backscatter_Doppler_bistatic
                bkscatt = wrappers.backscatter_Doppler_monoeq_polar
                # TODO: here we will need to pass the actual monostatic equivalent
                # angle of incidence
                # AT: REVIEW passing the monostatic equivalent inc angle
                ij_sbi, ij_dbi = bkscatt(
                    Sb,
                    wn["k"],
                    wn["phi"],
                    wnd_dir + bistatic_angle_me_d,
                    obs_geo_me_angles_d,
                    obs_geo_d_angles_j,
                    nwnd_local,
                    fetch,
                    'V',
                    degrees=False,
                    k_r=kr_c,
                    u10_local=nwnd_local,
                )
            else:
                Sb = wrappers.interpolate(S.flatten(), vtx_t, wts_t)
                Sb = Sb.reshape(wn["k"].shape)
                # call the bistatic wrapper
                # bkscatt = wrappers.backscatter_Doppler_bistatic
                bkscatt = wrappers.backscatter_Doppler_monoeq
                # TODO: here we will need to pass the actual monostatic equivalent
                # angle of incidence
                # AT: REVIEW passing the monostatic equivalent inc angle
                ij_sbi, ij_dbi = bkscatt(
                    Sb,
                    wn["k_x"],
                    wn["k_y"],
                    wn["dks"],
                    wnd_dir + bistatic_angle_me_d,
                    obs_geo_me_angles_d,
                    obs_geo_d_angles_j,
                    nwnd_mean,
                    fetch,
                    'V',
                    degrees=False,
                    k_r=kr_c,
                    u10_local=nwnd_local,
                )

            for key in nrcs_me2.keys():
                nrcs_me2[key][i, j] = ij_sbi[key]
            for key in dop_me2.keys():
                dop_me2[key][i, j] = ij_dbi[key]


        # Polarimetry is handled by separating three contributions:
        # - regular (Bragg) scattering
        # - specular type scattering (specular and wave breaking)
        # - cross-pol
        # Here I have a fixe geometry, i.e. all point are at the same range
        # LIST_BI =['Bragg', 'specular', 'wave_breaking', 'Bragg_cross',
        #          'specular_cross', 'wave_breaking_cross']
        # 1st satellite
        sigma_r = nrcs_me1["Bragg"][:, j]
        sigma_s = nrcs_me1["specular"][:, j] + nrcs_me1["wave_breaking"][:, j]
        sigma_cp = nrcs_me1["wave_breaking_cross"][:, j]
        cov_bi1 = polrot.monoeq2bistatic(
            sigma_r,
            sigma_s,
            sigma_cp,
            inc_tx,
            obs_geo_concordia.swth_geo,
            txpol=pol,
            rxpol=rxpol,
            method="fp",
        )
        # PLD: we compute a phasor with the amplitude set by the corresponding NRCS
        # and a small phase proportional to the Doppler velocity of the component
        # The factor 100 is arbitrary, but it should be fine
        wdop_r_MM = sigma_r * numpy.exp(1j * dop_me1["Bragg_vv"][:, j] / 100)
        # print("%f" % numpy.angle(wdop_r_MM[0]))
        wdop_r_mm = sigma_r * numpy.exp(1j * dop_me1["Bragg_hh"][:, j] / 100)
        wdop_s = nrcs_me1["specular"][:, j] * numpy.exp(
            1j * dop_me1["specular"][:, j] / 100
        ) + nrcs_me1["wave_breaking"][:, j] * numpy.exp(
            1j * dop_me1["wave_breaking"][:, j] / 100
        )
        wdop_cp = nrcs_me1["wave_breaking_cross"][:, j] * numpy.exp(
            1j * dop_me1["wave_breaking_cross"][:, j] / 100
        )
        xcov_bi1 = polrot.monoeq2bistatic(
            wdop_r_MM,
            wdop_s,
            wdop_cp,
            inc_tx,
            obs_geo_concordia.swth_geo,
            sigma_hh_r=wdop_r_mm,  # PLD: This should work, buit it is evil.
            txpol=pol,
            rxpol=rxpol,
            method="fp",
        )

        # NRCS and Doppler come from the (scattering) covariance matrices
        # Note that ground-projected Doppler velocity has to be 'unlogged'
        # The Doppler velocity is then converted to Doppler frequency [Hz]
        nrcsd["HA"][polbase[0]][:, j] = cov_bi1[:, 0, 0]
        nrcsd["HA"][polbase[1]][:, j] = cov_bi1[:, 1, 1]
        dopd["HA"][polbase[0]][:, j] = (
            numpy.angle(xcov_bi1[:, 0, 0])
            * (-100)
            * kr_c
            / numpy.pi
            * numpy.sin(inc_me)
        )
        dopd["HA"][polbase[1]][:, j] = (
            numpy.angle(xcov_bi1[:, 1, 1])
            * (-100)
            * kr_c
            / numpy.pi
            * numpy.sin(inc_me)
        )
        covd["HA"][:, j] = cov_bi1[:, 0, 1]

        # Polarimetry for the second satellite is equivalent to the first (but with different geometry)
        # 2nd satellite
        sigma_r = nrcs_me2["Bragg"][:, j]
        sigma_s = nrcs_me2["specular"][:, j] + nrcs_me1["wave_breaking"][:, j]
        sigma_cp = nrcs_me2["wave_breaking_cross"][:, j]
        # cov_bi2[:, j, : ,:]
        cov_bi2 = polrot.monoeq2bistatic(
            sigma_r,
            sigma_s,
            sigma_cp,
            inc_tx,
            obs_geo_discordia.swth_geo,
            txpol=pol,
            rxpol=rxpol,
            method="fp",
        )
        wdop_r_MM = sigma_r * numpy.exp(1j * dop_me2["Bragg_vv"][:, j] / 100)
        # print("%f" % numpy.angle(wdop_r_MM[0]))
        wdop_r_mm = sigma_r * numpy.exp(1j * dop_me2["Bragg_hh"][:, j] / 100)
        wdop_s = nrcs_me2["specular"][:, j] * numpy.exp(
            1j * dop_me2["specular"][:, j] / 100
        ) + nrcs_me2["wave_breaking"][:, j] * numpy.exp(
            1j * dop_me2["wave_breaking"][:, j] / 100
        )
        wdop_cp = nrcs_me2["wave_breaking_cross"][:, j] * numpy.exp(
            1j * dop_me2["wave_breaking_cross"][:, j] / 100
        )
        xcov_bi2 = polrot.monoeq2bistatic(
            wdop_r_MM,
            wdop_s,
            wdop_cp,
            inc_tx,
            obs_geo_discordia.swth_geo,
            sigma_hh_r=wdop_r_mm,  # PLD: This should work, buit it is evil.
            txpol=pol,
            rxpol=rxpol,
            method="fp",

        )

        # NRCS and Doppler come from the (scattering) covariance matrices
        nrcsd["HB"][polbase[0]][:, j] = cov_bi2[:, 0, 0]
        nrcsd["HB"][polbase[1]][:, j] = cov_bi2[:, 1, 1]
        dopd["HB"][polbase[0]][:, j] = (
            numpy.angle(xcov_bi2[:, 0, 0])
            * (-100)
            * kr_d
            / numpy.pi
            * numpy.sin(inc_me_d)
        )
        dopd["HB"][polbase[1]][:, j] = (
            numpy.angle(xcov_bi2[:, 1, 1])
            * (-100)
            * kr_d
            / numpy.pi
            * numpy.sin(inc_me_d)
        )
        covd["HB"][:, j] = cov_bi2[:, 0, 1]
        inc_out[j] = inc_tx

    # The integral scattering and Doppler for the monostatic
    if pol == "V" or pol == "v":
        nrcsd["S1"]["H"] = nrcs_mono["wave_breaking_cross"] * q
        nrcsd["S1"]["V"] = ((nrcs_mono["Bragg"] + nrcs_mono["specular"])
                            * (1 - q) + nrcs_mono["wave_breaking"] * q)
        dopd["S1"]["H"] = (
            -dop_mono["wave_breaking_cross"]
            * k0
            / numpy.pi
            * numpy.sin(obs_geo_concordia._inc_m)
        )
        dopd["S1"]["V"] = (
            (
                (-dop_mono["Bragg"] - dop_mono["specular"])
                - dop_mono["wave_breaking"]
            )
            * k0
            / numpy.pi
            * numpy.sin(obs_geo_concordia._inc_m)
        )
    else:
        print('Warning! For now only use V transmission!')
        nrcsd["S1"]["V"] = nrcs_mono["wave_breaking_cross"] * q
        nrcsd["S1"]["H"] = ((nrcs_mono["Bragg"] + nrcs_mono["specular"])
                            * (1 - q) + nrcs_mono["wave_breaking"] * q)
        dopd["S1"]["V"] = (
            -dop_mono["wave_breaking_cross"]
            * k0
            / numpy.pi
            * numpy.sin(obs_geo_concordia._inc_m)
        )
        dopd["S1"]["H"] = (
            (
                (-dop_mono["Bragg"] - dop_mono["specular"])
                - dop_mono["wave_breaking"]
            )
            * k0
            / numpy.pi
            * numpy.sin(obs_geo_concordia._inc_m)
        )
    nrcsd["incidence"] = inc_out

    # The Doppler velocity from the currents are added here
    # We assume it doesn't carry any polarimetric signature
    if add_current_Doppler:
        # Add TSC Doppler
        wl = 2 * numpy.pi / k0
        a = numpy.zeros(obs_geo_concordia._inc_m.shape + (3, 2))
        a[..., 0, 0] = - 2 / wl * numpy.sin(obs_geo_concordia._inc_m)
        a[..., 1, 0] = - 1 / wl * (numpy.sin(obs_geo_concordia._inc_m) + numpy.sin(obs_geo_concordia.inc_b) * numpy.cos(obs_geo_concordia.bist_ang))
        a[..., 1, 1] = 1 / wl * numpy.sin(obs_geo_concordia.inc_b) * numpy.sin(obs_geo_concordia.bist_ang)

        a[..., 2, 0] = - 1 / wl * (numpy.sin(obs_geo_discordia._inc_m) + numpy.sin(obs_geo_discordia.inc_b) * numpy.cos(obs_geo_discordia.bist_ang))
        a[..., 2, 1] = 1 / wl * numpy.sin(obs_geo_discordia.inc_b) * numpy.sin(obs_geo_discordia.bist_ang)
        tsc = numpy.stack([model['tsc_u'], model['tsc_v']], axis=-1)
        tsc_dop = numpy.einsum('...ij,...j->...i', a, tsc)
        dopd["S1"]["H"] = dopd["S1"]["H"] + tsc_dop[:, :, 0]
        dopd["S1"]["V"] = dopd["S1"]["V"] + tsc_dop[:, :, 0]
        dopd["HA"]["M"] = dopd["HA"]["M"] + tsc_dop[:, :, 1]
        dopd["HA"]["m"] = dopd["HA"]["m"] + tsc_dop[:, :, 1]
        dopd["HB"]["M"] = dopd["HB"]["M"] + tsc_dop[:, :, 2]
        dopd["HB"]["m"] = dopd["HB"]["m"] + tsc_dop[:, :, 2]
    # return cov_mono, dop_mono, q, cov_bi1, dop_bi1, cov_bi2, dop_bi2
    return nrcsd, covd, dopd, q



# This one is no longer used, so we will go.
def sum_items(dic: dict, cross=False) -> numpy.ndarray:
    if cross is True:
        _res = sum(dic[item] for item in dic if "cross" in item)
    else:
        _res = sum(dic[item] for item in dic if "cross" not in item)
    return _res


def add_noise(
    nrcs: dict, dop: dict, dx: float, par, dic_geom: Optional[dict] = {}
) -> None:
    nrcs.pop("incidence", None)
    if "obs_geo" in dic_geom.keys():
        obs_geo = dic_geom["obs_geo"]
    else:
        # REVIEW recall that build_geometry returns two ObsGeos, one for each
        # companion but for now we are only using one for the noise
        obs_geo, _ = obs_tools.build_geometry(par.parfile, par.incident_angle,
                                              dau=par.dau)
        dic_geom["obs_geo"] = obs_geo
    if "frstr_dual" in dic_geom.keys():
        fstr_dual = dic_geom["fstr_dual"]
        fstr_ati = dic_geom["fstr_ati"]
        fstr_s1 = dic_geom["fstr_s1"]
    else:
        fstr_dual, fstr_ati, fstr_s1 = obs_tools.build_performance_file(par)
        dic_geom["fstr_dual"] = fstr_dual
        dic_geom["fstr_ati"] = fstr_ati
        dic_geom["fstr_s1"] = fstr_s1
    radarm = RadarModel(
        obs_geo,
        fstr_s1,
        fstr_dual,
        fstr_ati,
        az_res=par.az_res,
        prod_res=dx,
        b_ati=par.b_ati,
    )
    isv = {}
    nrcs_o, dop_o, isv_o = radarm.add_errors(nrcs, dop, isv)
    return nrcs_o, dop_o, isv_o, dic_geom
