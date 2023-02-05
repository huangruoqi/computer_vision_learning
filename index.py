from UI_BASE.UI.app import App
from src.labeling_scene import LabelingScene

WIDTH = 1280
HEIGHT = 800

app = App(LabelingScene, WIDTH, HEIGHT)
app.run()