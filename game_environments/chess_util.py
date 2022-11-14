#Chess Gameplay Environment
import copy

#First coordinate is horizontal axis (files, letters), second coordinate is vertical axis (ranks, numbers)


class Board:
    def __init__(self):
        self.coordinates_to_names = {}
        self.names_to_coordinates = {}
        self.coordinates_to_occupied = {}
        alphabet = "abcdefgh"
        for x in range(1, 9):
            for y in range(1, 9):
                self.coordinates_to_names[(x, y)] =  alphabet[x - 1] + str(y)
                self.names_to_coordinates[alphabet[x - 1] + str(y)] = (x, y)
                self.coordinates_to_occupied[(x, y)] = None
    
    def print_board(self):
        print("\n  -------------------------")
        for x in range(8, 0, -1):
            tmp = str(x) + " |"
            for y in range(1, 9):
                coord = (y, x)
                if self.coordinates_to_occupied[coord] == None:
                    tmp += "  "
                else:
                    tmp += self.coordinates_to_occupied[coord].name
                tmp += "|"
            print(tmp)
            print("  -------------------------")
        print("   A  B  C  D  E  F  G  H")

class Player:
    def __init__(self, board: Board, color: int):
        self.color = color
        self.board = board
        self.opponent = None
        self.piece_set = []
        self.can_castle_kingside = True
        self.can_castle_queenside = True

    def add_opponent(self, opponent):
        self.opponent = opponent

    def find_moveset(self, board):
        moveset = {}
        player_king_location = None
        for location in board.coordinates_to_occupied:
            if isinstance(board.coordinates_to_occupied[location], King) and board.coordinates_to_occupied[location].color == self.color:
                player_king_location = location
                break
        for x in self.piece_set:
            piece_moveset = []
            if (not isinstance(x, King)):
                for y in x.find_moveset(board):
                    copied_board = copy.deepcopy(board)
                    copied_target_piece = copied_board.coordinates_to_occupied[x.location]
                    copied_target_piece.move(copied_board, y)
                    copied_king = copied_board.coordinates_to_occupied[player_king_location]
                    if (not copied_king.is_in_check(copied_board)):
                        piece_moveset.append(y)
                moveset[x.location] = piece_moveset
            else:
                moveset[x.location] = x.find_moveset(board)
        return moveset
        
    def find_moveset_length(self, board):
        moveset = self.find_moveset(board)
        #print(moveset)
        total = 0
        for x in moveset:
            total += len(moveset[x])
        return total

    def print_moveset(self):
        print("POSSIBLE PIECE MOVES:")
        for x in self.piece_set:
            print(x.name, ":", x.location)
            x.print_moveset()
            print("=============")

    def find_attackset(self, board):
        attackset = []
        for x in self.piece_set:
            attackset += x.find_attackset(board)
        #print("Attack set length:", len(list(set(attackset))))
        return list(set(attackset))

    def move(self, board):
        needs_request = True
        while(needs_request):
            needs_request = False
            if (self.color == 0):          
                requested_move = input("White's turn. Choose a move. \n")
            else:
                requested_move = input("Black's turn. Choose a move. \n")
            if (len(requested_move) == 5):
                split_ar = requested_move.split(" ")
                if len(split_ar) != 2:
                    needs_request = True
                    continue
                
                prior_location = split_ar[0]
                target_location = split_ar[1]
                if (prior_location not in board.names_to_coordinates or target_location not in board.names_to_coordinates):
                    needs_request = True
                    continue

                prior_location_coords = board.names_to_coordinates[prior_location]
                target_location_coords = board.names_to_coordinates[target_location]
                
                piece_in_prior_location = board.coordinates_to_occupied[prior_location_coords]
                if (piece_in_prior_location == None or piece_in_prior_location.color != self.color):
                    print("You don't have a piece there!")
                    needs_request = True
                    continue
                
                piece_moveset = piece_in_prior_location.find_moveset(board)
                if target_location_coords not in piece_moveset:
                    print("Not a valid move!")
                    needs_request = True
                    continue
                player_moveset = self.find_moveset(board)
                if target_location_coords not in player_moveset[prior_location_coords]:
                    print("King in check! Cannot move.")
                    needs_request = True
                    continue

                piece_in_prior_location.move(board, target_location_coords)
            else:
                print("Move cannot register. Try again.")
                needs_request = True
                continue



