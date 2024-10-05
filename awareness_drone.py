from djitellopy import Tello
import detection
import cv2


# what kind of objects can we detect?
face_detector = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
tracker = detection.TrackerState(detection.create_vit_tracker(), display_confidence=True)


# connect to the drone
drone = Tello()
drone.connect()
drone.streamon()  # start the video stream
x, y, w, h = None, None, None, None
snapshot_number = 0

# everything below happens in a "while" loop
while True:
    # 0. which key did the user press?
    key = cv2.waitKey(1) & 0xFF

    # 1. get one video frame from drone camera and detect people on it
    frame = drone.get_frame_read().frame
    x, y, w, h = detection.detect_biggest_face(face_detector, frame, previous_xywh=(x, y, w, h), tracker=tracker)
    nx, ny, size = detection.to_normalized_x_y_size(frame, x, y, w, h, draw_box=True)
    cv2.imshow("drone video", frame)  # show that video

    # 2. which key did the pilot press? drive the drone accordingly
    up_down_velocity, forward_velocity, turn_velocity, roll_velocity = 0, 0, 0, 0

    if key == ord('t'):
        drone.takeoff()

    if key == ord('l'):
        drone.land()

    if key == ord(' '):  # space = take picture
        snapshot_number = snapshot_number + 1
        cv2.imwrite(f'{snapshot_number}.jpg', frame)

    if key == ord('a'):
        turn_velocity = -50   # -50 is slow left turn, but can be all the way to -100 (faster)
    if key == ord('d'):
        turn_velocity = -50
    if key == ord('w'):
        forward_velocity = +100  # +50 is a slow forward move, but can be as high as +100

    drone.send_rc_control(roll_velocity, forward_velocity, up_down_velocity, turn_velocity)
