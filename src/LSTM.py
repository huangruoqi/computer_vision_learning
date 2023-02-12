import pandas as pd
import numpy as np
import tensorflow as tf
import os

df = pd.read_csv(os.path.join("data", "1676004101.mp4.csv"))

groups = {}

current_group_label = None
current_group = []
for row in df.itertuples():
    if current_group_label is None:
        current_group_label = row.label
    if current_group_label == row.label:
        current_group.append(row)
    else:
        groups[current_group_label] = current_group
        current_group_label = row.label
        current_group = []

if len(current_group):
    groups[current_group_label] = current_group

[print(i) for i in groups]

DB = pd.read_csv('New_CombinedData.csv', names = ["Target", "X","Y","Z","GX","GY","GZ"])

#Splitting Data into train and test
#For the data, I split the data into its training/testing portions 
#before seperating the label and features 
DS_train, DS_test = train_test_split(DB, test_size = 0.2)
#validation data. *Keep in mind validation data is different from test data
DS_train, DS_val = train_test_split(DS_train, test_size = 0.1)
'''The data was split into 3 groups. Training data,Testing data, and Validation 
data. First, did a 80/20 split. 80 being for the training data and 20 for the
testing data. Validation data for this project was taking 10% of the training 
data'''
#Seperating "Target" column and combining feature data
DS_valid = DS_val.copy()
y_val= DS_valid.pop("Target")
X_val = np.array(DS_valid)

#Seperating "Target" column and combining feature data
DS_train_features2 = DS_train.copy()
y_train = DS_train_features2.pop("Target")
X_train = np.array(DS_train_features2)

#Seperating "Target" column and combining feature data
DS_test_features1 = DS_test.copy()
y_test = DS_test_features1.pop("Target")
X_test = np.array(DS_test_features1)

#LSTM
inputs = tf.keras.Input(shape=(X_train.shape[1],))
expand_dims = tf.expand_dims(inputs, axis=2)
#Determined the hidden layer on arbitrary number
lstm = tf.keras.layers.LSTM(64, return_sequences=True)(expand_dims)
flatten = tf.keras.layers.Flatten()(lstm)
#output is 5, but expecting 4. With the code it excludes the highest number.
#Reads the value as [0,5) not [0,5]
outputs = tf.keras.layers.Dense(4,activation='softmax')(flatten)
model = tf.keras.Model(inputs = inputs, outputs = outputs)
print(model.summary())
#Compile
'''Used sparse_categorical_crossentropy as a work similar to this project used
sparse_categorical_crossentropy and it seems to also be effective for this 
project. Adam seems to be a general all rounder. Then added accuracy metric to
show accuracy for each epoch'''
model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

#Fit
'''epochs determine the amount of times the model would go through the code.
Validation_data should be derived from the training portion (referring to the 
80/20 cut). For this project we cut 10% of the training portion to be validation
data. Chosen Batch size was arbitrary.'''
history = model.fit(X_train,y_train, epochs = 50, validation_data =(X_val,y_val),
                    validation_split=0.2,
                    batch_size=32,
                    )

#Evaluation of model's accuracy
model_acc = model.evaluate(X_test,  y_test, verbose=0)[1]
print("Test Accuracy {:.3f}%".format(model_acc*100))
