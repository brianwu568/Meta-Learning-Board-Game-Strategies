import chess
import chess.engine
import numpy as np 

#make sure to run brew install stockfish first

#agent that plays a completely random legal move if the game is still ongoing
class RandomChess():
  def move(self, board):
    if (board.outcome(claim_draw = True) != None):
      return None
    next_move = np.random.choice(list(board.legal_moves))
    return next_move 
    
#agent that uses the Stockfish 14 program; can specify the depth of the research
#depth of 1 -> relatively naive, depth of 10 -> very strong Stockfish model
class Stockfish():
  def __init__(self, depth):
    self.depth = depth 
    self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
  
  def move(self, board):
    if (board.outcome(claim_draw = True) != None):
      return None
    next_move = self.engine.analyse(board, chess.engine.Limit(depth = self.depth))["pv"][0]
    return next_move 
  
  def analyze(self, board):
    return self.engine.analyse(board, chess.engine.Limit(depth = self.depth))

#simulates a game between two agents (White, Black) that have move() functions 
def simulate_game(White, Black, max_moves = 40):

    board = chess.Board() 
    moves = []
    num_moves = 0
    while (board.outcome(claim_draw = True) == None):

        num_moves += 1

        #white always has legal move, otherwise the while loop would have been broken 
        white_move = White.move(board)
        moves.append(white_move)
        board.push(white_move)
        
        black_move = Black.move(board)
        if (black_move == None): #Black cannot move or can claim a draw 
            break 
        else: 
            moves.append(black_move)
            board.push(black_move)

        if (num_moves >= max_moves): #exceeded maximum number of allowed moves 
            break 

    outcome = board.outcome(claim_draw = True)
    if (outcome != None):
        result = outcome.result() 
    else:
        result = None
    return moves, result

if __name__ == "__main__":

    #plays a Stockfish with depth 5 tree search against anothe Stockfish with depth 10 tree search 
    #can input our own model in the future and play it against a Stockfish version 

    White = Stockfish(5) #depth 5
    Black = Stockfish(10)

    moves, result = simulate_game(White, Black, max_moves = 40)
    print(moves) 
    print(result)

    White.engine.close()
    Black.engine.close()


