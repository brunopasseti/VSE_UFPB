import cv2.aruco as aruco
import cv2
import numpy as np
from math import sqrt, floor
from includes.Request import Request

class Detection():
    def __init__(self):
        self.distanceRefVector = [0, 0]
        self.distanceRef = 0
        self.arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.arucoParameters = aruco.DetectorParameters_create()
        self.ids = []
        self.corners = []
        self.origin = []
        self.centers = []
        self.Requests = []
        self.cap = 0

    def getFrame(self, cap):
        ret, frame = cap.read()
        if(not ret):
            return None
        return frame

    def mapPixelToGridLocation(self, coord):
        """dx = abs(coord[0] - self.origin[0])
        dy = abs(coord[1] - self.origin[1])
        x = (abs(coord[0] - self.origin[0])) / self.distanceRefVector[0]
        y = (abs(coord[1] - self.origin[1])) / self.distanceRefVector[1]
        rx = floor(x)
        ry = floor(y)
        print("dx {} dy {} x {} y {} rx {} ry {}".format(dx, dy, x, y, rx, ry))
        transformedCoord = (
            floor(abs(coord[0] - self.origin[0]) / self.distanceRefVector[0]),
            floor(abs(coord[1] - self.origin[1]) / self.distanceRefVector[1])
        )"""
        x = abs(coord[0] - self.origin[0]) / self.distanceRef
        y = abs(coord[1] - self.origin[1]) / self.distanceRef
        rx = round(x)
        ry = round(y)
        # print("x {} y {} rx {} ry {} ref{} refVecX{} refVecY{}".format(x, y, rx, ry, self.distanceRef, self.distanceRefVector[0], self.distanceRefVector[1]))
        transformedCoord = (
            round(abs(coord[0] - self.origin[0]) / self.distanceRef),
            round(abs(coord[1] - self.origin[1]) / self.distanceRef)
        )
        return transformedCoord

    def processFrame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def detectMarkers(self, grayFrame):
        corners, ids, rejectedImgPoints = aruco.detectMarkers(grayFrame, self.arucoDict, parameters=self.arucoParameters)
        # ret, frame = self.cap.read()
        # grayFrame = self.processFrame(frame)
        # corners1, ids1, rejectedImgPoints1 = aruco.detectMarkers(grayFrame, self.arucoDict, parameters=self.arucoParameters)
        # ret, frame = self.cap.read()
        # grayFrame = self.processFrame(frame)
        # corners2, ids2, rejectedImgPoints2 = aruco.detectMarkers(grayFrame, self.arucoDict, parameters=self.arucoParameters)
        self.corners = corners
        # for i in self.corners:
        #     for j in i:
        #         for k in j:
        #             print(k)
        # print(self.ids)
        # print(self.corners)
        if(ids is None):
            return
        self.ids = ids.flatten()

    def calibrate(self):
        if(type(self.ids) is None):
            return False
        if( 0 in self.ids and 1 in self.ids and 2 in self.ids):
            resultZero = np.where(self.ids == [0])
            resultOne = np.where(self.ids == [1])
            resultTwo = np.where(self.ids == [2])
            indexZero = resultZero[0][0]
            indexOne = resultOne[0][0]
            indexTwo = resultTwo[0][0]

            self.distanceRefVector = [abs(self.corners[indexOne][0][0][0] - self.corners[indexZero][0][0][0]),  abs(self.corners[indexTwo][0][0][1] - self.corners[indexZero][0][0][1])]
            self.distanceRef = abs(self.corners[indexOne][0][0][0] - self.corners[indexZero][0][0][0])
            self.origin = [self.corners[indexZero][0][0][0], self.corners[indexZero][0][0][1]]
            return True
        else:
            return False
        pass

    def detect(self):
        if(type(self.ids) is None):
            return
        #lista = list(self.ids)
        #lista = lista.sort()
        flag = False
        flag2 = False
        for index, id in enumerate(self.ids) :
            flag = False
            for tempPos in self.Requests:
                if(tempPos.getId() == id):
                    flag = True
                    flag2 = True
            if(flag):
                continue
            temp = Request()
            temp.setId(id)
            # if(id == 0):
            positionOnListCorners = np.where(self.ids == [id])
            positionOnListCorners = positionOnListCorners[0][0]
            pos = self.mapPixelToGridLocation(list(self.corners[positionOnListCorners][0][0]))
            temp.setGridLocation(pos[0],pos[1])
            self.Requests.append(temp)
            print(id, pos)
        return flag2
