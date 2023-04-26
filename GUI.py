from UI_BASE.UI.app import App
from src.scenes.select_scene_without_convert import SelectScene as S1
# from src.scenes.select_scene import SelectScene as S2
from src.scenes.labeling_scene import LabelingScene
from src.scenes.setting_scene import SettingScene
from src.vutils import load_settings


settings = load_settings()

app = App(
    [
        S1,
        LabelingScene,
        SettingScene,
    ],
    800,
    600,
    title="Videos",
    fps=settings["fps"],
)

app.run()
