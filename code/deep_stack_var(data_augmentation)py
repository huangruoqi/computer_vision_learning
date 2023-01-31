#############Deep Stacked Variational Neural Network model for classifying and detecting abnormal behavior (ransomware attack)  

############How this model works: 

###########################################It is clearly explained in this paper 

#############################################https://www.researchgate.net/publication/333324826_Industrial_Internet_of_Things_Based_Ransomware_Detection_using_Stacked_Variational_Neural_Network


##############How can use it:  

################################You can use it to test what you like or need.  



############If you would like to use this code, please cite this paper 


####“Al-Hawawreh M, Sitnikova E. Industrial Internet of Things Based Ransomware Detection using Stacked Variational Neural Network. 
###########InProceedings of the 3rd International Conference on Big Data and Internet of Things 2019 Aug 22 (pp. 126-130).” 





###########For any query or help contact me at:  Munahawari1@gmail.com 





#################################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib as mpl
from pylab import rcParams
import seaborn as sns
import datetime
from keras.layers import Lambda, Input, Dense, Lambda, BatchNormalization
from keras.models import Model, Sequential 
from keras.losses import mse, binary_crossentropy
from keras.utils import plot_model
from keras import backend as K
from keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import pandas as pd
from keras.models import load_model
from sklearn import preprocessing, metrics

import tkinter
from tkinter.filedialog import askopenfilename 

from numpy.random import seed
seed(1234)
from sklearn.metrics import (confusion_matrix, precision_recall_curve, auc,
                             roc_curve, recall_score, classification_report, f1_score,
                             precision_recall_fscore_support)

import cufflinks as cf

####### ##Deep learning libraries
import tensorflow as tf
import keras
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers
from ann_visualizer.visualize import ann_viz 
from sklearn.preprocessing import  StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from IPython.display import display, Math, Latex


#################################3 Reading data as CSV file  # change it to fit your data 
data= pd.read_csv(r'D:\final_ransom.csv', index_col=0, encoding = "ISO-8859-1")

print(data.shape)



###############################splitting data to training, valiadtion and  testing 
test_split = 0.3 #portion of data used for testing
val_split = 0.2 #portion of training data used for validation

first_test = int(data.shape[0] * (1 - test_split))
first_val = int(first_test * (1 - val_split))



#######################################Selecting rows and columns 
train = data.iloc[:first_val]
val = data.iloc[first_val:first_test]
test = data.iloc[first_test:]
x_train_df, x_val_df, x_test_df = train.iloc[:, 0:-1], val.iloc[:, 0:-1], test.iloc[:, 0:-1]
y_train_df, y_val_df, y_test_df = train.iloc[:, -1], val.iloc[:, -1], test.iloc[:, -1]

x_train, x_val, x_test = x_train_df.values, x_val_df.values, x_test_df.values
y_train, y_val, y_test = y_train_df.values, y_val_df.values, y_test_df.values



############################Building model  for vartional autoencoder 

latent_dim = 64 #number of latent variables to learn




input_dim = x_train.shape[1]
x = Input(shape=(input_dim, ))
encoder1 = Dense(1500, activation="tanh")(x)
encoder2 = Dense(520, activation="tanh" )(encoder1)
encoder3 = Dense(128, activation="tanh")(encoder2)
z_mean=Dense(latent_dim)(encoder3)
z_log_var=Dense(latent_dim)(encoder3)

def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(shape=K.shape(z_mean), mean=0., stddev=1.)
    return z_mean + K.exp(z_log_var / 2) * epsilon
z = Lambda(sampling)([z_mean, z_log_var])

decoder1= Dense(128, activation='tanh')(z)
decoder2= Dense(520, activation='tanh')(decoder1)
decoder3= Dense(1500, activation='tanh')(decoder2)
decoded_mean = Dense(input_dim, activation="tanh")(decoder3)

vae = Model(x, decoded_mean)


def vae_loss(x, decoded_mean):
    
    rec_loss = K.sum(K.binary_crossentropy(x, decoded_mean), axis=-1)
    kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean)- K.exp(z_log_var), axis=-1)   #KL divergence regularization . 
    
    return rec_loss+kl_loss

vae.compile(optimizer="RMSprop", loss=vae_loss)
vae.summary()

nb_epoch = 100
batch_size = 250


#####################################################Training model 
history = vae.fit(x_train,x_train,
                        epochs=nb_epoch,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(x_val, x_val),
                        verbose=1)
						
						
########################################Saving model weights
vae.save_weights('vae.h5')

 
 ######################################### Stacked now with fully connected deep neural network model 
def encoder(x):
    encoder1 = Dense(1500, activation="tanh")(x)
    encoder2 = Dense(520, activation="tanh" )(encoder1)
    encoder3 = Dense(128, activation="tanh")(encoder2)
    z_mean=Dense(latent_dim)(encoder3)
    return z_mean
	
def fc(enco):
    den = Dense(2, activation='selu')(enco)
    out = Dense(1, activation='sigmoid')(den)
    return out

encode = encoder(x)
full_model = Model(x,fc(encode))
for l1,l2 in zip(full_model.layers[:5],vae.layers[0:5]):
    l1.set_weights(l2.get_weights())
print (vae.get_weights()[0][1])
print(full_model.get_weights()[0][1])
for layer in full_model.layers[0:5]:
    layer.trainable = False
full_model.compile(optimizer="RMSprop", loss=vae_loss, metrics=['accuracy'])
full_model.summary()
############################################you can replace x_train data here with the output of data augumenation if you like. 
full_model.fit(x_train,y_train,
                        epochs=nb_epoch,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(x_val, x_val),
                        verbose=1)
						
full_model.save_weights('auto_classification.h5')
for layer in full_model.layers[0:5]:
    layer.trainable = True
full_model.fit(x_train,y_train,
                        epochs=nb_epoch,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(x_val, x_val),
                        verbose=1)

full_model.save_weights('classification_final.h5')





##############################################testmodel

pred=full_model.predict(x_test)

print("AUC(ROC): " + str(metrics.accuracy_score(y_test, pred.round())))
print("Precision: " + str(metrics.precision_score(y_test, pred.round())))
print("Recall: " + str(metrics.recall_score(y_test, pred.round())))
print("F1 score: " + str(metrics.f1_score(y_test, pred.round())))

