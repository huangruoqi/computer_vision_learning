from nn.lstm import LSTM
from mutils import ModelTest
from preprocessor import Balancer

DATA = [
    "SideView_1.mp4",
    "SideView_2.mp4",
    "SideView_3.mp4",
]
'''
    "FrontView_1.mp4",
    "FrontView_2.mp4",
    "FrontView_3.mp4",
'''
OPTIONS = {
    "preprocess": [Balancer(100, 10)],
    "batchsize": [i * 30 for i in range(1, 5)],
    "timestamp": [i * 5 for i in range(1, 6)],
    "optimizer": ["adam"],
    # "layer1": [{"units": 64 , "return_sequences": True} for i in range(1, 5)],
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
