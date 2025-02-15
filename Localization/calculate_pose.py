import math
import numpy as np
                           # METERS----------------------  RAD---------------------
def calculate_transformation(CAMERA_X, CAMERA_Y, CAMERA_Z, CAMERA_YAW, CAMERA_PITCH):
    sin_pitch = math.sin(CAMERA_PITCH)
    cos_pitch = math.cos(CAMERA_PITCH)
    
    sin_yaw = math.sin(CAMERA_YAW)
    cos_yaw = math.cos(CAMERA_YAW)

    # Camera Pitch + Z > X
    pitch_rotation = np.array([
        [1, 0, 0, 0],
        [0, cos_pitch, sin_pitch, 0],
        [0, -sin_pitch, cos_pitch, 0],
        [0, 0, 0, 1]
    ], dtype="object")

    # Change X and Y
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

    #tag_to_cam = np.matmul(R, t)
    #print(tag_to_cam)
    
    yaw = math.asin(-R[2, 0])
    #print(yaw * 180 / math.pi)
    get_global_position(tag)
    return tag_in_robot_frame, yaw

def get_coordinate_transform():
    # convert to field axes
    camera_axes_to_field_axes = np.array([
        [0, 0, 1, 0],
        [-1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, 0, 1]
    ], dtype="object")

    return camera_axes_to_field_axes

def get_global_position(tag):
    R = tag.pose_R
    t = tag.pose_t
    #print(-(R.T) @ t)
    #print(R, "\n", t)
    new_R = R.T
    new_t = -new_R @ t

    print(new_R, "\n", new_t)
    
    t = [t[0][0], t[1][0], t[2][0]]
    R = np.eye(3)
    t = [0,0,1]
    cam_to_tag = np.eye(4)
    
    cam_to_tag[:3, :3] = R
    cam_to_tag[:3, 3] = t
    #tag_to_cam = R @ t
    #print(tag_to_cam)
    #tag_to_cam = np.linalg.inv(cam_to_tag)
    #print(cam_to_tag, "\n", tag_to_cam)

    #tag_to_cam = [t[0], t[1], t[2], 1]
    
    #camera_to_robot = get_robot_to_camera_transform(0,0,0,math.radians(0),math.radians(0))

    #robot_to_tag = robot_to_cam @ tag_to_cam

    #tag_frame_pos = (get_coordinate_transform() @ tag_to_cam) @ camera_to_robot

    #print(tag_frame_pos)
    

def get_robot_to_camera_transform(CAMERA_X, CAMERA_Y, CAMERA_Z, CAMERA_YAW, CAMERA_PITCH):
    sin_pitch = -math.sin(CAMERA_PITCH)
    cos_pitch = -math.cos(CAMERA_PITCH)
    
    sin_yaw = -math.sin(CAMERA_YAW)
    cos_yaw = -math.cos(CAMERA_YAW)

    # Camera Pitch
    pitch_rotation = np.array([
        [1, 0, 0, 0],
        [0, cos_pitch, sin_pitch, 0],
        [0, -sin_pitch, cos_pitch, 0],
        [0, 0, 0, 1]
    ], dtype="object")

    # Camera Yaw
    yaw_rotation = np.array([
        [cos_yaw, -sin_yaw, 0, 0],
        [sin_yaw, cos_yaw, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]            
    ], dtype="object")
    
    # Translation of Camera Origin to Robot Origin
    camera_origin_to_robot_origin = np.array([
        [1, 0, 0, -CAMERA_X],
        [0, 1, 0, -CAMERA_Y],
        [0, 0, 1, -CAMERA_Z],
        [0, 0, 0, 1]
    ], dtype="object")

    # Camera Coordinates to World Coordinates
    # Move origin
    camera_to_robot = camera_origin_to_robot_origin @ (yaw_rotation @ pitch_rotation)
    
    return camera_to_robot
