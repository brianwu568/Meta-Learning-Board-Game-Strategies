#Playground file

from chess_util import Board, Player, Piece, Pawn, Knight, Rook, Bishop, Queen

board = Board()
white_player = Player(board, 0)
black_player = Player(board, 1)
white_player.add_opponent(black_player)
black_player.add_opponent(white_player)
black_player.check_opponent()
input()
#p1 = Pawn((1, 6), "P", 0, board, white_player)
#p2 = Pawn((2, 7), "P", 1, board, black_player)
h1w = Queen((1, 1), "B", 0, board, white_player)
h2w = Queen((3, 1), "B", 0, board, white_player)

h1b = Queen((4, 8), "B", 1, board, black_player)
h2b = Queen((3, 5), "B", 1, board, black_player)

current_player = white_player

while(True):
    board.print_board()
    current_player.print_moveset()
    current_player.move()
    
    if (current_player == white_player):
        current_player = black_player
    else:
        current_player = white_player