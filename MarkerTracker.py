# -*- coding: utf-8 -*-
"""
Marker tracker for locating n-fold edges in images using convolution.

@author: Henrik Skov Midtiby
"""
import cv2
import numpy as np

class MarkerTracker:
    '''
    Purpose: Locate a certain marker in an image.
    '''
    def __init__(self, order, kernelSize, scaleFactor):
        self.kernelSize = kernelSize
        (kernelReal, kernelImag) = self.generateSymmetryDetectorKernel(order, kernelSize)
        
        self.order = order
        self.matReal = kernelReal / scaleFactor
        self.matImag = kernelImag / scaleFactor
                  
    def generateSymmetryDetectorKernel(self, order, kernelsize):
        valueRange = np.linspace(-1, 1, kernelsize);
        temp1 = np.meshgrid(valueRange, valueRange)
        kernel = temp1[0] + 1j*temp1[1];
            
        magni = abs(kernel);
        kernel = kernel**order;
        kernel = kernel*np.exp(-8*magni**2);
                 
        return (np.real(kernel), np.imag(kernel))
    
    def locateMarker(self, frame):
        self.frameReal = frame.copy()
        self.frameImag = frame.copy()

        # Calculate convolution and determine response strength.
        self.frameReal = cv2.filter2D(self.frameReal, cv2.CV_32F, self.matReal)
        self.frameImag = cv2.filter2D(self.frameImag, cv2.CV_32F, self.matImag)
        self.frameRealSq = cv2.multiply(self.frameReal, self.frameReal, dtype = cv2.CV_32F)
        self.frameImagSq = cv2.multiply(self.frameImag, self.frameImag, dtype = cv2.CV_32F)
        self.frameSumSq = cv2.add(self.frameRealSq, self.frameImagSq, dtype = cv2.CV_32F)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(self.frameSumSq)

        (xm, ym) = max_loc
        return max_loc
        