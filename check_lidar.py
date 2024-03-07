import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar
import csv
from array import *

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320,240)) # Map Display resolution
pygame.mouse.set_visible(False)
lcd.fill((0,0,0)) # Map Display is black initially
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

# Registering the Lidar Data
file_Open = open("data01.csv", "w")
data= "Data; \n"
file_Open.write(data)
file_Open.close()

# variables
max_distance = 0

def process_data(data):
    global max_distancea
    lcd.fill((0,0,0))
    for angle in range(360):
        distance = data[angle]
        if distance > 0:
            # These are in polar coordinate system
            # We convert it into cartesian coordinate system
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
            lcd.set_at(point, pygame.Color(255, 255, 255)) # white pixels to identify objects
    pygame.display.update() # updating the map

scan_data = [0]*360
# an endless loop, as long the data is sending or the loop is not stopped.
try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (quality, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)
 
except KeyboardInterrupt:
    print('Stoping.')

lidar.stop()
lidar.disconnect()
print("LiDAR Disconnected.")
