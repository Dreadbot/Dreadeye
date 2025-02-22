from dt_apriltags import Detector
import math
import cv2
import numpy as np
import ntcore
import time
import wpiutil
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
    Camera(0, "right_cam_mtx", "right_cam_dst", -0.34, -0.25, -0.19, 45, -20), #-0.25, 0.19, 0.33, -45, -20) #0.34, -0.25, 0.19, -44.5, -20)
    Camera(2, "right_cam_mtx", "right_cam_dst", -0.34, 0.25, 0.19, -45, -20) # UNCALIBRATED
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
        cam.set_prop(cv2.CAP_PROP_EXPOSURE, 50)
        cam.set_prop(cv2.CAP_PROP_BRIGHTNESS, 0)
    
    while True:
        # Initialize NT values
        visionPositions = []
        seen_tag = False
        frame_start = time.process_time()
        #if cv2.waitKey(1) == ord('q') & 0xff:
        #    break
        for cam in cams:
            visionPoses = get_poses_from_cam(cam, at_detector)

            for pose in visionPoses:
                visionPositions.append(pose)
            # grayscale = cam.read()
            
            # # Use imshow to debug camera postions and IDs
            # cv2.imshow(str(cam.id), grayscale)

            # dst = cv2.undistort(grayscale, cam.mtx, cam.dst, None, cam.newmtx)
        
            # x, y, w, h = cam.roi
            # dst = dst[y:y+h, x:x+w]
            
            # tags = at_detector.detect(grayscale,
            #                           estimate_tag_pose=True,
            #                           camera_params=cam.get_parameters(),
            #                           tag_size=TAG_SIZE_INCHES * INCHES_TO_METERS)
            
            # for tag in tags:
            #     # We do not like tags that have much error >:(
            #     #print(tag.pose_err)
            #     if tag.pose_err > ACCEPTABLE_TAG_ERROR_LIMIT:
            #         continue
            #     seen_tag = True
                
            #     # offset, yaw = calculate_tag_offset(tag, cam.transform)
                
            #     # xOffset = offset[0][0][0]
            #     # yOffset = offset[1][0][0]
                
            #     #print(pose[:3, 3:])
            #     print(tag.pose_t, "\n", tag.pose_R)
            #     #visionOffsets.append(Position(xOffset, yOffset, yaw, tagID))
                
            # Publish all positions and values to be interpreted on the RIO
        positionPub.set(visionPositions)
        latencyPub.set(time.process_time() - frame_start)
        tagSeenPub.set(seen_tag)
        #inst.flush()
if __name__ == "__main__":
    main()
