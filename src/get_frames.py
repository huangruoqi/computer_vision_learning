import cv2
import os

join = os.path.join
cap = cv2.VideoCapture(join("video", "frontview.MOV"))  # change to available camera

frame = 0
low = 37140
high = 37380
step = 30
while cap.isOpened():
    success, image = cap.read()
    print(frame)
    frame += 1
    if not success:
        break

    if low <= frame and frame%step==0:
        cv2.imwrite(join("image", f"{frame}.png"), image)
    if frame > high:
        break

cap.release()

