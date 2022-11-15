import math
import os
import numpy as np

# Define Constants
DATA_PATH = "/data/dataset_2/"

# Get a list of the data files in the data path
data_file_list = os.listdir(DATA_PATH)

for data_file in data_file_list:
    full_file_path = DATA_PATH + str(data_file)
    with open(full_file_path, 'r') as f:
        for line in f:
            pass