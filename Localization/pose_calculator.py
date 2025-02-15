import numpy as np
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
        [-1, 0, 0,  0],
        [0,  1, 0,  0],
        [0,  0, -1, 0],
        [0,  0, 0,  1]                        
    ], dtype='object')
    
    rotated_pose = rotation @ new_pose
    print("\n", rotated_pose)
    return rotated_pose

def get_bot_to_cam(cam):
    pass

def get_pose_from_camera(tag, cam):
    cam_to_tag = get_cam_to_tag(tag)

    bot_to_cam = get_bot_to_cam(cam)
    
    tag_to_world = get_tag_to_world_by_tag_id(tag.id)

    return tag_to_world @ (cam_to_tag @ bot_to_cam)

#def temp_method():
#    print(get_tag_to_world_by_tag_id(0))
