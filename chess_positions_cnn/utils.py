import torch
import numpy as np
import chess
import chess.engine

# Define Constants
NUM_SQUARES = 64

# Dictionary to map chess pieces to numerical encodings
encodings_dict = {
    None: '0',
    'P': '1',     # white pawn
    'N': '2',     # white knight
    'B': '3',     # white bishop
    'R': '4',     # white rook
    'Q': '5',     # white queen
    'K': '6',     # white king
    'p': '7',     # black pawn
    'n': '8',     # black knight
    'b': '9',     # black bishop
    'r': '10',    # black rook
    'q': '11',    # black queen
    'k': '12'     # black king
}

def readfile(file):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    return_ar = []
    reader = open(file, 'r')
    total = 0
    for x in reader.readlines():
        if x[:3] == "1. ":
            total += 1
            board = chess.Board()
            for a in x.split(".")[1:]:
                if "1-0" not in a and "0-1" not in a and "1/2-1/2" not in a:
                    
                    move = a[1:a.rfind(" ")].split(" ")
                    board.push_san(move[0])
                    board.push_san(move[1])
                    position = []
                    for file in "abcdefgh":
                        for rank in "12345678":
                            piece = board.piece_at(chess.parse_square(file + rank))
                            if (piece != None):
                                position.append(board.piece_at(chess.parse_square(file + rank)).symbol())
                            else:
                                position.append(None)
                    info = engine.analyse(board, chess.engine.Limit(time=0.1))
                    return_ar.append([position, info['score'].pov(True)])   
            if (total >= 50):
                break
    return return_ar



# Given a 64x1 list of letters representing pieces, return a 64x1 torch tensor of numbers encoding the pieces
def convert_pieces_to_numerical(input_list: 'list[str]', 
    encodings_dict: 'dict[str, int]' = encodings_dict):
    # Ensure that the dimensions of the  list are 64x1
    assert(len(input_list) == NUM_SQUARES)

    # Get a list of letters mapped to their numerical encodings using encodings_dict
    mapped_list = [encodings_dict[elem] for elem in input_list]

    # Convert the mapped list to a torch tensor
    #mapped_tensor = torch.tensor(mapped_list, dtype = torch.int)

    return mapped_list

# Given a 64x1 torch tensor of numbers encoding the pieces, return a 64x13 one-hot tensor to pass into the CNN
def convert_numerical_to_one_hot(input_tensor: torch.tensor) -> torch.tensor:
    # Ensure that the length of the input index tensor is 64x1
    shape_dim_0 = input_tensor.size(dim = 0)
    shape_dim_1 = input_tensor.size(dim = 1)

    assert(shape_dim_0 == NUM_CLASSES)
    assert(shape_dim_1 == 1)

    # Convert a 64x1 torch.tensor index into a one-hot 64x13 tensor
    one_hot_tensor = torch.nn.functional.one_hot(
        tensor = input_tensor,
        num_classes = NUM_CLASSES
    )

    return one_hot_tensor
