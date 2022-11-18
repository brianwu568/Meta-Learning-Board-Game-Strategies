import connect_4_playground
def read_data(filename):
    file = open(filename, 'r')
    new_file = open('boards.txt', 'w')
    total = 0
    lines = file.readlines()
    for x in lines:
        moveset = x.split(' ')[0]
        board = connect_4_playground.run_game_autonomous(moveset)
        str = ""
        for col in range(8, 0, -1):
            for row in range(1, 9):
                piece = board.coordinates_to_occupied[(row, col)]
                if (piece == None):
                    str += "0 "
                elif (piece.name == "W"):
                    str += "1 "
                else:
                    str += "-1 "
        str += x.split(" ")[1].strip() + "\n"
        new_file.write(str)
    new_file.close()
    file.close()


def validate():
    new_file = open('boards.txt', 'r')
    lines = new_file.readlines()
    for x in lines:
        length = len(x.split(" "))
        if length != 65:
            print(x)