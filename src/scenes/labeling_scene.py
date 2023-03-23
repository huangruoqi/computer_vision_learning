from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.pixel_display import PixelDisplay
from UI_BASE.UI.components.slider import Slider
from UI_BASE.UI.utils import IMAGE
from ..vutils import VideoContainer
import os
import pandas
import numpy
import cv2

VIDEO_RESIZE_DIMENSION = 640, 480


class LabelingScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(LabelingScene, self).__init__(
            screen,
            bg_file=os.path.join("assets", "images", "white.png"),
            *args,
            **kwargs,
        )
        self.fps = kwargs.get("fps")
        screen_fps = 30
        self.fps_ratio = screen_fps / self.fps
        self.frame_count = 0

        self.labels = kwargs.get("labels")
        self.labels.append("Unlabeled")
        self.playing = False
        self.add(
            "play_pause",
            Button(
                image_file=(os.path.join("assets", "images", "play-solid.png")),
                height=50,
                x=25,
                y=self.height - 30,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.play(),
                can_hover=lambda: not self.slider.dragged,
            ),
        )
        self.add(
            "next",
            Button(
                image_file=(os.path.join("assets", "images", "arrow-right-solid.png")),
                height=50,
                x=self.width - 25,
                y=self.height - 30,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.next(),
                can_hover=lambda: not self.slider.dragged,
            ),
        )
        self.add(
            "save",
            Button(
                image_file=(os.path.join("assets", "images", "floppy-disk.png")),
                height=50,
                x=self.width - 50,
                y=80,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.save(),
                can_hover=lambda: not self.slider.dragged,
            ),
        )
        self.add(
            "close",
            Button(
                text="X",
                text_fontsize=50,
                x=self.width - 50,
                y=30,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.app.change_scene(
                    0, lambda scene: scene.refresh_videos()
                ),
                can_hover=lambda: not self.slider.dragged,
            ),
        )
        self.video_name = None
        self.vc = None

        def on_change(x):
            self.vc.set(int(self.vc.total * x))
            self.slider.set_progress(self.vc.progress())
            arr = self.vc.peek()
            if arr is not None:
                self.set_pixels(arr)

        self.slider = self.add(
            "slider",
            Slider(
                drag_width=self.width - 100 - self.width % 100,
                on_change=on_change,
                x=self.width / 2,
                y=self.height - 30,
                color=(200, 200, 200),
                interval=[0, 1],
                width=20,
                height=50,
            ),
            1,
        )

        video_width, video_height = VIDEO_RESIZE_DIMENSION
        self.pixels = self.add(
            "video",
            PixelDisplay(
                video_width, video_height, self.width / 2, (self.height - 60) / 2
            ),
        )
        self.current_label_index = -1
        self.frame2label = None

        def get_on_click(i):
            def on_click():
                self.current_label_index = i
                self.set_label()

            return on_click

        self.colors = list(ColorBar.colors.keys())
        self.colors[len(self.labels) - 1] = "black"
        for i, label in enumerate(self.labels):
            height = (self.height - 100) // 100 * 100
            x = (50 * i) // height * 200
            y = (50 * i) % height
            self.add(
                f"label_{label}",
                Button(
                    text=label,
                    text_fontsize=50,
                    x=x + 20,
                    y=y + 20,
                    align_mode="TOPLEFT",
                    color=ColorBar.colors[self.colors[i]],
                    on_click=get_on_click(i),
                    can_hover=lambda: not self.slider.dragged,
                ),
            )
        self.bar = self.add(
            "progress_bar",
            ColorBar(
                width=self.width - self.width % 100 - 100,
                height=50,
                x=self.width / 2,
                y=self.height - 30,
                on_click=lambda progress: on_change(progress),
            ),
        )
        self.buffered = self.add(
            "buffer_bar",
            ColorBar(
                width=self.width - self.width % 100 - 100,
                height=9,
                x=self.width / 2,
                y=self.height - 57,
                color="grey",
            ),
        )

    def set_video(self, video_path, video_name):
        self.video_name = video_name
        self.vc = VideoContainer(video_path, 2000)
        self.set_pixels(self.vc.peek())
        self.current_label_index = -1
        self.frame2label = numpy.array([-1] * self.vc.total)
        self.set_buffered_bar()

    def set_pixels(self, frame):
        video_width, video_height = VIDEO_RESIZE_DIMENSION
        res = cv2.resize(
            frame, dsize=(video_height, video_width), interpolation=cv2.INTER_CUBIC
        )
        self.pixels.set(res)

    def play(self):
        self.playing = True
        btn = self.get("play_pause")
        pos = btn.get_pos()
        btn.set_temp_image(
            IMAGE(os.path.join("assets", "images", "pause-solid.png"), False), height=50
        ).set_pos(pos)
        btn.on_click = lambda: self.pause()
        self.get("next").hide()
        self.get("save").hide()

    def pause(self):
        self.playing = False
        btn = self.get("play_pause")
        btn.show()
        btn.on_click = lambda: self.play()
        self.get("next").show()
        self.get("save").show()

    def next(self):
        self.set_display()

    def save(self):
        df = pandas.DataFrame(
            data={"label": list(map(lambda i: self.labels[i], self.frame2label))}
        )
        df.to_csv(os.path.join("data", f"{self.video_name}_labels.csv"))

    def set_display(self):
        self.set_label()
        self.slider.set_progress(self.vc.progress())
        arr = self.vc.next()
        if arr is not None:
            self.set_pixels(arr)

    def set_buffered_bar(self):
        self.vc.refresh_bound()
        l, r = self.vc.left_bound, self.vc.right_bound
        np_arr = numpy.array(
            [
                (150, 150, 150)
                if l <= i * self.vc.total // 100 <= r
                else (255, 255, 255)
                for i in range(100)
            ]
        )
        self.buffered.set_arr(np_arr)

    def set_label(self):
        self.frame2label[self.vc.absolute_index] = self.current_label_index
        self.bar.set_color(
            int(self.vc.absolute_index / self.vc.total * 100),
            self.colors[self.current_label_index],
        )

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked):
        super().update(delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked)
        self.set_buffered_bar()
        if not self.playing:
            return
        if not pressed:
            self.frame_count += 1
            if self.frame_count >= self.fps_ratio:
                self.set_display()
                self.frame_count -= self.fps_ratio

    def close(self):
        if self.vc is not None:
            self.vc.close()
        return super().close()
