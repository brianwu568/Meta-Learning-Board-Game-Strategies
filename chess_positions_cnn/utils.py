import torch
import numpy as np

# Define Constants
NUM_CLASSES = 64

# Dictionary to map chess pieces to numerical encodings
encodings_dict = {
    'EMPTY': 0,  # empty square
    'WP': 1,     # white pawn
    'WN': 2,     # white knight
    'WB': 3,     # white bishop
    'WR': 4,     # white rook
    'WQ': 5,     # white queen
    'WK': 6,     # white king
    'BP': 7,     # black pawn
    'BN': 8,     # black knight
    'BB': 9,     # black bishop
    'BR': 10,    # black rook
    'BQ': 11,    # black queen
    'BK': 12     # black king
}


# Given a 64x1 list of letters representing pieces, return a 64x1 torch tensor of numbers encoding the pieces
def convert_pieces_to_numerical(input_list: 'list[str]', 
    encodings_dict: 'dict[str, int]' = encodings_dict) -> torch.tensor:
    # Ensure that the dimensions of the input list are 64x1
    assert(len(input_list) == NUM_CLASSES)

    # Get a list of letters mapped to their numerical encodings using encodings_dict
    mapped_list = [encodings_dict[elem] for elem in input_list]

    # Convert the mapped list to a torch tensor
    mapped_tensor = torch.tensor(mapped_list, dtype = torch.int)

    return mapped_tensor

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
