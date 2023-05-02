from keras import Input, layers, Model

TIMESTEPS = 16
NUM_FEATURES = 27
class Encoder_Decoder:
    '''without repeat vector'''
    # inputs = Input(shape=(TIMESTEPS, NUM_FEATURES))
    # lstm = layers.LSTM(64, return_sequences=True)(inputs)
    # lstm = layers.LSTM(32, return_sequences=True)(lstm)
    # lstm = layers.LSTM(16, return_sequences=True)(lstm)
    # lstm = layers.LSTM(32, return_sequences=True)(lstm)
    # lstm = layers.LSTM(64, return_sequences=True)(lstm)
    # outputs = layers.LSTM(NUM_FEATURES, return_sequences=True)(lstm)
    # model = Model(inputs=inputs, outputs=outputs)
    '''with repeat vector'''
    inputs = Input(shape=(TIMESTEPS, NUM_FEATURES))
    lstm = layers.LSTM(64, return_sequences=True)(inputs)
    lstm = layers.LSTM(32, return_sequences=False)(lstm)
    repeat = layers.RepeatVector(TIMESTEPS)(lstm)
    lstm = layers.LSTM(32, return_sequences=True)(repeat)
    lstm = layers.LSTM(64, return_sequences=True)(lstm)
    outputs = layers.LSTM(NUM_FEATURES, return_sequences=True)(lstm)
    model = Model(inputs=inputs, outputs=outputs)

    def get_io(data):
        (x_train, y_train), (x_valid, y_valid), (x_test, y_test) = data
        return (x_train, x_train), (x_valid, x_valid), (x_test, x_test)

    def target_function(arr):
        return arr
