from UI_BASE.UI.app import App
from src.scenes.labeling_scene import LabelingScene
from src.scenes.select_scene import SelectScene
import os
import sys

MAX_HEIGHT = 900

scene_name = sys.argv[1]

app = None
if scene_name=="label":
    from label_config import LABELS, VIDEO_NAME, WIDTH, HEIGHT, FPS
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
else:
    app = App(
        SelectScene,
        800,
        600,
        title="Videos",
    )

app.run()
