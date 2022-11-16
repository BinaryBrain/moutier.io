class Panel:
    def __init__(self, width, height, offset_x, offset_y, title):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.title = title
        self.lines = []
        for x in range(self.width):
            self.lines.append([])
            for y in range(self.height):
                self.lines[x].append(" ")
