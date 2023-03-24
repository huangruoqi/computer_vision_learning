import cv2
import numpy as np
import pandas
import os
import mediapipe as mp

# import mediapipe.python.solutions.pose as mp_pose

from .vutils import load_settings
from .mutils import convert, offset

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# repeating 0 times means only convert one time.
REPEAT = 0

settings = load_settings()
labels2int = {b: a for a, b in enumerate(settings["labels"])}


def data_to_csv_back_up(data, labels, filename):
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


def data_to_csv(data, labels, filename):
    """without visibility"""
    prepared_data = {f"{'xyz'[i%3]}{i//3}": v for i, v in enumerate(list(zip(*data)))}
    """with visibility"""
    # prepared_data = {f"{'xyzv'[i%4]}{i//4}": v for i, v in enumerate(list(zip(*data)))}

    prepared_data["label"] = labels
    df = pandas.DataFrame(data=prepared_data)
    df.to_csv(os.path.join("data", f"{filename}.csv"))


def convert_video_with_label(video_name):
    labels = pandas.read_csv(os.path.join("data", f"{video_name}_labels.csv"))["label"]
    skip_frames = [True] * (len(labels) * (REPEAT + 1))
    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        data = []
        i = 0

        for j in range(REPEAT + 1):
            cap = cv2.VideoCapture(os.path.join("video", video_name))
            previous_landmarks = None
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print(f"Finish estimation for <{video_name}>")
                    break

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                if results.pose_landmarks:
                    converted_landmarks = convert(results.pose_world_landmarks.landmark)
                    if previous_landmarks is None:
                        previous_landmarks = converted_landmarks
                    else:
                        """without offset"""
                        final_landmarks = converted_landmarks
                        """with offset"""
                        # final_landmarks = offset(converted_landmarks, previous_landmarks)

                        previous_landmarks = converted_landmarks
                        data.append(final_landmarks)
                        skip_frames[i] = False
                else:
                    print(f"No pose found for <frame {i}>")
                i += 1
            cap.release()

        filtered_labels_with_unlabeled = []
        for k in range(len(labels) * (REPEAT + 1)):
            if not skip_frames[k]:
                filtered_labels_with_unlabeled.append(labels[k % len(labels)])
        filtered_data = []
        filtered_labels = []
        for k in range(len(data)):
            if filtered_labels_with_unlabeled[k] != "Unlabeled":
                filtered_data.append(data[k])
                filtered_labels.append(filtered_labels_with_unlabeled[k])
        data_to_csv(
            filtered_data,
            filtered_labels,
            video_name if REPEAT == 0 else f"{video_name}x{REPEAT+1}",
        )
