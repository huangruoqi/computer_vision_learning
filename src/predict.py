import os
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# mp_hands = mp.solutions.hands
LSTM = tf.keras.models.load_model(os.path.join("model", "LSTM_##"))

def convert(landmarks):
    nose = landmarks[0]
    result = []
    for landmark in landmarks[0:25]:
        x, y, z = landmark.x, landmark.y, landmark.z
        result.append(x - nose.x)
        result.append(y - nose.y)
        result.append(z - nose.z)
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
        if not results.pose_landmarks:
            # Model prediction
            inputs = convert(results.pose_world_landmarks)
            output = LSTM.predict(inputs)
            print(output)
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
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
