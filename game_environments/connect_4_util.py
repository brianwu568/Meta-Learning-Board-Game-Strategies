import copy
class Board:
    def __init__(self):
        self.coordinates_to_names = {}
        self.names_to_coordinates = {}
        self.coordinates_to_occupied = {}
        self.columns = {}
        alphabet = "abcdefgh"
        for x in range(1, 9):
            for y in range(1, 9):
                self.coordinates_to_names[(x, y)] =  alphabet[x - 1] + str(y)
                self.names_to_coordinates[alphabet[x - 1] + str(y)] = (x, y)
                self.coordinates_to_occupied[(x, y)] = None

    def check_win(self):
        #vertical
        for column in range(1, 9):
            for row in range(1, 6):
                if (self.coordinates_to_occupied[(column, row)] != None):
                    holder = self.coordinates_to_occupied[(column, row)].color
                    for offset in range(1, 4):
                        if (self.coordinates_to_occupied[(column, row + offset)] == None or self.coordinates_to_occupied[(column, row + offset)].color != holder):
                            holder = -1
                            break
                    if holder != -1:
                        return holder

        #horizontal
        for column in range(1, 6):
            for row in range(1, 9):
                if (self.coordinates_to_occupied[(column, row)] != None):
                    holder = self.coordinates_to_occupied[(column, row)].color
                    for offset in range(1, 4):
                        if (self.coordinates_to_occupied[(column + offset, row)] == None or self.coordinates_to_occupied[(column + offset, row)].color != holder):
                            holder = -1
                            break
                    if holder != -1:
                        return holder

        #main diagonal
        for column in range(1, 6):
            for row in range(4, 9):
                if (self.coordinates_to_occupied[(column, row)] != None):
                    holder = self.coordinates_to_occupied[(column, row)].color
                    for offset in range(1, 4):
                        if (self.coordinates_to_occupied[(column + offset, row - offset)] == None or self.coordinates_to_occupied[(column + offset, row - offset)].color != holder):
                            holder = -1
                            break
                    if holder != -1:
                        return holder

        #off diagonal
        for column in range(1, 6):
            for row in range(1, 6):
                if (self.coordinates_to_occupied[(column, row)] != None):
                    holder = self.coordinates_to_occupied[(column, row)].color
                    for offset in range(1, 4):
                        if (self.coordinates_to_occupied[(column + offset, row + offset)] == None or self.coordinates_to_occupied[(column + offset, row + offset)].color != holder):
                            holder = -1
                            break
                    if holder != -1:
                        return holder
        
        return -1

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
        moveset = []
        for column in range(1, 9):
            if self.board.coordinates_to_occupied[(column, 8)] == None:
                moveset.append(column)
        return moveset

    def move(self):
        needs_request = True
        while(needs_request):
            needs_request = False
            if (self.color == 0):          
                requested_move = input("White's turn. Choose a move. \n")
            else:
                requested_move = input("Black's turn. Choose a move. \n")

            if (len(requested_move) != 1):
                needs_request = True
                print("Move must be a single column letter. Try again.")
            if requested_move not in "abcdefgh":
                needs_request = True
                print("Move must be in range a-h. Try again.")
            
            column = "abcdefgh".index(requested_move) + 1
            if self.board.coordinates_to_occupied[(column, 8)] != None:
                needs_request = True
                print("Column no longer available. Try again.")

        row = 1
        while(self.board.coordinates_to_occupied[(column, row)] != None):
            row += 1      
        if (self.color == 0):
            name = "W"
        else:
            name = "B"
        new_piece = Piece((column, row), self.board, name, self.color, self)
        self.board.coordinates_to_occupied[(column, row)] = new_piece
        self.piece_set.append(new_piece)

class Piece:
    def __init__(self, location, board, name, color, player):
        self.location = location
        self.name = name
        self.board = board
        self.player = player
        self.color = color
        board.coordinates_to_occupied[self.location] = self
        self.player.piece_set.append(self)  



    