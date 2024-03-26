# Copyright (C) 2013 Oskar Maier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Oskar Maier
# version r0.3.0
# since 2013-08-23
# status Release

# Paco Lopez Dekker (f.lopezdekker@tudelft.nl)
# Extended to multi-variate input following Gerig et al. 1992.

# third-party modules
import numpy
from scipy.ndimage.filters import gaussian_filter

# path changes

# own modules
#from .utilities import xminus1d


# code


def anisotropic_diffusion(img, niter=1, kappa=50, gamma=0.1, voxelspacing=None, option=1):
    r"""
    Edge-preserving, XD Anisotropic diffusion.
    Parameters
    ----------
    img : array_like
        Input image (will be cast to numpy.float).
    niter : integer
        Number of iterations.
    kappa : integer
        Conduction coefficient, e.g. 20-100. ``kappa`` controls conduction
        as a function of the gradient. If ``kappa`` is low small intensity
        gradients are able to block conduction and hence diffusion across
        steep edges. A large value reduces the influence of intensity gradients
        on conduction.
    gamma : float
        Controls the speed of diffusion. Pick a value :math:`<= .25` for stability.
    voxelspacing : tuple of floats or array_like
        The distance between adjacent pixels in all img.ndim directions
    option : {1, 2, 3}
        Whether to use the Perona Malik diffusion equation No. 1 or No. 2,
        or Tukey's biweight function.
        Equation 1 favours high contrast edges over low contrast ones, while
        equation 2 favours wide regions over smaller ones. See [1]_ for details.
        Equation 3 preserves sharper boundaries than previous formulations and
        improves the automatic stopping of the diffusion. See [2]_ for details.
    Returns
    -------
    anisotropic_diffusion : ndarray
        Diffused image.
    Notes
    -----
    Original MATLAB code by Peter Kovesi,
    School of Computer Science & Software Engineering,
    The University of Western Australia,
    pk @ csse uwa edu au,
    <http://www.csse.uwa.edu.au>
    Translated to Python and optimised by Alistair Muldal,
    Department of Pharmacology,
    University of Oxford,
    <alistair.muldal@pharm.ox.ac.uk>
    Adapted to arbitrary dimensionality and added to the MedPy library Oskar Maier,
    Institute for Medical Informatics,
    Universitaet Luebeck,
    <oskar.maier@googlemail.com>
    June 2000  original version. -
    March 2002 corrected diffusion eqn No 2. -
    July 2012 translated to Python -
    August 2013 incorporated into MedPy, arbitrary dimensionality -
    References
    ----------
    .. [1] P. Perona and J. Malik.
       Scale-space and edge detection using ansotropic diffusion.
       IEEE Transactions on Pattern Analysis and Machine Intelligence,
       12(7):629-639, July 1990.
    .. [2] M.J. Black, G. Sapiro, D. Marimont, D. Heeger
       Robust anisotropic diffusion.
       IEEE Transactions on Image Processing,
       7(3):421-432, March 1998.
    """
    # define conduction gradients functions
    if option == 1:
        def condgradient(delta, spacing):
            return numpy.exp(-(delta/kappa)**2.)/float(spacing)
    elif option == 2:
        def condgradient(delta, spacing):
            return 1./(1.+(delta/kappa)**2.)/float(spacing)
    elif option == 3:
        kappa_s = kappa * (2**0.5)

        def condgradient(delta, spacing):
            top = 0.5*((1.-(delta/kappa_s)**2.)**2.)/float(spacing)
            return numpy.where(numpy.abs(delta) <= kappa_s, top, 0)

    # initialize output array
    out = numpy.array(img, dtype=numpy.float32, copy=True)

    # set default voxel spacing if not supplied
    if voxelspacing is None:
        voxelspacing = tuple([1.] * img.ndim)

    # initialize some internal variables
    deltas = [numpy.zeros_like(out) for _ in range(out.ndim)]

    for _ in range(niter):

        # calculate the diffs
        for i in range(out.ndim):
            slicer = [slice(None, -1) if j == i else slice(None) for j in range(out.ndim)]
            deltas[i][slicer] = numpy.diff(out, axis=i)

        # update matrices
        matrices = [condgradient(delta, spacing) * delta for delta, spacing in zip(deltas, voxelspacing)]

        # subtract a copy that has been shifted ('Up/North/West' in 3D case) by one
        # pixel. Don't as questions. just do it. trust me.
        for i in range(out.ndim):
            slicer = [slice(1, None) if j == i else slice(None) for j in range(out.ndim)]
            matrices[i][slicer] = numpy.diff(matrices[i], axis=i)

        # update the image
        out += gamma * (numpy.sum(matrices, axis=0))

    return out


