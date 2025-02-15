from pose_calculator import get_tag_to_world_by_tag_id
from pose_calculator import get_bot_to_cam
from pose_calculator import get_cam_to_tag
from pose_calculator import get_pose_from_camera
from pose_calculator import temp_method
from unittest.mock import patch, MagicMock
import numpy as np
import math
from camera_utils import Camera
#from dt_apriltags import Detector

bot_to_cam = np.array([
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1]
], dtype='object')

tag_to_world = np.array([
    [0,  0, -1, 10 ],
    [-1, 0,  0, 5  ],
    [0,  1,  0, 0.5],
    [0,  0,  0, 1  ]
], dtype='object')

def test_tag1_robot_in_front():
    cam_to_tag = np.array([
        [-1, 0, 0, 0   ],
        [0, 1, 0, -0.2],
        [0, 0, -1, 2   ],
        [0, 0, 0, 1   ]
    ], dtype='object')

    
    ttw_mock = patch('pose_calculator.get_tag_to_world_by_tag_id',
                     return_value=tag_to_world)
    ctt_mock = patch('pose_calculator.get_cam_to_tag',
                     return_value=(cam_to_tag, 0))
    btc_mock = patch('pose_calculator.get_bot_to_cam',
                     return_value=bot_to_cam)

    #ttw_mock.return_value = tag_to_world
    # ctt_mock.return_value = cam_to_tag, 0
    # btc_mock.return_value = bot_to_cam

    ttw_mock.start()
    ctt_mock.start()
    btc_mock.start()
    
    #cam_mock.read.return_value = None, None
    cam = Camera(0, 'right_cam_mtx', 'right_cam_dst', 0, 0, 0, 0, 0)
    cam.read = MagicMock(return_value=(None, None))
    print("\n", get_pose_from_camera(cam, None))
    #temp_method()
    ttw_mock.stop()
    ctt_mock.stop()
    btc_mock.stop()

def test_tag1_robot_angled():
    cos45 = math.cos(math.radians(-45))
    sin45 = math.sin(math.radians(-45))
    sqrt2 = math.sqrt(2)
    
    cam_to_tag = np.array([
        [-cos45,  0, sin45,  0   ],
        [0,       1, 0,      -0.2     ],
        [-sin45,  0, -cos45, 2   ],
        [0,       0, 0,      1       ]
    ], dtype='object')

    
    ttw_mock = patch('pose_calculator.get_tag_to_world_by_tag_id',
                     return_value=tag_to_world)
    ctt_mock = patch('pose_calculator.get_cam_to_tag',
                     return_value=(cam_to_tag, 0))
    btc_mock = patch('pose_calculator.get_bot_to_cam',
                     return_value=bot_to_cam)

    #ttw_mock.return_value = tag_to_world
    # ctt_mock.return_value = cam_to_tag, 0
    # btc_mock.return_value = bot_to_cam

    ttw_mock.start()
    ctt_mock.start()
    btc_mock.start()
    
    #cam_mock.read.return_value = None, None
    cam = Camera(0, 'right_cam_mtx', 'right_cam_dst', 0, 0, 0, 0, 0)
    cam.read = MagicMock(return_value=(None, None))
    print("\n", get_pose_from_camera(cam, None))
    #temp_method()
    ttw_mock.stop()
    ctt_mock.stop()
    btc_mock.stop()
