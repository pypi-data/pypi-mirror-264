''' Several simple examples of images and bundling scores '''

import matplotlib.pyplot as plt
import numpy as np

import bundling_score.bundling_score as bs
import bundling_score.plots as bp

from skimage.filters import gaussian

# Size of the image
N = 100
# Limit value for rx and ry, avoids padding
smax = 20

# Generate random image
image = np.random.rand(N, N)
score = bs.compute_score(image, smax=20)
print(f"Score of random image {score:.2f}")

bp.show_steps(image, smax=smax)

# Simple line
image = np.zeros((N, N))
image[N//2, :] = 1
image = gaussian(image, 5)
score = bs.compute_score(image, smax=20)
print(f"Score of simple line {score:.2f}")

bp.show_steps(image, smax=smax)

# Orthogonal lines
image = np.zeros((N, N))
image[N//2, :] = 1
image[:, N//2] = 1
image = gaussian(image, 5)
score = bs.compute_score(image, smax=20)
print(f"Score of orthogonal lines {score:.2f}")

# Parallel lines
image = np.zeros((N, N))
image[N//4, :] = 1
image[N//2, :] = 1
image[3 * N//4, :] = 1
image = gaussian(image, 5)
score = bs.compute_score(image, smax=20)
print(f"Score of parallel lines {score:.2f}")

bp.show_steps(image, smax=smax)

plt.show()
