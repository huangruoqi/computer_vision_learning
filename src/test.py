import os
import time
import numpy as np
from keras import layers, models, Input, Model
import pandas as pd
import tensorflow as tf

from mutils import group_data, group_data_score, split_data, RemoveVisibility

# use Early Stopping callback to detect val_loss increases
MAX_EPOCHS = 100
VALID_RATIO = 0.1
TEST_RATIO = 0.1
EARLY_STOP_VALID_PATIENCE = 10
EARLY_STOP_TRAIN_PATIENCE = 5
NUM_TRAIN_PER_SETUP = 2
DATA = [
    "1676842883.mp401",
    "1676843917.mp401",
    "1676842496.mp401",
    "1676842689.mp401",
]
OPTIONS = {
    # 'preprocess': [],
    'batchsize': [16, 20, 30],
    'timestamp': [32, 50],
    'optimizer': ['sgd', 'adam']
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
        self.preprocess = False
        self.preprocessor = None

        # x_train, y_train, x_valid, y_valid, x_test, y_test
        self.raw_data = split_data(
            data, VALID_RATIO, TEST_RATIO
        )

        self.defalut_params = {
            'batchsize': 16,
            'timestamp': 32,
            'optimizer': 'adam'
        }
        # for i in range(len(self.base_model.layers)):
        #     self.final_options[f'layer{i}']
        self.final_options = list(options.items())
        self.current_options = [None] * len(self.final_options)

        self.final_data = None
        self.final_params = None
        self.history = None


    def get_param(self, key):
        param = self.final_params.get(key)
        if param is None:
            return self.defalut_params[key]
        return param


    def process_options(self):
        self.final_data = list(self.raw_data)
        self.final_params = {}
        for i, (name, options) in enumerate(self.final_options):
            option_idx = self.current_options[i]
            if option_idx is None:
                continue
            option = options[option_idx]
            if name == 'preprocess':
                # x_train
                self.raw_data[0] = option.transform(self.raw_data[0])
                # x_valid
                self.raw_data[2] = option.transform(self.raw_data[2])
                # x_test
                self.raw_data[4] = option.transform(self.raw_data[4])
            elif name in ['batchsize', 'timestamp']:
                self.final_params[name] = option
            else:
                raise Exception(f"option <{name}> not found")
        timestamp = self.get_param('timestamp')
        for i in range(6):
            self.final_data[i] = (group_data_score if i&1 else group_data)(self.final_data[i], timestamp)

    def test(self):
        self.history = []
        self.test_helper(0)
        output_path = os.path.join("test_results", str(int(time.time())) + '.csv')
        pd.DataFrame(data=self.history, columns=list(next(zip(*self.final_options)))+['avg_epochs', 'avg_loss', 'avg_validation_loss', 'avg_test_loss']).to_csv(output_path)

    def test_helper(self, option_idx):
        if option_idx==len(self.final_options):
            self.history.append([b[a] for a, b in zip(self.current_options, list(zip(*self.final_options))[1])] + self.build())
            return
        if self.final_options[option_idx][0]=='preprocess':
            # without preprocessor
            self.test_helper(option_idx+1)
        for i, v in enumerate(self.final_options[option_idx][1]):
            self.current_options[option_idx] = i
            self.test_helper(option_idx+1)

    def build(self):
        print("=================================================================")
        for i, (name, option) in enumerate(self.final_options):
            idx = self.current_options[i]
            print(f'{name}: {None if idx is None else option[idx]}')
        print()
        self.process_options()
        x_train, y_train, x_valid, y_valid, x_test, y_test = self.final_data
        input_shape = (None, x_train.shape[1], x_train.shape[2])
        model_copy = models.clone_model(self.base_model)
        # inputs = Input(shape=input_shape)
        model_copy.layers[0]._batch_input_shape = input_shape
        model = models.model_from_json(model_copy.to_json())
        history = []
        for i in range(NUM_TRAIN_PER_SETUP):
            history.append(self.train(model))

        record = [sum(i)/len(i) for i in zip(*history)]
        print("Average [epochs: {:.0f} - loss: {:.5f} - val_loss: {:.5f} - test_loss: {:.5f}]".format(*record))
        print("-----------------------------------------------------------------")
        print()
        return record

    def train(self, clean_model):
        x_train, y_train, x_valid, y_valid, x_test, y_test = self.final_data
        model = models.clone_model(clean_model)
        model.compile(optimizer=self.get_param('optimizer'), loss='mse', metrics=['mse'])
        # print(model.summary())
        batchsize = self.get_param('batchsize')
        history = model.fit(
            x_train,
            y_train,
            epochs=MAX_EPOCHS,
            validation_data=(x_valid, y_valid),
            batch_size=batchsize,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(monitor="loss", patience=EARLY_STOP_TRAIN_PATIENCE, restore_best_weights=True, verbose=0, start_from_epoch=8),
                tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=EARLY_STOP_VALID_PATIENCE, restore_best_weights=True, verbose=0, start_from_epoch=8),
            ],
            verbose=0,
            shuffle=False
        )
        epochs = len(history.history['loss'])
        train_loss = model.evaluate(x_train, y_train, batch_size=batchsize, verbose=0)[0]
        valid_loss = model.evaluate(x_valid, y_valid, batch_size=batchsize, verbose=0)[0]
        test_loss = model.evaluate(x_test, y_test, batch_size=batchsize, verbose=0)[0]
        return epochs, train_loss, valid_loss, test_loss
        

if __name__ == '__main__':
    main()
        
        