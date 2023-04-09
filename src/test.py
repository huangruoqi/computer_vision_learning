from nn.lstm import LSTM
# from preprocessor import RemoveVisibility, PCA
from mutils import ModelTest

DATA = [
    "FrontView_1.mp4",
    "FrontView_2.mp4",
    "SideView_1.mp4",
    "SideView_2.mp4",
]
OPTIONS = {
    # "preprocess": [None],
    "batchsize": [16],
    "timestamp": [90, 180],
    "optimizer": ["adam"],
    "layer1": [{"units": 64 * i, "return_sequences": True} for i in range(1, 5)],
    # "layer2": [None, {"units": 128, "return_sequences": True}],
}
SETTINGS = {
    "max_epochs":100,
    "valid_ratio":0.3,
    "test_ratio":0,
    "early_stop_valid_patience":10,
    "early_stop_train_patience":5,
    "num_train_per_config":10,
    # "loss":'mse',
    # "metrics": ['mse'],
    "loss":"sparse_categorical_crossentropy",
    "metrics": ['accuracy'],
    "verbose": 1
}


ModelTest(LSTM.model, DATA, OPTIONS, **SETTINGS).run()
