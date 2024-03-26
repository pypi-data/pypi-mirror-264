"""Provides tools to do plots, useful for testing.

Ghislain de Labbey
Last updated May 12th 2023
"""

import numpy as np
import matplotlib.pyplot as plt
import bundling_score.bundling_score as bs
from scipy.linalg import norm


def orientation_from_q(qs):
    ''' Get orientation from nematic tensor'''
    nY, nX = qs.shape[:2]
    eigval, eigvects = np.linalg.eig(qs)
    m = eigval.argmax(axis=2)
    u = eigvects[np.arange(nY), np.arange(nX), :, m]
    u = np.zeros((nX, nY, 2))
    rr, cc = np.nonzero(norm(qs, axis=(2, 3)))

    u[rr, cc, 0] = np.sqrt(qs[rr, cc, 0, 0] + 1 / 2)
    u[rr, cc, 1] = np.sqrt(qs[rr, cc, 1, 1] + 1 / 2)

    rr, cc = np.nonzero(qs[..., 0, 1])
    u[rr, cc, 1] *= np.sign(qs[rr, cc, 0, 1])
    return u


def show_steps(image, smax=100, step=20):
    ''' Show all the different calculation steps. '''
    nY, nX = image.shape
    xx = np.array(range(nX))
    yy = np.array(range(nY))
    X, Y = np.meshgrid(xx, yy)

    grad = bs.get_gradient(image)
    qs, Qs = bs.get_nematic_tensor(image)
    u = orientation_from_q(qs)
    corr = bs.compute_correlations(Qs, smax)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(16, 9))
    ax = ax.ravel()
    ax[0].imshow(image, cmap='magma')
    ax[0].set_title('Original')

    ax[1].imshow(image)
    ax[1].quiver(X[::step, ::step],
                 Y[::step, ::step],
                 grad[::step, ::step, 1],
                 grad[::step, ::step, 0],
                 angles='xy',
                 scale_units='xy',
                 scale=4,
                 pivot='middle')
    ax[1].set_title('Gradient')

    ax[2].imshow(image)
    intens = image[::step, ::step] - np.min(image)
    ax[2].quiver(X[::step, ::step],
                 Y[::step, ::step],
                 intens * u[::step, ::step, 1],
                 intens * u[::step, ::step, 0],
                 angles='xy',
                 pivot='middle',
                 scale=4000,
                 headwidth=0,
                 headlength=0,
                 headaxislength=0)
    ax[2].set_title('Arrow-polar vector')

    # nem = ax[5].imshow(corr)

    # ax[5].set_title('Nematic correlations')
    # fig.colorbar(nem)


def show_direction(image, axes=None):
    ''' Show the direction on top of the image. '''
    nY, nX = image.shape
    xx = np.array(range(nX))
    yy = np.array(range(nY))
    X, Y = np.meshgrid(xx, yy)

    qs, _ = bs.get_nematic_tensor(image)
    u = orientation_from_q(qs)
    axes.imshow(image)
    axes.quiver(X, Y, u[..., 0], u[..., 1], u='xy', scale_units='xy')
