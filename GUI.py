from UI_BASE.UI.app import App
from src.scenes.labeling_scene import LabelingScene
from src.scenes.select_scene import SelectScene
from src.scenes.setting_scene import SettingScene
from src.vutils import load_settings


settings = load_settings()

app = App(
    [
        SelectScene,
        LabelingScene,
        SettingScene,
    ],
    800,
    600,
    title="Videos",
    fps=settings["fps"],
    labels=settings["labels"],
)

app.run()
