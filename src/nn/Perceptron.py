from keras import Input, layers, Sequential


class Perceptron:
    model = Sequential(
        [
            Input(shape=(1,)),
            layers.Dense(100, activation="sigmoid"),
            layers.Dense(200, activation="relu"),
            layers.Dense(10, activation="relu"),
            layers.Dense(1, activation="sigmoid"),
        ]
    )
