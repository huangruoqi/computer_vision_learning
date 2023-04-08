from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from ..convert import convert_video_with_label
import os


class SelectScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(SelectScene, self).__init__(
            screen,
            bg_file=os.path.join("assets", "images", "white.png"),
            *args,
            **kwargs,
        )
        self.item_pos = {}
        self.videos = None
        self.convert_task = None
        self.convert_task_wait = 0
        self.add(
            "title",
            Text(text="VIDEOS", align_mode="CENTER", size=66, x=self.width // 2, y=35),
        )
        self.ci = self.add(
            "convert_indicator",
            Text(
                text="Converting...",
                align_mode="CENTER",
                size=160,
                color=(100, 120, 140),
                x=self.width // 2,
                y=self.height // 2,
            ),
            4,
        )
        self.ci.hide()
        self.add(
            "settings",
            Button(
                image_file=(os.path.join("assets", "images", "settings.png")),
                height=30,
                x=self.width - 25,
                y=25,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.app.change_scene(2, lambda s: s.load_settings()),
            ),
        )

        def convert_video(i):
            self.ci.show()
            self.convert_task = i

        def label_video(name):
            self.app.change_scene(
                1, lambda scene: scene.set_video(os.path.join("video", name), name)
            )

        for i in range(10):
            x = (i & 1) * (self.width // 2)
            y = (i // 2) + 100 * (i // 2) + 70
            self.item_pos[i] = (x, y)
            self.add(f"item_{i}_name", Text(text="", x=x + 10, y=y + 10, size=24))
            self.add(
                f"item_{i}_label_bt",
                Button(
                    text="label",
                    x=x + 90,
                    y=y + 50,
                    text_fontsize=20,
                    on_click=(lambda x: lambda: label_video(self.videos[x][0]))(i),
                ),
            )
            self.add(
                f"item_{i}_convert_bt",
                Button(
                    text="convert",
                    x=x + 210,
                    y=y + 50,
                    text_fontsize=20,
                    on_click=(lambda x: lambda: convert_video(x))(i),
                ),
            )
            self.add(
                f"item_{i}_converted",
                Text(
                    text="Converted",
                    x=x + 200,
                    y=y + 50,
                    size=60,
                    color=(100, 120, 140),
                    align_mode="CENTER",
                    opacity=50,
                ),
                4,
            )
            self.get(f"item_{i}_converted").hide()
            # self.add(
            #     f"item_{i}_labeled",
            #     Text(
            #         text="Labeled",
            #         x=x + 200,
            #         y=y + 50,
            #         size=60,
            #         color=(100, 120, 140),
            #         align_mode="CENTER",
            #         opacity=50,
            #     ),
            #     4,
            # )
            # self.get(f"item_{i}_labeled").hide()

        self.refresh_videos()

    def refresh_videos(self):
        videos = self.get_videos()
        if videos == self.videos:
            return
        self.videos = videos
        for i in range(10):
            self.set_video(i, videos[i] if i < len(videos) else None)

    def set_video(self, index, info):
        if info is None:
            self.get(f"item_{index}_name").change_text("")
            self.get(f"item_{index}_label_bt").hide()
            self.get(f"item_{index}_convert_bt").hide()
            self.get(f"item_{index}_converted").hide()
            # self.get(f"item_{index}_labeled").hide()
        else:
            self.get(f"item_{index}_name").change_text(info[0])
            self.get(f"item_{index}_label_bt").show()
            if info[1]:
                self.get(f"item_{index}_convert_bt").show()
                # self.get(f"item_{index}_labeled").show()
            else:
                self.get(f"item_{index}_convert_bt").hide()
                # self.get(f"item_{index}_labeled").hide()
            if info[2]:
                self.get(f"item_{index}_converted").show()
            else:
                self.get(f"item_{index}_converted").hide()

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressed, keyboard_pressed):
        super().update(delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressed, keyboard_pressed)
        if self.convert_task is not None:
            if self.convert_task_wait > 1:
                convert_video_with_label(self.videos[self.convert_task][0])
                self.convert_task = None
                self.refresh_videos()
                self.ci.hide()
                self.convert_task_wait = 0
            else:
                self.convert_task_wait += 1

    def get_videos(self):
        videos = os.listdir("video")
        return [
            (
                v,
                os.path.exists(os.path.join("data", f"{v}_labels.csv")),
                os.path.exists(os.path.join("data", f"{v}.csv")),
            )
            for v in videos
        ]

    def close(self):
        return super().close()
