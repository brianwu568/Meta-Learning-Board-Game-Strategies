import chess 
import numpy as np
import tensorflow as tf 
from board_utils import * 

#gets the top k moves with probabilities
def run_inference(model, image, atlas, inverse_atlas, k = 5):

  num_moves = len(inverse_atlas.keys())
  preds = model.predict(np.expand_dims(image, axis = 0), verbose = 0)[0]

  official_board, player_move = unvectorize_image(image)

  legal_moves = [atlas[move] for move in chess.Board(official_board).legal_moves]
  mult = [1 if index in legal_moves else 0 for index in range(num_moves)]

  preds = preds * mult 

  top_k = np.argsort(preds)[::-1][:k]

  moves = [(inverse_atlas[index], preds[index]) for index in top_k]
  return moves, official_board, player_move

#predicts best k moves directly on a Python chess board
def predict_CNN(model, board_1, atlas, k = 5, isWhite = True):

  legal_moves = list(board_1.legal_moves)
  embedded_legal_moves = [atlas[l] for l in legal_moves]
  if (len(embedded_legal_moves) == 0):
      return -1

  if (isWhite == True):
      player = 1
  else:
      player = -1

  VECTORIZED_BOARD = np.expand_dims(generate_onehot(board_1.epd(), player), 0)
  output = model.predict(VECTORIZED_BOARD, verbose = 0)[0]
  probabilities = tf.nn.softmax(output)

  relevant_probs = [probabilities[i] for i in embedded_legal_moves]
  rankings = np.argsort(relevant_probs)[::-1][:k]

  return [(legal_moves[r], relevant_probs[r]) for r in rankings]

def get_metrics(model, val_images, val_labels):

  #element wise multiplicatoin on preds versus a matrix of legal moves 
  preds = model.predict(val_images, verbose = 0)
  pred_labels = np.argmax(preds, axis = -1)
  pred_labels_mult = np.argsort(preds, axis = -1)[:,-5:]

  correct = 0
  top5_correct = 0
  total = 0

  index = 0
  for pred, target in zip(pred_labels, val_labels):
    if (pred == target):
      correct += 1
    
    if (target in pred_labels_mult[index]):
      top5_correct += 1

    total += 1
    index += 1

  return correct / total * 100, top5_correct / total * 100