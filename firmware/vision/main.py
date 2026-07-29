import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'hand_landmarker.task')

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Hand tracking started. Press 'ESC' in the video window to exit.")

def interp(val, input_min, input_max, output_min, output_max):
    val = max(input_min, min(input_max, val))
    return output_min + (val - input_min) * (output_max - output_min) / (input_max - input_min)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            h, w, _ = frame.shape

            wrist = hand_landmarks[0]
            index_tip = hand_landmarks[8]
            middle_tip = hand_landmarks[12]
            ring_tip = hand_landmarks[16]
            pinky_tip = hand_landmarks[20]
            thumb_tip = hand_landmarks[4]

            wx, wy = int(wrist.x * w), int(wrist.y * h)
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            mx, my = int(middle_tip.x * w), int(middle_tip.y * h)
            rx, ry = int(ring_tip.x * w), int(ring_tip.y * h)
            px, py = int(pinky_tip.x * w), int(pinky_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

            dist_thumb = math.hypot(tx - wx, ty - wy)
            dist_index = math.hypot(ix - wx, iy - wy)
            dist_middle = math.hypot(mx - wx, my - wy)
            dist_ring = math.hypot(rx - wx, ry - wy)
            dist_pinky = math.hypot(px - wx, py - wy)

            angle_thumb = int(interp(dist_thumb, 50, 250, 0, 90))
            angle_index = int(interp(dist_index, 50, 250, 0, 90))
            angle_middle = int(interp(dist_middle, 50, 250, 0, 90))
            angle_ring = int(interp(dist_ring, 50, 250, 0, 90))
            angle_pinky = int(interp(dist_pinky, 50, 250, 0, 90))

            cv2.line(frame, (wx, wy), (ix, iy), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (mx, my), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (rx, ry), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (px, py), (255, 0, 0), 3)
            cv2.line(frame, (wx, wy), (tx, ty), (255, 0, 0), 3)
            
            cv2.putText(frame, f'Index Servo Angle: {angle_index} deg', (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f'Middle Servo Angle: {angle_middle} deg', (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f'Ring Servo Angle: {angle_ring} deg', (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f'Pinky Servo Angle: {angle_pinky} deg', (30, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f'Thumb Servo Angle: {angle_thumb} deg', (30, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if angle_thumb < 50 and angle_index < 50 and angle_middle < 50 and angle_ring < 50 and angle_pinky < 50:
                cv2.putText(frame, 'Hand Closed', (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(frame, 'Hand Opened', (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    cv2.imshow('Robotic Hand Vision Sandbox', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()