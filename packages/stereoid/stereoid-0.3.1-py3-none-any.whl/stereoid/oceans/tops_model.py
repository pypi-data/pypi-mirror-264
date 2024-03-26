from dataclasses import dataclass
from typing import Union, Optional
from pathlib import Path

import drama.constants as d_constants
import drama.geo.geometry as d_geo
import drama.geo.swath_geo as d_swath_geo
import drama.io.cfg as cfg
import numpy as np
import numpy.typing as npt
import scipy.linalg as linalg
from scipy.interpolate import CubicSpline, RegularGridInterpolator
import xarray as xr

import stereoid.oceans.radar_model
import stereoid.utils.config as st_config

BURST_DURATION = 3  # focus burst length in seconds
BURST_OVERLAP = 0.22  # in seconds
SLC_AZ_SAMPLING = 2e-3  # in seconds
SLC_NR_DEMARC_LINES = 20


@dataclass(frozen=True)
class TOPSParameters:
    """A class to store the TOPS burst parameters"""

    burst_length: float
    overlap_length: float
    burst_duration: float
    overlap_duration: float
    nr_of_bursts: int
    inc_near: npt.NDArray
    inc_far: npt.NDArray
    r_s: npt.NDArray
    burst_sensing_duration: npt.NDArray

    def acq_az_length(self) -> float:
        return (
            self.nr_of_bursts * self.burst_length
            - (self.nr_of_bursts - 1) * self.overlap_length
        )

    def mean_ground_rectilinear_v(self) -> float:
        return self.burst_length / self.burst_duration


