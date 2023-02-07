import pims
import time
import threading


class VideoContainer:
    def __init__(self, path, size):
        self.size = size * 4 // 4
        self.next_frame = self.size // 4
        self.previous_frame = self.size // 2
        self.absolute_index = 0

        self.circular_list_data = [None] * self.size
        self.circular_list_done = [False] * self.size
        self.current_index = 0

        self.stop = False
        self.current_index = 0

        self.loading_thread = threading.Thread(target=self.loop, args=())
        self.video = VideoRetriever(path)
        self.total = self.video.total
        self.reloading = False
        self.loading = False
        self.reload()
        self.loading_thread.start()

    def reload(self):
        self.reloading = True
        while self.loading and not self.stop:
            time.sleep(0.1)
        self.current_index = 0
        start = self.absolute_index - self.previous_frame
        self.current_index = self.previous_frame
        if self.absolute_index < self.previous_frame:
            start = 0
            self.current_index = self.absolute_index
        for i in range(self.size):
            self.circular_list_done[i] = False
        for i in range(self.previous_frame + self.next_frame):
            self.put(self.video.get(i + start), i)
        self.reloading = False

    def loop(self):
        while not self.stop:
            self.loading = False
            time.sleep(0.1)
            self.loading = True
            if self.reloading:
                continue
            start = self.current_index + self.next_frame
            abs_start = self.absolute_index + self.next_frame
            if not self.circular_list_done[self.mod(start)]:
                while not self.circular_list_done[self.mod(start - 1)]:
                    start = self.mod(start - 1)
                    abs_start -= 1
                for i in range(self.next_frame):
                    if self.reloading:
                        break
                    self.put(self.video.get(abs_start + i), start + i)

    def next(self):
        if self.absolute_index - self.previous_frame >= 0:
            self.circular_list_done[
                self.mod(self.current_index - self.previous_frame)
            ] = False
        result = self.peek()
        if self.absolute_index<self.total-1:
            self.absolute_index += 1
            self.current_index = self.mod(self.current_index + 1)
        return result
    
    def peek(self):
        if not self.circular_list_done[self.current_index]:
            return None
        return self.circular_list_data[self.current_index]

    def put(self, data, index):
        if data is None:
            self.circular_list_done[self.mod(index)] = False
        else:
            self.circular_list_data[self.mod(index)] = data.swapaxes(0, 1)
            self.circular_list_done[self.mod(index)] = True

    def set(self, index):
        # TODO : dynamic range update
        if (
            self.absolute_index - self.previous_frame
            < index
            < self.absolute_index + self.next_frame
        ):
            self.current_index = self.mod(
                self.current_index + index - self.absolute_index
            )
            self.absolute_index = index
        else:
            self.absolute_index = index
            self.reload()

    def progress(self):
        return self.absolute_index / self.total

    def mod(self, index):
        return index % self.size

    def close(self):
        self.stop = True
        self.loading_thread.join()


class VideoRetriever:
    def __init__(self, path):
        self.current_index = 0
        self.cap = pims.Video(path)
        self.total = len(self.cap)

    def get(self, index):
        if index >= self.total: return None
        if index < self.current_index:
            self.cap[0]
            self.current_index = 0
        for i in range(self.current_index + 1, index):
            self.cap[i]
        self.current_index = index
        return self.cap[index]
