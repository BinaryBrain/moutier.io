from color import Color
import constants


class Screen:
    def __init__(self):
        self.display = []
        self.panels = []
        self.frame_elements = {}
        self.width = 0
        self.height = 0
        self.set_empty_screen()

    def draw_in_panel(self, panel, lines):
        if panel not in self.panels:
            self.panels.append(panel)
            self.compute_screen_size()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if x < self.width and y < self.height:
                    panel.lines[x][y] = char

    def add_frame(self, width, height):
        self.frame_elements[(0, 0)] = constants.FRAME_TOP_LEFT
        self.frame_elements[(width - 1, 0)] = constants.FRAME_TOP_RIGHT
        self.frame_elements[(0, height - 1)] = constants.FRAME_BOTTOM_LEFT
        self.frame_elements[(width - 1, height - 1)] = constants.FRAME_BOTTOM_RIGHT
        for x in range(1, width - 1):
            self.frame_elements[(x, 0)] = constants.FRAME_HORIZONTAL
            self.frame_elements[(x, height - 1)] = constants.FRAME_HORIZONTAL
        for y in range(1, height - 1):
            self.frame_elements[(0, y)] = constants.FRAME_VERTICAL
            self.frame_elements[(width - 1, y)] = constants.FRAME_VERTICAL

    def draw_frame(self, panel):
        c = Color["RESET"]
        for coords in self.frame_elements:
            self.display[coords[0]][coords[1]] = c + self.frame_elements[coords]

    def draw_timer(self, timer):
        start_x = round(self.width / 2 - len(str(timer)) / 2)
        self.display[start_x - 1][0] = " "
        for i, c in enumerate(str(timer)):
            self.display[start_x + i][0] = c
        self.display[start_x + len(str(timer))][0] = " "

    def compute_screen_size(self):
        max_width = 0
        max_height = 0
        for p in self.panels:
            max_width = max(max_width, p.offset_x + p.width)
            max_height = max(max_height, p.offset_y + p.height)

        if max_width > self.width or max_height > self.height:
            self.width = max_width
            self.height = max_height
            self.set_empty_screen()

    def set_empty_screen(self):
        self.display = []
        for x in range(self.width):
            self.display.append([])
            for y in range(self.height):
                self.display[x].append(" ")

    def getCurrentScreen(self):
        self.compute_screen_size()
        screen = ""
        for p in self.panels:
            self.draw_frame(p)
            for y in range(p.height):
                for x in range(p.width):
                    self.display[x + p.offset_x][y + p.offset_y] = p.lines[x][y]

        for y in range(self.height):
            for x in range(self.width):
                screen += self.display[x][y]
            screen += "\r\n"
        screen += Color["RESET"]  # Don't bleed on the rest of the terminal
        screenHeight = screen.count("\n")
        screen = constants.CURSOR_PREVIOUS_LINE * screenHeight + screen
        return screen
