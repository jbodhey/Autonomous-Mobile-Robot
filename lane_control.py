import cv2
import time
from time import sleep
from gpiozero import Robot
from picamera.array import PiRGBArray
from picamera import PiCamera
from math import cos, sin, pi, floor

# initializing camera
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(0.1)
start_time = time.time()
x = 0 # x_coordinate
y = 0 # y_coordinate

# Initialsing the left / right motors
robot = Robot(right = (4,24,19), left = (17,22,18))

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        # capturing frames are in 'BGR' format (Blue-Green-Red)
        image = frame.array
        crop = image[140:-1, 20:310]  # Adjust the cropping region
        
        grayscale = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) # converting BGR to gray format
        Gblur = cv2.GaussianBlur(grayscale, (5, 5), 0) # blurring the image
        ret, thresh = cv2.threshold(Gblur, 190, 255, cv2.THRESH_BINARY) # applying threshold, pixels above 190 intensity will be converted to 255
        contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_NONE) # detecting contours
        
        #highlighting the contours with green border
        cv2.drawContours(crop, contours, -1, (0,255,0), thickness = 1)
        
        # reading the lidar_status
        with open("lidar_status.txt", "r") as status_file:
            status = status_file.read().strip()

        # robot stops if status is 'Stop'
        if status == "Stop":
            robot.stop()
            time.sleep(0.1)
            rawCapture.truncate(0)
            continue

        if len(contours) > 0:

            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(c)

            if M["m00"] != 0:

                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                # x and y coordinates are found

                if x < (crop.shape[1] / 3):
                        
                    print("Turning Left!")
                    robot.forward(0.50, curve_left = 0.4) # adjust the curve acceleration
                
                elif x > (crop.shape[1] * 2 / 3):
                        
                    print("Turning Right!")
                    robot.forward(0.50, curve_right = 0.4) # adjust the curve acceleration
                
                else:

                    print("On Track!")
                    robot.forward(0.50)
        
        else:

            print("Out of Track!")
            robot.stop()
            time.sleep(0.1)

        # highlighting the center point with red crosshair
        cv2.line(crop, (x, 0), (x, 720), (0, 0, 255), 1)
        cv2.line(crop, (0, y), (1280, y), (0, 0, 255), 1)
        #highlighting the contours with green border
        final = cv2.drawContours(crop, contours, -1, (0, 255, 0), 1)
        cv2.imshow("Camera", final)

        # Pressing Spacebar will stop the car
        if cv2.waitKey(1) & 0xFF == ord(' '):
            robot.stop()
            break
        
        rawCapture.truncate(0)

except KeyboardInterrupt:
    robot.stop()
    print("Stopping!")

finally:
    cv2.destroyAllWindows()
