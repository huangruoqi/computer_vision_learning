from UI_BASE.UI.components.numeric_input import NumericInput
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.pixel_display import PixelDisplay
from UI_BASE.UI.components.slider import Slider
from UI_BASE.UI.utils import IMAGE
from ..vutils import VideoContainer, load_settings
import os
import pandas
import numpy
import cv2

VIDEO_RESIZE_DIMENSION = 500, 500


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
        self.upper_bound = 0
        self.lower_bound = 0
        self.pos_dict = {}
        self.angle = 0

        self.add(
            "title",
            Text(text="", align_mode="CENTER", size=30, x=self.width // 2, y=35),
        )

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
                image_file=(os.path.join("assets", "images", "save.png")),
                height=30,
                x=self.width - 25,
                y=95,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.save(),
                can_hover=lambda: not self.slider.dragged,
            ),
        )

        def close_labeling(scene):
            self.vc.close()
            self.vc = None
            scene.refresh_videos()

        self.add(
            "close",
            Button(
                image_file=(os.path.join("assets", "images", "close.png")),
                height=30,
                x=self.width - 25,
                y=25,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.app.change_scene(0, close_labeling),
            ),
        )
        self.add(
            "settings",
            Button(
                image_file=(os.path.join("assets", "images", "settings.png")),
                height=30,
                x=self.width - 25,
                y=60,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.app.change_scene(2, lambda s: s.load_settings()),
            ),
        )
        self.add(
            "reset",
            Button(
                image_file=(os.path.join("assets", "images", "reset.png")),
                height=30,
                x=self.width - 25,
                y=130,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.rotate_view(),
            ),
        )
        self.is_score = False

        def toggle_score_label():
            self.pause()
            self.is_score = not self.is_score
            text_btn = self.get("score_label")
            text = "LABEL"
            if self.is_score:
                text = "SCORE"
            pos = text_btn.get_pos()
            text_btn.set_image(Text.get_font(30).render(text, True, (0, 0, 0))).set_pos(
                pos
            )
            self.render_label_bar_and_labels()

        self.label_prompt = self.add(
            "label_prompt",
            Text(
                "Choose label:",
                size=16,
                x=5,
                y=80,
            ),
        )

        self.score_input = self.add(
            f"score_input",
            NumericInput(
                image_file="assets/images/black.png",
                fontsize=30,
                value=0,
                color=(255, 255, 255),
                width=120,
                x=-1000,
                y=-1000,
                max_character=5,
                use_indicator=True,
            ),
        )
        self.score_input.hide()
        self.score_prompt = self.add(
            "score_prompt",
            Text(
                "Enter score:",
                size=16,
                x=-1000,
                y=-1000,
            ),
        )
        self.score_prompt.hide()

        def get_score_on_click():
            on_click = self.score_input.on_click

            def func():
                self.pause()
                on_click()

            return func

        self.score_input.on_click = get_score_on_click()

        self.add(
            "score_label",
            Button(
                text="LABEL",
                text_fontsize=30,
                x=self.width - 40,
                y=self.height - 80,
                color=(0, 0, 0),
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=toggle_score_label,
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
                parameter={"factor": 0.15},
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
        self.default_label_index = self.current_label_index
        self.frame2label = None

        self.labels = []
        self.colors = list(ColorBar.colors.keys())

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
    
    def rotate_view(self):
        self.pixels.rot90 += 1
        self.set_pixels(self.vc.peek())

    def set_video(self, video_path, video_name):
        self.video_name = video_name
        assert self.vc is None
        self.get("title").change_text(video_name)
        self.vc = VideoContainer(video_path, 3000, width=400, height=300)
        self.set_pixels(self.vc.peek())
        self.slider.set_progress(0)
        self.current_label_index = -1
        self.frame2label = numpy.array([-1] * self.vc.total)
        self.frame2score = numpy.array([float("nan")] * self.vc.total)
        self.set_buffered_bar()
        self.check_settings()
        self.pause()

    def set_labels(self, labels):
        def get_on_click(i):
            def on_click():
                self.current_label_index = i
                self.default_label_index = self.current_label_index
                self.set_label()

            return on_click

        for i, label in enumerate(self.labels):
            self.remove(f"label_{i}")
        self.labels = labels
        for i, label in enumerate(self.labels):
            x = 5
            y = 104 + i * 33
            self.pos_dict[i] = x, y
            label_btn = self.add(
                f"label_{i}",
                Button(
                    text=f"{i+1}.{label}",
                    align_mode="TOPLEFT",
                    color=ColorBar.colors[
                        self.colors[i if i < len(self.labels) - 1 else -1]
                    ],
                    on_click=get_on_click(i),
                    can_hover=lambda: not self.slider.dragged,
                    text_fontsize=20,
                    x=x,
                    y=y,
                ),
            )
            if self.is_score:
                label_btn.hide()
                label_btn.set_pos(-1000, -1000)

    def render_label_bar_and_labels(self):
        if self.is_score:
            for i, label in enumerate(self.labels):
                label_btn = self.get(f"label_{i}")
                if label_btn is not None:
                    label_btn.hide()
            self.label_prompt.hide()
            self.score_input.show()
            self.score_input.set_pos(self.width - 125, self.height // 3)
            self.score_prompt.show()
            self.score_prompt.set_pos(self.width - 125, self.height // 3 - 20)
            total = len(self.frame2score)
            for i, v in enumerate(range(0, total, int(total / 100))):
                if i == 100:
                    break
                score = self.frame2score[v]
                color = None
                if numpy.isnan(score):
                    color = [0, 0, 0]
                else:
                    color = [
                        int(
                            min(
                                230,
                                max(
                                    30,
                                    30
                                    + (score - self.lower_bound)
                                    / (self.upper_bound - self.lower_bound)
                                    * 200,
                                ),
                            )
                        )
                    ] * 3
                self.bar.set_color(i, tuple(color))
        else:
            for i, label in enumerate(self.labels):
                label_btn = self.get(f"label_{i}")
                if label_btn is not None:
                    label_btn.show()
                    label_btn.set_pos(self.pos_dict[i])
            self.score_input.hide()
            self.score_prompt.hide()
            self.label_prompt.show()
            total = len(self.frame2label)
            for i, v in enumerate(range(0, total, int(total / 100))):
                if i == 100:
                    break
                index = self.frame2label[v]
                if index == len(self.labels) - 1:
                    index = -1
                self.bar.set_color(i, self.colors[index])

    def check_settings(self):
        settings = load_settings()
        labels = settings.get("labels")
        labels.append("Unlabeled")
        upper_bound = settings.get("score_upper_bound")
        lower_bound = settings.get("score_lower_bound")
        if len(labels) < len(self.labels):
            for i in range(len(self.frame2label)):
                if self.frame2label[i] >= len(labels):
                    self.frame2label[i] = -1
        if not (self.upper_bound <= upper_bound and self.lower_bound >= lower_bound):
            for i in range(len(self.frame2score)):
                if not (lower_bound <= self.frame2score[i] <= upper_bound):
                    self.frame2score[i] = float("nan")
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.score_input.upper_bound = upper_bound
        self.score_input.lower_bound = lower_bound
        self.score_input.change_value(self.upper_bound)
        self.set_labels(labels)
        self.render_label_bar_and_labels()

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
        if self.is_score:
            df = pandas.DataFrame(data={"label": list(self.frame2score)})
            df.to_csv(os.path.join("data", f"{self.video_name}_labels.csv"))
        else:
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
        if self.is_score:
            score = self.score_input.value
            self.frame2score[self.vc.absolute_index] = score

            color = None
            if numpy.isnan(score):
                color = [0, 0, 0]
            else:
                color = [
                    int(
                        min(
                            200,
                            max(
                                100,
                                100
                                + (score - self.lower_bound)
                                / (self.upper_bound - self.lower_bound)
                                * 100,
                            ),
                        )
                    )
                ] * 3
            self.bar.set_color(
                int(self.vc.absolute_index / self.vc.total * 100), tuple(color)
            )

        else:
            index = self.current_label_index
            if index == len(self.labels) - 1:
                index = -1
            self.frame2label[self.vc.absolute_index] = self.current_label_index
            self.bar.set_color(
                int(self.vc.absolute_index / self.vc.total * 100),
                self.colors[index],
            )

    def reset_label(self):
        if self.is_score:
            self.frame2score = numpy.array([float("nan")] * self.vc.total)
        else:
            self.frame2label = numpy.array([-1] * self.vc.total)
            self.current_label_index = -1
            self.default_label_index = self.current_label_index
        self.bar.set_arr(numpy.array([(0, 0, 0)] * 100))

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressed, keyboard_pressed):
        if not any(keyboard_pressed.values()):
            self.current_label_index = self.default_label_index
        else:
            if keyboard_inputs:
                for i in range(len(keyboard_inputs) - 1, -1, -1):
                    if keyboard_inputs[i] == " ":
                        keyboard_inputs.pop(i)
                        if not self.playing:
                            self.play()
                            if self.is_score:
                                self.score_input.editing = False
                        else:
                            self.pause()
                            if self.is_score:
                                self.score_input.editing = True
                    else:
                        if '1' <= keyboard_inputs[i] <= '9':
                            label_index = int(keyboard_inputs[i]) - 1
                            print(label_index)
                            if label_index < len(self.labels):
                                self.current_label_index = label_index

        super().update(delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressed, keyboard_pressed)
        self.set_buffered_bar()
        if not self.playing:
            return
        if not mouse_pressed:
            self.frame_count += 1
            if self.frame_count >= self.fps_ratio:
                self.set_display()
                self.frame_count -= self.fps_ratio

    def close(self):
        if self.vc is not None:
            self.vc.close()
        return super().close()
