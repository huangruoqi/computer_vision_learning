from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.input import Input
import os
from src.vutils import load_settings


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
            Text(text="SETTINGS", align_mode="CENTER", size=66, x=self.width // 2, y=35),
        )
        self.settings = None
        self.label_keys = []
        self.load_labels()

    def load_labels(self):

        self.settings = load_settings()
        for label in self.label_keys:
            self.remove(label)
        for i, label in enumerate(self.settings['labels']):
            self.add(f'input_{i}', Input(
                image_file='assets/images/black.png', 
                text=label,
                fontsize=30, 
                color=(255,255,255), 
                x=100, 
                y=100+i*100,
                width=300
            ))
