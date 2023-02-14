import os
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from collections import deque
import pandas as pd

import pygame

FPS = 10
clock = pygame.time.Clock()

import sys
import random
import time
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from label_config import labels

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# mp_hands = mp.solutions.hands
LSTM = tf.keras.models.load_model(os.path.join("model", "kind_of_dumb"))

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
            outputs = LSTM.predict(np.array([inputs]))
            print([labels[next(filter(lambda x: x[1]==max(output), enumerate(output)))[0]] for output in outputs])
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

def split_data_without_label(df, valid_size=0.1, test_size = 0.2):
    df_input = df.copy()
    df_target = df_input.pop('label')
    x_train, x_valid, x_test = [], [], []
    y_train, y_valid, y_test = [], [], []
    n_test = int(len(df_input) * test_size)
    n_valid = int(len(df_input) * valid_size)
    n_train = len(df_input) - n_test - n_valid
    for i, row in enumerate(df_input.itertuples(index=False)):
        (x_train if i < n_train else x_valid if i < n_train+n_valid else x_test).append(row)
        (y_train if i < n_train else y_valid if i < n_train+n_valid else y_test).append(df_target[i])
    return np.array(x_train), np.array(y_train),np.array(x_valid), np.array(y_valid),np.array(x_test), np.array(y_test)
    

labels2int = {b:a for a, b in enumerate(labels+['Unlabeled'])}

def convert_df_labels(df1, labels2int):
    df = df1.copy()
    for i in range(len(df)):
        label = df['label'][i]
        df.at[i, 'label'] = labels2int[label]
    return df

# data = [
#     "1676004101"
# ]
# DBs = [pd.read_csv(os.path.join("data", f"{name}.mp4.csv"), index_col=0) for name in data]
# DB = pd.concat(DBs, axis=0, ignore_index=True, sort=False)
# DB = convert_df_labels(DB, labels2int)
# x_train, y_train, x_valid, y_valid, x_test, y_test = split_data_without_label(DB, 0, 0)

# for i in range(0, len(x_train), 20):
#     outputs = LSTM.predict(x_train[i:i+20])
#     print([(labels+["Unlabeled"])[next(filter(lambda x: x[1]==max(output), enumerate(output)))[0]] for output in outputs])
