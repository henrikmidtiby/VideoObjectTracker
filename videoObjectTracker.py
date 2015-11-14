# -*- coding: utf-8 -*-
"""
Python program til at finde røde cirkler i film.

Skrevet af: Henrik Skov Midtiby og Mads Dyrmann
Dato: 2014-10-06

Versionshistorik:
2015-10-19: Understøttelse for OpenCV3.0
            Tilføjet tjek for om video er færdiglæst
            Ændret threshold værdi til også at virke på græs
"""

import time
import cv2
import MarkerTracker

def main():
    cap = cv2.VideoCapture('input/2015-11-12 09.06.21.mp4')
            
    outputfile = open('output/positions.txt', 'w')
    tracker = MarkerTracker.MarkerTracker(4,  51,  1.0)
    counter = 0

    while(cap.isOpened()):
        counter += 1
        # Læs et nyt billede fra filmen.
        ret, frame = cap.read()
        
        #time.sleep(0.5)
        if not ret:
            break
        
        #frame = cv2.resize(frame, dsize = None, fx = 0.5, fy = 0.5)
        grayScaleImage = (cv2.split(frame)[0] + cv2.split(frame)[1] + cv2.split(frame)[2]) / 3.

        (xm,  ym)  = tracker.locateMarker(grayScaleImage)
        print("(x, y): %3d %3d" % (xm, ym))
        outputfile.write("%3d\t%3d\t%3d\n" % (counter, xm, ym))

#        cv2.line(frame, point1, point2, (255, 0, 0), 4)
        cv2.circle(frame, (xm,  ym), 20, (255, 0, 255), -1)

        cv2.imshow('frame', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    outputfile.close()
    return    


main()

