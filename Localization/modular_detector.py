import cv2
from camera_utils import Camera

INCHES_TO_METERS = 0.0254
cams = [
        #port num   X      Y        Z   pitch yaw
    Camera(0, 0, -0.332, -0.219, -0.192, 45, -20),
    Camera(4, 1, -0.332, 0.219, -0.192, -45, -20),
    #Camera(2, 2, 0.11, 0.01, -0.336, 180, 0)
]

def main():
    for cam in cams:
        # We get 100fps on MJPG compared to YUY2
        cam.set_prop(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cam.set_auto_exposure(1)
                    
        cam.set_prop(cv2.CAP_PROP_EXPOSURE, 20)
        cam.set_prop(cv2.CAP_PROP_BRIGHTNESS, 0)
        cam.start()

if __name__ == "__main__":
    main()
