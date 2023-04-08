from UI_BASE.UI.components.container import Container
from UI_BASE.UI.components.numeric_input import NumericInput
from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
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
            Text(text="Labels", align_mode="CENTER", size=40, x=self.width // 4, y=80),
        )
        self.add(
            "score",
            Text(
                text="Score", align_mode="CENTER", size=40, x=self.width // 4 * 3, y=80
            ),
        )
        self.score_input_lower = self.add(
            "score_lower",
            NumericInput(
                image_file="assets/images/black.png",
                fontsize=30,
                value=0,
                color=(255, 255, 255),
                width=120,
                x=self.width // 4 * 3 - 140,
                y=120,
                max_character=5,
            ),
        )
        self.score_input_upper = self.add(
            "score_upper",
            NumericInput(
                image_file="assets/images/black.png",
                fontsize=30,
                value=0,
                color=(255, 255, 255),
                width=120,
                x=self.width // 4 * 3 + 14,
                y=120,
                max_character=5,
            ),
        )
        self.add(
            "tilde",
            Text(
                text="~",
                size=50,
                align_mode="CENTER",
                x=self.width // 4 * 3,
                y=132,
            ),
        )
        self.add(
            "warning",
            Text(
                text="",
                align_mode="CENTER",
                size=30,
                color=(240, 50, 50),
                x=self.width * 3 // 4,
                y=self.height - 100,
            ),
        )

        def close():
            call_back = lambda s: 0
            if self.app.prev_scene_index == 0:
                call_back = lambda scene: scene.refresh_videos()
            elif self.app.prev_scene_index == 1:
                call_back = lambda scene: scene.check_settings()
            self.app.change_scene(self.app.prev_scene_index, call_back)

        self.add(
            "close",
            Button(
                image_file=(os.path.join("assets", "images", "close.png")),
                height=30,
                x=self.width - 25,
                y=25,
                animation="opacity",
                parameter={"factor": 0.5},
                on_click=close,
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
        self.upper_bound = 0
        self.lower_bound = 0
        self.valid_upper_bound = 0
        self.valid_lower_bound = 0
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
        self.upper_bound = self.settings["score_upper_bound"]
        self.lower_bound = self.settings["score_lower_bound"]
        self.valid_upper_bound = self.settings["score_upper_bound"]
        self.valid_lower_bound = self.settings["score_lower_bound"]
        self.score_input_lower.change_value(self.lower_bound)
        self.score_input_upper.change_value(self.upper_bound)
        for label in self.label_keys:
            self.remove(label)
            self.remove(f"{label}_remove")
        self.label_keys.clear()
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
        if self.upper_bound >= self.lower_bound:
            self.get("warning").change_text("")
            self.valid_upper_bound = self.upper_bound
            self.valid_lower_bound = self.lower_bound
        else:
            self.upper_bound = self.valid_upper_bound
            self.lower_bound = self.valid_lower_bound
            self.get("warning").change_text("Range not valid")
            self.score_input_lower.change_value(self.lower_bound)
            self.score_input_upper.change_value(self.upper_bound)

        self.settings["score_upper_bound"] = self.upper_bound
        self.settings["score_lower_bound"] = self.lower_bound
        save_settings(self.settings)

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressed, keyboard_pressed):
        super().update(delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressed, keyboard_pressed)
        self.upper_bound = self.score_input_upper.value
        self.lower_bound = self.score_input_lower.value
