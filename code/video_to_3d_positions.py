import cv2
import mediapipe as mp
import numpy as np
import pandas
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# world coordinates are defined as: origin at the middle of left and right hips
# might need to transform to other Landmark as origin
# and time data can be added as well

def data_to_csv(data, filename):
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
        f"{i}{j}": list(
            map(lambda x: next(filter(lambda y: y[0].name[0] == j, x.ListFields()))[1], v)
        )
        for i, v in enumerate(list(zip(*data)))
        for j in "xyzv"
    }

    df = pandas.DataFrame(data=prepared_data)
    df.to_csv(os.path.join("data" ,f"{filename}.csv"))



video_names = os.listdir("video")
for video_name in video_names:
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        data = []
        cap = cv2.VideoCapture(os.path.join('video', video_name))
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
                data.append(results.pose_world_landmarks.landmark)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            
            # uncomment this for display available
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            
            if cv2.waitKey(5) & 0xFF == 27:
              break
        cap.release()
        data_to_csv(data, video_name)

        # remove video after convertion finish
        # os.remove(os.path.join('video', video_name))


