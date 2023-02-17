from UI_BASE.UI.app import App
from src.labeling_scene import LabelingScene
import os
from label_config import LABELS, VIDEO_NAME, WIDTH, HEIGHT, FPS

MAX_HEIGHT = 900

app = App(
    LabelingScene,
    WIDTH,
    min(MAX_HEIGHT, HEIGHT + 60),
    fps=FPS,
    title="Video Labler",
    video_name=VIDEO_NAME,
    video_path=os.path.join(os.curdir, "video", VIDEO_NAME),
    video_width=WIDTH,
    video_height=HEIGHT,
    labels=LABELS,
)
app.run()
