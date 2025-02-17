import numpy as np
import math

def get_bot_to_camera_axes():    
    # pitch = np.array([
    #     [0, 0, 1],
    #     [0, 1, 0],
    #     [-1, 0, 0]             
    # ], dtype="object")
    
    # yaw = np.array([
    #     [0, -1, 0],
    #     [1, 0, 0],
    #     [0, 0, 1]                       
    # ],dtype="object")

    bot_to_cam = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ], dtype='object')
    #print(yaw @ pitch)
    
    #return yaw @ pitch
    return bot_to_cam

def get_tag_to_world_by_tag_id(id):
    # Parse YAML
    pass

def get_cam_to_tag(tag):
    R = tag.pose_R
    t = tag.pose_t
    new_R = R.T
    new_t = -new_R @ t
    new_pose = np.eye(4)
    new_pose[:3, :3] = new_R
    new_pose[:3, 3:] = new_t

    rotation = np.array([
        [-1, 0, 0, 0],
        [0,  1, 0, 0],
        [0,  0, -1, 0],
        [0, 0, 0, 1]                      
    ], dtype='object')

    # yaw_90 = np.array([
    #     [0, -1, 0, 0],
    #     [1, 0, 0, 0],
    #     [0, 0, 1, 0],
    #     [0, 0, 0, 1]           
    # ], dtype='object')
    
    rotated_pose = rotation @ new_pose
    
    return rotated_pose

def get_bot_to_cam(x, y, z, yaw_rad, pitch_rad):
    #pitch_rad += math.pi
    cos_yaw = math.cos(yaw_rad)
    sin_yaw = math.sin(yaw_rad)
    sin_pitch = math.sin(pitch_rad)
    cos_pitch = math.cos(pitch_rad)
    
    yaw = np.array([
        [cos_yaw,    0,    sin_yaw],
        [0,          1,    0      ],
        [-sin_yaw, 0,    cos_yaw]                      
    ], dtype='object')
    
    pitch = np.array([
        [1, 0,        0       ],
        [0, cos_pitch,  -sin_pitch],
        [0, sin_pitch,  cos_pitch]                      
    ], dtype='object')

    translation = [
        [x],
        [y],
        [z]]
    
    R = pitch @ yaw @ get_bot_to_camera_axes()
    new_R = R
    new_t = -new_R @ translation

    bot_to_cam = np.eye(4)
    bot_to_cam[:3, :3] = new_R
    bot_to_cam[:3, 3:] = new_t
    
    return bot_to_cam

def get_pose_from_camera(tag, cam):
    cam_to_tag = get_cam_to_tag(tag)

    bot_to_cam = cam.transform
    
    tag_to_world = get_tag_to_world_by_tag_id(tag.tag_id)

    return tag_to_world @ (cam_to_tag @ bot_to_cam)
    #return cam_to_tag @ bot_to_cam
