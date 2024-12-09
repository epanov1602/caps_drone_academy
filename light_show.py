from djitellopy import Tello
from time import sleep

# connect to the drone (but don't call 'streamon', since we don't need video)
drone = Tello()
drone.connect()


# which functions do we need in light show? start with these
def fly_square(length):
    drone.move_forward(length)
    drone.move_right(length)
    drone.move_back(length)
    drone.move_left(length)


def fly_circles(seconds, velocity):
    drone.send_rc_control(0, velocity, 0, 100)
    sleep(seconds)

def go_up(seconds):
    drone.send_rc_control(0, 0, 100, 0)
    sleep(seconds)
    drone.send_rc_control(0, 0, 0, 0)
    sleep(0.2)


# wait for someone to press enter?
#print("Press Enter, before drone draws three squares")
#pressed = input()


#  -- go up for 0.8 seconds?
go_up(0.8)

#  -- do three squares of size 50 centimeters?
for lap in range(3):
    fly_square(50)

#  -- maybe fly some circles for 6 seconds
fly_circles(seconds=6.0, velocity=50)

#  -- stop the movement and land
drone.send_rc_control(0, 0, 0, 0)
drone.land()
