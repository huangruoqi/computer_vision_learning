import pandas as pd
import numpy as np
import tensorflow as tf
import os
import sys
import random
import time
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from label_config import labels

data = [
    "1676242134.mp4",
    "1676265052.mp4x9",
]

DBs = [pd.read_csv(os.path.join("data", f"{name}.csv"), index_col=0) for name in data]

DB = pd.concat(DBs, axis=0, ignore_index=True, sort=False)

labels2int = {b:a for a, b in enumerate(labels+['Unlabeled'])}

def convert_df_labels(df1, labels2int):
    df = df1.copy()
    for i in range(len(df)):
        label = df['label'][i]
        df.at[i, 'label'] = labels2int[label]
    return df

DB = convert_df_labels(DB, labels2int)

def split_data_with_label(df, valid_size=0.1, test_size = 0.2):
    df_input = df.copy()
    df_target = df_input.pop('label')
    groups = {}
    current_group_label = None
    current_group = []
    for i, row in enumerate(df_input.itertuples(index=False)):
        if current_group_label is None:
            current_group_label = df_target[i]
        if current_group_label == df_target[i]:
            current_group.append(row)
        else:
            groups[current_group_label] = groups.get(current_group_label, [])
            groups[current_group_label].append(current_group)
            current_group_label = df_target[i]
            current_group = []
    if len(current_group):
        groups[current_group_label] = groups.get(current_group_label, [])
        groups[current_group_label].append(current_group)

    x_train, x_valid, x_test = [], [], []
    y_train, y_valid, y_test = [], [], []
    for label, group in groups.items():
        # random.shuffle(group)
        combined = [j for i in group for j in i]
        n_test = int(len(combined) * test_size)
        n_valid = int(len(combined) * valid_size)
        n_train = len(combined) - n_test - n_valid
        for i in range(len(combined)):
            (x_train if i < n_train else x_valid if i < n_train+n_valid else x_test).append(combined[i])
            (y_train if i < n_train else y_valid if i < n_train+n_valid else y_test).append(label)
    return np.array(x_train), np.array(y_train),np.array(x_valid), np.array(y_valid),np.array(x_test), np.array(y_test)
    
def split_data_without_label(df, valid_size=0.3, test_size = 0.1):
    df_input = df.copy()
    df_target = df_input.pop('label')
    x_train, x_valid, x_test = [], [], []
    y_train, y_valid, y_test = [], [], []
    n_test = int(len(df_input) * test_size)
    n_valid = int(len(df_input) * valid_size)
    n_train = len(df_input) - n_test - n_valid
    for i, row in enumerate(df_input.itertuples(index=False)):
        (x_train if i < n_train else x_valid if i < n_train+n_valid else x_test).append(row)
        (y_train if i < n_train else y_valid if i < n_train+n_valid else y_test).append(df_target[i])
    return np.array(x_train), np.array(y_train),np.array(x_valid), np.array(y_valid),np.array(x_test), np.array(y_test)
    

x_train, y_train, x_valid, y_valid, x_test, y_test = split_data_without_label(DB)
# groups = {}

# current_group_label = None
# current_group = []
# for row in df.itertuples():
#     if current_group_label is None:
#         current_group_label = row.label
#     if current_group_label == row.label:
#         current_group.append(row)
#     else:
#         groups[current_group_label] = groups.get(current_group_label, [])
#         groups[current_group_label].append(current_group)
#         current_group_label = row.label
#         current_group = []

# if len(current_group):
#     groups[current_group_label] = groups.get(current_group_label, [])
#     groups[current_group_label].append(current_group)

# [print(i, len(groups[i])) for i in groups]

#Seperating "Target" column and combining feature data

#LSTM
inputs = tf.keras.Input(shape=(x_train.shape[1],))
expand_dims = tf.expand_dims(inputs, axis=2)
#Determined the hidden layer on arbitrary number
lstm = tf.keras.layers.LSTM(128, return_sequences=True)(expand_dims)
flatten = tf.keras.layers.Flatten()(lstm)
#output is 5, but expecting 4. With the code it excludes the highest number.
#Reads the value as [0,5) not [0,5]
outputs = tf.keras.layers.Dense(len(labels2int),activation='softmax')(flatten)
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
history = model.fit(x_train,y_train, epochs = 5, validation_data =(x_valid,y_valid),
                    validation_split=0.2,
                    batch_size=32,
                    )

#Evaluation of model's accuracy
model_acc = model.evaluate(x_test, y_test, verbose=0)[1]
tf.keras.models.save_model(model, os.path.join("model", f"LSTM_{int(time.time()//1)}"))
print("Test Accuracy {:.3f}%".format(model_acc*100))
