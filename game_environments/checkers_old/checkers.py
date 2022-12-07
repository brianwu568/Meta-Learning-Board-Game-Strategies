# Import Required Packages
import gym
import numpy as np
import config
from stable_baselines import logger

# Define Player Class
class Player():
    def __init__(self, id, token):
        self.id = id
        self.token = token

# Define Token Class
class Token():
    def __init__(self, symbol, number):
        self.symbol = symbol
        self.number = number

# Define Checkers Board Environment
class CheckerboardEnv(gym.Env):
    metadata = {
        'render.modes': ['human']
    }
    
    def __init__(self, verbose = False, manual = False):
        super(CheckerboardEnv, self).__init__()
        self.name = 'checkers'
        self.manual = manual
        self.verbose = verbose

        self.rows = 8
        self.cols = 8
        self.grid_shape = (self.rows, self.cols)
        self.num_squares = self.rows * self.cols

        self.n_players = 2

        self.action_space = gym.spaces.Discrete(self.cols)
        self.observation_space = gym.spaces.Box(-1, 1, self.grid_shape + (3, ))

    # Observation Function
    @property
    def observation(self):
        if self.current_player.token_number == 1: # player 1
            # Define 3 positions, TODO:need to extend to 12 positions
            position_1 = np.array([1 if x.number == 1 else 0 for x in self.board])
            position_1 = position_1.reshape(self.grid_shape)
            position_2 = np.array([1 if x.number == -1 else 0 for x in self.board])
            position_2 = position_2.reshape(self.grid_shape)
            position_3 = np.array([self.can_be_placed(i) for i, x in enumerate(self.board)])
            position_3 = position_3.reshape(self.grid_shape)

        else: # player 2
            # Define 3 positions, TODO:need to extend to 12 positions
            position_1 = np.array([1 if x.number == -1 else 0 for x in self.board])
            position_1 = position_1.reshape(self.grid_shape)
            position_2 = np.array([1 if x.number == 1 else 0 for x in self.board])
            position_2 = position_2.reshape(self.grid_shape)
            position_3 = np.array([self.can_be_placed(i) for i, x in enumerate(self.board)])
            position_3 = position_3.reshape(self.grid_shape)

        position_stack = np.stack([position_1, position_2, position_3], axis = -1)
        return position_stack

    # Legal Actions
    @property
    def legal_actions(self):
        legal_actions_list = []
        for action_number in range(self.action_space.n):
            legal_or_not = self.is_legal(action_number)
            legal_actions_list.append(legal_or_not)

        legal_actions_array = np.array(legal_actions_list)
        return legal_actions_array

    # Check whether or not an actin is legal
    def is_legal(self, action_id):
        if self.board[action_id].number == 0:
            return 1
        else:
            return 0

    # Check whether or not a new piece can be placed
    def check_can_be_placed(self, square_number):
        if self.board[square_number].number == 0:
            for height in range(square_number + self.cols, self.num_squares, self.cols):
                if self.board[height].number == 0:
                    return 0
        else:
            return 0

        return 1

    # Check whether a player is playing on a particular square
    def check_player_on_square(self, board, square, player):
        square_number = board[square].number
        player_square_number = self.players[player].token_number
        
        if player_square_number == square_number:
            return True
        else:
            return False

    # Get the square on which a particular action occurred
    def get_square(self, board, action):
        for row in range(1, self.rows + 1):
            square = self.num_squares - (row * self.cols) + action
            if board[square].number == 0:
                return square


    # TODO: Check whether or not a game is over
    def check_game_over(self, board = None, player = None):
        if board == None:
            self.board = board
        if player == None:
            self.player = player


    # Player Attributes
    @property
    def get_current_player(self):
        current_player = self.players[self.current_player_num]
        return current_player

    # TODO: Increment the game state after the current action is performed
    def step(self, action):
        reward = [0, 0]

        # Check move legality
        if self.is_legal(action) == False:
            done = True
            reward = [1, 1]
            reward[self.current_player_num] = -1
        else:
            square = self.get_square(board, action)
            board[square] = self.current_player.token

            self.turns_taken += 1
            r, done = self.check_game_over()
            reward = [-r, -r]
            reward[self.current_player_num] = r

        self.done = done

        if done == False:
            self.current_player_num = (self.current_player_num + 1) % 2


    # Reset Game State
    def reset(self):
        self.board = [Token('.', 0)] * self.num_squares
        self.players = [
            Player('1', Token('X', 1)),
            Player('2', Token('0', -1))
        ]
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    # Render Game State
    def render(self, mode = 'human', close = False):
        logger.debug("")

        if close == True:
            return
        if self.done == True:
            logger.debug(f'GAME OVER')
        else:
            logger.debug(f"It is Player {self.current_player.id}'s turn to move")
        
        for i in range(0, self.num_squares, self.cols):
            logger.debug(
                '.'.join([x.symbol for x in self.board[i:(i + self.cols)]])
            )

        if self.verbose == True:
            logger.debug(f'\nObservation: \n{self.observation}')

        if self.done == False:
            logger.debug(f'\nLegal Actions:{[i for i, o in enumerate(self.legal_actions) if o != 0]}')

    # TODO: Define Rules for Moving
    def rules_move(self):
        pass

    # TODO: Define a list of winning states
    WINNERS = [
        [],
        []
    ]
