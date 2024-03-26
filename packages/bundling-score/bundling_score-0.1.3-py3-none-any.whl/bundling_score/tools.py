''' Provides secondary tools, that were useful in more specific cases.'''
import numpy as np

from skimage import filters
from skimage.draw import disk
from skimage.feature import match_template
from skimage.transform import warp_polar
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture


def auto_detect_crop(timelapse):
    ''' Autodetect position of cortex and crop

    This was useful when the ROI hadn't been extracted in FIJI'''
    image = timelapse[0]
    image = filters.median(image, footprint=disk(10))
    tmplate = disk(200)
    result = match_template(image, tmplate, pad_input=False)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[::-1]
    x += 200
    y += 200
    return timelapse[:, y - 150:y + 150, x - 150:x + 150]


def crop_fiji_roi(timelapse, roi, length=0, i=0):
    ''' Use ROI defined and saved with FIJI to crop the image.
    timelapse

    Arguments:
    timelapse -- timelpase to crop. Can be a 2D image.
    roi       -- list of ROIs to use
    length    -- length of the square to keep,
              detected from ROI if not explicitely given
    i         -- index of the roi in the list that is used'''

    roi_prop = list(roi)[i]
    roi_dict = roi[roi_prop]
    roi_rad = roi_dict['width'] / 2.
    r = roi_dict['top'] + roi_rad
    c = roi_dict['left'] + roi_rad

    if not length:
        if roi_dict['type'] == 'oval':
            length = int(roi_rad / np.sqrt(2))
        elif roi_dict['type'] == 'rectangle':
            length = min(roi_dict['width'], roi_dict['height']) // 2
        else:
            raise Exception('Shape not implemented')

    rr, cc = disk((r, c), roi_rad)
    res = np.copy(timelapse)
    res = res[...,
              int(r) - length:int(r) + length,
              int(c) - length:int(c) + length]
    # print(r, c)
    return res


def as_function_of_distance(corr, radius=100):
    '''Function of (x,y) to function of the distance by averaging over angle


    This can be useful because in an isotropic system, one expects C to depend
    only on s = ||r||'''

    nCY, nCX = corr.shape
    rr, cc = disk((nCY / 2, nCX / 2), min(nCY, nCX) / 2, shape=(nCX, nCY))
    tmp = np.zeros_like(corr)
    tmp[rr, cc] = corr[rr, cc]

    polar_corr = warp_polar(tmp, radius=radius)
    mean_corr_s = np.mean(polar_corr, axis=0)

    return mean_corr_s / mean_corr_s[0]


def find_dots(image, Nsig=6, show=False):
    '''Fit with two gaussians (one for main, other for outliers). Threshold to exclude outliers'''
    model = GaussianMixture(n_components=2)
    model.fit(image.reshape(-1, 1))
    i0 = np.argmax(model.weights_)
    mean, sig = model.means_[i0, 0], np.sqrt(model.covariances_[i0, 0])

    if show:
        plt.figure()
        plt.subplot(222)
        plt.hist(image)

        proba = np.zeros_like(image)
        for i in range(len(model.weights_)):
            xx = np.arange(0, np.max(image) + 1, 1)
            mean0, sig0, w0 = model.means_[i, 0], np.sqrt(
                model.covariances_[i, 0]), model.weights_[i]
            gauss = w0 / np.sqrt(2 * np.pi * sig0**2) * np.exp(
                -(xx - mean0)**2 / 2 / sig0**2)
            proba += gauss
            plt.plot(xx, gauss)
        plt.plot(xx, proba)
        plt.axvline(mean + Nsig * sig, color='k')

        image1 = image.copy()
        image1[image > mean + Nsig * sig] = np.nan
        plt.subplot(221)
        plt.imshow(image, vmin=0, vmax=mean + 2 * Nsig * sig)
        plt.subplot(223)
        plt.imshow(image1, vmin=0, vmax=mean + 2 * Nsig * sig)

    return image > mean + Nsig * sig
