#Playground file

from checkers_util import Board, Player, Piece




def run_game():
    board = Board()
    white_player = Player(board, 0)
    black_player = Player(board, 1)
    white_player.add_opponent(black_player)
    black_player.add_opponent(white_player)

    pieces = []
    for x in [1, 3, 5, 7]:
        for y in [1, 3]:
            pieces.append(Piece((x, y), board, "W", 0, white_player))
        pieces.append(Piece((x, 7), board, "B", 1, black_player))
    
    for x in [2, 4, 6, 8]:
        for y in [6, 8]:
            pieces.append(Piece((x, y), board, "B", 1, black_player))
        pieces.append(Piece((x, 2), board, "W", 0, white_player))
    current_player = white_player

    total = 0
    while(True):
        board.print_board()
        print(current_player.find_moveset())
        print(current_player.find_moveset_length())
        if (current_player.find_moveset_length() == 0):
            return 1 - current_player.color

        taken = current_player.move()

        if (not taken):
            if (current_player == white_player):
                current_player = black_player
            else:
                current_player = white_player
            total += 1
        else:
            total = 0
        if (total == 20):
            return -1

if __name__ == "__main__":
    winner = run_game()
    if (winner == 1):
        print("Black wins!")
    elif (winner == 0):
        print("White wins!")
    else:
        print("No one wins (draw)!")