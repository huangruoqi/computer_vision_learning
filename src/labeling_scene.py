from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.components.slider import Slider
from UI_BASE.UI.sound import Channel
from UI_BASE.UI.utils import IMAGE, SOUND



class LabelingScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(LabelingScene, self).__init__(screen, *args, **kwargs)
        # self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        def on_click():
            text = self.get("text")
            x, y = text.get_pos()
            text.set_pos(500 - x, 500 - y)
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
        self.add("text", Text(
            "something",
            x=200,
            y=300
        ))
        slider = self.add("slider", Slider(drag_width=200, on_change=lambda x: 0, x=500, y=500, color=(255,255,100)),1)
        self.add("progress_bar", ColorBar(200, 50, 500, 500, on_click=lambda pos:slider.set_slider_pos(pos.x)))

    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
