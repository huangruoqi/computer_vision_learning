from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.utils import IMAGE
# from ..convert import convert_video_with_label
import os

def label_video(name):
    os.system(f'poetry run python -B GUI.py label "{name}"')
import time
class SelectScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(SelectScene, self).__init__(screen, *args, **kwargs)
        self.item_pos = {}
        self.videos = None
        self.convert_task = None
        self.convert_task_wait = 0
        self.add("title", Text(text="VIDEOS", align_mode="CENTER", size=66, x=self.width//2, y=35))
        self.ci = self.add("convert_indicator", Text(text="Converting...", align_mode="CENTER", size=160, color=(100,120,140), x=self.width//2, y=self.height//2), 4)
        self.ci.hide()
        def convert_video(i):
            self.ci.show()
            self.convert_task = i
            
        for i in range(10):
            x = (i&1) * (self.width // 2)
            y = (i//2) + 100*(i//2) + 70
            self.item_pos[i] = (x, y)
            self.add(f"item_{i}_name", Text(
                text="", x=x+10, y=y+10, size=24
            ))
            self.add(f"item_{i}_label_bt", Button(
                text="label", x=x+120, y=y+50, text_fontsize=20,
                on_click=(lambda x: lambda: label_video(self.videos[x][0]))(i)
            ))
            self.add(f"item_{i}_convert_bt", Button(
                text="convert", x=x+180, y=y+50, text_fontsize=20,
                on_click=(lambda x: lambda: convert_video(x))(i)
            ))
            self.add(f"item_{i}_converted", Text(
                text="Converted", x=x+200, y=y+50, size=60, color=(100, 120, 140), align_mode="CENTER"
            ), 4)
            self.get(f"item_{i}_converted").hide()

        self.refresh_videos()

        

    def refresh_videos(self):
        videos = self.get_videos()
        if videos == self.videos: return
        self.videos = videos
        for i in range(10):
            self.set_video(i, videos[i] if i<len(videos) else None)

    def set_video(self, index, info):
        if info is None:
            self.get(f"item_{index}_name").change_text("")
            self.get(f"item_{index}_label_bt").hide()
            self.get(f"item_{index}_convert_bt").hide()
            self.get(f"item_{index}_converted").hide()
        else:
            self.get(f"item_{index}_name").change_text(info[0])
            self.get(f"item_{index}_label_bt").show()
            if info[1]:
                self.get(f"item_{index}_convert_bt").show()
            else:
                self.get(f"item_{index}_convert_bt").hide()
            if info[2]:
                self.get(f"item_{index}_converted").show()
            else:
                self.get(f"item_{index}_converted").hide()

    def update(self, delta_time, mouse_pos, clicked, pressed):
        super().update(delta_time, mouse_pos, clicked, pressed)
        if self.convert_task:
            if self.convert_task_wait > 1:
                # convert_video_with_label(self.videos[self.convert_task][0])
                time.sleep(5)
                self.convert_task = None
                self.ci.hide()
                self.convert_task_wait = 0
            else:
                self.convert_task_wait += 1



    def get_videos(self):
        videos = os.listdir("video")
        return [(
                    v, 
                    os.path.exists(os.path.join("data", f"{v}_labels.csv")),
                    os.path.exists(os.path.join("data", f"{v}.csv")),
                ) for v in videos]
        

    def close(self):
        return super().close()
