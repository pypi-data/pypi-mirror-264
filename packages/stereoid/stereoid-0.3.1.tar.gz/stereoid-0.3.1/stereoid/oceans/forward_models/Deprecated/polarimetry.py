__author__ = "Marcel Kleinherenbrink"
__email__ = "M.Kleinherenbrink@tudelft.nl"

def pol_monostatic(s_spec,s_bragg,s_break,pol='V'):
    # s_spec: specular sigma_0 received
    # s_bragg: bragg sigma_0 received
    # s_break: break sigma_0 received
    # pol: polarization transmitted

    # specular reflection
    if pol == 'V':
        VV_spec = s_spec*1.0
        HH_spec = 0.0
    if pol == 'H':
        VV_spec = 0.0
        HH_spec = s_spec * 1.0

    # bragg reflection
    if pol == 'V':
        VV_bragg = s_bragg*1.0
        HH_bragg = 0.0
    if pol == 'H':
        VV_bragg = 0.0
        HH_bragg = s_bragg * 1.0

    # wave breaking reflection
    if pol == 'V':
        VV_break = s_break * 0.5 # check the scaling
        HH_break = s_break * 0.5
    if pol == 'H':
        VV_break = s_break * 0.5  # check the scaling
        HH_break = s_break * 0.5

    return VV_spec,HH_spec,VV_bragg,HH_bragg,VV_break,HH_break


def pol_bistatic(s_spec,s_bragg,s_break,pol='V',theta_t=35,theta_r=40,phi=30):
    # s_spec: specular sigma_0 received
    # s_bragg: bragg sigma_0 received
    # s_break: break sigma_0 received
    # pol: polarization transmitted
    # theta_t: transmitted incidence angle [deg]
    # theta_r: received incidence angle [deg]
    # phi: ground-projected bistatic angle [deg]

    # convert to radians
    theta_t = np.deg2rad(theta_t)
    theta_r = np.deg2rad(theta_r)
    phi = np.deg2rad(phi)

    # specular reflection
    if pol == 'V':
        V_sc=0.5 # replace with rotations
        H_sc=0.5 # replace with rotations
        VV_spec = s_spec * V_sc
        HH_spec = s_spec * H_sc
    if pol == 'H':
        V_sc = 0.5  # replace with rotations
        H_sc = 0.5  # replace with rotations
        VV_spec = s_spec * V_sc
        HH_spec = s_spec * H_sc

    # bragg reflection
    if pol == 'V':
        V_sc = 0.5  # replace with rotations
        H_sc = 0.5  # replace with rotations
        VV_bragg = s_bragg * V_sc
        HH_bragg = s_bragg * H_sc
    if pol == 'H':
        V_sc = 0.5  # replace with rotations
        H_sc = 0.5  # replace with rotations
        VV_bragg = s_bragg * V_sc
        HH_bragg = s_bragg * H_sc

        # wave breaking reflection
        if pol == 'V':
            VV_break = s_break * 0.5  # check the scaling
            HH_break = s_break * 0.5
        if pol == 'H':
            VV_break = s_break * 0.5  # check the scaling
            HH_break = s_break * 0.5

    return VV_spec,HH_spec,VV_bragg,HH_bragg,VV_break,HH_break

if __name__ == '__main__':
    import numpy as np
