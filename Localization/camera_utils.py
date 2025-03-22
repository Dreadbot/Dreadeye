import cv2
import yaml
import numpy as np
import math
import threading
import time
from dt_apriltags import Detector
from network_tables import start_network_table
from pose_class import Position
from pose_calculator import get_bot_to_cam, get_poses_from_cam

class Camera(threading.Thread):
    def __init__(self, id, cam_num, x, y, z, yaw, pitch):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(id)
        self.id = id
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.mtx = np.load("Cameras/cam" + str(cam_num) + "_mtx.npy")
        self.dst = np.load("Cameras/cam" + str(cam_num) + "_dst.npy")
        self.frame = None
        self.newmtx, self.roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dst, (w,h), 1, (w,h))
        self.transform = get_bot_to_cam(x, y, z, math.radians(yaw), math.radians(pitch))
        self.tagSeenPub, self.latencyPub, self.positionPub, self.inst = start_network_table("Cam" + str(id))
        self.detector = Detector(searchpath=['apriltags'],
                                 nthreads=1,
                                 quad_decimate=1.0)
        self.tagSeen = False
        
    def read(self):
        frame = self.frame
        self.frame = None
        return frame
    
    def run(self):
        x, y, w, h = self.roi
        while True:
            _, frame = self.cap.read()
            self.timestamp = time.process_time()
            
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dst = cv2.undistort(grayscale, self.mtx, self.dst, None, self.newmtx)[y:y+h, x:x+w]

            self.frame = dst

            self.localize()
    
    def get_parameters(self):
        camera_params = [0] * 4
        camera_params[0] = self.newmtx[0][0]
        camera_params[1] = self.newmtx[1][1]
        camera_params[2] = self.newmtx[0][2]
        camera_params[3] = self.newmtx[1][2]
        return camera_params

    def get_timestamp(self):
        return self.timestamp
        
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

    def localize(self):
        visionPoses = get_poses_from_cam(self, self.detector)

        if len(visionPoses) != 0:
            self.tagSeen = True

        self.positionPub.set(visionPoses)
        self.latencyPub.set(time.process_time() - self.timestamp)
        self.tagSeenPub.set(self.tagSeen)
