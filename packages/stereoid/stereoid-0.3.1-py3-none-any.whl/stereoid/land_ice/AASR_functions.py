import numpy as np
import os

from drama.io import cfg
from drama.performance.sar import calc_aasr, calc_nesz, RASR, RASRdata, pattern, AASRdata, NESZdata, SARModeFromCfg
from drama.performance.sar.azimuth_performance import mode_from_conf
from rippl.resample_regular2irregular import Regular2irregular

def calculate_ambiguity_location(range_t, PRF, v_sat, wavelength=0.05564, amb_nos=None):
    """
    Calculate the location of the ambiguities in range and azimuth

    We assume that the speed of the satellite is more or less the same everywhere.

    :return:
    """

    if amb_nos == None:
        amb_nos = [1, 2]

    c = 299792458
    R0 = range_t * c

    az_distance = np.array(amb_nos)[:, None] * (wavelength * PRF * R0[None, :]) / (2 * v_sat)
    ra_distance = np.sqrt(R0[None, :]**2 + az_distance**2) - R0

    return az_distance, ra_distance


def get_max_gain_ambiguities(Namb):
    """
    Get the maximal gain from the ambiguities.

    :return:
    """

    # General setup
    main_dir = os.path.expanduser("~/surfdrive/TU_Delft/STEREOID/Data")
    rxname = 'airbus_dual_rx'
    txname = 'sentinel'
    is_bistatic = True
    runid = '2019_2'
    pardir = os.path.join(main_dir, 'PAR')
    pltdirr = os.path.join(os.path.join(os.path.join(main_dir, 'RESULTS'), 'Activation'), runid)
    parfile = os.path.join(pardir, ('Harmony_test.cfg'))
    conf = cfg.ConfigFile(parfile)
    mode = "IWS"
    Nswth = 3

    inclination_angles = np.linspace(15, 50, 351)

    # First calculate antenna patterns for aasr
    aasrs = []
    for swth in range(Nswth):
        aasr_ = calc_aasr(conf, mode, swth,
                          txname='sentinel',
                          rxname=rxname,
                          savedirr='',
                          t_in_bs=None,
                          n_az_pts=3,
                          view_patterns=False,
                          plot_patterns=False,
                          plot_AASR=False,
                          Tanalysis=20,
                          # vmin=-25.0, vmax=-15.0,
                          az_sampling=100, Namb=Namb,
                          bistatic=is_bistatic)
        aasrs.append(aasr_)

    aasr_values = np.zeros((Namb, len(inclination_angles)))

    # Sample for 0.1 degrees in inclination angle.
    for i_a in np.fliplr(range(Namb)):
        for aasr in aasrs:
            aasr_vals = np.max(aasr.aasr_par[:, :, i_a])
            aasr_values[i_a, :] = np.maximum(np.interp(inclination_angles, aasr.inc_v, aasr_vals, left=0, right=0), aasr_values[i_a, :])

    return aasr_values

def calc_RCMC(R0, PRF, v_sat, wavelength=0.5564, integration_time=0.5, squints=45, squint=False, az_freq, t_freq):
    """
    Calculate the range iso lines where the ambiguities are located on

    :return:
    """

    # Speed of light
    c = 299999000  # m/s

    # Calculate linear FM (Frequency Modulation??) rate
    Ka = (2 * v_sat**2) / (wavelength * R0)

    # Create a vector for intergration time
    no_samples = 100
    t_vec = np.arange(-no_samples / 2, no_samples / 2 + 1) * (integration_time / 2)

    # Squint angle
    if squint:
        # If there is a squint used
        squints = squints
    else:
        squints = np.zeros(no_samples)

    # TODO Beam center offset time?? (most likely the offset in range of the middle of the swath)
    t_off = 1

    # Calc range history
    range_history = R0 + (v_sat**2 * t_off) / R0 * (t_vec - t_off) + 0.5 * (v_sat**2 * (np.cos(squints))**2) / R0 * (t_vec - t_off)

    # range history in frequency domain
    range_history_f = R0 + v_sat**2 / (2 * R0) * (az_freq / Ka)**2

    # RCMC
    delta_R = (wavelength**2 * R0 * az_freq**2) / (8 * v_sat**2)

    # RCMC compensation
    p_rcmc = np.exp(np.i * (4 * np.pi * t_freq * delta_R) / c)

    return p_rcmc, range_history

def create_ambiguity_filters_gaussian(spread=3, N_amb=2, kernel_size=[5, 5]):
    """
    Create a filter based on a gaussian in range and azimuth.

    :param spread: How many pixels the gaussian is spread.

    :return:
    """

    kernel_size = np.array(kernel_size) + np.array([2, 2])
    az_values = np.arange(np.ceil(-kernel_size[0] / 2), np.ceil(kernel_size[0] / 2))
    ra_values = np.arange(np.ceil(-kernel_size[1] / 2), np.ceil(kernel_size[1] / 2))

    for n in range(N_amb):



    return gaussian_filters

def get_ambiguity_filter():
    """
    Create a filter for the ambiguities based on inverse processing:
    This step will do:

    First using the correct settings:
    - An FFT of a point target
    - Inverse azimuth compression
    - Inverse range migration
    Then:
    - Range migration using wrong location (ambiguity instead of real location)
    - Azimuth compression
    - IFFT to get final output

    :return:
    """


    pass


def get_ambiguity_gain(incidence_angle, swath_no=1, ):
    """
    Using settings for ATI/XTI mode we calculate the gain for the ambiguity.
    This is mainly done based on the drama toolbox.

    If needed the location in the burst is defined. If not we take the center of the burst as in input.
    Incidence angle should be given always.

    :return:
    """




def burst_ambiguity_interpolator():
    """
    This interpolator calculates the ambiguities for a burst
    This does include:
    - Change in gain pattern at the low or high range values
    - Change in gain pattern and ambiguity location due to the shape of the bursts
    - Change in squint angle due change in range and incidence angle
    - Change in R0 over range

    :return:
    """

    pass

def image_ambiguity_interpolator():
    """
    This interpolator only takes the change in incidence angle into account.
    This means that we disregard:
    - The changing gain pattern to the range edges of the burst
    - The differences due to the steering angle of the satellite

    It does take into account:
    - Change R0 for different incidence angles
    - Change in squint angle for different incidence angles

    :return:
    """

    pass

def calculate_burst_ambiguity_values(burst, burst_before, burst_after):
    """
    Calculate the ambiguity values, without the original values of a burst. To do so the burst before and after the
    original one are needed.

    :return:
    """

    pass

def calculate_image_ambiguity_values(image):
    """
    Calculate the ambiguities of a full image. Because this is not done burstwise we do not account for changes in
    steering angle of los of gain at the burst edges, which will give a small error in the final result.

    :return:
    """

    pass
