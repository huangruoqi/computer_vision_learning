from keras import Input, layers, Model


class LSTM:
    inputs = Input(shape=(1, 1))
    lstm = layers.LSTM(256, return_sequences=True)(inputs)
    lstm = layers.LSTM(32)(lstm)
    # outputs = layers.Dense(1, activation="sigmoid")(lstm)
    outputs = layers.Dense(3, activation="softmax")(lstm)
    model = Model(inputs=inputs, outputs=outputs)

    target_function = lambda arr: max(arr)