class Piece:
    def __init__(self, location: tuple, name: str, color: int, board: Board, player: Player):
        self.location = location
        self.name = name

        # white = 0, black = 1
        self.color = color
        self.board = board
        self.player = player
        board.coordinates_to_occupied[self.location] = self
        self.player.piece_set.append(self)

    def find_moveset(self, board):
        return NotImplementedError

    def find_attackset(self, board):
        return NotImplementedError

    def move(self, board, target_location):
        return NotImplementedError

    def print_moveset(self):
        print(self.find_moveset(self.board))
    
    def get_taken(self):
        self.player.piece_set.remove(self)

class Pawn(Piece):
    def find_moveset(self, board):
        moveset = []
        file, rank = self.location

        if self.color == 0:
            forward_1 = (file, rank + 1)
            diagonal_left = (file - 1, rank + 1)
            diagonal_right = (file + 1, rank + 1)
            if board.coordinates_to_occupied[forward_1] is None: 
                moveset.append(forward_1)
            if diagonal_left in board.coordinates_to_occupied and board.coordinates_to_occupied[diagonal_left] is not None and board.coordinates_to_occupied[diagonal_left].color == 1:
                moveset.append(diagonal_left)
            if diagonal_right in board.coordinates_to_occupied and board.coordinates_to_occupied[diagonal_right] is not None and board.coordinates_to_occupied[diagonal_right].color == 1:
                moveset.append(diagonal_right)
            if (rank == 2):      
                forward_2 = (file, rank + 2)                     
                if not board.coordinates_to_occupied[forward_2] and not board.coordinates_to_occupied[forward_1]: 
                    moveset.append(forward_2)

        else:
            forward_1 = (file, rank - 1)
            diagonal_left = (file - 1, rank - 1)
            diagonal_right = (file + 1, rank - 1)
            if board.coordinates_to_occupied[forward_1] is None: 
                moveset.append(forward_1)
            if diagonal_left in board.coordinates_to_occupied and board.coordinates_to_occupied[diagonal_left] is not None and board.coordinates_to_occupied[diagonal_left].color == 0:
                moveset.append(diagonal_left)
            if diagonal_right in board.coordinates_to_occupied and board.coordinates_to_occupied[diagonal_right] is not None and board.coordinates_to_occupied[diagonal_right].color == 0:
                moveset.append(diagonal_right)
            if (rank == 7):      
                forward_2 = (file, rank - 2)                     
                if not board.coordinates_to_occupied[forward_2] and not board.coordinates_to_occupied[forward_1]: 
                    moveset.append(forward_2)     
        
        return moveset

    def find_attackset(self, board):
        attackset = []
        file, rank = self.location

        if self.color == 0:
            diagonal_left = (file - 1, rank + 1)
            diagonal_right = (file + 1, rank + 1)
            if diagonal_left in board.coordinates_to_occupied:
                attackset.append(diagonal_left)
            if diagonal_right in board.coordinates_to_occupied:
                attackset.append(diagonal_right)

        else:
            diagonal_left = (file - 1, rank - 1)
            diagonal_right = (file + 1, rank - 1)
            if diagonal_left in board.coordinates_to_occupied:
                attackset.append(diagonal_left)
            if diagonal_right in board.coordinates_to_occupied:
                attackset.append(diagonal_right) 
        
        return attackset

    def move(self, board, target_location):
        
        if board.coordinates_to_occupied[target_location] is not None:
            board.coordinates_to_occupied[target_location].get_taken()
        
        board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        
        board.coordinates_to_occupied[self.location] = self

        if self.color == 0 and self.location[1] == 8:
            self.get_taken()
            new_piece = Queen(self.location, "WQ", 0, board, self.player)
            self.player.piece_set.append(new_piece)
        elif self.color == 1 and self.location[1] == 1:
            self.get_taken()
            new_piece = Queen(self.location, "BQ", 1, board, self.player)
            self.player.piece_set.append(new_piece)
        return board
        
