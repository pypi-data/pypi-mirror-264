"""Run analysis on rods of different lengths.

Can be used to create Fig.2.A of supplementary.

Ghislain de Labbey
Last updated May 12th 2023
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from skimage.draw import line_aa
from skimage.filters import gaussian

import bundling_score.bundling_score as bs
import bundling_score.plots as bp

N = 152
trials = 100
smax = 20

lmin, lmax, Nl = 1, 30, 30
ll = np.linspace(lmin, lmax - 1, Nl)

width1 = 1
sigma = 1

mean_corr_s = np.zeros((trials, Nl, 100))
score = np.zeros((trials, Nl))


def keep_inside(n, n0, n1):
    ''' Checks that number is in-between two others.

    Useful to avoid to draw the line outside of the image.'''
    if n < n0:
        return n0
    elif n > n1:
        return n1
    else:
        return n


def draw_line(image, center, angle, length, intensity=1):
    ''' Draw a line.'''
    oY, oX = center
    r0 = int(oY - length * np.sin(angle) / 2)
    r0 = keep_inside(r0, 0, N - 1)
    r1 = int(oY + length * np.sin(angle) / 2)
    r1 = keep_inside(r1, 0, N - 1)
    c0 = int(oX - length * np.cos(angle) / 2)
    c0 = keep_inside(c0, 0, N - 1)
    c1 = int(oX + length * np.cos(angle) / 2)
    c1 = keep_inside(c1, 0, N - 1)
    rr, cc, val = line_aa(r0, c0, r1, c1)
    image[rr, cc] += val * intensity


def create_image(length):
    ''' Create a bundle of given width, random position and orientation.'''
    image1 = np.zeros((N, N))
    center = np.random.randint((3 * N) // 8, (5 * N) // 8, 2)
    angle = np.random.rand() * 2 * np.pi
    draw_line(image1, center, angle, length)
    image1 = gaussian(image1, sigma=sigma)
    return image1


def trial(it, length):
    '''Generate image and compute score.'''
    image1 = create_image(length)
    return bs.compute_score(image1, smax=smax)


def compute(il):
    ''' Run all trials for one length.'''
    return [trial(it, ll[il]) for it in range(trials)]


# Show rods of different lengths
plt.figure('Rods')
plt.subplot(131)
plt.imshow(create_image(5))
plt.subplot(132)
plt.imshow(create_image(15))
plt.subplot(133)
plt.imshow(create_image(25))

# Show method
image = create_image(20)
bp.show_steps(image, smax=20)

# Compute for lots of images
a = [compute(il) for il in tqdm(range(Nl))]
a = np.array(a)

mean_score = np.mean(a, axis=1)
std_score = np.std(a, axis=1)

plt.figure('Compare')
plt.plot(ll, mean_score, label='Mean')
plt.fill_between(ll,
                 mean_score + std_score,
                 mean_score - std_score,
                 alpha=.3,
                 label='Standard deviation')
plt.legend()
plt.title('Rod of width 1px')
plt.ylabel(r'Correlation area (px$^2$)')
plt.xlabel('Rod length (px)')
plt.ylim(-5, 1.1 * np.max(mean_score + std_score))

plt.show()
