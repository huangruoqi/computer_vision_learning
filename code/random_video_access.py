import pims
import psutil
import copy
import time
first = time.time()    
v = []
for i in range(100):
    v.append(pims.Video("video/test2.mp4"))

while 1:
    pass







second = time.time()
print(second-first)
# v1 = pims.Video('video/test2.mp4')
# ram = psutil.virtual_memory().available
# frame_buffer_length = int(ram / 1280 / 720 / 3 * .7) 
# print(frame_buffer_length)
# ## let o be the object whose size you want to measure
# a = []
# for i in range(frame_buffer_length):
#     a.append(v[i])