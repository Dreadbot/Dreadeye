import numpy as np
import math
import json
from scipy.spatial.transform import Rotation as R

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

def initialize_tag_vectors():
    tag_poses = {}
    with open('2025-reefscape.json', 'r') as f:
        field_data = json.load(f)['tags']
        for tag in field_data:
            tag_poses[tag['ID']] = {'pose_t': tag['pose']['translation'], 'quaternion': tag['pose']['rotation']['quaternion']}
    return tag_poses

def get_tag_to_world_by_tag_id(tag_poses, id):
    tag_pose = tag_poses[id]
    unparsed_t = tag_pose['pose_t']
    unparsed_Q = tag_pose['quaternion']

    tag_t = [
        [unparsed_t['x']],
        [unparsed_t['y']],
        [unparsed_t['z']]
    ]

    tag_Q = [
        unparsed_Q['X'],
        unparsed_Q['Y'],
        unparsed_Q['Z'],
        unparsed_Q['W']
    ]
    
    tag_R = R.from_quat(tag_Q)

    tag_axes_to_world_axes = np.array([
        [0,  0,  1],
        [1,  0,  0],
        [0,  1,  0]
    ], dtype='object')

    tag_R_to_world_R = tag_R.as_matrix() @ tag_axes_to_world_axes

    tag_to_world = np.eye(4)

    tag_to_world[:3, :3] = tag_R_to_world_R
    tag_to_world[:3, 3:] = tag_t

    return tag_to_world

def get_cam_to_tag(tag):
    R = tag.pose_R
    t = tag.pose_t
    new_R = R.T
    new_t = -new_R @ t
    new_pose = np.eye(4)
    new_pose[:3, :3] = new_R
    new_pose[:3, 3:] = new_t
    #print(new_pose)
    rotation = np.array([
        [1, 0,  0,  0],
        [0,  -1,  0,  0],
        [0,  0,  -1, 0],
        [0,  0,  0,  1]                      
    ], dtype='object')

    # yaw_90 = np.array([
    #     [0, -1, 0, 0],
    #     [1, 0, 0, 0],
    #     [0, 0, 1, 0],
    #     [0, 0, 0, 1]           
    # ], dtype='object')
    
    rotated_pose = rotation @ new_pose
    #print(rotated_pose)
    return rotated_pose
    #return new_pose

def get_bot_to_cam(x, y, z, yaw_rad, pitch_rad):
    #pitch_rad += math.pi
    cos_yaw = math.cos(yaw_rad)
    sin_yaw = math.sin(yaw_rad)
    sin_pitch = math.sin(pitch_rad)
    cos_pitch = math.cos(pitch_rad)
    
    yaw = np.array([
        [cos_yaw,    0,    sin_yaw],
        [0,          1,    0      ],
        [-sin_yaw,   0,    cos_yaw]                    
    ], dtype='object')

    # yaw = np.array([
    #     [cos_yaw,  -sin_yaw,   0      ],
    #     [sin_yaw,  cos_yaw,    0      ],
    #     [0,        0,          1      ]                    
    # ], dtype='object')
    
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
    #new_R = R
    #R = yaw @ pitch @ get_bot_to_camera_axes()
    #R = get_bot_to_camera_axes() @ yaw @ pitch
    #R = yaw @ get_bot_to_camera_axes() @ pitch
    new_R = R
    new_t = new_R @ translation

    bot_to_cam = np.eye(4)
    bot_to_cam[:3, :3] = new_R
    bot_to_cam[:3, 3:] = new_t
    print("BOT_TO_CAM: ", "\n", bot_to_cam)
    return bot_to_cam

def get_pose_from_tag(cam, tag):
    cam_to_tag = get_cam_to_tag(tag)

    bot_to_cam = cam.transform
    tag_poses = initialize_tag_vectors()
    tag_to_world = get_tag_to_world_by_tag_id(tag_poses, tag.tag_id)
    print(cam_to_tag)
    return tag_to_world @ (cam_to_tag @ bot_to_cam)
    #return tag_to_world @ cam_to_tag

import cv2
from poseclass import Position

INCHES_TO_METERS = 0.0254
ACCEPTABLE_TAG_ERROR_LIMIT = 5.0e-6

def get_poses_from_cam(cam, detector):
    grayscale = cam.read()

    # cv2.imshow(str(cam.id), grayscale)
    
    tags = detector.detect(grayscale,
                           estimate_tag_pose=True,
                           camera_params=cam.get_parameters(),
                           tag_size=6.5 * INCHES_TO_METERS)

    visionPositions = []
    for tag in tags:
        #print(tag.pose_R)
        if tag.pose_err > ACCEPTABLE_TAG_ERROR_LIMIT:
            continue
        if tag.tag_id > 22:
            continue
        pose = get_pose_from_tag(cam, tag)
        x, y, z = pose[:3, 3]
        #print(pose[:3, :3])
        yaw = math.atan2(pose[1][0],pose[0][0])
        print(x, y, yaw * 180 / math.pi)
        visionPositions.append(Position(x, y, yaw))
    
    return visionPositions
