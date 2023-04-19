import cv2
import os

join = os.path.join
cap = cv2.VideoCapture(join("video", "frontview.mov"))  # change to available camera

frame = 0
low = 37140
high = 37380
step = 30
while cap.isOpened():
    success, image = cap.read()
    frame += 1
    if not success:
        break

    if low <= frame < high and frame%step==0:
        cv2.imwrite("image", f"{frame}.png")

