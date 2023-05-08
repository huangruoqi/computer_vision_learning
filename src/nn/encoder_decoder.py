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
    lstm = layers.LSTM(5, return_sequences=False)(inputs)
    repeat = layers.RepeatVector(TIMESTEPS)(lstm)
    outputs = layers.LSTM(NUM_FEATURES, return_sequences=True)(repeat)
    model = Model(inputs=inputs, outputs=outputs)

    def target_function(arr):
        return arr
