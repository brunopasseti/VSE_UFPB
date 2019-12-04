import cv2.aruco as aruco
import cv2
import numpy as np
from math import sqrt

class Detection():
    def __init__(self):
        self.distanceRefVector = [0, 0]
        self.distanceRef = 0
        self.arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.arucoParameters = aruco.DetectorParameters_create()
        self.ids = []
        self.corners = []
        self.origin = []

    def getFrame(self, cap):
        ret, frame = cap.read()
        if(not ret):
            return None
        return frame

    def processFrame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def detectMarkers(self, grayFrame):
        corners, ids, rejectedImgPoints = aruco.detectMarkers(grayFrame, self.arucoDict, parameters=self.arucoParameters)
        self.corners = corners
        self.ids = ids

    def calibrate(self):
        if( [0] in self.ids and [1] in self.ids ):
            # print("dentro do calibrate:", self.ids)
            resultZero = np.where(self.ids == [0])
            resultOne = np.where(self.ids == [1])
            indexOne = resultOne[0][0]
            indexZero = resultZero[0][0]
            self.distanceRefVector = [abs(self.corners[0][0][indexOne][1] - self.corners[0][0][indexZero][1]),  abs(self.corners[0][0][indexOne][0] - self.corners[0][0][indexZero][0])]
            self.distanceRef = sqrt(self.distanceRefVector[0]*self.distanceRefVector[0] + self.distanceRefVector[1]*self.distanceRefVector[1])
            
            return True
        else:
            return False
        pass
