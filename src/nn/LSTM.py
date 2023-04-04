from keras import Input, layers, Model

class LSTM:
    inputs = Input(shape=(1, 1))
    lstm = layers.LSTM(256, return_sequences=True)(inputs)
    lstm = layers.LSTM(256, return_sequences=True)(lstm)
    lstm = layers.LSTM(32)(lstm)
    outputs = layers.Dense(1, activation="sigmoid")(lstm)
    model = Model(inputs=inputs, outputs=outputs)
