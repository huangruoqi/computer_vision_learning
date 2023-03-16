import sys
import os
import tensorflow as tf
import time
import json
import numpy as np

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from mutils import (
    split_data,
    group_data,
    group_data_score,
    labels2int,
    save_model_info,
    Preprocessor,
)


# Don't remove the comment below
# MODEL_INFO
MODEL_NAME = "111"
DATA = [
    "1676842883.mp4" + MODEL_NAME[:2],
    "1676843917.mp4" + MODEL_NAME[:2],
    "1676842496.mp4" + MODEL_NAME[:2],
    "1676842689.mp4" + MODEL_NAME[:2],
]

EPOCHS = 40
VALID_RATIO = 0.1
TEST_RATIO = 0.1
BATCH_SIZE = 16
TIMESTAMPS = 32

x_train, y_train, x_valid, y_valid, x_test, y_test = split_data(
    DATA, VALID_RATIO, TEST_RATIO
)
p = Preprocessor()
x_train = group_data(x_train, TIMESTAMPS, p)
y_train = group_data_score(y_train, TIMESTAMPS)
x_valid = group_data(x_valid, TIMESTAMPS, p)
y_valid = group_data_score(y_valid, TIMESTAMPS)
x_test = group_data(x_test, TIMESTAMPS, p)
y_test = group_data_score(y_test, TIMESTAMPS)
inputs = tf.keras.Input(shape=(x_train.shape[1], x_train.shape[2]))
lstm = tf.keras.layers.LSTM(256, return_sequences=True)(inputs)
if MODEL_NAME[2] == "1":
    lstm = tf.keras.layers.Dropout(0.5)(lstm)
    lstm = tf.keras.layers.LSTM(32)(lstm)
    lstm = tf.keras.layers.Dropout(0.5)(lstm)
else:
    lstm = tf.keras.layers.LSTM(32)(lstm)
outputs = tf.keras.layers.Dense(1, activation="sigmoid")(lstm)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
print(model.summary())
model.compile(
    loss="mean_squared_error", optimizer="adam", metrics=["mean_squared_error"]
)
history = model.fit(
    x_train,
    y_train,
    epochs=EPOCHS,
    validation_data=(x_valid, y_valid),
    batch_size=BATCH_SIZE,
)
# MODEL_INFO
# Don't remove the comment above

evaluation = model.evaluate(x_test, y_test, verbose=0)
model_loss = evaluation[0]
if len(MODEL_NAME) == 0:
    MODEL_NAME = f"LSTM_{int(time.time()//1)}"
model_path = os.path.join("model", MODEL_NAME)
tf.keras.models.save_model(model, model_path)
print("Test loss {:.4f}".format(model_loss))
print(evaluation[1])

save_model_info("LSTM", __file__, model_path, model_loss)
print(list(zip(np.array(list(map(lambda x: x[0], model.predict(x_test)))), y_test)))
