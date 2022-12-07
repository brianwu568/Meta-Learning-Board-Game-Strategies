import math
import os
# import numpy as np
# import torch

GAME_ENDSTATES = []

# FIle Name
if 1:
    FILE_NAME = "no_italian_rules.py"
if 0:
    FILE_NAME = "italian_rules.py"

# Read in every single line of the game data file
with open(FILE_NAME) as f:
    for line in f:
        final_string = ""
        final_string += '['
        final_string += str(line)[:-1]
        final_string += ']'
        GAME_ENDSTATES.append(final_string)

print(GAME_ENDSTATES)
