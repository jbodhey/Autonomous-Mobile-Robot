from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Initialize the camera
camera = PiCamera()
camera.resolution = (864, 544)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(864, 544))
# allow the camera to warmup
time.sleep(0.1)
start_time = time.time()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # capturing the video frames in image variable
    image = frame.array

    # show the frame
    cv2.imshow("Frame", image)

    # Press Spacebar key to stop the loop
    if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # after 10 seconds, break from the loop
    if time.time() - start_time > 10:
        break
