def get_tag_to_world_by_tag_id(id):
    pass

def get_cam_to_tag(grayscale, detector):
    tags = detector.detect(grayscale,
                           estimate_tag_pose=True,
                           camera_params=cam.get_parameters(),
                           tag_size=TAG_SIZE_INCHES * INCHES_TO_METERS)
    
    pass

def get_bot_to_cam(camera):
    pass

def get_pose_from_camera(cam, detector):
    _, frame = cam.read()
    cam_to_tag, id = get_cam_to_tag(frame, detector)

    bot_to_cam = get_bot_to_cam(cam)
    
    tag_to_world = get_tag_to_world_by_tag_id(id)

    return tag_to_world @ (cam_to_tag @ bot_to_cam)
    #return bot_to_cam @ (cam_to_tag)

def temp_method():
    print(get_tag_to_world_by_tag_id(0))