class TOPSAcquisitions:
    """A class to implement functionality related to extracting and
    mosaicking TOPS bursts."""

    def __init__(
        self,
        parameters: TOPSParameters,
        az_offset: float,
        az_sampling: float = SLC_AZ_SAMPLING,
        nr_demarc_lines: int = SLC_NR_DEMARC_LINES,
    ):
        self.parameters = parameters
        self.az_offset = az_offset
        self.az_sampling = az_sampling
        self.nr_demarc_lines = nr_demarc_lines

    def get_burst(
        self,
        subswath: xr.Dataset,
        burst_nr: int,
        demarc: bool = True,
        data_var_name: str = "nrcs",
    ) -> xr.Dataset:
        """
        Retrieve a specific burst from the given subswath dataset.

        Parameters
        ----------
        subswath : xarray.Dataset
            Dataset representing the subswath from which to extract the burst.

        burst_nr : int
            The number of the burst to retrieve. The minimum is 1 and the
            maximum is determined by the number of bursts within the
            acquisition.

        Returns
        -------
        xarray.Dataset
            Dataset representing the specified burst.

        Notes
        -----
        This method extracts and returns a specific burst from the provided subswath dataset.
        The burst number (burst_nr) indicates the position of the desired burst.

        Examples
        --------
        >>> burst_data = tops_acqs.get_burst(subswath_data, 2)
        """
        az_start = subswath.isel(az=0).az
        burst_length = self.parameters.burst_length
        overlap_length = self.parameters.overlap_length
        starting_point = self.az_offset + az_start
        burst_beginning = starting_point + (
            (burst_nr - 1) * (burst_length - overlap_length)
        )
        burst_end = starting_point + (
            burst_nr * burst_length - (burst_nr - 1) * overlap_length
        )
        az_mask = (subswath.az >= burst_beginning) & (subswath.az <= burst_end)
        burst = subswath.isel(az=az_mask)
        # burst = subswath.sel(az=slice(burst_beginning, burst_end))
        demarc_interval = self.az_sampling * self.nr_demarc_lines
        mean_ground_rectilinear_v = self.parameters.mean_ground_rectilinear_v()
        demarc_length = demarc_interval * mean_ground_rectilinear_v
        mask_beginning = burst.az < (burst.az.min() + demarc_length)
        mask_end = burst.az > (burst.az.max() - demarc_length)
        mask_demarc = mask_beginning | mask_end

        burst_duration, burst_overlap = (
            self.parameters.burst_duration,
            self.parameters.overlap_duration,
        )
        zero_doppler_time = (
            burst.az - self.az_offset
        ).to_numpy() / mean_ground_rectilinear_v
        burst = burst.assign_coords(azimuth_time=("az", zero_doppler_time))
        # These are the exact zero-Doppler times of the first and last lines but
        # since we are not interpolating the subswath to these exact values, the
        # first and last values of zero_doppler_time can be different. Store
        # these exact values as attributes.
        switching_time = (subswath.subswath_number - 1) * 0.9
        burst_beginning_zdt = switching_time + (burst_nr - 1) * (
            burst_duration - burst_overlap
        )
        burst_end_zdt = (
            switching_time + burst_nr * burst_duration - (burst_nr - 1) * burst_overlap
        )
        cycle_time = 2.75
        initial_sensing_time = (
            0
            if (burst_nr == 1 and subswath.subswath_number == 1)
            else self.parameters.burst_sensing_duration[subswath.subswath_number - 1]
        )
        subswath_switching_time = 0.01
        if subswath.subswath_number == 1:
            initial_sensing_time = 0
        else:
            previous_subswath = subswath.subswath_number - 1
            i_of_previous_subswath = (previous_subswath - 1) % 3
            initial_sensing_time = (
                np.sum(
                    self.parameters.burst_sensing_duration[: i_of_previous_subswath + 1]
                )
                + len(range(i_of_previous_subswath + 1)) * subswath_switching_time
            )
        first_line_sensing_time = initial_sensing_time + (burst_nr - 1) * cycle_time
        last_line_sensing_time = (
            first_line_sensing_time
            + self.parameters.burst_sensing_duration[subswath.subswath_number - 1]
        )
        sensing_time = np.interp(
            burst.az,
            np.linspace(burst_beginning, burst_end),
            np.linspace(first_line_sensing_time, last_line_sensing_time),
        )
        burst = burst.assign(sensing_time=("az", sensing_time))
        burst = burst.assign_attrs(
            azimuth_overlap_length=overlap_length,
            first_zdt=burst_beginning_zdt,
            last_zdt=burst_end_zdt,
            first_line_sensing_time=first_line_sensing_time,
            last_line_sensing_time=last_line_sensing_time,
        )
        if demarc:
            burst["nrcs"] = burst.nrcs.where(~mask_demarc, np.nan)
        burst = burst.assign(mask_demarc=mask_demarc)
        return burst

    def mosaic(
        self,
        subswath: xr.Dataset,
        nr_of_bursts: int,
        remove_overlap: bool,
        demarc: bool = True,
        data_var_name: str = "nrcs",
    ) -> xr.Dataset:
        """
        Mosaic multiple bursts along the azimuth direction.

        Parameters
        ----------
        subswath : xarray.Dataset
            Dataset representing the subswath from which bursts are extracted.

        nr_of_bursts : int
            Number of bursts to mosaic.

        remove_overlap : bool
            Whether to remove the overlap regions of the bursts.

        Returns
        -------
        xarray.Dataset
            Mosaicked dataset containing bursts concatenated along the azimuth direction.

        Notes
        -----
        This method extracts bursts from the given subswath, removes azimuth overlap,
        and concatenates them along the azimuth direction to create a mosaicked dataset.

        The azimuth overlap length is determined from the attributes of the first burst.
        The specified number of bursts (nr_of_bursts) are processed and mosaicked.

        Examples
        --------
        >>> mosaic_dataset = tops_acqs.mosaic(subswath_data, 3)
        """
        az_sampling = subswath.az[1] - subswath.az[0]
        b1 = self.get_burst(subswath, 1, demarc, data_var_name)
        if remove_overlap:
            overlap_length = b1.attrs["azimuth_overlap_length"]
            samples_overlap = int(np.floor(overlap_length / az_sampling) / 2)
            if not samples_overlap:
                raise ValueError(
                    "There are no overlapping samples to remove. This can occur then the sampling is too coarse or if the bursts are created without the overlap regions.",
                    overlap_length,
                    az_sampling,
                )
            b1 = b1.isel(az=slice(samples_overlap, -samples_overlap))
        lines = np.linspace(0, len(b1.az) - 1, len(b1.az))
        b1 = b1.assign_coords(line=("az", lines))
        b1 = b1.swap_dims({"az": "line"})
        bursts = [b1]
        for i in range(2, nr_of_bursts + 1):
            burst = self.get_burst(subswath, i, demarc, data_var_name)
            if remove_overlap:
                burst = burst.isel(az=slice(samples_overlap, -samples_overlap))
            lines = np.linspace(
                bursts[i - 2].isel(line=-1).line + 1,
                bursts[i - 2].isel(line=-1).line + 1 + len(burst.az) - 1,
                len(burst.az),
            )
            burst = burst.assign_coords(line=("az", lines))
            burst = burst.swap_dims({"az": "line"})
            bursts.append(burst)
        return xr.concat(bursts, dim="line")

    def extract_subswath(
        self, data: xr.Dataset, subswath_nr: int, drop_invalid: Optional[bool] = False
    ) -> xr.Dataset:
        """
        Extract a specific subswath from the given dataset.

        Parameters
        ----------
        data : xarray.Dataset
            The input dataset containing subswaths.

        subswath_nr : int
            The number indicating the subswath to be extracted starting from 1.

        drop_invalid : bool
            If True, the samples that correspond to switching time from the
            previous burst to the current one are dropped. If False, the samples
            at that location are replaced with NaN.

        Returns
        -------
        xarray.Dataset
            Dataset representing the specified subswath.

        Notes
        -----
        This method extracts and returns a specific subswath from the provided xarray dataset.
        The subswath number (subswath_nr) is used to identify the desired subswath.
        """
        subswath_nr -= 1
        inc_near = self.parameters.inc_near[subswath_nr]
        inc_far = self.parameters.inc_far[subswath_nr]
        if "sat" in data.dims:
            subswath_mask = (
                (data.isel(sat=0).inc >= inc_near) & (data.isel(sat=0).inc <= inc_far)
            ).to_numpy()
        else:
            subswath_mask = ((data.inc >= inc_near) & (data.inc <= inc_far)).to_numpy()
        subswath_range_cut = data.isel(grg=subswath_mask)
        subswath_switching_time = 0.9
        mean_ground_rectilinear_v = self.parameters.mean_ground_rectilinear_v()
        azimuth_switching_gap = (
            subswath_switching_time * mean_ground_rectilinear_v * subswath_nr
        )
        starting_az = subswath_range_cut.az.min()
        subswath_starting_az = starting_az + azimuth_switching_gap
        subswath_range_cut = subswath_range_cut.assign_attrs(
            subswath_number=subswath_nr + 1
        )
        return subswath_range_cut.where(
            subswath_range_cut.az >= subswath_starting_az, np.nan, drop=drop_invalid
        )


