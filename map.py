from square import Square
from squareState import SquareState


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = []
        for x in range(width):
            self.squares.append([])
            for y in range(height):
                self.squares[x].append(Square(SquareState.NEUTRAL))

    def __str__(self):
        asciiMap = ""
        for y in range(self.height):
            for x in range(self.width):
                asciiMap += str(self.squares[x][y])
            asciiMap += "\r\n"
        return asciiMap

    def to_lines(self):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(str(self.squares[x][y]))
            lines.append(line)
        return lines

    # TODO draw players here or in screen.py
    # self.squares[player.posX][player.posY] = str(player)

    def update(self, player):
        self.squares[player.prev_pos_x][player.prev_pos_y] = Square(SquareState.TRAIL, player)
