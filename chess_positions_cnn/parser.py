import math
import os
import numpy as np

# Define Constants
DATA_PATH = "/data/dataset_2/"


def get_all_games():
    # Define Empty Dictionary
    game_dict = {}

    # Get a list of the data files in the data path
    data_file_list = os.listdir(DATA_PATH)

    # Loop over all of the data files 
    for data_file in data_file_list:
        current_game_data = get_game_data(data_file)
        game_dict[data_file] = current_game_data

    return game_dict


def get_game_data(data_file):
    full_file_path = DATA_PATH + str(data_file)
    list_of_games = []

    # Parse out only the encoded game sequence
    with open(full_file_path, 'r') as f:
            for line in f:
                if (not str(line).startswith('[')) or (str(line) != '' or str(line) != ' '):
                    list_of_games.append(line)

    return list_of_games
