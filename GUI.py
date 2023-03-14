from UI_BASE.UI.app import App
from src.scenes.labeling_scene import LabelingScene
from src.scenes.select_scene import SelectScene

from label_config import LABELS, WIDTH, HEIGHT, FPS
app = App(
    [SelectScene, LabelingScene],
    800,
    600,
    title="Videos",
    fps=FPS,
    labels=LABELS,
)

app.run()
