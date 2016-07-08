# -*- coding: utf-8 -*-
"""
Python program for tracking certain markers in videos.

Written by: Henrik Skov Midtiby
Date: 2015-11-14
"""

import cv2
import MarkerTracker
import math


def main(video_file_to_analyze, output_filename, order_of_marker, size_of_kernel):
    # Open video file for reading and output file for writing.
    cap = cv2.VideoCapture()
    cap.open(video_file_to_analyze)
    output_file = open(output_filename, 'w')

    # Initialize the marker tracker.
    tracker = MarkerTracker.MarkerTracker(order_of_marker, size_of_kernel, 1.0)

    # Main loop
    counter = 0
    while cap.isOpened():
        counter += 1
        # Read a new image from the file.
        ret, frame = cap.read()

        # Halt if reading failed.
        if not ret:
            break

        # Convert image to grayscale.
        # gray_scale_image = (cv2.split(frame)[0] + cv2.split(frame)[1] + cv2.split(frame)[2]) / 3.
        gray_scale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Locate marker in image.
        (xm, ym) = tracker.locate_marker(gray_scale_image)

        # Write determined marker position to file.
        output_file.write("%3d\t%3d\t%3d\t%.2f\n" % (counter, xm, ym, tracker.orientation))

        # Mark the center of the marker and show the annotated image.
        cv2.circle(frame, (xm, ym), 20, (255, 0, 255), -1)

        dist = 50
        point1 = (xm, ym)
        point2 = (math.trunc(xm + dist * math.cos(tracker.orientation)),
                  math.trunc(ym + dist * math.sin(tracker.orientation)))
        cv2.line(frame, point1, point2, (255, 0, 255), 2)
        cv2.imshow('frame', frame)

        # Break the look if the key 'q' was pressed. 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    output_file.close()
    return


# Launch the program.
# video_file_to_analyze = 'input/2015-11-12 09.06.21.mp4'
video_file_to_analyze = '/home/henrik/Dropbox/Camera Uploads/2016-07-08 06.22.55.mp4'
output_file = 'output/positions2.txt'
order_of_marker = 6
size_of_kernel = 201
main(video_file_to_analyze, output_file, order_of_marker, size_of_kernel)
