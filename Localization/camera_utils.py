import cv2
import yaml
import numpy as np
import math
from calculate_pose import calculate_transformation
    
class Camera:
    def __init__(self, id, mtx, dst, x, y, z, yaw, pitch):
        self.cap = cv2.VideoCapture(id)
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.mtx = np.load(mtx + ".npy")
        self.dst = np.load(dst + ".npy")
        self.newmtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dst, (w,h), 1, (w,h))
        self.transform = calculate_transformation(x, y, z, math.radians(yaw), math.radians(90 + pitch))
    
    def read(self):
        _, frame = self.cap.read()
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return grayscale
    
    def get_parameters(self):
        camera_params = [0] * 4
        camera_params[0] = self.newmtx[0][0]
        camera_params[1] = self.newmtx[1][1]
        camera_params[2] = self.newmtx[0][2]
        camera_params[3] = self.newmtx[1][2]
        return camera_params
    
    def set_prop(self, prop, val):
        for _ in range (0, 10):
            self.cap.set(prop, val)
            if self.cap.get(prop) != val:
                continue
            else: 
                return
        raise ValueError()

    def set_auto_exposure(self, val):
        try:
            self.set_prop(cv2.CAP_PROP_AUTO_EXPOSURE, val)
        except ValueError:
            raise ValueError("Failed to set AUTO EXPOSURE to %d", val)

