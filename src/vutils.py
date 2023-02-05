import pims
import time
import threading


class VideoContainer:
    def __init__(self, path, size):
        self.size = size * 4 // 4
        self.next_frame = self.size // 4
        self.previous_frame = self.size // 2
        self.absolute_index = 0

        self.circular_list_data = [None]*self.size
        self.circular_list_done =  [False]*self.size
        self.current_index = 0

        self.stop = False
        self.video = VideoRetriever(path)
        for i in range(self.previous_frame+self.next_frame):
            self.put(self.video.get(i), i)

        self.loading_thread = threading.Thread(target=self.loop, args=())
        self.loading_thread.start()

    def loop(self):
        while not self.stop:
            time.sleep(0.1)
            if self.circular_list_done[self.mod(self.current_index + self.next_frame)] is False:
                start = self.current_index+self.next_frame
                abs_start = self.absolute_index+self.next_frame
                if self.circular_list_done[self.mod(start-1)] is False:
                    while self.circular_list_done[self.mod(start-1)] is False:
                        start = self.mod(start - 1)
                        abs_start-=1
                for i in range(self.next_frame):
                    self.put(self.video.get(abs_start+i), start+i)

    def next(self):
        self.absolute_index += 1
        if self.absolute_index - self.previous_frame > 0:
            self.circular_list_done[self.mod(self.current_index - self.previous_frame)] = False
        self.current_index = self.mod(self.current_index + 1)
        result = self.circular_list_data[self.current_index]
        return result

    def put(self, data, index):
        self.circular_list_data[self.mod(index)] = data
        self.circular_list_done[self.mod(index)] = True



    def set(self, index):
        if self.absolute_index - self.previous_frame < index < self.absolute_index + self.next_frame:
            self.current_index = self.mod(self.current_index + self.absolute_index - index)

        self.absolute_index = index

    def mod(self, index):
        return index % self.size

    def close(self):
        self.stop = True
        self.loading_thread.join()

class VideoRetriever:
    def __init__(self, path):
        self.current_index = 0
        self.cap = pims.Video(path)

    def get(self, index):
        print(index)
        for i in range(self.current_index + 1, index):
            self.cap[i]
        self.current_index = index
        return self.cap[index]
