"""
Copyright (C) 2022 OceanDataLab
author: Lucile Gaultier
"""

import sys
import argparse
import logging
import pickle
from pathlib import Path

import numpy as np
from drama.geo import QuickRadarGeometry

import stereoid.utils.tools as tools
import stereoid.oceans.run_scenario as run_scenario
import stereoid.oceans.tools.write_tools as write_tools


def setup_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('params_file', nargs='?', type=str, default=None,
                        help='Path of the parameters file')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Display debug log messages')
    return parser


def partition_swan():
    """
    Partitions the output of the SWAN model into a smaller dataset.

    The output of swan can be large, in the order of GB. Partitioning it, and
    saving the smaller partitioned dataset into netCDF format can be useful as
    it allows the creation of smaller test cases.
    """
    main_logger = logging.getLogger()
    main_logger.handlers = []
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)

    parser = setup_arg_parser()
    parser.add_argument('--partition', action='store_true', default=False,
                        help='Partition the SWAN dataset according to the sizeaz and sizer parameters of the parameter file. If this flag is not set the entire SWAN dataset is read in memory and saved to disk as a netCDF file.')
    args = parser.parse_args()
    if args.params_file is None:
        main_logger.error('Please specify a parameter file')
        sys.exit(1)
    if args.debug is True:
        main_logger.setLevel(logging.DEBUG)

    file_param = args.params_file
    p = tools.load_python_file(file_param)

    # Read model Data and SWAN spectra

    try:
        run_scenario.run_partition_swan(p, args.partition)
    except KeyboardInterrupt:
        main_logger.error('\nInterrupted by user (Ctrl+C)')
        sys.exit(1)
    sys.exit(0)


def run_harmony_fwd():
    """
    Run the scientific workbench for Harmony.
    """
    main_logger = logging.getLogger()
    main_logger.handlers = []
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)

    parser = setup_arg_parser()
    args = parser.parse_args()
    if args.params_file is None:
        main_logger.error('Please specify a parameter file')
        sys.exit(1)
    if args.debug is True:
        main_logger.setLevel(logging.DEBUG)

    file_param = args.params_file
    p = tools.load_python_file(file_param)
    try:
        run_scenario.run_stereoid_fwd(p)  # , args.die_on_error)
    except KeyboardInterrupt:
        main_logger.error('\nInterrupted by user (Ctrl+C)')
        sys.exit(1)
    sys.exit(0)


def compute_lut():
    """
    Run the scientific workbench for Harmony.
    """
    main_logger = logging.getLogger()
    main_logger.handlers = []
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)

    parser = setup_arg_parser()
    args = parser.parse_args()
    if args.params_file is None:
        main_logger.error('Please specify a parameter file')
        sys.exit(1)
    if args.debug is True:
        main_logger.setLevel(logging.DEBUG)

    file_param = args.params_file
    p = tools.load_python_file(file_param)
    try:
        run_scenario.compute_lut(p)  # , args.die_on_error)
    except KeyboardInterrupt:
        main_logger.error('\nInterrupted by user (Ctrl+C)')
        sys.exit(1)
    sys.exit(0)


def run_harmony_inv():
    """
    Run the scientific workbench for Harmony.
    """
    main_logger = logging.getLogger()
    main_logger.handlers = []
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)

    parser = setup_arg_parser()
    args = parser.parse_args()
    if args.params_file is None:
        main_logger.error('Please specify a parameter file')
        sys.exit(1)
    if args.debug is True:
        main_logger.setLevel(logging.DEBUG)

    file_param = args.params_file
    p = tools.load_python_file(file_param)
    try:
        run_scenario.run_inversion(p)  # , args.die_on_error)
    except KeyboardInterrupt:
        main_logger.error('\nInterrupted by user (Ctrl+C)')
        sys.exit(1)
    sys.exit(0)


def convert_to_netcdf():
    """
    Convert the pickled output of the scientific workbench to NETCDF format.
    """
    main_logger = logging.getLogger()
    main_logger.handlers = []
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, default=None,
                        help='Path of the pickled file')
    parser.add_argument('params_file', nargs='?', type=str, default=None,
                        help='Path of the parameters file')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Display debug log messages')
    args = parser.parse_args()
    if args.input_file is None:
        main_logger.error('Please specify a pickle file')
        sys.exit(1)
    if args.debug is True:
        main_logger.setLevel(logging.DEBUG)
    input_path = Path(args.input_file).expanduser()
    if args.params_file:
        p = tools.load_python_file(args.params_file)
        run_scenario.make_default(p)
        run_scenario.make_default_fwd(p)
        output_path = f"{p.obs_file}.nc"
    else:
        p = None
        output_path = input_path.with_suffix(".nc")
    with open(input_path, "rb") as f:
        result = pickle.load(f)
        qgeo = QuickRadarGeometry(693E3, degrees=False)
        gr_v = qgeo.inc_to_gr(result["inc_m"])
        dic_geometry = {"inc": np.stack((result["inc_m"][0],
                                         result["inc_b_c"][0],
                                         result["inc_b_d"][0]), axis=-1),
                    "bist_ang": np.stack((np.zeros_like(result["bist_ang_c"][0]),
                                          result["bist_ang_c"][0],
                                          result["bist_ang_d"][0]), axis=-1),
                    "grg": gr_v[0],
                    "az": np.arange(0, result["model"]["sst"].shape[0], 1) *result["model"]["dy"],
                    }
        # The old pickled output have dimensions called "lon" and "lat" but
        # save_scene expects "longitude" and "latitude"
        vars_to_rename = {"lon": "longitude", "lat": "latitude"}
        for key in vars_to_rename:
            if key in result["model"]:
                result["model"][vars_to_rename[key]] = result["model"].pop(key)
        if "sar" in input_path.name:
            for key in dic_geometry:
                dic_geometry[key] = dic_geometry[key][::p.spec_samp[1]]
            if result["model"]["latitude"].shape != result["imacs"]["HA"]["M"].shape:
                for item in vars_to_rename.items():
                    result["model"][item] = result["model"][item][::p.spec_samp[0], ::p.spec_samp[1]]
            result |= dic_geometry
            write_tools.save_scene(output_path, ("imacs", "cut_off"), result, global_attr=p)
        else:
            result |= dic_geometry
            write_tools.save_scene(output_path, ("nrcs", "dop"), result, global_attr=p)
    sys.exit(0)
