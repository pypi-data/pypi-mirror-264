from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
import xarray as xr
import drama.io.cfg as cfg
import drama.geo.geometry as d_geo
import drama.geo.swath_geo as d_swath_geo
import drama.constants as d_constants

from stereoid.oceans.radar_model import ObsGeo, RadarModel
from stereoid.oceans.tops_model import TopsModel
import stereoid.utils.config as st_config
import stereoid.sar_performance as sar_perf


def get_burst(subswath, burst_nr):
    burst_beginning = az_start + ((burst_nr - 1) * (burst_length - overlap_length))
    burst_end = az_start + (burst_nr * burst_length - (burst_nr - 1) * overlap_length)
    burst = subswath.sel(az=slice(burst_beginning, burst_end))
    slc_az_sampling = 2.05e-3  # in seconds
    slc_nr_demarc_lines = 20
    demarc_interval = slc_az_sampling * slc_nr_demarc_lines
    demarc_length = demarc_interval * mean_ground_rectilinear_v
    mask_beginning = burst.az < (burst.az.min() + demarc_length)
    mask_end = burst.az > (burst.az.max() - demarc_length)
    mask_demarc = np.logical_or(mask_beginning, mask_end)
    burst_beginning_zdt = (burst_nr - 1) * (burst_duration - burst_overlap)
    burst_end_zdt = burst_nr * burst_duration - (burst_nr - 1) * burst_overlap
    zero_doppler_time = np.linspace(
        burst_beginning_zdt, burst_end_zdt, burst.az.shape[0]
    )
    burst = burst.assign_coords(azimuth_time=("az", zero_doppler_time))
    burst = burst.assign_attrs(azimuth_overlap_length=overlap_length)
    burst["nrcs"] = burst.nrcs.where(~mask_demarc, np.nan)
    burst = burst.assign(mask_demarc=mask_demarc)
    return burst


if __name__ == "__main__":
    path_to_results = Path(
        "~/Code/stereoid_public/stereoid_inputs_and_outputs/RESULTS/Scenarios/California/SWAN"
    ).expanduser()
    path_to_nrcs = (
        path_to_results
        / "nrcs_L1_All_obs_California_T01_SWAN_350_x_050_300_y_350_650_rot_0_05.nc"
    )
    user_cfg_path = (
        Path("~/Code/stereoid_public/stereoid_inputs_and_outputs/PAR/").expanduser()
        / "user.cfg"
    )
    nrcs = xr.open_dataset(path_to_nrcs)
    # path to PAR file
    # Set this to the directory of your data and model results
    paths = st_config.parse(user_cfg_path, section="Paths")
    parfile = paths["par"] / f"Hrmny_2021_1.cfg"
    par_data = cfg.ConfigFile(parfile)
    swath = d_swath_geo.SingleSwath(par_file=parfile, orb_type="sunsync")
    qgeo = d_geo.QuickRadarGeometry(swath.Horb, degrees=True)
    r_e = np.linalg.norm(
        swath.xyz[swath.asc_idx[0] : swath.asc_idx[-1], 0], axis=1
    )  # Local earth radius at near range over an entire orbit
    cs = CubicSpline(swath.lats[swath.asc_idx[0] : swath.asc_idx[-1], 0], r_e)
    r_e = cs(nrcs.isel(grg=0).latitude)
    inc_near = par_data.IWS.inc_near
    inc_far = par_data.IWS.inc_far
    n = np.sqrt(d_constants.gm_earth / swath.a**3)
    theta_l = qgeo.inc_to_look(inc_near[0])
    beta = inc_near[0] - theta_l
    v_g = r_e * n * np.cos(np.deg2rad(beta))
    v_s = np.linalg.norm(swath.v_ecef[swath.asc_idx[0] : swath.asc_idx[-1]], axis=1)
    cs = CubicSpline(swath.lats[swath.asc_idx[0] : swath.asc_idx[-1], 0], v_s)
    v_s = cs(nrcs.isel(grg=0).latitude)
    v_r = np.sqrt(v_s * v_g)
    burst_duration = 2.75  # focus burst length in seconds
    burst_overlap = 0.22  # in seconds
    mean_ground_rectilinear_v = np.mean(v_r)
    burst_length = mean_ground_rectilinear_v * burst_duration
    overlap_length = mean_ground_rectilinear_v * burst_overlap
    nr_of_bursts = 8
    az_length = nr_of_bursts * burst_length - (nr_of_bursts - 1) * overlap_length
    az_start = 100e3
    nrcs_slice = nrcs.sel(az=slice(az_start, az_start + az_length))
    grg_near = qgeo.inc_to_gr(inc_near + 0.14)
    grg_far = qgeo.inc_to_gr(inc_far)
    nrcs_iw1 = nrcs_slice.interp(
        grg=np.arange(grg_near[0], grg_far[0], 50),
        az=np.arange(nrcs_slice.az[0], nrcs_slice.az[-1], 50),
        method="cubic",
    )
    b1 = get_burst(nrcs_iw1, 1)
    print(b1)
    b1_drop_nan = b1.where(~b1.mask_demarc, drop=True)
    obs_geo = ObsGeo(
        b1.sel(sat="S1", pol="M").inc.to_numpy(),
        b1.sel(sat="HA", pol="M").inc.to_numpy(),
        b1.sel(sat="HA", pol="M").bist_ang.to_numpy(),
    )
    fstr_dual = sar_perf.sarperf_files(
        paths["main"], "hrmny_2021_tripple", mode="IWS", parpath=parfile
    )
    fstr_ati = sar_perf.sarperf_files(
        paths["main"], "hrmny_2021_tripple_ati", mode="IWS", parpath=parfile
    )
    fstr_s1 = sar_perf.sarperf_files(
        paths["main"],
        "sentinel",
        is_bistatic=False,
        mode="IWS",
        parpath=parfile,
    )
    zero_dopple_time = b1_drop_nan.azimuth_time - np.median(b1_drop_nan.azimuth_time)
    radarm = TopsModel(
        zero_dopple_time,
        obs_geo,
        fstr_s1,
        fstr_dual,
        fstr_ati,
        az_res=20,
        prod_res=1000,
        b_ati=10,
    )
    radarm.add_errors(
        b1_drop_nan.nrcs,
        np.zeros_like(b1_drop_nan.nrcs),
        np.zeros_like(b1_drop_nan.nrcs),
    )
