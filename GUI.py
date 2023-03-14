import json
from UI_BASE.UI.app import App
from src.scenes.labeling_scene import LabelingScene
from src.scenes.select_scene import SelectScene

setting_file = open("settings.json")
settings = json.load(setting_file)
setting_file.close()

app = App(
    [SelectScene, LabelingScene],
    800,
    600,
    title="Videos",
    fps=settings["fps"],
    labels=settings["labels"],
)

app.run()
