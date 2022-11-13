#Chess Gameplay Environment

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
        for x in range(8, 0, -1):
            tmp = "|"
            for y in range(1, 9):
                coord = (y, x)
                if self.coordinates_to_occupied[coord] == None:
                    tmp += "x"
                else:
                    tmp += self.coordinates_to_occupied[coord].name
                tmp += "|"
            print(tmp)
            print("-----------------")


class Player:
    def __init__(self, board: Board, color: int):
        self.color = color
        self.board = board

        self.piece_set = []

    def find_moveset(self):
        print("POSSIBLE MOVES:")
        for x in self.piece_set:
            print(x.name, ":", x.location)
            x.print_moveset()
            print("=============")

    def move(self):
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
                if (prior_location not in self.board.names_to_coordinates or target_location not in self.board.names_to_coordinates):
                    needs_request = True
                    continue

                prior_location_coords = self.board.names_to_coordinates[prior_location]
                target_location_coords = self.board.names_to_coordinates[target_location]
                
                piece_in_prior_location = self.board.coordinates_to_occupied[prior_location_coords]
                if (piece_in_prior_location == None or piece_in_prior_location.color != self.color):
                    print("You don't have a piece there!")
                    needs_request = True
                    continue
                
                moveset = piece_in_prior_location.find_moveset()
                if target_location_coords not in moveset:
                    print("Not a valid move!")
                    needs_request = True
                    continue
                piece_in_prior_location.move(target_location_coords)
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

        self.board.coordinates_to_occupied[self.location] = self
        self.player.piece_set.append(self)

    def find_moveset(self):
        return NotImplementedError
    
    def move(self, target_location):
        return NotImplementedError

    def print_moveset(self):
        print(self.find_moveset())
    
    def get_taken(self):
        self.player.piece_set.remove(self)


class Pawn(Piece):
    def find_moveset(self):
        moveset = []
        file, rank = self.location

        if self.color == 0:
            forward_1 = (file, rank + 1)
            diagonal_left = (file - 1, rank + 1)
            diagonal_right = (file + 1, rank + 1)
            if self.board.coordinates_to_occupied[forward_1] is None: 
                moveset.append(forward_1)
            if diagonal_left in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[diagonal_left] is not None and self.board.coordinates_to_occupied[diagonal_left].color == 1:
                moveset.append(diagonal_left)
            if diagonal_right in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[diagonal_right] is not None and self.board.coordinates_to_occupied[diagonal_right].color == 1:
                moveset.append(diagonal_right)
            if (rank == 2):      
                forward_2 = (file, rank + 2)                     
                if not self.board.coordinates_to_occupied[forward_2]: 
                    moveset.append(forward_2)

        else:
            forward_1 = (file, rank - 1)
            diagonal_left = (file - 1, rank - 1)
            diagonal_right = (file + 1, rank - 1)
            if self.board.coordinates_to_occupied[forward_1] is None: 
                moveset.append(forward_1)
            if diagonal_left in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[diagonal_left] is not None and self.board.coordinates_to_occupied[diagonal_left].color == 0:
                moveset.append(diagonal_left)
            if diagonal_right in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[diagonal_right] is not None and self.board.coordinates_to_occupied[diagonal_right].color == 1:
                moveset.append(diagonal_right)
            if (rank == 7):      
                forward_2 = (file, rank - 2)                     
                if not self.board.coordinates_to_occupied[forward_2]: 
                    moveset.append(forward_2)     
        
        return moveset

    def move(self, target_location):
        
        if self.board.coordinates_to_occupied[target_location] is not None:
            self.board.coordinates_to_occupied[target_location].get_taken()
        
        self.board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        
        self.board.coordinates_to_occupied[self.location] = self

        if self.color == 0 and self.location[1] == 8:
            self.get_taken()
            new_piece = Pawn(self.location, "White Queen (Promoted)", 0, self.board, self.player)
            self.player.piece_set.append(new_piece)
