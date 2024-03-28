"""Provides tools to perform the nematic analysis.

!!! Caution !!!
The bundling score is in px^2, it has to be multiplied by the square of the
spatial resolution to get um^2.

Ghislain de Labbey
Last updated February 29th 2024
"""

import numpy as np

from scipy import ndimage
from scipy.signal import fftconvolve


def get_gradient(image):
    ''' Computes the gradient. '''
    nY, nX = image.shape
    # Gradient kernels
    kx = np.array([[0, 0, 0], [1, 0, -1], [0, 0, 0]])
    ky = np.array([[0, 1, 0], [0, 0, 0], [0, -1, 0]])

    # Convolve to get gradient
    x_grad = ndimage.convolve(image, kx)
    x_grad = x_grad.astype(float)
    y_grad = ndimage.convolve(image, ky)
    y_grad = y_grad.astype(float)

    grad = np.zeros((nY, nX, 2))
    grad[..., 1] = x_grad
    grad[..., 0] = y_grad
    return grad


def get_nematic_tensor(image):
    '''Compute the nematic tensor.

    See notes for mathematical definition of Q.'''
    grad = get_gradient(image)
    grad_norm = np.linalg.norm(grad, axis=2)
    qs = 1 / 2 * np.eye(2)[None, None, :, :] * grad_norm[:, :, None,
                                                         None]**2 - np.einsum(
                                                             'ijk,ijl->ijkl',
                                                             grad, grad)

    # Normalize by intensity, not gradient
    rr, cc = np.nonzero(grad_norm)
    qs[rr, cc, ...] /= grad_norm[rr, cc, None, None]**2
    Qs = np.zeros_like(qs)
    Qs[rr, cc, ...] = qs[rr, cc, ...] * image[rr, cc, None, None]

    return qs, Qs


def compute_correlations(Qs, smax):
    ''' Spatial correlations are convolution with itself reversed.

    The second argument is cropped to avoid padding.
    Uses fftconvolve because way faster if fft-based. '''
    nY, nX = Qs.shape[:2]
    corr = [[
        fftconvolve(Qs[::-1, ::-1, i, j],
                    Qs[smax:nY - smax, smax:nX - smax, i, j],
                    mode='valid') for i in range(2)
    ] for j in range(2)]
    corr = np.array(corr)

    # Sum over xx, xy, yx, yy components
    corr = np.sum(corr, axis=(0, 1))
    return corr / np.max(corr)


def compute_score(image, smax=100, normalization='none'):
    ''' Compute the bundling score

    !!! Caution !!!
    The bundling score is in px^2, it has to be multiplied by the square of the
    spatial resolution to get um^2.'''
    image = image.astype(float)
    nY, nX = image.shape
    if smax > min(nX, nY) // 2 - 1:
        smax = min(nX, nY) // 2 - 1
        print("Warning: maximal s changed to " + str(smax))

    if normalization == 'intensity':
        _, Qs = get_nematic_tensor(image)
    elif normalization == 'none':
        Qs, _ = get_nematic_tensor(image)
    else:
        print("Unknown normalization, switching to intensity")
        Qs, _ = get_nematic_tensor(image)
    corr = compute_correlations(Qs, smax)
    return np.trapz(np.trapz(corr, axis=0)) / np.max(corr)
