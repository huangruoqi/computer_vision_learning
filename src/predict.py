import os
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame
import sys

MODEL_NAME = "kind_of_dumb"
FPS = 10


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "model", MODEL_NAME)))
from label_config import LABELS


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# mp_hands = mp.solutions.hands
clock = pygame.time.Clock()

LSTM = tf.keras.models.load_model(os.path.join("model", MODEL_NAME))

def convert(landmarks):
    nose = landmarks[0]
    result = []
    for landmark in landmarks[0:25]:
        x, y, z, v = landmark.x, landmark.y, landmark.z, landmark.visibility
        result.append(x - nose.x)
        result.append(y - nose.y)
        result.append(z - nose.z)
        result.append(v)
    return np.array(result)


cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if results.pose_landmarks is not None:
            # Model prediction
            inputs = convert(results.pose_world_landmarks.landmark)
            outputs = LSTM.predict(np.array([inputs]), verbose=0)
            print([LABELS[next(filter(lambda x: x[1]==max(output), enumerate(output)))[0]] for output in outputs][0])
            landmark = results.pose_landmarks.landmark
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            )
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow("Pose Classification", cv2.flip(image, 1))
        if cv2.waitKey(1) & 0xFF == 27:
            break
        delta_time = clock.tick(FPS)
cap.release()
