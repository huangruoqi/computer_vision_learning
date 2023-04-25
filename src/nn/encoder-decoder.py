from keras import Input, layers, Model

class Encoder_Decoder:
    inputs = Input(shape=(16, 27))
    lstm = layers.LSTM(256, return_sequences=True)(inputs)
    outputs = layers.Dense(1, activation="sigmoid")(lstm)
    lstm = layers.LSTM(256, return_sequences=True)(outputs)
    outputs = layers.Flatten()
    outputs = layers.Reshape(shape=(1,1))
    model = Model(inputs=inputs, outputs=outputs)

    def get_io(data):
        (x_train, y_train), (x_valid, y_valid), (x_test, y_test) = data
        return (x_train, x_train), (x_valid, x_valid), (x_test, x_test)