def tops_parameters(
    latitude: npt.ArrayLike,
    user_cfg_path: Path,
    par_file_name: Union[str, Path],
    burst_duration: float = BURST_DURATION,
    burst_overlap: float = BURST_OVERLAP,
) -> TOPSParameters:
    """
    Create the TOPS parameters for the track defiend by the parameter file.

    Parameters
    ----------
    user_cfg_path : Union[str, Path]
        The path to the user config file.
    par_file_name : Union[float, npt.ArrayLike]
        The path to the parameter file.
    """
    paths = st_config.parse(user_cfg_path, section="Paths")
    parfile = paths["par"] / par_file_name
    par_data = cfg.ConfigFile(parfile)
    swath = d_swath_geo.SingleSwath(par_file=parfile, orb_type="sunsync")
    qgeo = d_geo.QuickRadarGeometry(swath.Horb, degrees=False)
    r_e = linalg.norm(
        swath.xyz[swath.asc_idx[0] : swath.asc_idx[-1], 0], axis=1
    )  # Local earth radius at near range over an entire orbit
    cs = CubicSpline(swath.lats[swath.asc_idx[0] : swath.asc_idx[-1], 0], r_e)
    r_e = cs(latitude)
    inc_near = np.deg2rad(par_data.IWS.inc_near)
    n = np.sqrt(d_constants.gm_earth / swath.a**3)
    theta_l = qgeo.inc_to_look(inc_near[0])
    beta = inc_near[0] - theta_l
    v_g = r_e * n * np.cos(beta)
    v_s = np.linalg.norm(swath.v_ecef[swath.asc_idx[0] : swath.asc_idx[-1]], axis=1)
    cs = CubicSpline(swath.lats[swath.asc_idx[0] : swath.asc_idx[-1], 0], v_s)
    v_s = cs(latitude)
    v_r = np.sqrt(v_s * v_g)
    mean_ground_rectilinear_v = np.mean(v_r)
    burst_length = mean_ground_rectilinear_v * burst_duration
    overlap_length = mean_ground_rectilinear_v * burst_overlap
    nr_of_bursts = 8
    inc_far = np.deg2rad(par_data.IWS.inc_far)
    # Calculate slant range
    cs = CubicSpline(
        swath.lats[swath.asc_idx[0] : swath.asc_idx[-1], 0],
        swath.R[swath.asc_idx[0] : swath.asc_idx[-1], 0],
    )
    r_s = cs(latitude)
    return TOPSParameters(
        burst_length,
        overlap_length,
        burst_duration,
        burst_overlap,
        nr_of_bursts,
        inc_near,
        inc_far,
        r_s,
        par_data.IWS.burst_length,
    )


