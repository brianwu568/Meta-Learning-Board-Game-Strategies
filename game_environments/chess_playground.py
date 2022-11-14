#Playground file

from chess_util import Board, Player, Piece, Pawn, Knight, Rook, Bishop, Queen, King



#p1 = Pawn((1, 6), "P", 0, board, white_player)
#p2 = Pawn((2, 7), "P", 1, board, black_player)



def run_game():
    board = Board()
    white_player = Player(board, 0)
    black_player = Player(board, 1)
    white_player.add_opponent(black_player)
    black_player.add_opponent(white_player)

    pieces = []
    pieces.append(King((5, 1), "WK", 0, board, white_player))
    pieces.append(King((5, 8), "BK", 1, board, black_player))
    pieces.append(Queen((4, 1), "WQ", 0, board, white_player))
    pieces.append(Queen((4, 8), "BQ", 1, board, black_player))
    for x in range(1, 9):
        pieces.append(Pawn((x, 2), "WP", 0, board, white_player))
        pieces.append(Pawn((x, 7), "BP", 1, board, black_player))
    for x in [1, 8]:
        pieces.append(Rook((x, 1), "WR", 0, board, white_player))
        pieces.append(Rook((x, 8), "BR", 1, board, black_player))
    for x in [2, 7]:
        pieces.append(Knight((x, 1), "WN", 0, board, white_player))
        pieces.append(Knight((x, 8), "BN", 1, board, black_player))
    for x in [3, 6]:
        pieces.append(Bishop((x, 1), "WB", 0, board, white_player))
        pieces.append(Bishop((x, 8), "BB", 1, board, black_player))

    current_player = white_player

    while(True):
        board.print_board()
        #print(current_player.find_moveset_length(board))
        if (current_player.find_moveset_length(board) == 0):
            for x in current_player.piece_set:
                if isinstance(x, King):
                    if x.is_in_check(board):
                        return 1 - current_player.color
                    else:
                        return -1
                    
        current_player.move(board)
        
        if (current_player == white_player):
            current_player = black_player
        else:
            current_player = white_player

if __name__ == "__main__":
    winner = run_game()
    if (winner == 1):
        print("Black wins!")
    elif (winner == 0):
        print("White wins!")
    else:
        print("No one wins (draw)!")