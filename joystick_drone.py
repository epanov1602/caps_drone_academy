from djitellopy import Tello
from time import sleep
import cv2
import pygame

pygame.init()
pygame.joystick.init()
n_joysticks = pygame.joystick.get_count()
assert n_joysticks == 1, "ERROR: we expect to see exactly one connected joystick, but we have " + str(n_joysticks)

# we will be using joystick number 0
joystick0 = pygame.joystick.Joystick(0)
print("joystick 0 has " + str(joystick0.get_numbuttons()) + " buttons")
print("joystick 0 has " + str(joystick0.get_numaxes()) + " axes")

# connect to the drone
drone = Tello()
drone.connect()
drone.streamon()


# everything below happens in a "while" loop
while True:
    # 0. grab a video frame from drone camera, and show it in "car video" window
    frame = drone.get_frame_read().frame
    cv2.imshow("car video", frame)
    cv2.waitKey(1)

    # 1. get the new joystick events (if nothing new, then sleep for 0.01s and try again
    if not pygame.event.get():
        sleep(0.01)
        continue


    # 2. are some buttons pressed?
    if joystick0.get_button(0):
        drone.takeoff()
    # maybe add a button to call drone.land() ?
    # maybe also add buttons to call drone.flip_forward(), drone.flip_back(), drone.flip_right(), drone.flip_left() ?

    up_down_velocity, forward_velocity, turn_velocity, roll_velocity = 0, 0, 0, 0

    # 3. if drone is flying, set the drone velocity from the sticks of the joystick
    if drone.is_flying:
        turn_velocity = -100 * joystick0.get_axis(0)  # if the axis is at -0.5, I want the speed to be +50
        # maybe set some other velocities from other sticks?

    # 4. send those velocities to the drone
    drone.send_rc_control(int(roll_velocity), int(forward_velocity), int(up_down_velocity), int(turn_velocity))
