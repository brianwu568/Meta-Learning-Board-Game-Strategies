import os 
import glob 
import re
import sys 

import csv
import io

import chess
import chess.engine
import chess.pgn
import tqdm
from tqdm import tqdm

#use for the Kingbase dataset
def process_games_from_PGN(PGN_filename, max_games_to_record = 5000):
    with open(PGN_filename,"rb") as file: 
        text = file.read().decode('latin-1')

    games = []
    game_num = 0
    for line in text.split("]"):
        winner = None 
        white_move = None 
        black_move = None 
        if (line[:6] == "\r\n\r\n1."):
            moves = []
            winner = None
            for move_encoding in line.split("."):
                entries = move_encoding.replace(" ","\n").replace("\r","\n").split("\n")
                #print(entries)
                cleaned_entries = []
                for entry in entries: 
                    if (entry != "" and entry != " "):
                        cleaned_entries.append(entry) 
                
                if (len(cleaned_entries) < 2):
                #print(cleaned_entries)
                    continue 

                white_move = cleaned_entries[0]
                black_move = cleaned_entries[1]
                if (black_move[:7] == "1/2-1/2"):
                    winner = "tie"
                    black_move = None 
                elif (black_move[:3] == "1-0"):
                    winner = "white"
                    black_move = None 
                elif (black_move[:3] == "0-1"):
                    winner = "black"
                    black_move = None 
                
                #print(white_move, black_move)
                if (black_move != None):
                    moves.extend([white_move, black_move])
                else:
                    moves.append(white_move)
                
                if (len(cleaned_entries) >= 3):
                    result = cleaned_entries[2] 
                if (result == "1/2-1/2"):
                    winner = "tie"
                elif (result == "1-0"):
                    winner = "white"
                elif (result == "0-1"):
                    winner = "black"
                
                if (winner != None):
                    break         
                
            if (winner != None):
                games.append(
                    {"winner": winner, "moves": moves}
                )
            game_num += 1
            
            if (game_num >= max_games_to_record):
                break
    
    return games 

#use for the chess.com database of games
def extract_from_csv(csv_filename, max_games_to_record = 1000):
    new_data = []
    with open(csv_filename,"r") as file: 
        reader = csv.reader(file)
        for row_number, row in enumerate(tqdm(reader)): 
            if (row_number == 0):
                continue 
            if (len(row) < 14):
                continue 

            pgn = row[13]
            game = chess.pgn.read_game(io.StringIO(pgn))
            
            board = chess.Board()
            moves = []
            for move in game.mainline_moves():
            #moves.append(board.san(move))
                if (move not in list(board.legal_moves)):
                    break 
                moves.append(move)
                board.push(move)

            new_data.append({"result": game.headers["Result"], "moves": moves})

            if (len(new_data) >= max_games_to_record):
                break 

    #print("Number of Recorded Games Recorded: {}".format(len(new_data)))
    return new_data 

def extract_from_stockfish(stockfish_csv, max_positions_to_record = 10000):

  data = []
  num_games = 0
  with open(stockfish_csv, "r") as file: 
    reader = csv.reader(file)
    for row_number, row in enumerate(tqdm(reader)):
      if (row_number == 0 or len(row) < 2):
        continue 
      
      board_pgn = row[0].split(" ")[0]

      try: 
        evaluation = eval(row[1])

      except: 
        #if ("#" in row[1]):
        #  evaluation = eval(row[1][1:]) * 100
        #else: 
        continue 

      data.append({"board": board_pgn, "eval": evaluation})
      num_games += 1

      if (num_games >= max_positions_to_record):
        break 
    
  return data 


def structure_chess_data(data, max_games, max_half_moves = 40, san = False):
  boards = []
  list_moves = []
  player_states = [] #1 for white, -1 for black

  #MAX_GAMES = 10000
  agg_data = data[:max_games]

  ENUM_PLAYER = {"WHITE": 1, "BLACK": -1}

  for game in tqdm(agg_data): 
    moves = game["moves"]
    board = chess.Board()
    boards.append(board.epd())

    curr_player = "WHITE"
    player_states.append(ENUM_PLAYER[curr_player])

    MAX_INDEX = min(max_half_moves, len(moves))
    
    for move_idx, move in enumerate(moves[:max_half_moves]):
      #current move 
      #next_moves.append(move)
      #move_2 = board.push_san(move)
      #next_moves.append(move_2)
      if (san == False):
        board.push(move)
        list_moves.append(move)
      
      else:
        move_encoded = board.push_san(move)
        list_moves.append(move_encoded)

      curr_player = "BLACK" if curr_player == "WHITE" else "WHITE" #use 1 -1 instead 

      #including information for the next move or not 
      if (move_idx != MAX_INDEX - 1): #on the last index SHOULD NOT RUN ON FINAL LOOP
        player_states.append(ENUM_PLAYER[curr_player])
        boards.append(board.epd())
  
  assert len(boards) == len(list_moves)
  assert len(list_moves) == len(player_states)

  return boards, list_moves, player_states 

def getKingBase_partitioned(folder_path, max_games_each = 100):

  folder_path = os.path.abspath(folder_path)
  aggregate_data = []
  for PGN_f in tqdm(list(glob.glob(os.path.join(folder_path, "*")))):
    data = process_games_from_PGN(os.path.abspath(PGN_f), max_games_each)

    aggregate_data.extend(data)
  
  return aggregate_data

def getKingBase_random(folder_path, max_games, verbose = False):
  folder_path = os.path.abspath(folder_path)
  aggregate_data = {}
  total_games = 0
  for PGN_f in tqdm(list(glob.glob(os.path.join(folder_path, "*")))):
    data = process_games_from_PGN(os.path.abspath(PGN_f), max_games)
    aggregate_data[PGN_f] = data 
    total_games += len(data)

  data = []
  for opening_type in aggregate_data: 
    num_games = len(aggregate_data[opening_type])
    sample_size = int(max_games * num_games / total_games)
    sample_indices = np.random.choice(list(range(num_games)), size = sample_size, 
                                        replace = False)
    data.extend([aggregate_data[opening_type][i] for i in sample_indices])

    if (verbose == True):
      print("Loaded {} PGNs from file {} into storage".format(len(data), opening_type))
      
  return data
  
if __name__ == "__main__":

    #uses chess.com 
    data = extract_from_csv(os.path.abspath(sys.argv[1]), 10000)
    boards,moves,player_states = structure_chess_data(data, 40, san = False)

    #uses Kingbase 
    #data = process_games_from_PGN(PGN_filename, 10000)

    