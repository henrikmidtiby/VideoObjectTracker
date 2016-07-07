# -*- coding: utf-8 -*-
"""
Marker tracker for locating n-fold edges in images using convolution.

@author: Henrik Skov Midtiby
"""
import cv2
import numpy as np


class MarkerTracker:
    """
    Purpose: Locate a certain marker in an image.
    """

    def __init__(self, order, kernel_size, scale_factor):
        self.kernel_size = kernel_size
        (kernel_real, kernel_imag) = self.generate_symmetry_detector_kernel(order, kernel_size)

        self.order = order
        self.mat_real = kernel_real / scale_factor
        self.mat_imag = kernel_imag / scale_factor

    @staticmethod
    def generate_symmetry_detector_kernel(order, kernel_size):
        value_range = np.linspace(-1, 1, kernel_size)
        temp1 = np.meshgrid(value_range, value_range)
        kernel = temp1[0] + 1j * temp1[1]

        magnitude = abs(kernel)
        kernel = np.power(kernel, order)
        kernel = kernel * np.exp(-8 * magnitude ** 2)

        return np.real(kernel), np.imag(kernel)

    def locate_marker(self, frame):
        frame_real = frame.copy()
        frame_imag = frame.copy()

        # Calculate convolution and determine response strength.
        frame_real = cv2.filter2D(frame_real, cv2.CV_32F, self.mat_real)
        frame_imag = cv2.filter2D(frame_imag, cv2.CV_32F, self.mat_imag)
        frame_real_squared = cv2.multiply(frame_real, frame_real, dtype=cv2.CV_32F)
        frame_imag_squared = cv2.multiply(frame_imag, frame_imag, dtype=cv2.CV_32F)
        frame_sum_squared = cv2.add(frame_real_squared, frame_imag_squared, dtype=cv2.CV_32F)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(frame_sum_squared)

        return max_loc
