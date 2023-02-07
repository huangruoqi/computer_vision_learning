from UI_BASE.UI.app import App
from src.labeling_scene import LabelingScene
import os
from label_config import labels, video_name

WIDTH = 1280
HEIGHT = 780

app = App(
    LabelingScene,
    WIDTH,
    HEIGHT,
    video_path=os.path.join(os.curdir, "video", video_name),
    labels=labels,
)
app.run()
