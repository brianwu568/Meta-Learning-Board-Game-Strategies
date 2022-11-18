from asyncore import file_dispatcher
import chess.engine
import chess
import chess.svg

import tensorflow as tf
from tensorflow.keras import datasets, layers, models

import os
import imageio
from tqdm import tqdm 
import matplotlib.pyplot as plt 
import numpy as np 
import glob 
import cairosvg

import json

import google_drive_downloader
from google_drive_downloader import GoogleDriveDownloader as gdd

def engine_best(board, Engine, depth = 10):
    if (board.outcome(claim_draw = True) != None):
      return None
    next_move = Engine.analyse(board, chess.engine.Limit(depth = depth))["pv"][0]
    return next_move 

def evaluate(board, Engine, depth = 10):
  adv = Engine.analyse(board, chess.engine.Limit(depth = depth)).get("score").white()
  white_winning_prob = None 
  if (adv.score() != None):
    adv = adv.score() #centipawn advantage
    P = adv / 100
    #convert the centipawn advantage into a win probabiltiy
    white_winning_prob = 1/(1+10**(-P/4)) 
  else: 
    if (adv.mate() > 0): #white has mate 
      white_winning_prob = 1
    else: #black has mate 
      white_winning_prob = 0
  return white_winning_prob 

def build_CNN(input_height = 8, input_width = 8, input_channels = 6):
  model = models.Sequential()
  model.add(layers.Conv2D(128, (3, 3), activation='relu', padding = "same",input_shape=(
        input_height, input_width, input_channels)))
  model.add(layers.MaxPooling2D((2, 2)))
  model.add(layers.Dropout(0.5))
  model.add(layers.Conv2D(256, (3, 3), activation='relu', padding = "same"))
  model.add(layers.MaxPooling2D((2, 2)))
  model.add(layers.Dropout(0.5))
  model.add(layers.Flatten())
  model.add(layers.Dense(128, activation='relu'))
  model.add(layers.Dense(1, activation = "sigmoid"))
  return model 

def generate_data(kingbase_data, Engine, max_games = 10, max_half_moves = 20): #10 for just test running, increase for actual training
    data_images = []
    labels_images = []

    game_number = 0

    set_pgns = set() #ensures no duplicate boards in the dataset
    for game in tqdm(kingbase_data[:max_games]):
        board = chess.Board() 
        if (game_number == 0):
            W = evaluate(board, Engine)
            pgn = board.epd()
            data_images.append(pgn)
            labels_images.append(W)
            set_pgns.add(pgn)
            
        for move in game["moves"][:max_half_moves]: #up to 20 half-moves for now
            board.push_san(move)
            pgn = board.epd()
            if (pgn not in set_pgns):
                data_images.append(pgn)
                W = evaluate(board, Engine)
                labels_images.append(W)
                set_pgns.add(pgn)
    
        game_number += 1

    return data_images, labels_images

def split_train_val(images, labels, train_portion = 0.8):

    assert train_portion >=0 and train_portion <= 1
    n = len(images)

    train_cutoff = int(n * train_portion)

    #shuffle the data
    permutation_indices = np.random.permutation(n)
    images = [images[i] for i in permutation_indices]
    labels = [labels[i] for i in permutation_indices]

    train_images = np.array(images[:train_cutoff])
    train_labels = np.array(labels[:train_cutoff])
    val_images = np.array(images[train_cutoff:])
    val_labels = np.array(labels[train_cutoff:])

    return train_images, train_labels, val_images, val_labels 

def generate_onehot_image_from_pgn(pgn):
    NUM_CHANNELS = 6 
    pgn_relevant = pgn.split(" ", 1)[0]
    board_rows = pgn_relevant.split("/")
    FILLER = [0 for _ in range(NUM_CHANNELS)]
    ENCODERS = np.array(np.eye(NUM_CHANNELS))

    indexer = {'p': 0, 'b': 1, 'n': 2, 'r': 3, 'q': 4, 'k': 5,
                'P': 0, 'B': 1, 'N': 2, 'R': 3, 'Q': 4, 'K': 5}
    image = []
    for row in board_rows:
        image_row = [] 
        for col in row:
            if (col.isdigit() == True):
                for _ in range(int(col)):
                    image_row.append(FILLER)
            else: 
                multiplier = -1 if col.islower() == True else 1
                image_row.append(multiplier * ENCODERS[indexer[col]])
        image.append(image_row)
    
    return np.array(image) 

def encode_images(data_images):
    vectorized_images = []
    for i in tqdm(range(len(data_images))):
        image_pgn = data_images[i]
        vectorized_images.append(generate_onehot_image_from_pgn(image_pgn))
    return np.array(vectorized_images)

"""
levearge CNN position evaluation model to make optimal move predictions
using the minmax algorithm 
"""
def predict_minmax(CNN_model, board_1, isWhite = True):
  moves = []
  boards_pgns = []
  all_outputs = []
  for next_move in list(board_1.legal_moves):
    moves.append(next_move)
    board_copy = board_1.copy()
    board_copy.push(next_move)
    boards_pgns = []
    for opponent_move in list(board_copy.legal_moves):
      board_double = board_copy.copy()
      board_double.push(opponent_move) 
      boards_pgns.append(board_double.epd())
    vectorized_boards = np.array([generate_onehot_image_from_pgn(b) for b in boards_pgns])
    output = [v[0] for v in list(model.predict(vectorized_boards, verbose = 0))]
    
    if (isWhite == True):
      all_outputs.append(np.min(output))
    else:
      all_outputs.append(np.max(output)) #worst case scenario for black 

    #if white, trying to maxmin the output 
  rankings = np.argsort(all_outputs)
  ranked_moves = list([moves[i] for i in rankings])
  
  if (isWhite == True):
    return ranked_moves[-1] #trying to maximize the minimum
  else:
    return ranked_moves[0] #trying to minimize the maximum 

"""
baseline minmax model whose position evaluator is based solely 
"""

"""
deeper tree search using extended minimax idea (TODO)
"""
def tree_search(CNN_model, board, search_depth, beam_width, isWhite = True):
    pass

if __name__ == "__main__":

    if ("KingBase-games-small.json" not in os.listdir(".")):
        #download the dataset from google drive
        gdd.download_file_from_google_drive(file_id = "1-0LDYzii4XJfMqRT8h6L6HgXvrtGAhd2",
                dest_path = "./KingBase-games-small.json")
    
    with open("KingBase-games-small.json","r") as file:
        data = json.load(file)

    Engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    images_pgn, labels = generate_data(data, Engine)

    train_images_pgn, train_labels, val_images_pgn, val_labels = split_train_val(images_pgn, labels, 0.8)
    train_images = encode_images(train_images_pgn)
    val_images = encode_images(val_images_pgn)

    print(train_images.shape, val_images.shape, train_labels.shape, val_labels.shape)

    model = build_CNN(8,8,6)

    model.compile(optimizer='adam',
              loss=tf.keras.losses.MeanSquaredError())

    num_epochs = 10
    history = model.fit(train_images, train_labels, epochs=num_epochs,
                    validation_data = (val_images, val_labels))

    training_loss = tf.keras.metrics.mean_squared_error(
        train_labels, model.predict(train_images))
    print("MSE Error in Training: {:5f}".format(training_loss[0]))
    val_loss = tf.keras.metrics.mean_squared_error(
        val_labels, model.predict(val_images))
    print("MSE Error in Validation: {:5f}".format(val_loss[0]))

    #play the engine against itself (TODO)

    Engine.close()