import cv2
import numpy as np
import pandas
import os
import mediapipe as mp
import sys
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from label_config import VIDEO_NAME

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# repeating 0 times means only convert one time.
REPEAT = 0
DATA_NAME = VIDEO_NAME

def data_to_csv(data, labels, filename):
    """
    data = [
        [Landmark0, Landmark1, ... , landmark32], # frame 1
        [Landmark0, Landmark1, ... , landmark32], # frame 2
        [Landmark0, Landmark1, ... , landmark32], # frame 3
        ...
    ]
    """
    """
    prepared_data = {
        '0x': [frame 1's Landmark0.x, frame 2's Landmark0.x, ... , frame n's Landmark0.x],
        '0y': [frame 1's Landmark0.y, frame 2's Landmark0.y, ... , frame n's Landmark0.y],
        '0z': [frame 1's Landmark0.z, frame 2's Landmark0.z, ... , frame n's Landmark0.z],
        '0v': [frame 1's Landmark0.v, frame 2's Landmark0.v, ... , frame n's Landmark0.v],
        ...
        '32x': [frame 1's Landmark32.x, frame 2's Landmark32.x, ... , frame n's Landmark32.x],
        '32y': [frame 1's Landmark32.y, frame 2's Landmark32.y, ... , frame n's Landmark32.y],
        '32z': [frame 1's Landmark32.z, frame 2's Landmark32.z, ... , frame n's Landmark32.z],
        '32v': [frame 1's Landmark32.v, frame 2's Landmark32.v, ... , frame n's Landmark32.v],
    } # x, y, z - world coordnates | v - visibility
    """
    prepared_data = {
        f"{j}{i}": list(
            map(
                lambda x: next(filter(lambda y: y[0].name[0] == j, x.ListFields()))[1],
                v,
            )
        )
        for i, v in enumerate(list(zip(*data)))
        for j in "xyzv"
    }
    prepared_data["label"] = labels
    df = pandas.DataFrame(data=prepared_data)
    df.to_csv(os.path.join("data", f"{filename}.csv"))


# convert origin to nose coordinates
def convert(landmarks):
    nose = landmarks[0]
    for landmark in landmarks:
        x, y, z = landmark.x, landmark.y, landmark.z
        landmark.x = x - nose.x
        landmark.y = y - nose.y
        landmark.z = z - nose.z
    # only need upper body coordinates
    return landmarks[0:25]


# video_names = os.listdir("video")
# for video_name in video_names:
try:
    labels = pandas.read_csv(os.path.join("data", f"{VIDEO_NAME}_labels.csv"))[
        "label"
    ]
    skip_frames = [True] * (len(labels) * (REPEAT+1))
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        data = []
        i = 0

        for j in range(REPEAT+1):
            cap = cv2.VideoCapture(os.path.join("video", VIDEO_NAME))
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print(f"Finish estimation for <{VIDEO_NAME}>")
                    break

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                if results.pose_landmarks:
                    converted_landmarks = convert(results.pose_world_landmarks.landmark)
                    data.append(converted_landmarks)
                    skip_frames[i] = False
                else:
                    print(f"No pose found for <frame {i}>")
                i += 1

                # Draw the pose annotation on the image.
                # image.flags.writeable = True
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # mp_drawing.draw_landmarks(
                #     image,
                #     results.pose_landmarks,
                #     mp_pose.POSE_CONNECTIONS,
                #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                # )

                # # uncomment this for display available
                # cv2.imshow("MediaPipe Pose", cv2.flip(image, 1))
                # if cv2.waitKey(1) & 0xFF == 27:
                #     break
            cap.release()

        filtered_labels_with_unlabeled = []
        for k in range(len(labels)*(REPEAT+1)):
            if not skip_frames[k]:
                filtered_labels_with_unlabeled.append(labels[k%len(labels)])
        filtered_data = []
        filtered_labels = []
        for k in range(len(data)):
            if filtered_labels_with_unlabeled[k] != "Unlabeled":
                filtered_data.append(data[k])
                filtered_labels.append(filtered_labels_with_unlabeled[k])
        data_to_csv(filtered_data, filtered_labels, DATA_NAME if REPEAT==0 else f"{DATA_NAME}x{REPEAT+1}")

except FileNotFoundError as e:
    print(
        f"Please edit `label_config.py` and label <{VIDEO_NAME}> with `make label`"
    )