class TopsModel(stereoid.oceans.radar_model.RadarModel):
    def __init__(
        self,
        t_in_bs: Union[float, npt.ArrayLike],
        posting: float,
        *args,
        **kwargs,
    ):
        """
        Implements a Terrain Observation by Progressive Scans (TOPS) multistatic radar model.

        Parameters
        ----------
        t_in_bs : Union[float, npt.ArrayLike]
            The zero-Doppler time within the burst [s].
        posting : float
            The posting of the data [m]. This is the resolution cell
            spacing of the data which can be different from the
            product resolution due to resampling.
        The rest of the arguments are the same as RadarModel.
        """
        self.t_in_bs = t_in_bs
        self.posting = posting
        super().__init__(*args, **kwargs)
        # Let's overload the NESZ interpolators to make them 2-dimensional
        s1_inc_v = self.s1_nesz.inc_v
        dual_inc_v = self.dual_nesz.inc_v
        ati_inc_v = self.ati_nesz.inc_v
        if not self.degrees:
            s1_inc_v = np.deg2rad(s1_inc_v)
            dual_inc_v = np.deg2rad(dual_inc_v)
            ati_inc_v = np.deg2rad(ati_inc_v)
        self.inc2s1_nesz = RegularGridInterpolator(
            (self.s1_nesz.t_in_burst, s1_inc_v),
            self.s1_nesz.nesz,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )
        self.inc2dual_nesz = RegularGridInterpolator(
            (self.dual_nesz.t_in_burst, dual_inc_v),
            self.dual_nesz.nesz,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )
        self.inc2ati_nesz = RegularGridInterpolator(
            (self.ati_nesz.t_in_burst, ati_inc_v),
            self.ati_nesz.nesz,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )

    def sigma_nrcs(self, nrcs_v):
        """
        Compute SNR driven NRCS uncertainty.

        Parameters
        ----------
        nrcs_v : ndarray
            NRCS values, last dimension should have two or three elements,
            corresonding to the Sentinel-1 and one or two companions.

        Returns
        -------
        ndarray
            NRCS measurement uncertainties, with same dimensions as nrcs_v.
        """
        t_new, inc_new = np.meshgrid(
            self.t_in_bs, self.obs_geo.inc_m, indexing="ij", sparse=True
        )
        nesz_hrmny = 10 ** (self.inc2dual_nesz((t_new, inc_new)) / 10)
        nesz_S1 = 10 ** (self.inc2s1_nesz((t_new, inc_new)) / 10)
        # RegularGridInterpolator always returns an array, so the check on the
        # type of nesz_harmony is no longer needed.
        if (nrcs_v.shape[-1] == 2) and (nrcs_v.ndim <= 3):
            neszs = np.stack((nesz_S1, nesz_hrmny), axis=-1)
        elif (nrcs_v.shape[-1] == 2) and (nrcs_v.ndim == 4):
            # In this case the nrcs has n_az x n_rg x n_sat x pol dimensions, so
            # stack the neszs of S-1 and the companions and add a singleton
            # dimension to broadcast over the polarisations.
            neszs = np.stack((nesz_S1, nesz_hrmny, nesz_hrmny), axis=-1)
            neszs = neszs[..., np.newaxis]
        else:
            neszs = np.stack((nesz_S1, nesz_hrmny, nesz_hrmny), axis=-1)
        snrs = nrcs_v / neszs
        n_looks = self.prod_res**2 / self.az_res / self.grg_res
        alpha_p = np.sqrt(1 / n_looks * ((1 + 1 / snrs) ** 2 + 1 / snrs**2))
        sigma_nrcs = alpha_p * nrcs_v
        return sigma_nrcs
