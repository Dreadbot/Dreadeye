import cv2
from camera_utils import Camera
from mjpeg_streamer import MjpegServer

IP_ADDRESS = "10.36.56.15" # should match coprocessor

server = MjpegServer(IP_ADDRESS, 1181)

# all measurements in Meters and Degrees
cams = [
        #port num X-back Y-      Z-down  yaw  pitch-down from horizontal
    Camera(0, 0, -0.332, -0.219, -0.192, 45, -20, server),
    Camera(2, 1, -0.332, 0.219, -0.192, -45, -20, server),
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
        server.start()

if __name__ == "__main__":
    main()
