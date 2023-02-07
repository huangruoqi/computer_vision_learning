from UI_BASE.UI.app import App
from src.labeling_scene import LabelingScene
import os
from label_config import labels, video_name, width, height


app = App(
    LabelingScene,
    width,
    height + 60,
    video_name=video_name,
    video_path=os.path.join(os.curdir, "video", video_name),
    labels=labels,
)
app.run()
