from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.input import Input
import os


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
        self.add('input', Input(
            image_file='assets/images/black.png', 
            fontsize=30, 
            color=(255,255,255), 
            x=100, 
            y=100,
        ))
