import os 
import glob 
import argparse 
import sys 
import tqdm 
from tqdm import tqdm 
import chess 
import chess.pgn
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import os
import imageio
import matplotlib.pyplot as plt 
import numpy as np 
import glob 
import json
import csv 
import datetime 
from datetime import datetime

from board_utils import * 
from chess_moves_utils import * 
from extractor_utils import * 
from move_model import * 
from other_utils import * 

def metrics_plot(train_metrics, val_metrics, metric_name, plot_title, filename):
    epochs = len(train_metrics)
    plt.plot(range(epochs), train_metrics, color = "blue", label = "train_{}".format(metric_name))
    plt.plot(range(epochs), val_metrics, color = "green", label = "val_{}".format(metric_name))
    plt.title(plot_title)
    plt.xlabel("Epochs")
    plt.ylabel(metric_name)
    plt.legend()
    
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    
    max_games_to_load_each = 1000
    #/Users/benjaminyan/Downloads/KingBaseLite2019-pgn
    data = getKingBase_partitioned("/Users/benjaminyan/Downloads/KingBaseLite2019-pgn", max_games_to_load_each)

    max_games_store = 500
    max_half_moves = 40
    board, list_moves, player_states = structure_chess_data(data, max_games_store, max_half_moves, san = True)

    print("\nNumber of Boards in Data: {}\n".format(len(board)))

    atlas, inverse_atlas = generate_atlas()
    print("Number of Atlas Moves: {}\n".format(len(atlas.keys())))
    embedding_size = len(atlas.keys())

    labels = []
    for move in list_moves: 
        labels.append(embed_chessMove(move, atlas))
    
    train_images_pgn, train_labels, train_states, val_images_pgn, val_labels, val_states = split_train_val(
    board, labels, player_states, 0.8)
    train_images = encode_images(train_images_pgn, train_states)
    val_images = encode_images(val_images_pgn, val_states)
    print()
    print("Train Img Shape, Val Img Shape, Train Labels Shape, Val Labels Shape")
    print(train_images.shape, val_images.shape, train_labels.shape, val_labels.shape, "\n")

    model = build_CNN_hybrid(embedding_size)

    model.compile(optimizer= tf.keras.optimizers.Adam(learning_rate=1e-4),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])
    
    train_cap = 500 
    val_cap = 100 
    epochs = 10

    history = model.fit(train_images[:train_cap], train_labels[:train_cap], epochs=epochs,
                validation_data = (val_images[:val_cap], val_labels[:val_cap]))
        
    time = datetime.now()
    time_str = time.strftime("%Y-%m-%d-%H:%M:%S")

    #log out history metrics to a LOGS folder
    logs = {
        "loss": history.history["loss"],
        "accuracy": history.history["accuracy"],
        "val_loss": history.history["val_loss"],
        "val_accuracy": history.history["val_accuracy"]} 
    
    with open("logs/logging-{}.json".format(time_str), "w") as write_file:
        json.dump(logs, write_file, indent=4)

    #plots out the metrics to the PLOTS folder
    filename_loss = "plots/training-loss-{}.jpg".format(time_str)
    metrics_plot(logs["loss"], logs["val_loss"], "loss", "CE Loss of Chess Move Prediction", filename_loss)

    filename_acc = "plots/training-accuracy-{}.jpg".format(time_str)
    metrics_plot(logs["accuracy"], logs["val_accuracy"], "accuracy", "Top-1 Accuracy of Chess Move Prediction", filename_acc)
    
    #save out the model if desired to MODELS folder
    save_out_model = False 
    if (save_out_model == True):
        model.save("models/CNN_predictor_{}.h5".format(time_str))



    