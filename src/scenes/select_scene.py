from UI_BASE.UI.scene import Scene
from UI_BASE.UI.components.button import Button
from UI_BASE.UI.components.text import Text
from UI_BASE.UI.components.color_bar import ColorBar
from UI_BASE.UI.utils import IMAGE
# from ..convert import convert_video_with_label
import os

def label_video(name):
    os.system(f'poetry run python -B GUI.py label "{name}"')

class SelectScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(SelectScene, self).__init__(screen, *args, **kwargs)
        self.item_pos = {}
        self.videos = None
        self.add("Title", Text(text="VIDEOS", align_mode="CENTER", size=66, x=self.width//2, y=35))
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
                # on_click=(lambda x: lambda: convert_video_with_label(self.videos[x][0]))(i)
            ))
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
        else:
            self.get(f"item_{index}_name").change_text(info[0])
            self.get(f"item_{index}_label_bt").show()
            if info[1]:
                self.get(f"item_{index}_convert_bt").show()
            else:
                self.get(f"item_{index}_convert_bt").hide()



    def get_videos(self):
        videos = os.listdir("video")
        return [(v, os.path.exists(os.path.join("data", f"{v}_labels.csv"))) for v in videos]
        

    def close(self):
        return super().close()
