from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.input import Input
import os
from src.vutils import load_settings, save_settings


class SettingScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(SettingScene, self).__init__(
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
            Text(
                text="SETTINGS", align_mode="CENTER", size=66, x=self.width // 2, y=35
            ),
        )
        self.add(
            "label",
            Text(text="Labels", align_mode="CENTER", size=44, x=self.width // 4, y=80),
        )
        self.add(
            "fps",
            Text(text="FPS", align_mode="CENTER", size=44, x=self.width // 4 * 3, y=80),
        )
        self.add(
            "close",
            Button(
                image_file=(os.path.join("assets", "images", "close.png")),
                height=30,
                x=self.width - 25,
                y=25,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.app.change_scene(
                    self.app.prev_scene_index,
                    lambda scene: scene.refresh_videos()
                    if self.app.prev_scene_index == 0
                    else 0,
                ),
            ),
        )
        self.add(
            "save",
            Button(
                image_file=(os.path.join("assets", "images", "save.png")),
                height=30,
                x=self.width - 25,
                y=60,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=lambda: self.save_settings(),
            ),
        )
        self.input_counter = 0

        def add_button_on_click():
            self.add_label_editor(len(self.label_keys), "")
            if len(self.label_keys) < 12:
                self.add_button.show()
                self.add_button.set_pos(
                    self.width // 4, 130 + len(self.label_keys) * 40
                )
            else:
                self.add_button.hide()

        self.add_button = self.add(
            "add",
            Button(
                image_file=(os.path.join("assets", "images", "add.png")),
                height=30,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=add_button_on_click,
            ),
        )
        self.settings = None
        self.label_keys = []

    def add_label_editor(self, i, label):
        self.input_counter += 1
        self.label_keys.append(f"input_{self.input_counter}")

        def get_remove_func(x):
            def remove():
                label = self.label_keys.pop(x)
                self.remove(label)
                self.remove(f"{label}_remove")
                for j, label in enumerate(self.label_keys):
                    self.get(label).set_pos(self.width // 4 - 150, 120 + j * 40)
                    r = self.get(f"{label}_remove")
                    r.set_pos(self.width // 4 + 170, 120 + j * 40 + 14)
                    r.on_click = get_remove_func(j)
                if len(self.label_keys) < 12:
                    self.add_button.show()
                    self.add_button.set_pos(
                        self.width // 4, 130 + len(self.label_keys) * 40
                    )
                else:
                    self.add_button.hide()

            return remove

        self.add(
            f"input_{self.input_counter}",
            Input(
                image_file="assets/images/black.png",
                text=label,
                fontsize=26,
                color=(255, 255, 255),
                x=self.width // 4 - 150,
                y=120 + i * 40,
                width=300,
            ),
        )
        self.add(
            f"input_{self.input_counter}_remove",
            Button(
                image_file="assets/images/minus.png",
                height=26,
                x=self.width // 4 + 170,
                y=120 + i * 40 + 14,
                on_click=get_remove_func(i),
            ),
        )

    def load_settings(self):
        self.settings = load_settings()
        for label in self.label_keys:
            self.remove(label)
            self.remove(f"{label}_remove")
        for i, label in enumerate(self.settings["labels"][:12]):
            self.add_label_editor(i, label)
        if len(self.label_keys) < 12:
            self.add_button.show()
            self.add_button.set_pos(self.width // 4, 130 + len(self.label_keys) * 40)
        else:
            self.add_button.hide()

    def save_settings(self):
        labels = []
        for label in self.label_keys:
            text = self.get(label).text
            if len(text.strip()) != 0:
                labels.append(text)
        self.settings["labels"] = labels
        save_settings(self.settings)
