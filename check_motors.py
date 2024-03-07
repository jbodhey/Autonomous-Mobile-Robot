from gpiozero import Robot
from time import sleep

# Initialsing the left / right motors
robot = Robot(right = (4,24,19), left = (17,22,18))

# Forward movement
robot.forward(0.50)
sleep(1)
robot.stop()
sleep(1)

# Backward movement
robot.backward(0.50)
sleep(1)
robot.stop()
sleep(1)

# Move Right
robot.right(0.50)
sleep(1)
robot.stop()
sleep(1)

# Move Left
robot.left(0.50)
sleep(1)
robot.stop()
sleep(1)

# Make a right circular motion
robot.forward(0.50, curve_right = 0.8)
sleep(5)
robot.stop()
sleep(1)

# Make a left circular motion
robot.forward(0.50, curve_left = 0.8)
sleep(5)
robot.stop()
sleep(1)
