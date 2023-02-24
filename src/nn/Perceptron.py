import sys
import os
import tensorflow as tf
from tensorflow.keras import Input, Sequential
from tensorflow.keras.layers import Dense
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from mutils import split_data, labels2int, save_model_info

# Don't remove the comment below
#MODEL_INFO
MODEL_NAME  = "Perceptron_Test"
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

model = Sequential([
    Dense(100,activation='sigmoid', input_shape=(x_train.shape[1],)),
    Dense(200,activation='relu'),
    Dense(10,activation='relu'),
    Dense(len(labels2int),activation='softmax'),
])
print(model.summary())
model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
history = model.fit(x_train,y_train, epochs=EPOCHS, validation_data =(x_valid,y_valid), shuffle=True
                    # validation_split=0.2,
                    # batch_size=BATCH_SIZE,
                    )
#MODEL_INFO
# Don't remove the comment above

model_acc = model.evaluate(x_test, y_test, verbose=0)[1]
if len(MODEL_NAME)==0:
    MODEL_NAME = f"Perceptron_{int(time.time()//1)}"
model_path = os.path.join("model", MODEL_NAME)
tf.keras.models.save_model(model, model_path)
print("Test Accuracy {:.3f}%".format(model_acc*100))

save_model_info("Perceptron", __file__, model_path, model_acc)
