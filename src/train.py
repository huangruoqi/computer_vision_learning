from nn.lstm import LSTM
from nn.encoder_decoder import Encoder_Decoder
from preprocessor import Jitter
from mutils import ModelTrain

DATA = [
    "FrontView_3.mp4",
    "FrontView_2.mp4",
    "FrontView_1.mp4",
    "SideView_1.mp4",
    "SideView_2.mp4",
    "SideView_3.mp4",
]
OPTIONS = {
    # "preprocess": Jitter(),
    "batchsize": 40,
    "timestamp": 5,
    "optimizer": "adam",
}
SETTINGS = {
    "max_epochs":1000,
    "valid_ratio":0.3,
    "test_ratio":0,
    "early_stop_valid_patience":20,
    "early_stop_train_patience":20,
    "num_train_per_config":10,
    "loss":'mse',
    "metrics": ['mse'],
    # "loss":"sparse_categorical_crossentropy",
    # "metrics": ['accuracy'],
    "verbose": 1
}

ModelTrain(Encoder_Decoder, DATA, OPTIONS, **SETTINGS).run()