#Playground file

from connect_4_util import Board, Player




def run_game():
    board = Board()
    white_player = Player(board, 0)
    black_player = Player(board, 1)
    white_player.add_opponent(black_player)
    black_player.add_opponent(white_player)

    current_player = white_player

    total = 0
    while(True):
        board.print_board()
        current_player.move()
        
        win_status = board.check_win()
        if (win_status != -1):
            return win_status

        if (current_player == white_player):
            current_player = black_player
        else:
            current_player = white_player
        if (len(current_player.find_moveset()) == 0):
            return -1

def run_game_autonomous(moveset):
    board = Board()
    white_player = Player(board, 0)
    black_player = Player(board, 1)
    white_player.add_opponent(black_player)
    black_player.add_opponent(white_player)

    current_player = white_player

    total = 0
    for x in moveset:
        #board.print_board()
        current_player.move_autonomous(x)
        if (current_player == white_player):
            current_player = black_player
        else:
            current_player = white_player
    return board

if __name__ == "__main__":
    winner = run_game()
    if (winner == 1):
        print("Black wins!")
    elif (winner == 0):
        print("White wins!")
    else:
        print("No one wins (draw)!")