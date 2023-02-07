from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.pixel_display import PixelDisplay
from UI_BASE.UI.components.slider import Slider
from UI_BASE.UI.sound import Channel
from UI_BASE.UI.utils import IMAGE, SOUND
from .vutils import VideoContainer
import pygame
import numpy


class LabelingScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(LabelingScene, self).__init__(screen, *args, **kwargs)
        # self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        labels = kwargs.get("labels")
        labels.append("Others")
        self.playing = False
        self.add(
            "play_pause",
            Button(
                image=IMAGE("play-solid.png"),
                height=50,
                x=50,
                y=self.height-30,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.play()
            ),
        )
        self.add(
            "next",
            Button(
                image=IMAGE("arrow-right-solid.png"),
                height=50,
                x=self.width-50,
                y=self.height-30,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.next()
            ),
        )
        self.vc = VideoContainer(kwargs.get("video_path"), 2000)
        def on_change(x):
            self.vc.set(int(self.vc.total * x))
            self.slider.set_progress(self.vc.progress())
            arr = self.vc.peek()
            if arr is not None:
                self.pixels.set(arr)

        self.slider = self.add(
            "slider",
            Slider(
                drag_width=self.width - 100 - self.width%100,
                on_change=on_change,
                x=self.width / 2,
                y=self.height-30,
                color=(200, 200, 200),
                interval=[0, 1],
                width=20,
                height=50,
            ),
            1,
        )

        self.bar = self.add(
            "progress_bar",
            ColorBar(
                width=self.width - self.width % 100 - 100,
                height=50,
                x=self.width / 2,
                y=self.height-30,
                on_click=lambda progress: on_change(progress),
            ),
        )
        video_width, video_height = self.width, self.height-60
        self.pixels = self.add(
            "video", PixelDisplay(video_width,video_height, video_width/ 2, video_height / 2)
        )
        self.pixels.set(self.vc.peek())
        self.current_label_index = -1
        self.frame2label = numpy.array([-1] * self.vc.total)

        def get_on_click(i):
            def on_click():
                self.current_label_index = i
                self.set_label()

            return on_click

        self.colors = list(ColorBar.colors.keys())
        self.colors[len(labels)-1] = "black"
        for i, label in enumerate(labels):
            self.add(
                f"label_{label}",
                Button(
                    text=label,
                    text_fontsize=50,
                    x=60,
                    y=50 + 60 * i,
                    align_mode="TOPLEFT",
                    color=ColorBar.colors[self.colors[i]],
                    on_click=get_on_click(i),
                ),
            )

    def play(self):
        self.playing = True
        btn = self.get("play_pause")
        pos = btn.get_pos()
        btn.set_temp_image(IMAGE("pause-solid.png"), height=50).set_pos(pos)
        btn.on_click = lambda: self.pause()
        self.get("next").hide()

    def pause(self):
        self.playing = False
        btn = self.get("play_pause")
        btn.show()
        btn.on_click = lambda: self.play()
        self.get("next").show()

    def next(self):
        self.set_display()

    def set_display(self):
        self.set_label()
        self.slider.set_progress(self.vc.progress())
        arr = self.vc.next()
        if arr is not None:
            self.pixels.set(arr)

    def set_label(self):
        self.frame2label[self.vc.absolute_index] = self.current_label_index
        self.bar.set_color(
            int(self.vc.absolute_index / self.vc.total * 100),
            self.colors[self.current_label_index],
        )

    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
        if not self.playing:
            return
        if not pressed:
            self.set_display()

    def close(self):
        self.vc.close()
        return super().close()
