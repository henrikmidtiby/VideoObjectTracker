# -*- coding: utf-8 -*-
"""
Python program for tracking certain markers in videos.

Written by: Henrik Skov Midtiby
Date: 2015-11-14
"""

import cv2
import MarkerTracker

def main(videoFileToAnalyze, outputFile, orderOfMarker, sizeOfKernel):
    # Open video file for reading and output file for writing.
    cap = cv2.VideoCapture(videoFileToAnalyze)
    outputfile = open(outputFile, 'w')
    
    # Initialize the marker tracker.
    tracker = MarkerTracker.MarkerTracker(orderOfMarker,  sizeOfKernel,  1.0)

    # Main loop
    counter = 0
    while(cap.isOpened()):
        counter += 1
        # Read a new image from the file.
        ret, frame = cap.read()
        
        # Halt if reading failed.
        if not ret:
            break
        
        # Cnovert image to grayscale.
        grayScaleImage = (cv2.split(frame)[0] + cv2.split(frame)[1] + cv2.split(frame)[2]) / 3.

        # Locate marker in image.
        (xm,  ym)  = tracker.locateMarker(grayScaleImage)

        # Write determined marker position to file.
        outputfile.write("%3d\t%3d\t%3d\n" % (counter, xm, ym))

        # Mark the center of the marker and show the annotated image.
        cv2.circle(frame, (xm,  ym), 20, (255, 0, 255), -1)
        cv2.imshow('frame', frame)
        
        # Break the look if the key 'q' was pressed. 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    outputfile.close()
    return    

# Launch the program.
videoFileToAnalyze = 'input/2015-11-12 09.06.21.mp4'
outputFile = 'output/positions.txt'
orderOfMarker = 4
sizeOfKernel = 51
main(videoFileToAnalyze, outputFile, orderOfMarker, sizeOfKernel)
    

