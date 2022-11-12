from square import Square


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = []
        for x in range(width):
            self.squares.append([])
            for y in range(height):
                self.squares[x].append(Square(x, y))

    def __str__(self):
        asciiMap = ""
        for x in range(self.width):
            for y in range(self.height):
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
        if square.is_owned and square.owner is player:
            pass
        else:
            self.squares[player.prev_pos_x][player.prev_pos_y] = Square(
                player.prev_pos_x, player.prev_pos_y, square.owner, player
            )
