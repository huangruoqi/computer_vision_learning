from nn.lstm import LSTM
from preprocessor import RemoveVisibility, PCA
from mutils import ModelTest

DATA = [
    "1676842883.mp401",
    "1676843917.mp401",
    "1676842496.mp401",
    "1676842689.mp401",
]
OPTIONS = {
    "preprocess": [None, RemoveVisibility()],
    "batchsize": [16],
    "timestamp": [32, 50],
    "optimizer": ["adam"],
    "layer1": [None, {"units": 128, "return_sequences": True}],
    "layer2": [None, {"units": 128, "return_sequences": True}],
}


ModelTest(LSTM.model, DATA, OPTIONS, ).run()
