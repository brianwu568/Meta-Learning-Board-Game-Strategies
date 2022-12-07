import math
import os
import numpy as np
import torch

GAME_ENDSTATES = []
NEW_GAME_ENDSTATES = []
GAME_OUTCOMES = []
NUMBER_OF_PIECES = []
BOARDS = []
BOARD = [[0] * 8 for _ in range(8)]

OUTCOME_DICTIONARY = {
    "WHITE_WIN": 1,
    "BLACK_WIN": -1,
    "DRAW": 0
}

PIECE_DICTIONARY = {
    "EMPTY": 0,
    "WHITE_REGULAR": 1,
    "WHITE_KING": 2,
    "BLACK_REGULAR": -1,
    "BLACK_KING": -2
}

POSITION_DICTIONARY = {
    1: [0,1],
    2: [0,3],
    3: [0,5],
    4: [0,7],

    5: [1,0],
    6: [1,2],
    7: [1,4],
    8: [1,6],

    9: [2,1],
    10: [2,3],
    11: [2,5],
    12: [2,7],

    13: [3,0],
    14: [3,2],
    15: [3,4],
    16: [3,6],

    17: [4,1],
    18: [4,3],
    19: [4,5],
    20: [4,7],

    21: [5,0],
    22: [5,2],
    23: [5,4],
    24: [5,6],

    25: [6,1],
    26: [6,3],
    27: [6,5],
    28: [6,7],

    29: [7,0],
    30: [7,2],
    31: [7,4],
    32: [7,6]
}

###
# Returns a list of torch.tensors, in which each tensor is a game state representing a 8x8 checkers board with appropriate pieces filled in.
###
def main_function():
    # Define File Name
    if 1:
        FILE_NAME = "no_italian_rules.py"
    if 0:
        FILE_NAME = "italian_rules.py"

    # Read in every single line of the game data file
    with open(FILE_NAME) as f:
        for line in f:
            final_string = ""
            final_string += str(line)[:len(line)-1]
            final_string  = final_string.split(',')

            # Remove extraneous C pointers (not needed)
            final_string = final_string[:-4]

            outcome = final_string[-1]
            agent_color = final_string[-2]

            # Parse Result
            result = 0
            if outcome == 'EGDB_DRAW':
                result = 0
            elif outcome == 'EGDB_WIN':
                if agent_color == 'EGDB_WHITE':
                    result = 1 # white win: 1
                else:
                    result = -1 # black win: -1
            else: # outcome == 'EGDB_LOSS'
                if agent_color == 'EGDB_WHITE':
                    result = -1 # black win: -1
                else:
                    result = 1 # white win: 1

            final_string = final_string[:-2]

            # Extract Number of Pieces
            number_of_pieces = final_string[-1]
            final_string = final_string[:-1]

            GAME_ENDSTATES.append(final_string)
            GAME_OUTCOMES.append(result)
            NUMBER_OF_PIECES.append(number_of_pieces)

    # Remove some extraneous characters
    for game_state in GAME_ENDSTATES:
        new_game_state = []

        # Remove Quotation Mark from last term
        last_term = game_state[-1]
        last_term_modified = last_term.replace('"', '')
        game_state[-1] = last_term_modified

        # Split at Colon
        for item in game_state:
            if ":" not in item:
                new_game_state.append(item)
            else:
                split_list = item.split(':')
                for split_list_elem in split_list:
                    new_game_state.append(split_list_elem)

        # Remove First Term
        new_game_state = new_game_state[1:]

        NEW_GAME_ENDSTATES.append(new_game_state)

    # TESTER FUNCTION: Print New Game Endstates
    # for game_state in NEW_GAME_ENDSTATES:
    #     print(game_state)
    #     print("")

    for datapoint in NEW_GAME_ENDSTATES:
        BOARD = [[0] * 8 for i in range(8)]
        current_color = ""
        contains_king = False

        for position in datapoint:
            # Set Color
            if 'B' in position:
                current_color = "BLACK"
            if 'W' in position:
                current_color = "WHITE"

            # Figure out whether the piece is a king
            if 'K' in position:
                contains_king = True
            else:
                contains_king = False

            # Parse out the square number
            if ('B' in position or 'W' in position) and ('K' in position): # remove first two characters
                square_number = int(position[2:])
            elif ('B' in position or 'W' in position) and not ('K' in position): # remove first character
                square_number = int(position[1:])
            elif not ('B' in position or 'W' in position) and ('K' in position): # remove first character
                square_number = int(position[1:])
            else: # do not remove any leading characters
                square_number = int(position)

            # Modify the relevant square on the Game Board
            game_board_square_indices = POSITION_DICTIONARY[square_number]
            pos_0 = int(game_board_square_indices[0])
            pos_1 = int(game_board_square_indices[1])
            
            if contains_king == True:
                if current_color == "BLACK":
                    BOARD[pos_0][pos_1] = PIECE_DICTIONARY["BLACK_KING"]
                elif current_color == "WHITE":
                    BOARD[pos_0][pos_1] = PIECE_DICTIONARY["WHITE_KING"]
                else:
                    pass
            else: # contains_king == False
                if current_color == "BLACK":
                    BOARD[pos_0][pos_1] = PIECE_DICTIONARY["BLACK_REGULAR"]
                elif current_color == "WHITE":
                    BOARD[pos_0][pos_1] = PIECE_DICTIONARY["WHITE_REGULAR"]
                else:
                    pass

        BOARDS.append(torch.tensor(BOARD))

    # TESTER FUNCTION: Print out each board
    # for b in BOARDS:
    #     print(b)
    #     print("")

    return BOARDS

def main():
    main_function()

if __name__ == "__main__":
    main()
