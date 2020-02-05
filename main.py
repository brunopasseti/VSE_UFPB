import cv2
import matplotlib
import numpy as np
from includes.Detection import Detection
import cv2.aruco as aruco
import time
import pprint as pp
from enum import Enum

method = cv2.TM_SQDIFF
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)


class states(Enum):
    CALIBRATE = 1
    DETECT = 2
    MATRIX = 3
    MAP = 4
    WAIT = 5
    STOP = 6

def main():
    prev = 0
    frame_rate = 30
    frame_count = 0
    state = states.CALIBRATE
    equalityFrameCounter = 0
    oldState = states.CALIBRATE
    oldDistanceVector = 0
    a = Detection()
    a.cap = cap
    frame1 = a.getFrame(cap)
    frame2 = a.getFrame(cap)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('c'):
            state = states.CALIBRATE
            equalityFrameCounter = 0
            oldDistanceVector = 0
        if cv2.waitKey(1) & 0xFF == ord('s'):
            state = states.STOP
            equalityFrameCounter = 0
            oldDistanceVector = 0
        if cv2.waitKey(1) & 0xFF == ord('d'):
            state = states.DETECT
            equalityFrameCounter = 0
            oldDistanceVector = 0

        time_elapsed = time.time() - prev
        if not (time_elapsed > 1./frame_rate):
            continue

        frame = a.getFrame(cap)
        processedFrame = a.processFrame(frame)
        a.detectMarkers(processedFrame)
        if (state == states.STOP):
            equalityFrameCounter = equalityFrameCounter + 1

        if(state == states.WAIT):
            equalityFrameCounter = equalityFrameCounter + 1
            if(equalityFrameCounter > 120):
                state = states(oldState.value+1)
                equalityFrameCounter = 0
                print(a.origin)

        if(state == states.CALIBRATE):
            if(a.calibrate()):
                print(a.distanceRef, a.distanceRefVector)
                if(a.distanceRefVector == oldDistanceVector):
                    equalityFrameCounter = equalityFrameCounter + 1
                else:
                    equalityFrameCounter = 0
                oldDistanceVector = a.distanceRefVector

            frame = aruco.drawDetectedMarkers(frame, a.corners)

            if(equalityFrameCounter == 10):
                equalityFrameCounter = 0
                oldState = states.CALIBRATE
                state = states.WAIT

        if(state == states.DETECT):
            bool = a.detect()
            if(not bool):
                print([(i.id, i.gridLocation) for i in a.Requests])
                oldState = states.DETECT
                state = states.WAIT
            frame = aruco.drawDetectedMarkers(frame, a.corners)

        font = cv2.FONT_HERSHEY_SIMPLEX

        frame = cv2.flip(frame, -1)

        frame = cv2.putText(frame, str(state.name), (50, 75), font, 2, (255,0,0), 1, cv2.LINE_AA)
        frame = cv2.putText(frame, str(equalityFrameCounter), (50, 125), font, 2, (0,0,255), 1, cv2.LINE_AA)

        cv2.imshow('frame', frame)

        prev = time.time()

if __name__ == '__main__':
    main()
