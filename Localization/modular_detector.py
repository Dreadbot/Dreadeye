import cv2
from camera_utils import Camera
from mjpeg_streamer import MjpegServer

IP_ADDRESS = "10.36.56.6" # should match coprocessor

server = MjpegServer(IP_ADDRESS, 1181)

# all measurements in Meters and Degrees
cams = [
        #port num X-back Y-      Z-down  yaw  pitch-down from horizontal
    #Camera(0, 2, 0.273, 0.284, -0.186, 45, -20, server),
    Camera(2, 1, 0.336, 0.120, -0.177, 180, -20, server),
    Camera(4, 0, 0.273, -0.284, -0.186, -90, -20, server)
]

def main():
    for cam in cams:
        # We get 100fps on MJPG compared to YUY2
        cam.set_prop(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cam.set_auto_exposure(1)
        cam.set_prop(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cam.set_prop(cv2.CAP_PROP_FRAME_HEIGHT, 800)
        cam.set_prop(cv2.CAP_PROP_EXPOSURE, 10)
        cam.set_prop(cv2.CAP_PROP_BRIGHTNESS, 0)
        cam.start()
    server.start()

if __name__ == "__main__":
    main()
