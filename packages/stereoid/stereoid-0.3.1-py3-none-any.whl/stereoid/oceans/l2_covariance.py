"""l2_covariance computes the semi-theoretical L2 covariance matrices of the related to the wind speed and total surface currents in terms of L1 uncertainties.

To arrive to the L2 covariance, we assume a multidimensional GMF relating the wind (or surface stress equivalent wind) to the NRCS for each observation geometry and polarization.
"""

from pathlib import Path

import numpy as np


def pseudo_inverse_h(a):
    """Compute the (Moore-Penrose) pseudo-inverse of a Hermitian matrix.
    It is assumed that a has linearly independent columns. Thus matrix
    A^{*}A is invertible. The pseudo-inverse is computed as
    A^+ = (A^* A)^{-1} A^*.

    Parameters
    ----------
    a : (L, M, N, N) array_like
        Real symmetric or complex hermetian matrix to be pseudo-inverted

    Returns
    -------
    (N, N, M, L) ndarray
        The pseudo-inverse of matrix a.
    """
    # JˆH \cdot J
    # we also transpose while we are at it
    ah_a = np.einsum("jimn,jkmn->mnik", a, a)
    aha_inv = np.linalg.inv(ah_a)
    return np.einsum("mnik,jkmn->mnij", aha_inv, a)


class L2Cov:
    """l2_cov holds the inputs required to compute the L2 covariances matrices and provides methods to compute them.
    """

    def __init__(self, radar_model, inc_master_d, forward_model):
        """Initialise L2Cov. Extract the nrcs and jacobian from the forward_model

        Parameters
        ----------
        radar_model : stereoid.oceans.radar_model.RadarModel
            The radar model for which to compute the covariance matrices. Holds information regarding the geometry and NESZ.

        inc_master_d : float
            Incidence angle of the master satellite. Covariance matrices are computed for this angle. [degree]

        forward_model : stereoid.oceans.forward_model.FwdModel
            The forward model relating the NRCS to wind speeds.
        """
        self.radar_model = radar_model
        self.inc_master_d = inc_master_d
        self.fwdm = forward_model
        self.jacobian = self.fwdm.fwd_jacobian(self.inc_master_d)[0]
        self.nrcs = self.fwdm.nrcs_lut(0, cart=True)

    def cov_wind_noise(self, nrcs=None, jacobian=None):
        """Compute the covariance matrix of the measurement noise.

        Parameters
        ----------
        nrcs : (3, N, N) ndarray
            NRCS for the 3 systems (master and 2 companions) at N*N wind velocity components

        jacobian : (3, 2, N, N) ndarray
            jacobian of NRCS with respect to wind velocity.

        Returns
        -------
        (N, N, 2, 2) ndarray
            2 by 2 covariance matrix of the two wind velocity components for the N*N different combinations of wind velocity
        """
        if nrcs is None:
            nrcs = np.transpose(self.nrcs, axes=(1, 2, 0))
        if jacobian is None:
            jacobian = self.jacobian
        variance_nrcs = np.square(self.radar_model.sig1ma_nrcs(nrcs))
        cov_s = np.zeros((jacobian.shape[2], jacobian.shape[3], jacobian.shape[0], jacobian.shape[0]))
        # assign the variances to the diagonal of the jacobian.shape[2] * jacobian.shape[3] cov_s matrices
        np.einsum('ijkk->ijk', cov_s)[...] = variance_nrcs
        j_pi = pseudo_inverse_h(jacobian)
        return np.einsum("mnik,mnkj,mnlj->mnil", j_pi, cov_s, j_pi)

    def cov_wind_geo(self, nrcs=None, jacobian=None):
        """Compute the covariance matrix of the geophysical noise.

        Parameters
        ----------
        nrcs : (3, N, N) ndarray
            NRCS for the 3 systems (master and 2 companions) at N*N wind velocity components

        jacobian : (3, 2, N, N) ndarray
            jacobian of NRCS with respect to wind velocity.

        Returns
        -------
        (N, N, 2, 2) ndarray
            2 by 2 covariance matrix of the two wind velocity components for the N*N different combinations of wind velocity
        """
        if nrcs is None:
            nrcs = self.nrcs
        if jacobian is None:
            jacobian = self.jacobian
        cov_g = np.zeros((jacobian.shape[2], jacobian.shape[3], jacobian.shape[0], jacobian.shape[0]))
        for ind in range(3):
            cov_g[:, :, ind, ind] = nrcs[ind]**2
        alpha_a = np.radians(self.radar_model.obs_geo.bist_ang / 2)
        cov_g[:, :, 0, 1] = nrcs[0] * nrcs[1] * np.cos(alpha_a)
        cov_g[:, :, 1, 0] = cov_g[:, :, 0, 1]
        cov_g[:, :, 0, 2] = nrcs[0] * nrcs[2] * np.cos(alpha_a)
        cov_g[:, :, 2, 0] = cov_g[:, :, 0, 2]
        cov_g[:, :, 1, 2] = nrcs[1] * nrcs[2] * np.cos(2*alpha_a)
        cov_g[:, :, 2, 1] = cov_g[:, :, 1, 2]
        u_u = self.fwdm.w_u
        u_v = self.fwdm.w_v
        u_mag = np.sqrt(u_v[:, np.newaxis] ** 2 + u_u ** 2)
        k_g = 0.06 * np.exp(-u_mag/12)
        cov_g = k_g.reshape(u_mag.shape + (1, 1))**2 * cov_g
        j_pi = pseudo_inverse_h(jacobian)
        return np.einsum("mnik,mnkj,mnlj->mnil", j_pi, cov_g, j_pi)

    def polar_cov_w(self):
        u_phi = np.arctan2(self.u_v, self.u_u)
        j_p2c = np.zeros(self.u_mag.shape + (2, 2))
        j_p2c[:, :, 0, 0] = np.cos(u_phi)
        j_p2c[:, :, 0, 1] = -1 * self.u_mag * np.sin(u_phi)
        j_p2c[:, :, 1, 0] = np.sin(u_phi)
        j_p2c[:, :, 1, 1] = self.u_mag * np.cos(u_phi)
        j_c2p = np.linalg.inv(j_p2c)
        cartesian_cov_w = cartesian_cov_w()
        return np.einsum("mnik,mnkj,mnlj->mnil", j_c2p, cartesian_cov_w, j_c2p)
