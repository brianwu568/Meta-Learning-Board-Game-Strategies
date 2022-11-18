import matplotlib.pyplot as plt 
import numpy as np
import chess 
import chess.engine 
import os 
import glob 
import cairosvg
import chess.svg

from run_stockfish import simulate_game

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

#clears the folder of frame images to eliminate remnant files from previous simulations
def clear_directory(dirname):
    images = glob.glob('./{}/*'.format(dirname))
    for img in images:
        os.remove(img)

def get_filename(directory = "static", move_number = 0, advantage = 0, format = "svg"):
    return os.path.join(directory, "move_{:04d}_{:08d}.{}".format(move_number, advantage, format))

def render_images(directory, moves, san_format = False, debug = False):
    clear_directory(directory)
    height = 300; width = 300
    Analyzer = Stockfish(depth = 10)
    board = chess.Board() 
    for move_number, move in enumerate(moves):
        if (san_format == True):
            board.push_san(move)
        else: 
            board.push(move)
        
        #evaluate board advantage
        adv = Analyzer.analyze(board).get("score").white()
        if (adv.score() != None):
            adv = adv.score() #centipawn advantage
        else: 
            if (adv.mate() > 0): #white has mate 
                adv = 10000
            else: #black has mate 
                adv = -10000

        if (debug == False):
            svg = chess.svg.board(board=board,size=400, lastmove = move)
            with open(get_filename(directory, move_number = move_number + 1, advantage = adv),"w") as file: 
                file.write(svg)
            cairosvg.svg2png(url=get_filename(directory, move_number = move_number + 1, advantage = adv), 
                            write_to=get_filename(directory, move_number = move_number + 1, advantage = adv, format = "png"), 
                            output_width=width, output_height=height)
    
    Analyzer.engine.close()

def plot_game(directory = "static", filename = "game.jpg"):

  relevant_images = sorted(list(glob.glob(os.path.join(directory, "*.png"))))
  num_images = len(relevant_images) 

  num_cols = 4
  num_rows = (num_images + num_cols - 1) // num_cols 
  fig,ax = plt.subplots(figsize = (3 * num_cols,3.5 * num_rows), 
                        nrows = num_rows, ncols = num_cols)

  for image_num in range(num_images): 
    image = relevant_images[image_num]

    advantage = round(int(image.split("/")[-1].split("_")[2].replace(".png","")) / 100,2)
    if (advantage > 0):
      advantage = "+{}".format(advantage)
    if (image_num % 2 == 0):
      title = "Move {} ({}): {}".format(image_num // 2 + 1, "White", advantage)
    else:
      title = "Move {} ({}): {}".format((image_num - 1) // 2 + 1, "Black", advantage)

    ax[image_num // num_cols, image_num % num_cols].imshow(plt.imread(image))
    ax[image_num // num_cols, image_num % num_cols].axis("off")
    ax[image_num // num_cols, image_num % num_cols].set_title(title,
                                                              fontsize = 10)
  
  plt.savefig(filename)

if __name__ == "__main__":

    san_moves = ['e2e4', 'e7e5', 'g1f3', 'd7d5', 'f1b5', 'b8c6', 'b5c6', 'b7c6']
    moves = [chess.Move.from_uci(m) for m in san_moves]
    render_images("static", moves, False, False)
    plot_game("static", "CNN-playing-itself.png")

    """
    White = Stockfish(16)
    Black = Stockfish(4)

    moves, result = simulate_game(White, Black)
    render_images("static", moves, False, False)
    plot_game("static", "stockfish16-stockfish4-game.jpg")

    White.engine.close()
    Black.engine.close()
    """

