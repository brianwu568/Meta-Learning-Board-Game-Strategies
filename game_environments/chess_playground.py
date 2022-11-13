#Playground file

from chess_util import Board, Player, Piece, Pawn

board = Board()
white_player = Player(board, 0)
black_player = Player(board, 1)
p1 = Pawn((1, 6), "P", 0, board, white_player)
p2 = Pawn((2, 7), "P", 1, board, black_player)

current_player = white_player

while(True):
    board.print_board()
    current_player.find_moveset()
    current_player.move()
    
    if (current_player == white_player):
        current_player = black_player
    else:
        current_player = white_player