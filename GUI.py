from UI_BASE.UI.app import App
from src.scenes.labeling_scene import LabelingScene
from src.scenes.select_scene import SelectScene
import os
import sys

MAX_HEIGHT = 900

scene_name = sys.argv[1]

app = None
if scene_name=="label":
    from label_config import LABELS, WIDTH, HEIGHT, FPS
    video_name = sys.argv[2]
    app = App(
        LabelingScene,
        WIDTH,
        min(MAX_HEIGHT, HEIGHT + 60),
        fps=FPS,
        title="Video Labler",
        video_name=video_name,
        video_path=os.path.join(os.curdir, "video", video_name),
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
