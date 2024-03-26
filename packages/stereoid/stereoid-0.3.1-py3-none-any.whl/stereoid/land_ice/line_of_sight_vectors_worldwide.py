
import numpy as np
import matplotlib.pyplot as plt
import cartopy
from scipy import sparse
import os
import pickle

import stereoid.utils.config as st_config
from drama.performance.sar import SARModeFromCfg
from drama.io import cfg
from drama.mission.timeline import LatLonTimeline


class LOSVectors():

    def __init__(self):
        # Set up radar parameters
        # Change the second parameter of `SARModeFromCfg` to the acquisition mode of interest: `"EW"`, `"WM"`, `"stripmap"`.

        config = st_config.parse()
        run_id = "2020_1"
        self.par_file = config["par"] / f"Hrmny_{run_id}.cfg"
        self.mode = SARModeFromCfg(cfg.ConfigFile(self.par_file), "IWS")

    def interpolate_satellite_orbits(self, min_lat=-90, max_lat=85, orbit_resolution=0.05):
        """
        Apply the actual interpolation of the orbits.

        :return:
        """

        lon_repeat_cycle = 360 / 175

        # Start with 0.1 degrees for a repeat cycle.
        self.latitudes = np.linspace(min_lat, max_lat, 1751)
        self.longitudes = np.linspace(0, lon_repeat_cycle * 5, 101)[:-1]

        lat_grid, lon_grid = np.meshgrid(self.latitudes, self.longitudes)
        self.lats = np.ravel(lat_grid)
        self.lons = np.ravel(lon_grid) - 180

        timeline = LatLonTimeline(par_file=self.par_file, lats=self.lats, lons=self.lons,
                                  inc_angle_range=(self.mode.incs[0, 0], self.mode.incs[-1, 1]),
                                  dlat=orbit_resolution, dlon=orbit_resolution)
        asc_acqs, dsc_acqs = timeline.compute_timeline()
        self.inc_asc = [np.rad2deg(acq.theta_i) for acq in asc_acqs]
        self.inc_dsc = [np.rad2deg(acq.theta_i) for acq in dsc_acqs]
        self.inc_tot = [np.rad2deg(np.concatenate((acq_asc.theta_i, acq_desc.theta_i))) for (acq_asc, acq_desc) in
                   zip(asc_acqs, dsc_acqs)]

        # northing points on ground
        self.northing_asc = [np.rad2deg(acq.northing) for acq in asc_acqs]
        self.northing_dsc = [np.rad2deg(acq.northing) for acq in dsc_acqs]
        self.northing_tot = [np.rad2deg(np.concatenate((acq_asc.northing, acq_desc.northing))) for (acq_asc, acq_desc) in
                        zip(asc_acqs, dsc_acqs)]

    def get_los_vectors(self, sat_dist=250000):
        """
        Calculate the LOS vectors for both the 3D velocities as the penetration depth estimation.

        :return:
        """

        flatten = lambda l: [item for sublist in l for item in sublist]

        # Incidence angles
        flat_inc_asc = np.array(flatten(self.inc_asc))
        flat_inc_dsc = np.array(flatten(self.inc_dsc))
        flat_inc_tot = np.array(flatten(self.inc_tot))

        # northing points on ground
        flat_northing_asc = np.array(flatten(self.northing_asc)) - 90
        flat_northing_dsc = np.array(flatten(self.northing_dsc)) + 90

        shape = (len(self.longitudes), len(self.latitudes))
        self.no_aq_asc = np.array([len(dat) for dat in self.inc_asc]).reshape(shape).transpose()
        self.no_aq_dsc = np.array([len(dat) for dat in self.inc_dsc]).reshape(shape).transpose()

        loc_ids_asc = []
        seq_ids_asc = []
        for i, inc in enumerate(self.inc_asc):
            loc_ids_asc.extend([i for n in range(len(inc))])
            seq_ids_asc.extend(list(range(len(inc))))
        loc_ids_dsc = []
        seq_ids_dsc = []
        for i, inc in enumerate(self.inc_dsc):
            loc_ids_dsc.extend([i for n in range(len(inc))])
            seq_ids_dsc.extend(list(range(len(inc))))
        loc_ids_tot = []
        seq_ids_tot = []
        for i, inc in enumerate(self.inc_tot):
            loc_ids_tot.extend([i for n in range(len(inc))])
            seq_ids_tot.extend(list(range(len(inc))))

        h = 693000  # Height of satellite

        # Calculate the range for Sentinel-1 and Harmony
        R_asc = h / np.sin(np.deg2rad(90 - flat_inc_asc))
        R_dsc = h / np.sin(np.deg2rad(90 - flat_inc_dsc))
        R_tot = h / np.sin(np.deg2rad(90 - flat_inc_tot))
        R_h_asc = np.sqrt(R_asc ** 2 + sat_dist ** 2)
        R_h_dsc = np.sqrt(R_dsc ** 2 + sat_dist ** 2)
        R_h_tot = np.sqrt(R_tot ** 2 + sat_dist ** 2)
        R_h_ground_asc = np.sqrt(R_h_asc ** 2 - h ** 2)
        R_h_ground_dsc = np.sqrt(R_h_dsc ** 2 - h ** 2)

        # Calculate the new incidence angle for harmony
        inc_h_asc = 90 - np.rad2deg(np.arcsin(h / R_h_asc))
        inc_h_dsc = 90 - np.rad2deg(np.arcsin(h / R_h_dsc))
        inc_h_tot = 90 - np.rad2deg(np.arcsin(h / R_h_tot))

        # Calculate the northing of the Harmony satellite points
        northing_h_asc_front = flat_northing_asc + np.rad2deg(np.arctan(sat_dist / R_h_ground_asc))
        northing_h_dsc_front = flat_northing_dsc - np.rad2deg(np.arctan(sat_dist / R_h_ground_dsc))
        northing_h_asc_back = flat_northing_asc + np.rad2deg(np.arctan(sat_dist / R_h_ground_asc))
        northing_h_dsc_back = flat_northing_dsc - np.rad2deg(np.arctan(sat_dist / R_h_ground_dsc))

        # Calculate the normal vector using [North-South, West-East, vertical] as a reference grid.
        s1_vector_asc_flat = np.swapaxes(
            np.array([[np.cos(np.deg2rad(flat_northing_asc)) * np.cos(np.deg2rad(flat_inc_asc))],
                      [np.sin(np.deg2rad(flat_northing_asc)) * np.cos(np.deg2rad(flat_inc_asc))],
                      [np.sin(np.deg2rad(flat_inc_asc))]]), 0, 2)
        s1_vector_dsc_flat = np.swapaxes(
            np.array([[np.cos(np.deg2rad(flat_northing_dsc)) * np.cos(np.deg2rad(flat_inc_dsc))],
                      [np.sin(np.deg2rad(flat_northing_dsc)) * np.cos(np.deg2rad(flat_inc_dsc))],
                      [np.sin(np.deg2rad(flat_inc_dsc))]]), 0, 2)
        h_vector_asc_back_flat = np.swapaxes(
            np.array([[np.cos(np.deg2rad(northing_h_asc_back)) * np.cos(np.deg2rad(inc_h_asc))],
                      [np.sin(np.deg2rad(northing_h_asc_back)) * np.cos(np.deg2rad(inc_h_asc))],
                      [np.sin(np.deg2rad(inc_h_asc))]]), 0, 2)
        h_vector_dsc_back_flat = np.swapaxes(
            np.array([[np.cos(np.deg2rad(northing_h_dsc_back)) * np.cos(np.deg2rad(inc_h_dsc))],
                      [np.sin(np.deg2rad(northing_h_dsc_back)) * np.cos(np.deg2rad(inc_h_dsc))],
                      [np.sin(np.deg2rad(inc_h_dsc))]]), 0, 2)
        h_vector_asc_front_flat = np.swapaxes(
            np.array([[np.cos(np.deg2rad(northing_h_asc_front)) * np.cos(np.deg2rad(inc_h_asc))],
                      [np.sin(np.deg2rad(northing_h_asc_front)) * np.cos(np.deg2rad(inc_h_asc))],
                      [np.sin(np.deg2rad(inc_h_asc))]]), 0, 2)
        h_vector_dsc_front_flat = np.swapaxes(
            np.array([[np.cos(np.deg2rad(northing_h_dsc_front)) * np.cos(np.deg2rad(inc_h_dsc))],
                      [np.sin(np.deg2rad(northing_h_dsc_front)) * np.cos(np.deg2rad(inc_h_dsc))],
                      [np.sin(np.deg2rad(inc_h_dsc))]]), 0, 2)

        # Select the max/min incidence angles for every point.
        # Create sparse matrix
        row_size = np.max(seq_ids_tot) + 1
        inc_h_matrix = np.zeros((len(self.lats), row_size))
        inc_h_matrix[loc_ids_tot, seq_ids_tot] = inc_h_tot
        inc_matrix = np.zeros((len(self.lats), row_size))
        inc_matrix[loc_ids_tot, seq_ids_tot] = flat_inc_tot
        sorted_id = np.argsort(inc_h_matrix, axis=1)
        sorted_data = np.sort(inc_h_matrix, axis=1)
        first_non_zero = np.argmax(sorted_data != 0, axis=1)
        ids_inc = np.concatenate((first_non_zero[:, None], first_non_zero[:, None] + 1,
                                  np.ones(first_non_zero.shape)[:, None] * (row_size - 2),
                                  np.ones(first_non_zero.shape)[:, None] * (row_size - 1)), axis=1).astype(np.int64) + \
                  np.tile(np.arange(len(self.lats))[:, None], (1, 4)) * row_size
        # If the index from one of the first arrays is the same as one of the last, this value is not valid
        valid_1 = (ids_inc[:, 0] < ids_inc[:, 2]) * (ids_inc[:, 0] < ids_inc[:, 3]) == False
        valid_2 = (ids_inc[:, 1] < ids_inc[:, 2]) * (ids_inc[:, 1] < ids_inc[:, 3]) == False
        id_matrix = sorted_id.ravel()[ids_inc.ravel()].reshape((len(self.lats), 4)) + \
                    np.tile(np.arange(len(self.lats))[:, None], (1, 4)) * row_size

        ids_inc[valid_1, 0] = 0
        ids_inc[valid_2, 1] = 0
        id_matrix[valid_1, 0] = 0
        id_matrix[valid_2, 1] = 0

        # Those are the 4 different inclination angles we can use of every pixel used for penetration depth estimation.
        self.inc_h_values = sorted_data.ravel()[ids_inc]
        self.inc_values = inc_matrix.ravel()[id_matrix]

        # Select the most diverse vectors
        # Procedure is more or less the same
        asc_ids = np.zeros((len(self.lats), 2)).astype(np.int32)
        dsc_ids = np.zeros((len(self.lats), 2)).astype(np.int32)

        for ids, inc, loc_ids, seq_ids in zip([asc_ids, dsc_ids], [flat_inc_asc, flat_inc_dsc],
                                              [loc_ids_asc, loc_ids_dsc], [seq_ids_asc, seq_ids_dsc]):
            # Reorder incidence angles
            row_size = np.maximum(np.max(seq_ids_asc), np.max(seq_ids_dsc)) + 1
            inc_matrix = np.zeros((len(self.lats), row_size))
            inc_matrix[loc_ids, seq_ids] = inc
            sorted_id = np.argsort(inc_matrix, axis=1)
            sorted_data = np.sort(inc_matrix, axis=1)
            first_non_zero = np.argmax(sorted_data != 0, axis=1)

            ids[:, 0] = sorted_id[np.arange(len(self.lats)), first_non_zero]
            ids[:, 1] = sorted_id[np.arange(len(self.lats)), -1]

        # The vectors used to estimate 3D movement over the ice in Antarctica.
        self.h_vector_front = np.zeros((len(self.lats), 4, 3))
        self.h_vector_front[:, 0, :] = h_vector_asc_front_flat[asc_ids[:, 0], 0, :]
        self.h_vector_front[:, 1, :] = h_vector_asc_front_flat[asc_ids[:, 1], 0, :]
        self.h_vector_front[:, 2, :] = h_vector_dsc_front_flat[dsc_ids[:, 0], 0, :]
        self.h_vector_front[:, 3, :] = h_vector_dsc_front_flat[dsc_ids[:, 1], 0, :]

        self.h_vector_back = np.zeros((len(self.lats), 4, 3))
        self.h_vector_back[:, 0, :] = h_vector_asc_back_flat[asc_ids[:, 0], 0, :]
        self.h_vector_back[:, 1, :] = h_vector_asc_back_flat[asc_ids[:, 1], 0, :]
        self.h_vector_back[:, 2, :] = h_vector_dsc_back_flat[dsc_ids[:, 0], 0, :]
        self.h_vector_back[:, 3, :] = h_vector_dsc_back_flat[dsc_ids[:, 1], 0, :]

        self.s1_vector = np.zeros((len(self.lats), 4, 3))
        self.s1_vector[:, 0, :] = s1_vector_asc_flat[asc_ids[:, 0], 0, :]
        self.s1_vector[:, 1, :] = s1_vector_asc_flat[asc_ids[:, 1], 0, :]
        self.s1_vector[:, 2, :] = s1_vector_dsc_flat[dsc_ids[:, 0], 0, :]
        self.s1_vector[:, 3, :] = s1_vector_dsc_flat[dsc_ids[:, 1], 0, :]

    def save_orbit_vectors(self, los_file):

        incs = [self.inc_asc, self.inc_dsc, self.inc_tot]
        northings = [self.northing_asc, self.northing_dsc, self.northing_tot]

        with open(los_file, 'wb') as data_file:
            pickle.dump([incs, northings, self.latitudes, self.longitudes, self.lats, self.lons], data_file)

    def load_orbit_vectors(self, los_file):

        if os.path.exists(los_file):
            with open(los_file, 'rb') as data_file:
                [incs, northings, self.latitudes, self.longitudes, self.lats, self.lons] = pickle.load(data_file)

            [self.inc_asc, self.inc_dsc, self.inc_tot] = incs
            [self.northing_asc, self.northing_dsc, self.northing_tot] = northings

            # After loading these values calculate the actual vectors.
            self.get_los_vectors()

            return True

        else:
            return False