class Knight(Piece):
    def find_moveset(self, board):
        file, rank = self.location

        moveset = []
        file_offset = [-2, -1, 1, 2, 2, 1, -1, -2]
        rank_offset = [-1, -2, -2, -1, 1, 2, 2, 1]

        for move in zip(file_offset, rank_offset):
            target_location = (file + move[0], rank + move[1])
            if target_location in board.coordinates_to_occupied and (board.coordinates_to_occupied[target_location] is None or board.coordinates_to_occupied[target_location].color != self.color):
                moveset.append(target_location)
        return moveset

    def find_attackset(self, board):
        file, rank = self.location

        attackset = []
        file_offset = [-2, -1, 1, 2, 2, 1, -1, -2]
        rank_offset = [-1, -2, -2, -1, 1, 2, 2, 1]

        for move in zip(file_offset, rank_offset):
            target_location = (file + move[0], rank + move[1])
            if target_location in board.coordinates_to_occupied:
                attackset.append(target_location)
        return attackset

    def move(self, board, target_location):
        
        if board.coordinates_to_occupied[target_location] is not None:
            board.coordinates_to_occupied[target_location].get_taken()
        
        board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        
        board.coordinates_to_occupied[self.location] = self
        return board

class Rook(Piece):
    def __init__(self, location: tuple, name: str, color: int, board: Board, player: Player):
        Piece.__init__(self, location, name, color, board, player)
        self.kingside = (sum(self.location) % 2) != self.player.color


    def find_moveset(self, board):
        file, rank = self.location
        moveset = []

        #move left:
        traverser = (file - 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)

        #move right
        traverser = (file + 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser) 

        #move up
        traverser = (file, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)    

        #move down
        traverser = (file, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)       

        return moveset

    def get_taken(self):
        Piece.get_taken(self)
        if (self.kingside):
            self.player.can_castle_kingside = False
        else:
            self.player.can_castle_queenside = False

    def find_attackset(self, board):
        file, rank = self.location
        attackset = []

        #move left:
        traverser = (file - 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)

        #move right
        traverser = (file + 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)

        #move up
        traverser = (file, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser) 

        #move down
        traverser = (file, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)   

        return attackset

    def move(self, board, target_location):
        if (self.kingside == True):
            self.player.can_castle_kingside = False
        else:
            self.player.can_castle_queenside = False

        if board.coordinates_to_occupied[target_location] is not None:
            board.coordinates_to_occupied[target_location].get_taken()
        
        board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        
        board.coordinates_to_occupied[self.location] = self

class Bishop(Piece):
    def find_moveset(self, board):
        file, rank = self.location
        moveset = []

        #move up left:
        traverser = (file - 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)

        #move up right
        traverser = (file + 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser) 

        #move down left
        traverser = (file - 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)    

        #move down right
        traverser = (file + 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)       

        return moveset

    def find_attackset(self, board):
        file, rank = self.location
        attackset = []

        #move up left:
        traverser = (file - 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if traverser in board.coordinates_to_occupied:
            attackset.append(traverser)   

        #move up right
        traverser = (file + 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if traverser in board.coordinates_to_occupied:
            attackset.append(traverser)   

        #move down left
        traverser = (file - 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if traverser in board.coordinates_to_occupied:
            attackset.append(traverser)     

        #move down right
        traverser = (file + 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if traverser in board.coordinates_to_occupied:
            attackset.append(traverser)       

        return attackset

    def move(self, board, target_location):
        
        if board.coordinates_to_occupied[target_location] is not None:
            board.coordinates_to_occupied[target_location].get_taken()
        
        board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        
        board.coordinates_to_occupied[self.location] = self

class Queen(Piece):
    def find_moveset(self, board):
        file, rank = self.location
        moveset = []

        #move left
        traverser = (file - 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)

        #move right
        traverser = (file + 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser) 

        #move up
        traverser = (file, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)    

        #move down
        traverser = (file, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser) 

        #move up left:
        traverser = (file - 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)

        #move up right
        traverser = (file + 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser) 

        #move down left
        traverser = (file - 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)    

        #move down right
        traverser = (file + 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            moveset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] != None):
            if board.coordinates_to_occupied[traverser].color != self.color:
                moveset.append(traverser)       

        return moveset

    def find_attackset(self, board):
        file, rank = self.location
        attackset = []

        #move left
        traverser = (file - 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)

        #move right
        traverser = (file + 1, rank)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)
        #move up
        traverser = (file, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)  

        #move down
        traverser = (file, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)

        #move up left:
        traverser = (file - 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)

        #move up right
        traverser = (file + 1, rank + 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] += 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)

        #move down left
        traverser = (file - 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] -= 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)  

        #move down right
        traverser = (file + 1, rank - 1)
        while traverser in board.coordinates_to_occupied and board.coordinates_to_occupied[traverser] == None:
            attackset.append(traverser)
            traverser = list(traverser)
            traverser[0] += 1
            traverser[1] -= 1
            traverser = tuple(traverser)
        if (traverser in board.coordinates_to_occupied):
            attackset.append(traverser)   

        return attackset

    def move(self, board, target_location):
        
        if board.coordinates_to_occupied[target_location] is not None:
            board.coordinates_to_occupied[target_location].get_taken()
        
        board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        
        board.coordinates_to_occupied[self.location] = self

        return board

