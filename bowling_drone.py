from djitellopy import Tello
import detection
import cv2
import pupil_apriltags as apriltags
#from ultralytics import YOLO

# what kind of objects can we detect?
face_detector = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
tag_detector = apriltags.Detector(families="tag36h11", quad_sigma=0.2)
tracker = detection.TrackerState(detection.create_vit_tracker(), display_confidence=True)
#model = YOLO("resources/yolov8s.pt")  # model to detect common objects like "person", "car", "cellphone" (see "COCO")


# connect to the drone
drone = Tello()
drone.connect()
drone.streamon()  # start the video stream

x, y, w, h = None, None, None, None
last_seen_nx = 0

# everything below happens in a "while" loop
while True:
    # 0. which buttons did the user press?
    key = cv2.waitKey(1) & 0xFF
    if key == ord('l'):
        drone.land()  # L = land
    elif key == ord('t'):
        drone.takeoff()  # T = takeoff
    elif key == ord('f'):
        drone.flip_forward()  # F = flip forward

    # 1. get one video frame from drone camera
    frame = drone.get_frame_read().frame

    # 2. detect an object on that frame
    x, y, w, h = detection.detect_biggest_apriltag(tag_detector, frame, tracker=tracker)
    #x, y, w, h = detection.detect_biggest_face(face_detector, frame, previous_xywh=(x, y, w, h), tracker=tracker)

    # 3. convert X and Y into "normalized nX and nY" (which are = 0, 0 when object in the middle of the screen)
    nx, ny, size = detection.to_normalized_x_y_size(frame, x, y, w, h, draw_box=True)
    if nx is not None:
        last_seen_nx = nx

    # 4. how do we want the drone to move?
    up_down_velocity = 0
    forward_velocity = 0
    turn_velocity = 0
    roll_velocity = 0
    status = ""

    if not drone.is_flying:
        # -- if the drone is not flying, velocity zero please
        up_down_velocity = forward_velocity = turn_velocity = roll_velocity = 0
        status = "not flying"
    elif nx is None:
        # -- if the object is NOT seen now, keep rotation in the direction where it was last seen (if seen)
        turn_velocity = -55 if last_seen_nx < 0 else +55
        status = "looking for object"
    else:
        # -- otherwise fly towards the object
        if nx <= -15:
            """the object is on the left!"""
            status = f"turning left: nx={nx}"
            turn_velocity = -35
            roll_velocity = -40

        if nx >= 15:
            status = f"turning right: nx={nx}"
            """exercise 1: the object is on the right, can you make the drone turn right
             by setting velocities like above?"""

        if ny - size / 2 >= 24:
            status = f"object above: ny={ny}, size={size}"
            """exercise 2: object is too far above, can you make the drone go up by setting up_down_velocity = 30?"""

        if ny + size / 2 <= -2:
            status = f"object us too far below: ny={ny}, size={size}"
            """exercise 3: you want the drone to go down, right?"""

        if status == "":
            forward_velocity = 50
            status = "charge!"

    cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 128), thickness=2)
    cv2.imshow("drone video", frame)

    # when the object is right in front of us? (nx > -15 and nx < 15 and ny < 20 and ny > -15)

    drone.send_rc_control(roll_velocity, forward_velocity, up_down_velocity, turn_velocity)
