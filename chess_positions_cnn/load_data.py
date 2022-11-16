import utils
import os
import numpy as np

DATA_PATH = "data/dataset_2/"
data_file = open("chess_data.txt", "w")

def get_all_games():
    # Define Empty Dictionary
    
    

    # Get a list of the data files in the data path
    data_file_list = os.listdir(DATA_PATH)

    # Loop over all of the data files 
    for file in data_file_list:
        if "20" in file:
            data = utils.readfile(DATA_PATH + file)
            for point in data:
                score = str(point[1])
                if (score[0] == "+"):
                    score = int(score[1:])/100
                elif (score[0] == "-"):
                    score = -int(score[1:])/100
                else:
                    score = 0
                data_file.write(" ".join(utils.convert_pieces_to_numerical(point[0])) + " " + str(score) + "\n")
    
    

get_all_games()
data_file.close()