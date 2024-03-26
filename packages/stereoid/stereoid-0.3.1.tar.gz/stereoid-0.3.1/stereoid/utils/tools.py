import logging
import sys
import os
from typing import Optional

# Define logger level for debug purposes
logger = logging.getLogger(__name__)



def load_python_file(file_path: str):
    """Load a file and parse it as a Python module."""
    # REVIEW: wouldn't it be better if we used ConfigParser instead?
    if not os.path.exists(file_path):
        raise IOError('File not found: {}'.format(file_path))

    full_path = os.path.abspath(file_path)
    python_filename = os.path.basename(full_path)
    module_name, _ = os.path.splitext(python_filename)
    module_dir = os.path.dirname(full_path)
    if module_dir not in sys.path:
        sys.path.append(module_dir)

    module = __import__(module_name, globals(), locals(), [], 0)
    return module


def progress(n0: int, n1: int, step: Optional[int]=1,
             progress_bar: Optional[bool]=True):
    try:
        from tqdm import tqdm
    except ImportError:
        progress_bar = False
        logger.error('tqdm not available to display progress bar')
    if progress_bar is True:
        progress = tqdm(range(n0, n1, step))
    else:
        progress = range(n0, n1, step)
    return progress


def initialize_parameters(p):
    p.run_id = getattr(p, '', None)
    return None


def print_info_spec(spec_type: str):
    if spec_type == "SWAN_noneq":
        logger.info(
            "Non_equilibrium spectrum from SWAN \n"
            "Local wind used for Kudryavtsev spectrum \n"
            "Transfer functions to alter short waves by currents"
        )
    if spec_type == "Elf_noneq":
        logger.info(
            "Non-equilibrium spectrum from Elfouhaily \n"
            "Non-local wind used for Kudryavtsev spectrum \n"
            "Transfer functions to alter short waves by currents and wind anomalies"
        )
    if spec_type == "LUT":
        logger.info(
            "Non_equilibrium spectrum from Elfouhaily \n"
            "Local wind used for Kudryavtsev spectrum \n"
            "No transfer functions"
        )
