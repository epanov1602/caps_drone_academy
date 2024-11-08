import pygame
from time import sleep

pygame.init()
pygame.joystick.init()
n_joysticks = pygame.joystick.get_count()
assert n_joysticks == 1, "ERROR: we expect to see exactly one connected joystick, but we have " + str(n_joysticks)

# we will be using joystick number 0
joystick0 = pygame.joystick.Joystick(0)
print("joystick 0 has " + str(joystick0.get_numbuttons()) + " buttons")
print("joystick 0 has " + str(joystick0.get_numaxes()) + " axes")

while True:
    # 1. get the new joystick events (if nothing new, then sleep for 0.01s and try again
    if not pygame.event.get():
        sleep(0.01)
        continue

    # 2. are some buttons pressed?
    if joystick0.get_button(0):
        print("button 0 pressed")
    if joystick0.get_button(1):
        print("button 1 pressed")
    if joystick0.get_button(2):
        print("button 2 pressed")
    # ... add more if you need

    # 3. are some sticks pushed? (a typical stick normally has two axes: an up-down axis and a right-left axis)
    if joystick0.get_axis(0) > 0.1 or joystick0.get_axis(0) < -0.1:
        print("axis 0 is at " + str(joystick0.get_axis(0)))
    if joystick0.get_axis(1) > 0.1 or joystick0.get_axis(1) < -0.1:
        print("axis 1 is at " + str(joystick0.get_axis(1)))
    # ... add more if you need

    ## 4. if I want button 0 to be a play-pretend takeoff, then my code is
    #if joystick0.get_button(0):
    #    print("drone taking off")  # with a real drone I should write: drone.takeoff()

