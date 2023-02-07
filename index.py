from UI_BASE.UI.app import App
from src.labeling_scene import LabelingScene
import os
from label_config import labels, video_name

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

app = App(
    LabelingScene,
    VIDEO_WIDTH,
    VIDEO_HEIGHT + 60,
    video_path=os.path.join(os.curdir, "video", video_name),
    labels=labels,
)
app.run()
