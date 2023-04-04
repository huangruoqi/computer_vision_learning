from nn.lstm import LSTM
from preprocessor import RemoveVisibility, PCA
from mutils import ModelTrain

DATA = [
    "1676842883.mp401",
    "1676843917.mp401",
    "1676842496.mp401",
    "1676842689.mp401",
]
OPTIONS = {
}


ModelTrain(LSTM.model, DATA, OPTIONS).run()