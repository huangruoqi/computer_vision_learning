from UI_BASE.UI.app import App
from src.labeling_scene import LabelingScene
import os

WIDTH = 1280
HEIGHT = 780

app = App(LabelingScene, WIDTH, HEIGHT, video_path=os.path.join(os.curdir, "video", "test2.mp4"))
app.run()