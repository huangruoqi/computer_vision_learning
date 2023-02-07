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



class LabelingScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(LabelingScene, self).__init__(screen, *args, **kwargs)
        # self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        def on_click():
            bar = self.get("progress_bar")
            for i in range(10):
                bar.set_color(i ,"green")

        self.add("abc", Button(
            text="abc",
            text_fontsize=100,
            x=100,
            y=100,
            on_click=on_click,
        ))
        def on_change(x):
            self.vc.set(int(self.vc.total*x))
            self.slider.set_progress(self.vc.progress())

        self.slider = self.add("slider", Slider(drag_width=self.width-100, on_change=on_change, x=self.width/2, y=750, color=(200,200,200), interval=[0,1],width=20,height=50),1)

        self.add("progress_bar", ColorBar(self.width-self.width%100, 50, self.width/2, 750, on_click=lambda progress: on_change(progress)))
        self.pixles = self.add("video", PixelDisplay(1280, 720, self.width/2, 720/2))
        self.vc = VideoContainer(kwargs.get("video_path"),1000)


    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
        self.pixles.set(self.vc.next())
        if not pressed:
            self.slider.set_progress(self.vc.progress())

    def close(self):
        self.vc.close()
        return super().close()