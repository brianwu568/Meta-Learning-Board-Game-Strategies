"""
file for parsing the dense PGN docs that contain over a million recorded grandmaster games
of the KingBase dataset.

KingBase database (2019) can be found here: https://archive.org/details/KingBaseLite2019
"""

import os 
import glob 
import re
import sys 

def process_games_from_PGN(PGN_filename, max_games_to_record = 5000):
    with open(PGN_filename,"rb") as file: 
        text = file.read().decode('latin-1')

    games = []
    game_num = 0
    for line in text.split("]"):
        winner = None 
        white_move = None 
        black_move = None 
        if (line[:6] == "\r\n\r\n1."):
            moves = []
            winner = None
            for move_encoding in line.split("."):
                entries = move_encoding.replace(" ","\n").replace("\r","\n").split("\n")
                #print(entries)
                cleaned_entries = []
                for entry in entries: 
                    if (entry != "" and entry != " "):
                        cleaned_entries.append(entry) 
                
                if (len(cleaned_entries) < 2):
                #print(cleaned_entries)
                    continue 

                white_move = cleaned_entries[0]
                black_move = cleaned_entries[1]
                if (black_move[:7] == "1/2-1/2"):
                    winner = "tie"
                    black_move = None 
                elif (black_move[:3] == "1-0"):
                    winner = "white"
                    black_move = None 
                elif (black_move[:3] == "0-1"):
                    winner = "black"
                    black_move = None 
                
                #print(white_move, black_move)
                if (black_move != None):
                    moves.extend([white_move, black_move])
                else:
                    moves.append(white_move)
                
                if (len(cleaned_entries) >= 3):
                    result = cleaned_entries[2] 
                if (result == "1/2-1/2"):
                    winner = "tie"
                elif (result == "1-0"):
                    winner = "white"
                elif (result == "0-1"):
                    winner = "black"
                
                if (winner != None):
                    break         
                
            if (winner != None):
                games.append(
                    {"winner": winner, "moves": moves}
                )
            game_num += 1
            
            if (game_num >= max_games_to_record):
                break
    
    return games 

#gathers information from a list of games to learn information 
#about how grandmasters play openings
def rank_openings(games, num_moves, K = 10):
    openings = {}
    for game in games: 
        moves = game["moves"]
        if (len(moves) < 2 * num_moves):
            continue 
        opening = tuple(moves[:2 * num_moves])
        if (opening in openings):
            openings[opening] += 1
        else: 
            openings[opening] = 1

    total_games = len(games)
    
    #outputs the top K openings with num_moves (a turn from each player counts as a move)
    for opening,freq in sorted(openings.items(), key = lambda item: item[1], reverse = True)[:K]:
        print(opening, "{:6f}".format(freq / total_games))
    
    #returns the full dictionary of openings 
    return openings

if __name__ == "__main__":

    PGN_filename = sys.argv[1]
    max_games = int(sys.argv[2])

    games = process_games_from_PGN(os.path.abspath(PGN_filename), max_games)
    print("Number of Games Recorded: {}".format(len(games)))
    print("\nSample Game: {}".format(games[0]))

