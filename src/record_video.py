import cv2
import numpy as np
import os
import time
from _thread import start_new_thread
import pygame

MAX_TIME = 3 * 60
FPS = 10
clock = pygame.time.Clock()
# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # change to available camera
stop = False


def record_until(max_time):
    time.sleep(max_time)
    global stop
    stop = True


# Check if camera opened successfully
if cap.isOpened() == False:
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter(
    os.path.join("video", f"{int(time.time())}.mp4"),
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (frame_width, frame_height),
)

start_new_thread(record_until, (MAX_TIME,))

while True:
    if stop:
        break
    ret, frame = cap.read()

    if ret == True:
        # Write the frame into the file 'output.avi'
        image = frame.copy()
        out.write(frame)

        # uncomment this for display available
        cv2.imshow("Recording", cv2.flip(image, 1))
        cv2.waitKey(1)

        delta_time = clock.tick(FPS)
        # print(f"FPS: {1000/delta_time}")

    # Break the loop
    else:
        print("No image avaliable")
        break

# When everything done, release the video capture and video write objects
cap.release()
out.release()
