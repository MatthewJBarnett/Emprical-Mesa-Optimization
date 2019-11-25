import Gridworld

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
import numpy as np
import os


class Convolutional:
	def __init__(self, num_filters, filter_dimensions, input_shape, pooling_shape, dense_shape, num_categories):
		""" Initializes the neural network """
		self.model = Sequential()
		self.model.add(Convolution2D(num_filters, filter_dimensions[0], \
				filter_dimensions[1], activation='relu', input_shape=input_shape))
		self.model.add(MaxPooling2D(pool_size=pooling_shape))
		self.model.add(Dropout(0.2))
		self.model.add(Flatten())
		self.model.add(Dense(dense_shape, activation='relu'))
		self.model.add(Dropout(0.2))
		self.model.add(Dense(dense_shape, activation='relu'))
		self.model.add(Dropout(0.2))
		self.model.add(Dense(num_categories, activation='softmax'))
		
		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	
	def train(self, X, y):
		self.model.fit(X, y, batch_size=32, nb_epoch=3, verbose=1)
	
	def predict(self, x):
		x = x.reshape(x.shape[0], x.shape[1], 1)
		return self.model.predict(np.array([x]))[0]
	
	def evaluate(self, X_test, y_test):
		score = self.model.evaluate(X_test, Y_test, verbose=0)
		return score
	
	def save(self, filename): 
		self.model.save_weights("model.h5")
