import sys
import os
import tensorflow as tf
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from mutils import split_data, labels2int, save_model_info

# Don't remove the comment below
#MODEL_INFO
MODEL_NAME  = ""
DATA        = [
    "1676842496.mp4",
    "1676842883.mp4",
    "1676843917.mp4",
    "1676842689.mp4",
]
EPOCHS      = 10
VALID_RATIO = 0.1
TEST_RATIO  = 0.1
BATCH_SIZE  = 1

x_train, y_train, x_valid, y_valid, x_test, y_test = split_data(DATA, VALID_RATIO, TEST_RATIO)

inputs = tf.keras.Input(shape=(x_train.shape[1],))
expand_dims = tf.expand_dims(inputs, axis=2)
lstm = tf.keras.layers.LSTM(128, return_sequences=True)(expand_dims)
flatten = tf.keras.layers.Flatten()(lstm)
outputs = tf.keras.layers.Dense(len(labels2int),activation='softmax')(flatten)
model = tf.keras.Model(inputs = inputs, outputs = outputs)
print(model.summary())
model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
history = model.fit(x_train,y_train, epochs=EPOCHS, validation_data =(x_valid,y_valid),
                    validation_split=0.2,
                    batch_size=BATCH_SIZE,
                    )
#MODEL_INFO
# Don't remove the comment above

model_acc = model.evaluate(x_test, y_test, verbose=0)[1]
if len(MODEL_NAME)==0:
    MODEL_NAME = f"LSTM_{int(time.time()//1)}"
model_path = os.path.join("model", MODEL_NAME)
tf.keras.models.save_model(model, model_path)
print("Test Accuracy {:.3f}%".format(model_acc*100))

save_model_info("LSTM", __file__, model_path, model_acc)
