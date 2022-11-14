import copy
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
        print("\n  -----------------")
        for x in range(8, 0, -1):
            tmp = str(x) + " |"
            for y in range(1, 9):
                coord = (y, x)
                if self.coordinates_to_occupied[coord] == None:
                    tmp += " "
                else:
                    tmp += self.coordinates_to_occupied[coord].name
                tmp += "|"
            print(tmp)
            print("  -----------------")
        print("   A B C D E F G H")

class Player:
    def __init__(self, board: Board, color: int):
        self.color = color
        self.board = board
        self.opponent = None
        self.piece_set = []

    def add_opponent(self, opponent):
        self.opponent = opponent

    def find_moveset(self):
        moveset = {}
        capture_possible = False
        for x in self.piece_set:
            if len(x.capture_available()) > 0:
                capture_possible = True
                break
        if capture_possible:
            for x in self.piece_set:
                moveset[x.location] = x.capture_available()
        else:
            for x in self.piece_set:
                moveset[x.location] = x.find_moveset()
        
        return moveset

    def find_moveset_length(self):
        moveset = self.find_moveset()

        total = 0
        for x in moveset:
            total += len(moveset[x])
        return total

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
                
                if target_location_coords not in self.find_moveset()[prior_location_coords]:
                    needs_request = True
                    print("Not a valid move!")
                    continue
                return piece_in_prior_location.move(target_location_coords)
            else:
                print("Move cannot register. Try again.")
                needs_request = True
                continue



class Piece:
    def __init__(self, location, board, name, color, player):
        self.location = location
        self.name = name
        self.board = board
        self.player = player
        self.color = color
        board.coordinates_to_occupied[self.location] = self
        self.player.piece_set.append(self)  
        self.promoted = True

    def capture_available(self):
        available = []
        file, rank = self.location
        if (self.color == 0):
            one_left_location = (file - 1, rank + 1)
            one_right_location = (file + 1, rank + 1)
            two_left_location = (file - 2, rank + 2)
            two_right_location = (file + 2, rank + 2)
        else:
            one_left_location = (file - 1, rank - 1)
            one_right_location = (file + 1, rank - 1)
            two_left_location = (file - 2, rank - 2)
            two_right_location = (file + 2, rank - 2)
        if one_left_location in self.board.coordinates_to_occupied and two_left_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[one_left_location] != None and self.board.coordinates_to_occupied[one_left_location].color != self.color and self.board.coordinates_to_occupied[two_left_location] == None:
            available.append(two_left_location)
        if one_right_location in self.board.coordinates_to_occupied and two_right_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[one_right_location] != None and self.board.coordinates_to_occupied[one_right_location].color != self.color and self.board.coordinates_to_occupied[two_right_location] == None:
            available.append(two_right_location)

        if self.promoted:
            if (self.color == 0):
                backwards_one_left_location = (file - 1, rank - 1)
                backwards_one_right_location = (file + 1, rank - 1)
                backwards_two_left_location = (file - 2, rank - 2)
                backwards_two_right_location = (file + 2, rank - 2)
            else:
                backwards_one_left_location = (file - 1, rank + 1)
                backwards_one_right_location = (file + 1, rank + 1)
                backwards_two_left_location = (file - 2, rank + 2)
                backwards_two_right_location = (file + 2, rank + 2)
            if backwards_one_left_location in self.board.coordinates_to_occupied and backwards_two_left_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[backwards_one_left_location] != None and self.board.coordinates_to_occupied[backwards_one_left_location].color != self.color and self.board.coordinates_to_occupied[backwards_two_left_location] == None:
                available.append(backwards_two_left_location)
            if backwards_one_right_location in self.board.coordinates_to_occupied and backwards_two_right_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[backwards_one_right_location] != None and self.board.coordinates_to_occupied[backwards_one_right_location].color != self.color and self.board.coordinates_to_occupied[backwards_two_right_location] == None:
                available.append(backwards_two_right_location)


        return available

    def find_moveset(self):
        file, rank = self.location
        moveset = []
        available = self.capture_available()
        if (len(available) != 0):
            moveset = copy.deepcopy(available)
        else:
            if (self.color == 0):
                one_left_location = (file - 1, rank + 1)
                one_right_location = (file + 1, rank + 1)
            else:
                one_left_location = (file - 1, rank - 1)
                one_right_location = (file + 1, rank - 1)
            if one_left_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[one_left_location] == None:
                moveset.append(one_left_location)
            if one_right_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[one_right_location] == None:
                moveset.append(one_right_location)
            
            if self.promoted:
                if (self.color == 0):
                    backwards_one_left_location = (file - 1, rank - 1)
                    backwards_one_right_location = (file + 1, rank - 1)
                else:
                    backwards_one_left_location = (file - 1, rank + 1)
                    backwards_one_right_location = (file + 1, rank + 1)
                if backwards_one_left_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[backwards_one_left_location] == None:
                    moveset.append(backwards_one_left_location)
                if backwards_one_right_location in self.board.coordinates_to_occupied and self.board.coordinates_to_occupied[backwards_one_right_location] == None:
                    moveset.append(backwards_one_right_location)

        return moveset

    def move(self, target_location):
        piece_taken = False
        if abs(target_location[1] - self.location[1]) == 2:
            intermediate_location = (int((target_location[0] + self.location[0])/2), int((target_location[1] + self.location[1])/2))
            self.board.coordinates_to_occupied[intermediate_location].get_taken()
            piece_taken = True
        self.board.coordinates_to_occupied[self.location] = None
        self.location = target_location
        self.board.coordinates_to_occupied[self.location] = self

        if (self.color == 0 and self.location[1] == 8) or (self.color == 1 and self.location[1] == 1):
            self.promoted = True

        return piece_taken



    def get_taken(self):
        self.player.piece_set.remove(self)
        self.board.coordinates_to_occupied[self.location] = None


    