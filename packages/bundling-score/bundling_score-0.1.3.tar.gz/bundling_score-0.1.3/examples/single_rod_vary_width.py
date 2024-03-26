"""Run analysis on rods of different widths.

Can be used to create Fig.2.B of supplementary.

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
sigma = 1

wmin, wmax, Nw = 1, 30, 30
ww = np.linspace(wmin, wmax, Nw, dtype='int')


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


def create_image(width):
    ''' Create a bundle of given width, random position and orientation.'''
    image1 = np.zeros((N, N))
    center = np.random.randint((3 * N) // 8, (5 * N) // 8, 2)

    angle = np.random.rand() * np.pi
    draw_line(image1, center, angle, 20, np.random.rand())
    for ii in range(2, width + 1):
        shift = (1 - 2 * (ii % 2)) * ii // 2
        draw_line(image1, center + shift * np.array(
            (np.cos(angle), -np.sin(angle))), angle, 20, np.random.rand())

    image1 = gaussian(image1, sigma)
    return image1


def trial(it, width):
    '''Generate image and compute score.'''
    image1 = create_image(width)
    score = bs.compute_score(image1, smax=smax)
    return score


def compute(iw):
    ''' Run all trials for one width.'''
    return [trial(it, ww[iw]) for it in range(trials)]


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
a = [compute(iw) for iw in tqdm(range(Nw))]
a = np.array(a)

mean_score = np.mean(a, axis=1)
std_score = np.std(a, axis=1)

mean_score = np.zeros(Nw)
std_score = np.zeros_like(mean_score)
for iw in tqdm(range(Nw)):
    mean_score[iw] = np.mean(a[iw])
    std_score[iw] = np.std(a[iw])

plt.figure('Compare')
plt.plot(ww, mean_score, label='Mean')
plt.fill_between(ww,
                 mean_score + std_score,
                 mean_score - std_score,
                 alpha=.3,
                 label='Standard deviation')
plt.legend()
plt.title('Rod of length 20px')
plt.ylabel(r'Correlation area (px$^2$)')
plt.xlabel('Rod width (px)')
plt.ylim(0, 1.1 * (np.max(mean_score + std_score)))

plt.show()
