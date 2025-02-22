from pose_calculator import get_tag_to_world_by_tag_id
from pose_calculator import get_bot_to_cam
from pose_calculator import get_cam_to_tag
from pose_calculator import get_pose_from_tag
#from pose_calculator import temp_method
from unittest.mock import patch, MagicMock
import numpy as np
import math
from camera_utils import Camera
#from dt_apriltags import Detector
INCHES_TO_METERS = 0.0254
bot_to_cam = np.array([
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1]
], dtype='object')

tag_to_world = np.array([
    [0,  0, 1, 13.89 ],
    [1, 0,  0, 5  ],
    [0,  1,  0, 0.5],
    [0,  0,  0, 1  ]
], dtype='object')

def test_tag1_robot_in_front():

    pose_t = [[1],
              [0.2],
              [2]]

    pose_R = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ], dtype='object')

    
    ttw_mock = patch('pose_calculator.get_tag_to_world_by_tag_id',
                     return_value=tag_to_world)
    #ctt_mock = patch('pose_calculator.get_cam_to_tag',
    #                 return_value=cam_to_tag)
    btc_mock = patch('pose_calculator.get_bot_to_cam',
                     return_value=bot_to_cam)

    ttw_mock.return_value = tag_to_world
    # ctt_mock.return_value = cam_to_tag, 0
    btc_mock.return_value = bot_to_cam

    ttw_mock.start()
    #ctt_mock.start()
    btc_mock.start()
    
    #cam_mock.read.return_value = None, None
    cam = Camera(0, 'right_cam_mtx', 'right_cam_dst', 0, 0, 0, 0, 0)
    cam.read = MagicMock(return_value=(None, None))
    tag = MagicMock()
    tag.pose_t = pose_t
    tag.pose_R = pose_R
    tag.tag_id = 7
    pose = get_pose_from_tag(cam, tag)
    #yaw = -math.atan2(pose[0][2], pose[1][2])
    yaw = math.atan2(pose[1][0],pose[0][0])
    #yaw = math.acos(pose[2][2])
    #yaw = math.asin(pose[2, 0])
    print("\n", pose, yaw)
    #temp_method()
    ttw_mock.stop()
    #ctt_mock.stop()
    btc_mock.stop()

def test_tag0_robot_angled():
    cos45 = math.cos(math.radians(45))
    sin45 = math.sin(math.radians(45))
    sqrt2 = math.sqrt(2)

    pose_t = [[0],
              [0],
              [2]]

    pose_R = np.array([
        [cos45,  0, sin45],
        [0,      1, 0    ],
        [-sin45, 0, cos45]
    ], dtype='object')
    # cam_to_tag = np.array([
    #     [-cos45,  0, sin45,  0   ],
    #     [0,       1, 0,      -0.2     ],
    #     [-sin45,  0, -cos45, 2   ],
    #     [0,       0, 0,      1       ]
    # ], dtype='object')

    
    ttw_mock = patch('pose_calculator.get_tag_to_world_by_tag_id',
                     return_value=tag_to_world)
    #ctt_mock = patch('pose_calculator.get_cam_to_tag',
    #                 return_value=(tag_R, tag_t))
    btc_mock = patch('pose_calculator.get_bot_to_cam',
                     return_value=bot_to_cam)

    #ttw_mock.return_value = tag_to_world
    # ctt_mock.return_value = cam_to_tag, 0
    btc_mock.return_value = bot_to_cam

    ttw_mock.start()
    #ctt_mock.start()
    btc_mock.start()
    
    #cam_mock.read.return_value = None, None
    cam = Camera(0, 'right_cam_mtx', 'right_cam_dst', 0, 0, 0, 0, 0)
    cam.read = MagicMock(return_value=(None, None))
    tag = MagicMock()
    tag.pose_t = pose_t
    tag.pose_R = pose_R
    tag.tag_id = 7
    print("\n", get_pose_from_tag(cam, tag))
    #temp_method()
    ttw_mock.stop()
    #ctt_mock.stop()
    btc_mock.stop()

def test_tag0_robot_angled_to_bot():
    cos45 = math.cos(math.radians(45))
    sin45 = math.sin(math.radians(45))
    sqrt2 = math.sqrt(2)

    pose_t = [[0],
              [0],
              [0]]

    pose_R = np.array([
        [cos45,  0, sin45],
        [0,      1, 0    ],
        [-sin45, 0, cos45]
    ], dtype='object')
    # cam_to_tag = np.array([
    #     [-cos45,  0, sin45,  0   ],
    #     [0,       1, 0,      -0.2     ],
    #     [-sin45,  0, -cos45, 2   ],
    #     [0,       0, 0,      1       ]
    # ], dtype='object')

    
    #ttw_mock = patch('pose_calculator.get_tag_to_world_by_tag_id',
    #                 return_value=tag_to_world)
    #ctt_mock = patch('pose_calculator.get_cam_to_tag',
    #                 return_value=(tag_R, tag_t))
    #btc_mock = patch('pose_calculator.get_bot_to_cam',
    #                 return_value=bot_to_cam)
    #ttw_mock.return_value = tag_to_world
    # ctt_mock.return_value = cam_to_tag, 0
    #btc_mock.return_value = bot_to_cam

    #ttw_mock.start()
    #ctt_mock.start()
    #btc_mock.start()
    
    #cam_mock.read.return_value = None, None
    cam = Camera(0, 'right_cam_mtx', 'right_cam_dst', 13.25, -9, 7.5, -45, 20)
    cam.read = MagicMock(return_value=(None, None))
    tag = MagicMock()
    tag.pose_t = pose_t
    tag.pose_R = pose_R
    tag.tag_id = 7
    #print("\n", get_pose_from_camera(tag, cam))
    #temp_method()
    #ttw_mock.stop()
    #ctt_mock.stop()
    #btc_mock.stop()

    identity = [[0],
                [0],
                [0],
                [1]]
    print("\n", cam.transform)
    translation = (cam.transform @ identity)
    print("should be cam pos", "\n", translation)
    print(translation[0][0] * translation[0][0] + translation[1][0] * translation[1][0] + translation[2][0] * translation[2][0])
    robot_frame_camera = [[13.25],
                          [-9],
                          [7.5],
                          [1]]
    print("should be identity", "\n", cam.transform @ robot_frame_camera)
    point_out_of_bot = [[25],
                        [0],
                        [7.5],
                        [1]]
    print(cam.transform @ point_out_of_bot)

    