class King(Piece):
    def __init__(self, location: tuple, name: str, color: int, board: Board, player: Player):
        Piece.__init__(self, location, name, color, board, player)

    def find_moveset(self, board):

        moveset = []
        file, rank = self.location

        opponent_attackset = self.player.opponent.find_attackset(board)

        file_offset = [-1, -1, 0, 1, 1, 1, 0, -1]
        rank_offset = [0, 1, 1, 1, 0, -1, -1, -1]

        for move in zip(file_offset, rank_offset):
            target_location = (file + move[0], rank + move[1])
            if target_location in board.coordinates_to_occupied and (board.coordinates_to_occupied[target_location] == None or board.coordinates_to_occupied[target_location].color != self.color):
                if target_location not in opponent_attackset:
                    moveset.append(target_location)


        #Castling
        if (self.player.can_castle_kingside and not self.is_in_check(board) and (file + 1, rank) not in opponent_attackset and (file + 2, rank) not in opponent_attackset and board.coordinates_to_occupied[(file + 1, rank)] == None and board.coordinates_to_occupied[(file + 2, rank)] == None):
            moveset.append((file + 2, rank))

        if (self.player.can_castle_queenside and not self.is_in_check(board) and (file - 1, rank) not in opponent_attackset and (file - 2, rank) not in opponent_attackset and (file - 3, rank) not in opponent_attackset and board.coordinates_to_occupied[(file - 1, rank)] == None and board.coordinates_to_occupied[(file - 2, rank)] == None and board.coordinates_to_occupied[(file - 3, rank)] == None):
            moveset.append((file - 2, rank))
            

        return moveset

    def find_attackset(self, board):
        attackset = []
        file, rank = self.location

        file_offset = [-1, -1, 0, 1, 1, 1, 0, -1]
        rank_offset = [0, 1, 1, 1, 0, -1, -1, -1]

        for move in zip(file_offset, rank_offset):
            target_location = (file + move[0], rank + move[1])
            if target_location in board.coordinates_to_occupied:
                attackset.append(target_location)
        return attackset

    def move(self, board, target_location):
        if board.coordinates_to_occupied[target_location] is not None:
            board.coordinates_to_occupied[target_location].get_taken()
        
        if (target_location[0] - self.location[0] == 2):
            #Castling kingside
            #Find kingside rook
            for piece in self.player.piece_set:
                if isinstance(piece, Rook):
                    if piece.kingside:
                        location = piece.location
                        piece.move(board, (location[0] - 2, location[1]))
                        break

        elif (target_location[0] - self.location[0] == -2):
            for piece in self.player.piece_set:
                if isinstance(piece, Rook):
                    if not piece.kingside:
                        location = piece.location
                        piece.move(board, (location[0] + 3, location[1]))
                        break
        board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        
        board.coordinates_to_occupied[self.location] = self
        self.player.can_castle_kingside = False
        self.player.can_castle_queenside = False
    def is_in_check(self, board):
        opponent_attackset = self.player.opponent.find_attackset(board)
        return self.location in opponent_attackset

    
