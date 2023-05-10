from nn.lstm import LSTM
from mutils import ModelTest, split_data
from preprocessor import Balancer, Jitter, StableFilter, UnstableFilter
from nn.encoder_decoder import Encoder_Decoder


DATA = [
    "SideView_1.mp4",
    "SideView_2.mp4",
    "SideView_3.mp4",
    "FrontView_1.mp4",
    "FrontView_2.mp4",
    "FrontView_3.mp4",
]

OPTIONS = {
    "preprocess": [StableFilter(stable_label=0, padding=30)],
    "batchsize": [40],
    "timestamp": [16],
    "optimizer": ["adam"],
    "layer1": [{"units": i*5} for i in range(1, 10)],
}

MAX_EPOCHS = 200

SETTINGS = {
    "max_epochs":200,
    "valid_ratio":0.3,
    "test_ratio":0,
    "early_stop_valid_patience":20,
    "early_stop_train_patience":20,
    "num_train_per_config":10,
    "loss":'mae',
    "metrics": ['mae'],
    # "loss":"sparse_categorical_crossentropy",
    # "metrics": ['accuracy'],
    "verbose": 1,
    "test_data": [UnstableFilter(stable_label=0, padding=10).transform(split_data([DATA[5]], 0, 0)[0]), StableFilter(stable_label=0, padding=30).transform(split_data([DATA[5]], 0, 0)[0])]
}


ModelTest(Encoder_Decoder, DATA[:5], OPTIONS, **SETTINGS).run()
