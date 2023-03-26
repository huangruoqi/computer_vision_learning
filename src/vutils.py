import cv2
import pims
import time
import threading
import json
import os


def load_settings():
    setting_file = open(os.path.join("assets", "settings.json"))
    settings = dict(json.load(setting_file))
    setting_file.close()
    return settings


def save_settings(settings):
    with open(os.path.join("assets", "settings.json"), "w") as f:
        json.dump(settings, f)


class VideoContainer:
    def __init__(self, path, size, width=None, height=None):
        self.size = size * 4 // 4
        self.next_frame = self.size // 4
        self.previous_frame = self.size // 2
        self.absolute_index = 0
        self.left_bound = 0
        self.right_bound = 0
        self.resizing = True
        self.width = width
        self.height = height
        if width is None or height is None:
            self.resizing = False

        self.circular_list_data = [None] * self.size
        self.current_index = 0

        self.stop = False

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
        for i in range(self.next_frame):
            self.put(self.video.get(i + start), i)
        self.left_bound = start - 1
        self.right_bound = start + self.next_frame
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
            if abs_start >= self.total:
                start -= abs_start - self.right_bound
                abs_start = self.right_bound
                for i in range(self.next_frame):
                    if self.reloading:
                        break
                    if abs_start + i >= self.total:
                        break
                    self.put(self.video.get(abs_start + i), start + i)
                    self.right_bound = abs_start + i + 1
                continue
            if abs_start >= self.right_bound:
                start -= abs_start - self.right_bound
                abs_start = self.right_bound
                for i in range(self.next_frame):
                    if self.reloading:
                        break
                    self.put(self.video.get(abs_start + i), start + i)
                    self.right_bound = abs_start + i + 1

    def next(self):
        result = self.peek()
        if (
            self.absolute_index < self.total - 1
            and self.absolute_index < self.right_bound - 1
        ):
            self.absolute_index += 1
            self.current_index = self.mod(self.current_index + 1)
        return result

    def refresh_bound(self):
        if self.absolute_index + self.previous_frame > self.total:
            return
        self.left_bound = max(
            self.absolute_index - self.previous_frame, -1, self.left_bound
        )

    def peek(self):
        return self.circular_list_data[self.current_index]

    def put(self, data, index):
        if data is not None:
            if self.resizing:
                data = cv2.resize(
                    data, dsize=(self.width, self.height), interpolation=cv2.INTER_CUBIC
                )
            self.circular_list_data[self.mod(index)] = data.swapaxes(0, 1)
        else:
            self.circular_list_data[self.mod(index)] = data

    def set(self, index):
        if self.left_bound < index < self.right_bound:
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
        if index >= self.total:
            return None
        if index < self.current_index:
            self.cap[0]
            self.current_index = 0
        for i in range(self.current_index + 1, index):
            self.cap[i]
        self.current_index = index
        return self.cap[index]