def anisotropic_diffusion_mv(data, niter=1, kappa=50, gamma=0.1, voxelspacing=None, option=1,
                             diagdiff=False, gf=None):
    r"""
    Edge-preserving, XD Anisotropic diffusion.
    Parameters
    ----------
    img : array_like
        Input data, we assume last dimension corresponds to multiple variables.
    niter : integer
        Number of iterations.
    kappa : integer
        Conduction coefficient, e.g. 20-100. ``kappa`` controls conduction
        as a function of the gradient. If ``kappa`` is low small intensity
        gradients are able to block conduction and hence diffusion across
        steep edges. A large value reduces the influence of intensity gradients
        on conduction.
    gamma : float
        Controls the speed of diffusion. Pick a value :math:`<= .25` for stability.
    voxelspacing : tuple of floats or array_like
        The distance between adjacent pixels in all img.ndim directions
    option : {1, 2, 3}
        Whether to use the Perona Malik diffusion equation No. 1 or No. 2,
        or Tukey's biweight function.
        Equation 1 favours high contrast edges over low contrast ones, while
        equation 2 favours wide regions over smaller ones. See [1]_ for details.
        Equation 3 preserves sharper boundaries than previous formulations and
        improves the automatic stopping of the diffusion. See [2]_ for details.
    gf: GradientFunction like object to compute gradients in a different way. This
        only works 2D.
    diagdiff: Use also diagonal elements, implemented for 2-D.
    Returns
    -------
    anisotropic_diffusion : ndarray
        Diffused image.
    Notes
    -----
    Original MATLAB code by Peter Kovesi,
    School of Computer Science & Software Engineering,
    The University of Western Australia,
    pk @ csse uwa edu au,
    <http://www.csse.uwa.edu.au>
    Translated to Python and optimised by Alistair Muldal,
    Department of Pharmacology,
    University of Oxford,
    <alistair.muldal@pharm.ox.ac.uk>
    Adapted to arbitrary dimensionality and added to the MedPy library Oskar Maier,
    Institute for Medical Informatics,
    Universitaet Luebeck,
    <oskar.maier@googlemail.com>
    June 2000  original version. -
    March 2002 corrected diffusion eqn No 2. -
    July 2012 translated to Python -
    August 2013 incorporated into MedPy, arbitrary dimensionality -
    April 2021 incorporated to stereoid, adding multi-variate variant [3]
    References
    ----------
    .. [1] P. Perona and J. Malik.
       Scale-space and edge detection using ansotropic diffusion.
       IEEE Transactions on Pattern Analysis and Machine Intelligence,
       12(7):629-639, July 1990.
    .. [2] M.J. Black, G. Sapiro, D. Marimont, D. Heeger
       Robust anisotropic diffusion.
       IEEE Transactions on Image Processing,
       7(3):421-432, March 1998.
       [3] G. Gerig, O. Kubler, R. Kikinis, and F. A. Jolesz,
       “Nonlinear anisotropic filtering of MRI data,”
       IEEE Transactions on Medical Imaging, vol. 11, no. 2, pp. 221–232,
       Jun. 1992, doi: 10.1109/42.141646.

    """
    # define conduction gradients functions
    if option == 1:
        def condgradient(delta_kap2, spacing):
            return numpy.exp(-delta_kap2)/float(spacing)
    elif option == 2:
        def condgradient(delta_kap2, spacing):
            return 1./(1.+delta_kap2)/float(spacing)
    elif option == 3:
        def condgradient(delta_kap2, spacing):
            top = 0.5 * (1. - delta_kap2/2)**2 / float(spacing)
            return numpy.where(delta_kap2 <= 2, top, 0)

    # kappa_s = kappa * (2**0.5)
    #
    # def condgradient(delta, spacing):
    #     top = 0.5*((1.-(delta/kappa_s)**2.)**2.)/float(spacing)
    #     return numpy.where(numpy.abs(delta) <= kappa_s, top, 0)

    # initialize output array
    out = numpy.array(data, dtype=numpy.float32, copy=True)
    # initialize kappa_e
    if isinstance(kappa, (list,  tuple, numpy.ndarray)):
        kappa_e = kappa
    else:
        kappa_e = tuple([kappa] * (data.shape[-1]))
    # set default voxel spacing if not supplied
    if voxelspacing is None:
        voxelspacing = [1.] * (data.ndim - 1)
    if diagdiff:
        voxelspacing_d = [numpy.sqrt(numpy.sum(numpy.array(voxelspacing)**2))] * (data.ndim - 1)
        voxelspacing = voxelspacing + voxelspacing_d
    voxelspacing = tuple(voxelspacing)
    # initialize some internal variables
    # deltas = [[numpy.zeros_like(out) for _ in range(out.ndim - 1)] for vnd in range(out.shape[-1])]
    if diagdiff:
        deltas = numpy.zeros((int((out.ndim - 1)**2),) + out.shape)
        grads = numpy.zeros((int((out.ndim - 1)**2),) + out.shape)
    else:
        deltas = numpy.zeros((out.ndim - 1,) + out.shape)
        grads = numpy.zeros((out.ndim - 1,) + out.shape)
    for _ in range(niter):

        # calculate the diffs
        if diagdiff:
            deltas[0][0:-1, :] = numpy.diff(out, axis=0)
            deltas[1][:, :-1] = numpy.diff(out, axis=1)
            deltas[2][0:-1, 0:-1] = (out[1:,1:] - out[:-1, :-1])
            deltas[3][0:-1, 0:-1] = (out[0:-1, 1:] - out[1:, :-1])
            grads = deltas
        else:
            for i in range(out.ndim - 1):
                slicer = [slice(None, -1) if j == i else slice(None) for j in range(out.ndim)]
                deltas[i][tuple(slicer)] = numpy.diff(out, axis=i)
            if gf is None:
                grads = deltas
            else:
                for vnd in range(out.shape[-1]):
                    grads[0][..., vnd], grads[1][..., vnd] = gf.gradient(out[..., vnd])

        # update matrices
        matrices = []

        for i in range(grads.shape[0]):
            delta_kap2 = 0
            for vnd in range(out.shape[-1]):
                delta_kap2 = delta_kap2 + (grads[i, ..., vnd] / kappa_e[vnd])**2
            condgr = condgradient(delta_kap2, voxelspacing[i])
            matrices.append(condgr[..., numpy.newaxis] * deltas[i])

        # subtract a copy that has been shifted ('Up/North/West' in 3D case) by one
        # pixel. Don't ask questions. just do it. trust me.
        # for i in range(out.ndim - 1):
        #     slicer = [slice(1, None) if j == i else slice(None) for j in range(out.ndim)]
        #     matrices[i][tuple(slicer)] = numpy.diff(matrices[i], axis=i)
        if diagdiff:
            matrices[0][1:, :] = numpy.diff(matrices[0], axis=0)
            matrices[1][:, 1:] = numpy.diff(matrices[1], axis=1)
            matrices[2][1:, 1:] = matrices[2][1:,1:] - matrices[2][:-1, :-1]
            matrices[3][1:, 1:] = matrices[3][0:-1, 1:] - matrices[3][1:, :-1]
        else:
            for i in range(out.ndim - 1):
                slicer = [slice(1, None) if j == i else slice(None) for j in range(out.ndim)]
                matrices[i][tuple(slicer)] = numpy.diff(matrices[i], axis=i)

        # update the image
        out += gamma * (numpy.sum(matrices, axis=0))

    return out


#%%
if __name__ == "__main__":
    dat = numpy.random.rand(1000,1000,3)
    fdat = anisotropic_diffusion_mv(dat, 10, diagdiff=True)
    isinstance(numpy.array([1,2]), (tuple, list, numpy.ndarray))
