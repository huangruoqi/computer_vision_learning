import json
import os
from UI_BASE.UI.app import App
from src.scenes.labeling_scene import LabelingScene
from src.scenes.select_scene import SelectScene
from src.scenes.setting_scene import SettingScene

setting_file = open(os.path.join("assets", "settings.json"))
settings = json.load(setting_file)
setting_file.close()

app = App(
    [SettingScene, SelectScene, LabelingScene],
    800,
    600,
    title="Videos",
    fps=settings["fps"],
    labels=settings["labels"],
)

app.run()
