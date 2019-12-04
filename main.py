import cv2
import matplotlib
import numpy as np
from includes.Detection import Detection
import cv2.aruco as aruco
import time
import pprint as pp

method = cv2.TM_SQDIFF
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

state = "Calibrating"

prev = 0
frame_rate = 30

while True:
    time_elapsed = time.time() - prev
    if not (time_elapsed > 1./frame_rate):
        continue
    a = Detection()
    frame = a.getFrame(cap)
    # frame = cv2.flip(frame)
    processedFrame = a.processFrame(frame)
    a.detectMarkers(processedFrame)
    # if(not a.ids):
        # continue
    if(a.calibrate()):
        print(a.distanceRef, a.distanceRefVector)
    frame = aruco.drawDetectedMarkers(frame, a.corners)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        state = "Calibrating"
    prev = time.time()
