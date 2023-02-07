import cv2
import numpy as np
import os
from picamera.array import PiRGBArray
from picamera import PiCamera

rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
