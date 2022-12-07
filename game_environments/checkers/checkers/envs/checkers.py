# Import Required Packages
import gym
import numpy as np
import config
from stable_baselines import logger
from gym import spaces, error, utils
from gym.utils import seeding

# Define Checkers Board Environment
class CheckersEnv(gym.env):
    ###
    # This Checkers Board Environment has 1 for the white player and -1 for the black player. Default player is 1 (white)
    ###

    def __init__(self, print_debug = True):
        self.board;
        self.kings;
        self.print_debug = print_debug;

    def reset(self):
        # Initialize Board, then set up player positions
        one_side_players = np.zeros([3, 8])
        for i in range(0, 3):
            alternating_list = [
                [0, 0],
                [0, 2],
                [0, 4],
                [0, 6],
                [1, 1],
                [1, 3],
                [1, 5],
                [1, 7]
            ]
            # Set up white players
            for elem in alternating_list:
                current_row = elem[0]
                current_col = elem[1]
                one_side_players[current_row, current_col] = 1

        # Now set up the entire board
        self.board = np.vstack([
            # White
            one_side_players[1, :],
            one_side_players[0, :],
            one_side_players[1, :],
            one_side_players[2, :],
            # Black
            one_side_players[2, :] * -1,
            one_side_players[0, :] * -1,
            one_side_players[1, :] * -1,
            one_side_players[0, :] * -1
        ])

        # Bugfix: Ensure all negative zeros become regular zeros
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i, j] == 0:
                    self.board[i, j] = 0

        # Print out the board for debugging
        if self.print_debug == True:
            print("Initialized Board")
            print(self.board)

    # Function to get the correct player orientation
    def get_orientation(self, player):
        if player == 1: # white is playing
            return self.board
        else: # black is playing
            flipped_board = np.flipud(self.board)
            return flipped_board

    # Function to print out the board
    def render_board(self):
        print(self.board)

    # Function to return the score (white, black):
    def get_score(self):
        white_score = len(np.where(self.board == 1)[0])
        black_score = len(np.where(self.board == -1)[0])
        scoreboard = [
            white_score,
            black_score
        ]
        return scoreboard

    # Function to identify whether a move is a capturing move or not. If not, returns simple 'False' indicator;
    # If yes, then it returns a tuple [capturing_new_position, new_position]
    def is_capturing(
        self,
        player,
        original_position,
        new_position,
        horizontal_delta,
        vertical_delta
    ):
        # If move is out of bounds, then we know this is not a capturing move, so we return false.
        new_col = new_position[0]
        new_row = new_position[1]
        if (-1 < new_row < 8) == False:
            return False
        if (-1 < new_col < 8) == False:
            return False

        # Define the new capturing position
        new_capturing_position = [
            new_col + vertical_delta,
            new_row + horizontal_delta
        ]

        # Check whether or not the opponent is on the new position
        current_player_position = self.board[new_col, new_row]
        opposing_player = player * -1
        if current_player_position != opposing_player:
            return False

        # Ensure that the new capturing position does not go out of bounds
        new_capturing_col = new_capturing_position[0]
        new_capturing_row = new_capturing_position[1]

        if (-1 < new_capturing_col < 8) == False:
            return False
        if (-1 < new_capturing_row < 8) == False:
            return False

        # If the new capturing position is empty, then we capture
        if self.board[new_capturing_col, new_capturing_row] == 0:
            pos_tuple = [new_capturing_position, new_position]
            return pos_tuple

        # If we get to this point, then it is not possible to capture anymore
        return False

        
    # Define a Function to see if there is a required move for the current player
    def get_required_move(self, player, skip_rotate = False):
        required_moves = []
        vertical_delta = -1

        # Rotate the grid if the player is black
        if player == -1 and skip_rotate == False:
            self.board = np.flipud(self.board)

        # Find required moves
        current_pieces = np.where(self.board == player)
        for i in range(0, len(current_pieces[0])):
            current_piece_loc = [current_pieces[0][i], current_pieces[1][i]]
            if self.is_capturing(
                player,
                current_piece_loc,
                new_position = [
                    current_piece_loc[0] - 1,
                    current_piece_loc[1] - 1
                ],
                horizontal_delta = -1,
                vertical_delta = vertical_delta
            ) != False:
                required_moves.append(
                    [current_piece_loc, [current_piece_loc[0] - 1, current_piece_loc[1] - 1]]
                )
            if self.is_capturing(
                player,
                current_piece_loc,
                new_position = [
                    current_piece_loc[0] + 1,
                    current_piece_loc[1] - 1
                ],
                horizontal_delta = 1,
                vertical_delta = vertical_delta
            ) != False:
                required_moves.append(
                    [current_piece_loc, [current_piece_loc[0] + 1, current_piece_loc[1] - 1]]
                )

        # Rotate the grid back
        if player == -1 and skip_rotate == False:
            self.board = np.flipud(self.board)

        return required_moves
    
    def fix_board():
        if player == -1: # player is black
            self.board = np.flipud(self.board)


    # Function to return the score at a certain state during the game
    def get_score(self, player):
        scores = {}
        # calculate scores for player
        
        for i in range(-1, 2, 2):
            scores[i] = 0
            current_pieces = np.where(self.board == player)
            for i in range(0, len(current_pieces[0])):
                current_piece_col = current_pieces[0][i]
                current_piece_row = current_pieces[1][i]
                if [current_piece_col, current_piece_row] in self.kings:
                    scores[i] += 2 # kings have double the score
                else:
                    scores[i] += 1

        # Reverse scoring order if necessary
        if player == 1: # black
            return scores[1] - scores[-1]
        else: # white
            return scores[-1] - scores[1]


    # Function to increment Game State
    # Player: Either 1 or -1
    # Original Position: [x, y] tuple
    # horizontal_delta: -1 for left, 1 for right
    # vertical_delta: -1 for up, 1 for down
    def increment_game_state(self, player, original_position, horizontal_delta, vertical_delta):
        previous_player_score = self.get_score(player)

        if player == -1:
            self.board = np.flipud(self.board)

        new_position = [
            original_position[0] + vertical_delta,
            original_position[1] + horizontal_delta
        ]

        # Debugging Utility
        if self.print_debug == True:
            print("Original: ", "left" if horizontal_delta == -1 else "right",
            "up" if vertical_delta == -1 else "down", "New: ", new_position)

        # Ensure that the original position is not out of bounds
        if original_position[0] < 0 or original_position[0] > 7 or original_position[1] < 0 or original_position[1] > 7:
            if self.print_debug == True:
                print("Original position out of bounds")
            self.fix_board(player)
            return False

        # Ensure that the new position is not ount of bounds
        if (-1 < new_position[0] < 8) != True:
            if self.print_debug == True:
                print("New position is out of bounds - horizontal.")
            self.fix_board(player)
            return False
        if (-1 < new_position[1] < 8) != True:
            if self.print_debug == True:
                print("New position is out of bounds - vertical.")
            self.fix_board(player)
            return False

        # Regular pieces cannot move downwards
        if vertical_delta == 1 and original_position not in self.kings:
            if self.print_debug == True:
                print("Downwards move cannot be made by regular pieces")
            self.fix_board(player)
            return False

        # If you do not have a piece on the original position
        if self.board[original_position[0], original_position[1]] != player:
            if self.print_debug == True:
                print("Original position does not contain movable piece by player")
            self.fix_board(player)
            return False

        # Ensure that we are able to capture here
        capturing_indicator = self.is_capturing(
            player, original_position, new_position, horizontal_delta, vertical_delta
        )

        if capturing_indicator != False:
            # Set capturing position to empty
            self.board[capturing_indicator[1][0], capturing_indicator[1][1]] = 0
            # Remove from kings list if applicable
            if capturing_indicator[1] in self.kings:
                self.kings.remove(capturing_indicator[1])
            # Debugging Utility
            if self.print_debug == True:
                print("Capturing Move")

        # Check to ensure that we are not moving onto another filled spot
        if self.board[new_position[0], new_position[1]] != 0:
            if self.print_debug == True:
                print("Not an empty spot")
            self.fix_board(player)
            return False

        # Check if we have to do a required move, and if this move is required or ont
        required_moves = self.get_required_move(player, skip_rotate = True)
        if len(required_moves) > 0:
            if [original_position, new_position] not in required_moves:
                if self.print_debug == True:
                    print("Current move not in list of required moves")
                self.fix_board(board)
                return False
        
        # Update list of kings
        if new_position[0] == 0:
            if self.print_debug == True:
                print("King found")
            self.kings.append(new_position)


        # Remove kings as necessary
        if original_position in self.kings:
            self.kings.remove(original_position)
            if new_position[0] != 0: # not empty
                self.kings.append(new_position)

        # Move player to new position, make original position empty
        self.board[original_position[0], original_position[1]] = 0
        self.board[new_position[0], new_position[1]] = player

        # Board mirroring if player is Black
        if player == -1:
            self.board = np.flipud(self.board)

        # Debugging Utilities
        if self.print_debug == True:
            print("Original: ", original_position, "left" if horizontal_delta == -1 else "right",
            "up" if vertical_delta == -1 else "down", "New: ", new_position)
            print("")
            print(self.board)

        # Wrap up function activity, set done counter
        if np.sum(np.abs(self.board)) == 0:
            self.done = True # we are done with the game

        # Return scoring
        new_scoreboard = self.get_score(player)
        score_delta = new_scoreboard - previous_player_score
        return score_delta

    
    # Get a list of possible actions [position, new position]
    def get_possible_actions(self, player, skip_rotate = False):
        if player == -1 and skip_rotate == False: # Black
            self.board = np.flipud(self.board)

        # First, check to see if there are any mandatory actions
        required_moves = self.get_required_move()
        if len(required_moves) != 0:
            if player == -1 and skip_rotate == False:
                self.board = np.flipud(self.board)
            
            return required_moves

        # If there are no mandatory actions, then we find all possible actions for the player
        all_possible_moves = []
        current_pieces = np.where(self.board == player)
        for i in range(0, len(current_pieces[0])):
            current_piece = [current_pieces[0][i], current_pieces[1][i]]
            # Add possible moves for regular pieces
            up_left = [current_piece, [current_piece[0] - 1, current_piece[1] - 1]]
            up_right = [current_piece, [current_piece[0] - 1, current_piece[1] + 1]]
            all_possible_moves.append(up_left)
            all_possible_moves.append(up_right)
            if current_piece in self.kings:
                # Additional backward moves possible for kings
                down_left = [current_piece, [current_piece[0] + 1, current_piece[1] - 1]]
                down_right = [current_piece, [current_piece[0] + 1, current_piece[1] + 1]]
                all_possible_moves.append(down_left)
                all_possible_moves.append(down_right)

        if player == -1 and skip_rotate == False:
            self.board = np.flipud(self.board)

        return all_possible_moves
