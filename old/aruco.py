import cv2
import cv2.aruco as aruco
import matplotlib
import numpy as np
import time
# import pygame

method = cv2.TM_SQDIFF
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

state = "Calibrating"

prev = 0
frame_rate = 30
while(True):
    # Capture frame-by-frame
    time_elapsed = time.time() - prev
    if not (time_elapsed > 1./frame_rate):
        continue
    ret, frame = cap.read()
    # print(frame.type(), template.type())
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners, ids)
    frame = aruco.drawDetectedMarkers(frame, corners)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        state = "Calibrating"
    prev = time.time()




# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
