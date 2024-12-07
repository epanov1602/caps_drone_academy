from djitellopy import Tello
from time import sleep

# connect to the drone (but don't call 'streamon', since we don't need video)
drone = Tello()
drone.connect()

# take off and then wait for someone to press enter
drone.send_rc_control(0, 0, 0, 0)
drone.takeoff()

print("Press Enter, before drone draws three squares")
pressed = input()

drone.send_rc_control(0, 0, 100, 0)
sleep(0.8)
drone.send_rc_control(0, 0, 0, 0)
sleep(0.2)

#  -- move forward 25 cm?
#drone.move_forward(25)

#  -- and do three squares of size 50 centimeters?
#for lap in range(3):
#    drone.move_forward(50)
#    drone.move_right(50)
#    drone.move_back(50)
#    drone.move_left(50)

#  -- maybe fly some circles for 6 seconds
drone.send_rc_control(0, 100, 0, 100)
sleep(6)

#  -- stop the movement and land
drone.send_rc_control(0, 0, 0, 0)
drone.land()