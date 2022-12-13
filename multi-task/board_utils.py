import chess
import chess.pgn 
import numpy as np
import tqdm 
from tqdm import tqdm 

def render_square(square):
  square_mapper = {}
  index = 1
  for row in ["a","b","c","d","e","f","g","h"]:
    for col in [i for i in range(1,8+1)]:
      square_mapper[row + str(col)] = index
      index += 1
  
  if (square in square_mapper):
    return square_mapper[square]
  else:
    print("bruh")
    return 0

def generate_onehot_simple(pgn):

    NUM_CHANNELS = 6 
    pgn_relevant, rel_player, castling, en_passant  = pgn.split(" ")
    rel_player = rel_player.strip().lower()


    PLAYER = 1 if rel_player == "w" else -1

    castling = castling.strip()
    en_passant = en_passant.strip()

    #include a buffer 8 x 8 x 1 of information 
    extra_states = np.zeros(shape = (8,8,1))
    if ("K" in castling):
      extra_states[0,0,0] = 1
    if ("Q" in castling):
      extra_states[1,0,0] = 1
    if ("k" in castling):
      extra_states[2,0,0] = 1
    if ("q" in castling):
      extra_states[3,0,0] = 1
    if (en_passant != "-"):
      extra_states[4,0,0] = render_square(en_passant)

    #pgn_relevant = pgn.split(" ", 1)[0]

    board_rows = pgn_relevant.split("/")
    FILLER = [0 for _ in range(NUM_CHANNELS)] + [PLAYER]
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
                image_row.append(list(multiplier * ENCODERS[indexer[col]]) + [PLAYER])
        
        image.append(image_row)
    
    #add some extra stuff for the additional information 
    #print(np.array(image).shape, extra_states.shape)

    return np.concatenate((np.array(image), extra_states), axis = -1)

def generate_onehot(pgn, isWhite = True):

    if (isWhite == True):
      PLAYER = 1 
    else: 
      PLAYER = -1

    NUM_CHANNELS = 6 
    pgn_relevant, rel_player, castling, en_passant  = pgn.split(" ")
    rel_player = rel_player.strip()
    castling = castling.strip()
    en_passant = en_passant.strip()

    #include a buffer 8 x 8 x 1 of information 
    extra_states = np.zeros(shape = (8,8,1))
    if ("K" in castling):
      extra_states[0,0,0] = 1
    if ("Q" in castling):
      extra_states[1,0,0] = 1
    if ("k" in castling):
      extra_states[2,0,0] = 1
    if ("q" in castling):
      extra_states[3,0,0] = 1
    if (en_passant != "-"):
      extra_states[4,0,0] = render_square(en_passant)

    #pgn_relevant = pgn.split(" ", 1)[0]

    board_rows = pgn_relevant.split("/")
    FILLER = [0 for _ in range(NUM_CHANNELS)] + [PLAYER]
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
                image_row.append(list(multiplier * ENCODERS[indexer[col]]) + [PLAYER])
        
        image.append(image_row)
    
    #add some extra stuff for the additional information 
    #print(np.array(image).shape, extra_states.shape)

    return np.concatenate((np.array(image), extra_states), axis = -1)

def encode_images_simple(data_images):
    vectorized_images = []

    for i in tqdm(range(len(data_images))):
        image_pgn = data_images[i]
        vectorized_images.append(generate_onehot_simple(image_pgn))
    return np.array(vectorized_images)

def encode_images(data_images, player_states):
    vectorized_images = []

    for i in tqdm(range(len(data_images))):
        image_pgn = data_images[i]
        player_state = player_states[i]
        vectorized_images.append(generate_onehot(image_pgn, player_state))

        #vectorized_images.append(generate_onehot_image_from_pgn(image_pgn, player_state))
    return np.array(vectorized_images)
  
def unrender_square(signature):
  inverse_square_mapper = {}
  index = 1
  for row in ["a","b","c","d","e","f","g","h"]:
    for col in [i for i in range(1,8+1)]:
      inverse_square_mapper[index] = row + str(col)
      index += 1
  
  if (signature in inverse_square_mapper):
    return inverse_square_mapper[signature]
  else:
    return 0

def unvectorize_image(board_image):
  indexer = {'p': 0, 'b': 1, 'n': 2, 'r': 3, 'q': 4, 'k': 5,
                'P': 0, 'B': 1, 'N': 2, 'R': 3, 'Q': 4, 'K': 5}
  inverse_indexer = {}
  for key,value in indexer.items():
    if (key.islower() == True):
      inverse_indexer[value] = key

  fen_components = [] #list of strings 
  for row in range(board_image.shape[0]):

    row_str = ""
    ongoing_streak = 0
    for col in range(board_image.shape[1]): 
      
      piece = None 

      for index, elem in enumerate(board_image[row,col][:-2]):
        if (elem == -1):
          piece = inverse_indexer[index]
          break 
        if (elem == 1):
          piece = inverse_indexer[index].upper()
          break 
      
      if (piece != None):
        if (ongoing_streak > 0):
          row_str += str(ongoing_streak)
          ongoing_streak = 0
        row_str += piece
      else: 
        ongoing_streak += 1
      
    if (ongoing_streak > 0):
      row_str += str(ongoing_streak)
    
    fen_components.append(row_str)
    

  official_board = "/".join(fen_components)
  player_turn = board_image[0,0,-2]
  if (player_turn == 1):
    official_board += " w"
  else:
    official_board += " b"
  
  castling = ""
  if (board_image[0,0,-1] == 1):
    castling += "K"
  if (board_image[1,0,-1] == 1):
    castling += "Q"
  if (board_image[2,0,-1] == 1):
    castling += "k"
  if (board_image[3,0,-1] == 1):
    castling += "q"
  
  if (castling == ""):
    official_board += " -"
  else:
    official_board += " {}".format(castling)
  
  en_passant = board_image[4,0,-1]
  if (en_passant != 0):
    official_board += " {}".format(unrender_square(en_passant))
  else:
    official_board += " -"
  
  #lastly, en_passant 
  return official_board, player_turn
