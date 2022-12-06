import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

def build_CNN_hybrid(embedding_size):

  inputs = tf.keras.layers.Input(shape=[8,8,8])
  x = inputs[:,:,:,:-1]
  
  stack = []
  stack.append(layers.Conv2D(256, (3, 3), activation='relu', padding = "same",input_shape=(8,8,7)))
  stack.append(layers.MaxPooling2D((2, 2)))
  stack.append(layers.Dropout(0.5))
  stack.append(layers.Conv2D(512, (3, 3), activation='relu', padding = "same"))
  stack.append(layers.MaxPooling2D((2, 2)))
  stack.append(layers.Dropout(0.4))
  stack.append(layers.Flatten())
  stack.append(layers.Dense(2056, activation='relu'))
  stack.append(layers.Dropout(0.4))
  stack.append(layers.Dense(embedding_size, activation = "softmax"))

  for layer in stack:
    x = layer(x)

  return tf.keras.Model(inputs=inputs, outputs=x)

if __name__ == "__main__":
    model = build_CNN_hybrid(100)
    model.summary()