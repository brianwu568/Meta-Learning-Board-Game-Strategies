import numpy as np
import os 

def split_train_val(images, labels, states, train_portion = 0.8):

    assert train_portion >=0 and train_portion <= 1
    n = len(images)

    train_cutoff = int(n * train_portion)

    #shuffle the data
    permutation_indices = np.random.permutation(n)
    images = [images[i] for i in permutation_indices]
    labels = [labels[i] for i in permutation_indices]
    states = [states[i] for i in permutation_indices]

    train_images = np.array(images[:train_cutoff])
    train_labels = np.array(labels[:train_cutoff])
    train_states = np.array(states[:train_cutoff])


    val_images = np.array(images[train_cutoff:])
    val_labels = np.array(labels[train_cutoff:])
    val_states = np.array(states[train_cutoff:])

    return train_images, train_labels, train_states, val_images, val_labels, val_states 

