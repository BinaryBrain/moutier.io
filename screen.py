from color import Color
import constants


class Screen:
    def __init__(self, world_map):
        self.width = world_map.width + 2
        self.height = world_map.height + 2
        self.display = []
        for x in range(self.width):
            self.display.append([])
            for y in range(self.height):
                self.display[x].append(" ")

    def draw_on_map(self, characters, offset_x, offset_y):
        # Account for frame size
        offset_x += 1
        offset_y += 1
        for y, line in enumerate(characters):
            for x, char in enumerate(line):
                if x + offset_x < self.width and y + offset_y < self.height:
                    self.display[x + offset_x][y + offset_y] = char

    def draw_frame(self):
        c = Color["RESET"]
        self.display[0][0] = c + constants.FRAME_TOP_LEFT
        self.display[self.width - 1][0] = c + constants.FRAME_TOP_RIGHT
        self.display[0][self.height - 1] = c + constants.FRAME_BOTTOM_LEFT
        self.display[self.width - 1][self.height - 1] = c + constants.FRAME_BOTTOM_RIGHT
        for x in range(1, self.width - 1):
            self.display[x][0] = c + constants.FRAME_HORIZONTAL
            self.display[x][self.height - 1] = c + constants.FRAME_HORIZONTAL
        for y in range(1, self.height - 1):
            self.display[0][y] = c + constants.FRAME_VERTICAL
            self.display[self.width - 1][y] = c + constants.FRAME_VERTICAL

    def draw_timer(self, timer):
        start_x = round(self.width / 2 - len(str(timer)) / 2)
        self.display[start_x - 1][0] = " "
        for i, c in enumerate(str(timer)):
            self.display[start_x + i][0] = c
        self.display[start_x + len(str(timer))][0] = " "

    def getCurrentScreen(self):
        screen = ""
        for y in range(self.height):
            for x in range(self.width):
                screen += self.display[x][y]
            screen += "\r\n"
        screen += Color["RESET"]  # Don't bleed on the rest of the terminal
        screenHeight = screen.count("\n")
        screen = constants.CURSOR_PREVIOUS_LINE * screenHeight + screen
        return screen
