from dt_apriltags import Detector
import math
import cv2
import numpy as np
import ntcore
import time
import wpiutil
import datetime
from wpiutil import wpistruct
from network_tables import start_network_table
from camera_utils import Camera
#from calculate_pose import calculate_tag_offset
#from calculate_pose import calculate_transformation
from poseclass import Position
from pose_calculator import get_poses_from_cam

INCHES_TO_METERS = 0.0254                                                                                     # OFFSET FROM ROBOT--------------------------
cams = [                                                                                                       # METERS-----------------------  RAD---------
          #id    matrix          distortion     X  Y  Z  yaw  pitch
    Camera(0, "cam0_mtx", "cam0_dst", -0.332, -0.25, -0.192, 45, -20),
    #Camera(4, "cam1_mtx", "cam1_dst", -0.332, 0.25, -0.192, -45, -20),
    Camera(2, "cam2_mtx", "cam2_dst", 0.11, 0.01, -0.336, 180, 0)
]

def main():
    # Initialize Network Table
    tagSeenPub, latencyPub, positionPub, inst = start_network_table()
    
    # Initialize Detector. https://github.com/duckietown/lib-dt-apriltags
    at_detector = Detector(searchpath=['apriltags'],
                           nthreads=1,        # Ask Calvin why we use 2 threads
                           quad_decimate=1.0) # use high res 1.0, low res 2.0

    for cam in cams:
        # We get 100fps on MJPG compared to YUY2
        cam.set_prop(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # DO NOT USE TRY EXCEPT IN FINAL CODE. IF MULTIPLE CAMERAS USE DIFFERENT VALUES FOR THIS, INITIALIZE PRIOR
        try:
            # Our Cameras use 1 as the manual. run v4l2-ctl -d /dev/videoX -L to see
            cam.set_auto_exposure(1)
        except ValueError:
            cam.set_auto_exposure(0.25)
        
        # Set Exposure and Brightness to reasonable values. Tweak if necessary.
        cam.set_prop(cv2.CAP_PROP_EXPOSURE, 20)
        cam.set_prop(cv2.CAP_PROP_BRIGHTNESS, 0)
        cam.start()

    with open("./Logs/" + str(datetime.datetime.now()) + ".csv", "a") as f:
        while True:
            # Initialize NT values
            seen_tag = False
            frame_start = time.process_time()
            if cv2.waitKey(1) == ord('q') & 0xff:
                break
            for cam in cams:
                #print(frame_start)
                if cam.frame is None:
                    continue
                cv2.imshow(str(cam.id), cam.read())
                frame_start = time.process_time()
            
                visionPoses = get_poses_from_cam(cam, at_detector)

                if len(visionPoses) != 0:
                    print(frame_start, cam.id)
                    seen_tag = True
                #print(visionPoses) 
                # Publish all positions and values to be interpreted on the RIO
                positionPub.set(visionPoses)
                latencyPub.set(time.process_time() - frame_start)
                #for pose in visionPoses:
                #    f.write(f"{frame_start},{cam.id},{pose.x},{pose.y},{pose.r},{pose.ID}\n")
            tagSeenPub.set(seen_tag)
        #inst.flush()
if __name__ == "__main__":
    main()
