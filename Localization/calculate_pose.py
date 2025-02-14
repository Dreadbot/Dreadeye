import math
import numpy as np
                           # METERS----------------------  RAD---------------------
def calculate_transformation(CAMERA_X, CAMERA_Y, CAMERA_Z, CAMERA_YAW, CAMERA_PITCH):
    sin_pitch = math.sin(CAMERA_PITCH)
    cos_pitch = math.cos(CAMERA_PITCH)
    
    sin_yaw = math.sin(CAMERA_YAW)
    cos_yaw = math.cos(CAMERA_YAW)

    # Camera Pitch
    pitch_rotation = np.array([
        [1, 0, 0, 0],
        [0, cos_pitch, sin_pitch, 0],
        [0, -sin_pitch, cos_pitch, 0],
        [0, 0, 0, 1]
    ], dtype="object")

    # FRC Fields use X as depth opposed to cameras
    camera_axes_to_robot_axes = np.array([
        [0, 1, 0, 0],
        [-1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype="object")

    # Translation of Camera Origin to Robot Origin
    camera_origin_to_robot_origin = np.array([
        [cos_yaw, -sin_yaw, 0, CAMERA_X],
        [sin_yaw, cos_yaw, 0, CAMERA_Y],
        [0, 0, 1, CAMERA_Z],
        [0, 0, 0, 1]
    ], dtype="object")

    # Camera Coordinates to World Coordinates
    # Rotate Axes onto World Axes
    corrected_pitch = np.matmul(camera_axes_to_robot_axes, pitch_rotation)
    # Move origin
    overall_transformation = np.matmul(camera_origin_to_robot_origin, corrected_pitch)
    
    return overall_transformation

# AT detector results, matrices from init
def calculate_tag_offset(tag, overall_transformation):
    t = tag.pose_t
    R = tag.pose_R
    
    tag_in_camera_frame = np.array([[t[0]], [t[1]], [t[2]], [1]], dtype="object")
    
    # Actual Coordinate Transform
    tag_in_robot_frame = np.matmul(overall_transformation, tag_in_camera_frame)

    yaw = math.asin(-R[2, 0])
    print(yaw)
    return tag_in_robot_frame
