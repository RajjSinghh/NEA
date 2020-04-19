import tensorflow as tf
import os
import cv2
import matplotlib.pyplot as plt
import random
import numpy as np
from tensorflow.keras.layers import Activation,  MaxPooling2D


DATADIR = "data"
CATEGORIES = [0, 1, 2, 3, 4, 5,6, 7, 8, 9, "+", "x", "div", "-"]

mnist = tf.keras.datasets.mnist
(xtrain, ytrain), (xtest, ytest) = mnist.load_data()

xtrain, xtest, ytrain, ytest = list(xtrain), list(xtest), list(ytrain), list(ytest)


def Create_Dataset(xtrain, ytrain, xtest,ytest):
	for category in CATEGORIES[11:]:
		path = os.path.join(DATADIR, category)
		for image in os.listdir(path):
			image_arr = cv2.imread(os.path.join(path, image), cv2.IMREAD_GRAYSCALE)
			for i in range(85):
				place = random.randint(0, len(xtrain))
				xtrain.insert(place, image_arr)
				ytrain.insert(place, CATEGORIES.index(category))
			for i in range(15):
				place = random.randint(0, len(xtest))
				xtest.insert(place, image_arr)
				ytest.insert(place, CATEGORIES.index(category))
	return xtrain, ytrain, xtest,ytest

	
xtrain, ytrain, xtest, ytest = Create_Dataset(xtrain, ytrain, xtest, ytest)
xtrain, ytrain, xtest, ytest = np.array(xtrain), np.array(ytrain), np.array(xtest), np.array(ytest)

print(len(xtrain))
print(len(ytrain)) 

#model = tf.keras.models.Sequential()
#
#model.add(tf.keras.layers.Flatten())
#model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
#model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
#model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
#model.add(tf.keras.layers.Dense(14, activation=tf.nn.softmax))
#
#
#
##`model.add(tf.keras.layers.Dense(16, activation=tf.nn.sigmoid))
##`model.add(tf.keras.layers.Dense(16, activation=tf.nn.sigmoid))
##`model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
#model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=["accuracy"]  )
#xtrain = xtrain / 256
#xtest = xtest / 256
#model.fit(xtrain, ytrain, epochs=10)
#
#model.save('read.model')


model = tf.keras.models.load_model('read.model')
val_loss, val_acc = model.evaluate(xtest, ytest)

print(val_loss, val_acc)

##OBJECTIVE MET, 99% training accuracy, 97% test accuracy

##TODO refine to prevent overfitting, test iteratively
