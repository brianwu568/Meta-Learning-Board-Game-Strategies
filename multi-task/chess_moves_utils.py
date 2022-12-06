import chess 
import chess.pgn

def generate_atlas():

  rows = ["a","b","c","d","e","f","g","h"]
  cols = list(range(1,8+1))
  pieces = ["","R"]
  
  moves = []

  squares = []
  for row in rows: 
    for col in cols: 
      squares.append("{}{}".format(row,col))

  for state_1 in squares: 
    for state_2 in squares: 
      if (state_1 != state_2):
        moves.append(chess.Move.from_uci("{}{}".format(state_1,state_2)))
  
  promotion_moves = []
  for piece in ["q","r","n","b"]:
    for col_1,col_2 in [(2,1),(7,8)]:
      for i, row in enumerate(rows):
        if (row == "a"):
          promotion_moves.append("{}{}{}{}{}".format(row,col_1,rows[0],col_2,piece))
          promotion_moves.append("{}{}{}{}{}".format(row,col_1,rows[1],col_2,piece))
        elif (row == "h"):
          promotion_moves.append("{}{}{}{}{}".format(row,col_1,rows[-1],col_2,piece))
          promotion_moves.append("{}{}{}{}{}".format(row,col_1,rows[-2],col_2,piece))
        else: 
          promotion_moves.append("{}{}{}{}{}".format(row,col_1,rows[i],col_2,piece))
          promotion_moves.append("{}{}{}{}{}".format(row,col_1,rows[i-1],col_2,piece))
          promotion_moves.append("{}{}{}{}{}".format(row,col_1,rows[i+1],col_2,piece))
  
  print("Number of Promotion Moves: {}".format(len(promotion_moves)))
  for move in promotion_moves: 
    moves.append(chess.Move.from_uci(move))

  atlas = {}
  inverse_atlas = {}
  for index,move in enumerate(moves):
    atlas[move] = index
    inverse_atlas[index] = move 
  
  return atlas, inverse_atlas 

def embed_chessMove(move, atlas):
  if (move not in atlas):
    return -1 
  return atlas[move] 

def decode_chessMove(move, inverse_atlas):
  if (move not in inverse_atlas):
    return -1 
  return inverse_atlas[move]

def embed_all_moves(moves, atlas):
  labels = []
  for move in moves: 
    labels.append(embed_chessMove(move, atlas))
  return labels

def decode_all_labels(labels, inverse_atlas):
  moves = []
  for label in labels: 
    moves.append(decode_chessMove(label, inverse_atlas))
  return moves

