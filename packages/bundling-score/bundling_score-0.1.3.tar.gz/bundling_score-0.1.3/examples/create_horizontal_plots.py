''' Several simple examples of images and bundling scores '''

import matplotlib.pyplot as plt
import numpy as np

import bundling_score.bundling_score as bs
import bundling_score.plots as bp

from skimage.filters import gaussian
from scipy.linalg import norm
from skimage.io import imread
from skimage.color import rgb2gray

plt.ion()
plt.close('all')

# Size of the image
N = 10
# Limit value for rx and ry, avoids padding
smax = 20
# Simple line
image = np.zeros((N, N))
image[N // 2, :] = 1
image[:, N // 2] = 1
image = gaussian(image, .5)

qs, Qs = bs.get_nematic_tensor(image)
grad = bs.get_gradient(image)
norm_grad = norm(grad, axis=2)
rr, cc = np.nonzero(norm_grad)
grad[rr, cc, :] /= norm_grad[rr, cc, None]
u = bp.orientation_from_q(qs)

nY, nX = image.shape
xx = np.array(range(nX))
yy = np.array(range(nY))
X, Y = np.meshgrid(xx, yy)

plt.subplot(131)
plt.imshow(image, cmap='gray')
plt.quiver(X,
           Y,
           grad[..., 1],
           grad[..., 0],
           angles='xy',
           width=.02,
           scale=1,
           scale_units='xy',
           color='xkcd:blue')
plt.axis('off')
plt.title("Gradient")

plt.subplot(132)
plt.imshow(image, cmap='gray')
plt.quiver(X,
           Y,
           u[..., 1],
           u[..., 0],
           angles='xy',
           width=.02,
           scale=2,
           scale_units='xy',
           color='xkcd:pink',
           headwidth=0,
           headlength=0,
           headaxislength=0)

plt.title("Orientation")
plt.axis('off')
plt.show()

# image = np.zeros((N, N))
# image[N // 2, :] = 1
# image[:, N // 2] = 1
# image = gaussian(image, .5)

# qs, Qs = bs.get_nematic_tensor(image)
# grad = bs.get_gradient(image)
# norm_grad = norm(grad, axis=2)
# rr, cc = np.nonzero(norm_grad)
# grad[rr, cc, :] /= norm_grad[rr, cc, None]
# u = bp.orientation_from_q(qs)
# u[..., 0] = 1
# u[..., 1] = 0
# u[Y > nY // 2, 0] = 0
# u[Y > nY // 2, 1] = 1

ax = plt.subplot(133)
# plt.imshow(image, cmap='gray')
# plt.imshow(np.zeros_like(image), cmap='gray')
corr = np.einsum('ijk,ijk->ij', u[1:, 1:, :], u[:-1, :-1, :])**2 - 1 / 3
plt.imshow(corr)

plt.quiver(X - 1,
           Y - 1,
           u[..., 1],
           u[..., 0],
           angles='xy',
           width=.02,
           scale=2,
           scale_units='xy',
           color='xkcd:pink',
           pivot='middle',
           headwidth=0,
           headlength=0,
           headaxislength=0)
shift = 0
plt.quiver(X + shift,
           Y + shift,
           u[..., 1],
           u[..., 0],
           angles='xy',
           width=.02,
           scale=2,
           scale_units='xy',
           color='xkcd:green',
           pivot='middle',
           headwidth=0,
           headlength=0,
           headaxislength=0,
           alpha=.75)
shift = shift - 1 / 2
plt.plot([-1.5, N - 1.5, N - 1.5, -1.5, -1.5],
         [-1.5, -1.5, N - 1.5, N - 1.5, -1.5],
         color='k')
plt.plot([shift, N + shift, N + shift, shift, shift],
         [shift, shift, N + shift, N + shift, shift],
         color='k')
plt.axis('off')
ax.set_aspect('equal')
plt.title("Correlations")

plt.savefig("examples/img/illutration0.svg", transparent=True)
