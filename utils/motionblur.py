import math
import random
import numpy as np
from numpy import ndarray
from numpy.fft import fft2, ifft2


"""
Applies motion blur with random orientation, and given probability and blur range

The image is slightly shifted to preserve the bounding boxes
"""


def np_fftconvolve(a, b):
    return np.real(ifft2(fft2(a) * fft2(b, s=a.shape)))


def motion_blur(img, intensity, angle):
    if intensity % 2:
        print("Motion Blur: Intensity must be a pair number. Rounding to the nearest upper pair integer.")
        intensity += 1

    kernel = generate_kernel(intensity, angle)
    result_img = np.zeros(img.shape)
    result_conv = np.stack((np_fftconvolve(img[:, :, 0], kernel),
                            np_fftconvolve(img[:, :, 1], kernel),
                            np_fftconvolve(img[:, :, 2], kernel)), axis=2)
    result_img[
                0:img.shape[0] - int(math.floor(intensity / 2)),
                0:img.shape[1] - int(math.floor(intensity / 2)), :
               ] = result_conv[
                int(math.floor(intensity / 2)):img.shape[0],
                int(math.floor(intensity / 2)):img.shape[1], :
                               ]

    return result_img


def convolute(img, kernel):
    if kernel.shape[0] != kernel.shape[1] or not (kernel.shape[0] % 2) or not (kernel.shape[1] % 2):
        return 0
    result_img: ndarray = np.zeros(
        (img.shape[0] - kernel.shape[0] + 1, img.shape[1] - kernel.shape[1] + 1, img.shape[2]))
    for ix, iy, ic in np.ndindex(result_img.shape):
        for kx, ky in np.ndindex(kernel.shape):
            print(ix)
            result_img[ix, iy, ic] += kernel[kx, ky] * img[ix + kx, iy + ky, ic]
    return result_img


def generate_kernel(length, angle=0):
    if length % 2:
        return 0
    x1, x2, y1, y2 = polar_to_coord(length, math.radians(angle % 90))
    values = bresenham(x1, x2, y1, y2)
    kernel = np.zeros((length + 1, length + 1))
    for value in values:
        kernel[value[0], value[1]] = 1 / len(values)

    if angle % 180 >= 90:
        kernel = np.flip(kernel.T, 0)

    return kernel


def polar_to_coord(length, angle):
    x = math.cos(angle) * length / 2
    y = math.sin(angle) * length / 2
    return int(length / 2 - x), int(length / 2 + x), int(length / 2 - y), int(length / 2 + y)


def bresenham(x1, x2, y1, y2):
    pixels = []
    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)

    y = y1
    for x in range(x1, x2 + 1):
        pixels.append((x, y))
        slope_error_new = slope_error_new + m_new

        if slope_error_new >= 0:
            y = y + 1
            slope_error_new = slope_error_new - 2 * (x2 - x1)

    return pixels
