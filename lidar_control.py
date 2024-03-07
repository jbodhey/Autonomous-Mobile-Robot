import os
from math import cos, sin, pi, floor
import pygame
import csv
from adafruit_rplidar import RPLidar
from array import *

# initializing Lidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

max_distance = 0

def process_data(data):
    global max_distance
    i = 160
    count = 0
    # only checking in front of the car
    for angle in range(160, 200):
        distance = data[angle]
        if distance > 0:
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)

            # the car is 24.8 cm long, if the obstracle is 
            # in the range of 18 cm in front of the car
            # then the count will be 1, and the car will stop.
            while i <= 199:
                if (data[i] - 248 <= 180) and (data[i] >= 248):
                    count = count + 1
                    break
                i = i + 1
            
            if count != 0:
                print("Stop")
                with open("lidar_status.txt", "w") as f:
                    f.write("Stop")
                    f.close()
                # afterwards, if there is no object, then the
                # count will be again 0 to move forward.
                if (data[i] - 248 >= 180) and (data[i] >= 248):
                    count = 0
                    break
            
            else:
                print("Forward")
                with open("lidar_status.txt", "w") as f:
                    f.write("Forward")
                    f.close()
# scan data array
scan_data = [0]*360 

try:
    print(RPLidar.info)
    for scan in lidar.iter_scans():
        for (quality, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stoping.')

lidar.stop()
lidar.disconnect()
print("LiDAR Disconnected.")
