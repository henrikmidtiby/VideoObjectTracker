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

import cv2
import numpy as np
import time

def main():
    cap = cv2.VideoCapture('input/2015-11-11 12.50.19.mp4')
    
    if cv2.__version__[0]=='3': #if opencv 3.0
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    else: #if opencv<30.
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        
    VidOut = cv2.VideoWriter('output/output.avi',fourcc,20,(720,480))    
    
    while(cap.isOpened()):
        # Læs et nyt billede fra filmen.
        ret, frame = cap.read()
        #time.sleep(0.5)
        if not ret:
            break        
        
        # Vis billedet på skærmen.
        cv2.imshow('frame', frame)

        
#                    point4 = (frame.shape[1], cy) 
#                    cv2.line(frame, point1, point2, (255, 0, 0), 4)
#                   cv2.circle(frame, (cx, cy), 20, (255, 0, 255), -1)

        VidOut.write(frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    VidOut.release()    
    return    


main()
