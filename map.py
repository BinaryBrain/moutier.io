class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = []
        for x in range(width):
            self.squares.append([])
            for y in range(height):
                self.squares[x].append(' ')

    def __str__(self):
        asciiMap = ""
        for x in range(self.width):
            for y in range(self.height):
                asciiMap += str(self.squares[x][y])
            asciiMap += "\r\n"
        return asciiMap
