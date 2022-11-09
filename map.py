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

    def update(self, player):
        square = self.squares[player.prev_pos_x][player.prev_pos_y]
        if square.state is SquareState.OWNED and square.owner is player:
            pass
        else:
            self.squares[player.prev_pos_x][player.prev_pos_y] = Square(SquareState.TRAIL, player)

    def remove_player_trail(self, player):
        for y in range(self.height):
            for x in range(self.width):
                square = self.squares[x][y]
                if square.state is SquareState.TRAIL and square.owner is player:
                    self.squares[x][y].state = SquareState.NEUTRAL
                    self.squares[x][y].owner = None

    def convert_owned_zone(self, player):
        # TODO Convert to owned zone
        pass
