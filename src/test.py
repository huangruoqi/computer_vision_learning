import numpy as np
from keras import layers, models, Input, Model
import tensorflow as tf

from mutils import group_data, group_data_score, split_data

# use Early Stopping callback to detect val_loss increases
MAX_EPOCHS = 100
VALID_RATIO = 0.1
TEST_RATIO = 0.1
DATA = [
    "1676842883.mp401",
    "1676843917.mp401",
    "1676842496.mp401",
    "1676842689.mp401",
]
OPTIONS = {
    # 'preprocess': [],
    # 'batchsize': [16, 32],
    'timestamp': [16, 32, 64],
}

def main():
    inputs = Input(shape=(16, 27))
    lstm = layers.LSTM(256, return_sequences=True)(inputs)
    lstm = layers.LSTM(32)(inputs)
    outputs = layers.Dense(1, activation="sigmoid")(lstm)
    model = Model(inputs=inputs, outputs=outputs)
    m = ModelTest(model, DATA, OPTIONS)
    m.test()

class ModelTest:
    def __init__(self, base_model, data, options):
        self.counter = 0
        self.base_model = base_model

        # x_train, y_train, x_valid, y_valid, x_test, y_test
        self.raw_data = split_data(
            data, VALID_RATIO, TEST_RATIO
        )

        self.defalut_params = {
            'preprocess': [],
            'batchsize': 16,
            'timestamp': 32,
        }
        # for i in range(len(self.base_model.layers)):
        #     self.final_options[f'layer{i}']
        self.final_options = []
        self.expand_options(options.items())
        print(self.final_options)
        self.current_options = [None] * len(self.final_options)

        self.final_data = None
        self.final_params = None


    def get_param(self, key):
        param = self.final_params.get(key)
        if param is None:
            return self.defalut_params[key]
        return param


    def expand_options(self, options, name=None):
        for option in options:
            if isinstance(option[1], list) and callable(option[1][0]):
                self.expand_options(option[1], name=option[0])
            else:
                if name is None:
                    self.final_options.append(option)
                else:
                    self.final_options.append((name, option))
                

    def process_options(self):
        self.final_data = list(self.raw_data)
        self.final_params = {}
        for i, (name, options) in enumerate(self.final_options):
            option_idx = self.current_options[i]
            print(self.current_options)
            print(option_idx)
            if option_idx is None:
                continue
            option = options[option_idx]
            if name == 'preprocess':
                # x_train
                self.process(option, self.raw_data[0])
                # x_valid
                self.process(option, self.raw_data[2])
                # x_test
                self.process(option, self.raw_data[4])
            elif name in ['batchsize', 'timestamp']:
                self.final_params[name] = option
            else:
                raise Exception(f"option <{name}> not found")
        timestamp = self.get_param('timestamp')
        for i in range(6):
            self.final_data[i] = (group_data_score if i&1 else group_data)(self.final_data[i], timestamp)

    def process(self, func, data):
        return [func(row) for row in data]

    def test(self, option_idx=0):
        if option_idx==len(self.final_options):
            self.build()
            return

        if callable(self.final_options[option_idx][0]):
            self.current_options[option_idx] = None
            self.test(option_idx+1)
            for i, v in enumerate(self.final_options[option_idx][1]):
                self.current_options[option_idx] = i
                self.test(option_idx+1)
        else:
            for i, v in enumerate(self.final_options[option_idx][1]):
                self.current_options[option_idx] = i
                self.test(option_idx+1)

    def build(self):
        self.process_options()
        x_train, y_train, x_valid, y_valid, x_test, y_test = self.final_data
        input_shape = (None, x_train.shape[1], x_train.shape[2])
        model_copy = models.clone_model(self.base_model)
        # inputs = Input(shape=input_shape)
        model_copy.layers[0]._batch_input_shape = input_shape
        model = models.model_from_json(model_copy.to_json())
        model.compile(optimizer='adam', loss='mse', metrics=['mse'])
        print(model.summary())
        history = model.fit(
            x_train,
            y_train,
            epochs=MAX_EPOCHS,
            validation_data=(x_valid, y_valid),
            batch_size=self.get_param('batchsize'),
            callbacks=[
                tf.keras.callbacks.EarlyStopping(monitor="loss", patience=5, restore_best_weights=True, verbose=1, start_from_epoch=8),
                tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True, start_from_epoch=8),
            ]
        )
        evaluation = model.evaluate(x_test, y_test, verbose=0)
        model_loss = evaluation[0]
        
        

if __name__ == '__main__':
    main()
        
        