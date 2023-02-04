import pims
v = pims.Video('video/test2.mp4')
import psutil
    
ram = psutil.virtual_memory().available
frame_buffer_length = int(ram / 1280 / 720 / 3 * .7) 
print(frame_buffer_length)
## let o be the object whose size you want to measure
a = []
for i in range(frame_buffer_length):
    a.append(v[i])
print("d")
while 1:
    pass