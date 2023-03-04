from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.pixel_display import PixelDisplay
from UI_BASE.UI.components.slider import Slider
from UI_BASE.UI.utils import IMAGE, SOUND
import os


class SelectScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(SelectScene, self).__init__(screen, *args, **kwargs)

    def close(self):
        self.vc.close()
        return super().close()
