# -*- coding: utf-8 -*-
"""
Python program for tracking certain markers in videos.

Written by: Henrik Skov Midtiby
Date: 2015-11-14
"""

import cv2
import MarkerTracker
import math


def track_marker_in_video(video_file_to_analyze_filename, output_filename_input, order_of_marker_input, size_of_kernel_input):
    # Open video file for reading and output file for writing.
    cap = cv2.VideoCapture()
    cap.open(video_file_to_analyze_filename)
    output_file = open(output_filename_input, 'w')

    # Initialize the marker tracker.
    tracker = MarkerTracker.MarkerTracker(order_of_marker_input, size_of_kernel_input, 1.0)

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
        gray_scale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Locate marker in image.
        marker_pose = tracker.locate_marker(gray_scale_image)

        # Show and write to file information about the detected marker.
        string_to_file = "%3d\t%3d\t%3d\t%.2f\t%.2f\n" % (
        counter, marker_pose.x, marker_pose.y, marker_pose.theta, marker_pose.quality)
        print(string_to_file[0:-1])
        output_file.write(string_to_file)

        # Mark the center of the marker
        cv2.circle(frame, (marker_pose.x, marker_pose.y), 20, (255, 0, 255), -1)
        cv2.circle(frame, (marker_pose.x, marker_pose.y), size_of_kernel_input / 2, (255, 0, 255), 1)

        # Mark the orientation of the detected marker
        dist = 50
        point1 = (marker_pose.x, marker_pose.y)
        point2 = (math.trunc(marker_pose.x + dist * math.cos(marker_pose.theta)),
                  math.trunc(marker_pose.y + dist * math.sin(marker_pose.theta)))
        cv2.line(frame, point1, point2, (255, 0, 255), 2)

        # Show the annotated image.
        cv2.imshow('frame', frame)

        # Break the look if the key 'q' was pressed. 
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    output_file.close()
    return


# Launch the program.
# video_file_to_analyze = 'input/2015-11-12 09.06.21.mp4'
video_file_to_analyze = '/home/henrik/Dropbox/Camera Uploads/2016-07-08 06.22.55.mp4'
output_filename = 'output/positions2.txt'
order_of_marker = 6
size_of_kernel = 201
track_marker_in_video(video_file_to_analyze, output_filename, order_of_marker, size_of_kernel)