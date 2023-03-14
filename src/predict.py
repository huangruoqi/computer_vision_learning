import os
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame
import sys
import json

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from mutils import convert, offset, Preprocessor

MODEL_NAME = "Score"
FPS = 10
TIMESTAMPS = 16


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# mp_hands = mp.solutions.hands
clock = pygame.time.Clock()

MODEL = tf.keras.models.load_model(os.path.join("model", MODEL_NAME))
input_buffer = []

cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    previous_landmarks = None
    preprocessor = Preprocessor()
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
            converted_landmarks = convert(results.pose_world_landmarks.landmark)
            if previous_landmarks is None:
                previous_landmarks = converted_landmarks
            else:
                offset_landmarks = offset(converted_landmarks, previous_landmarks)
                previous_landmarks = converted_landmarks
                input_buffer.append(offset_landmarks)
                if len(input_buffer) >= TIMESTAMPS:
                    inputs = np.array([preprocessor.transform(np.array(input_buffer))])
                    outputs = MODEL.predict(inputs, verbose=0)
                    print(outputs)
                    # print([LABELS[next(filter(lambda x: x[1]==max(output), enumerate(output)))[0]] for output in outputs])
                    input_buffer.clear()
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
