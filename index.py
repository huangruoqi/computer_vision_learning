from UI_BASE.UI.app import App
from src.labeling_scene import LabelingScene
import os
from label_config import labels, video_name, width, height, fps

MAX_HEIGHT = 900

app = App(
    LabelingScene,
    width,
    min(MAX_HEIGHT, height + 60),
    fps=fps,
    title="Video Labler",
    video_name=video_name,
    video_path=os.path.join(os.curdir, "video", video_name),
    video_width=width,
    video_height=height,
    labels=labels,
)
app.run()
