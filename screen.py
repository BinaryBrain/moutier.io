from color import Color
import constants


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = ""
        self.loadAssets()
        self.display = []
        for x in range(self.width):
            self.display.append([])
            for y in range(self.height):
                self.display[x].append(" ")

    def loadAssets(self):
        with open("assets/frame.txt", "r") as f:
            self.frame = f.read()

    def draw(self, characters, offset_x, offset_y):
        for y, line in enumerate(characters):
            for x, char in enumerate(line):
                if x + offset_x < self.width and y + offset_y < self.height:
                    self.display[x + offset_x][y + offset_y] = char

    def getCurrentScreen(self):
        screen = ""
        for y in range(self.height):
            for x in range(self.width):
                screen += self.display[x][y]
            screen += "\r\n"
        screen += Color["RESET"]  # Don't bleed on the rest of the terminal
        screenHeight = screen.count('\n')
        screen = constants.CURSOR_PREVIOUS_LINE * screenHeight + screen
        return screen
