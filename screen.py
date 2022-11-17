from color import Color
import const


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
            self.add_frame(panel)
            self.compute_screen_size()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if x < self.width and y < self.height:
                    panel.lines[x][y] = char

    def add_frame(self, panel):
        width = panel.width + 2
        height = panel.height + 2
        o_x = panel.offset_x
        o_y = panel.offset_y

        self.add_frame_element(0b0101, o_x, o_y)
        self.add_frame_element(0b0110, o_x + width - 1, o_y)
        self.add_frame_element(0b1001, o_x, o_y + height - 1)
        self.add_frame_element(0b1010, o_x + width - 1, o_y + height - 1)
        for x in range(o_x + 1, o_x + width - 1):
            self.add_frame_element(0b0011, x, o_y)
            self.add_frame_element(0b0011, x, o_y + height - 1)
        for y in range(o_y + 1, o_y + height - 1):
            self.add_frame_element(0b1100, o_x, y)
            self.add_frame_element(0b1100, o_x + width - 1, y)

    def add_frame_element(self, frame_element, x, y):
        if (x, y) not in self.frame_elements:
            self.frame_elements[(x, y)] = frame_element
        else:
            self.frame_elements[(x, y)] |= frame_element

    def draw_frames(self):
        c = Color["RESET"]
        for coords in self.frame_elements:
            self.display[coords[0]][coords[1]] = (
                c + const.FRAME_PART[self.frame_elements[coords]]
            )

    def reset_panels(self):
        self.panels = []
        self.frame_elements = {}
        self.set_empty_screen()

    def compute_screen_size(self):
        max_width = 0
        max_height = 0
        for p in self.panels:
            max_width = max(max_width, p.offset_x + p.width + 2)
            max_height = max(max_height, p.offset_y + p.height + 2)

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

    def generate_next_display(self):
        for p in self.panels:
            for y in range(p.height):
                for x in range(p.width):
                    if x == p.width - 1:
                        self.display[x + p.offset_x + 1][y + p.offset_y + 1] = (
                            p.lines[x][y] + Color["RESET"]
                        )
                    else:
                        self.display[x + p.offset_x + 1][y + p.offset_y + 1] = p.lines[
                            x
                        ][y]
        self.draw_frames()

        for p in self.panels:
            start_x = round(p.width / 2 - len(p.title) / 2)
            self.display[p.offset_x + start_x - 1][p.offset_y] = " "
            for i, c in enumerate(p.title):
                self.display[p.offset_x + start_x + i][p.offset_y] = c
            self.display[p.offset_x + start_x + len(p.title)][p.offset_y] = " "

    def getCurrentScreen(self):
        self.compute_screen_size()
        screen = ""
        for y in range(self.height):
            for x in range(self.width):
                screen += self.display[x][y]
            screen += "\r\n"
        screen += Color["RESET"]  # Don't bleed on the rest of the terminal
        screenHeight = screen.count("\n")
        screen = const.CURSOR_PREVIOUS_LINE * screenHeight + screen
        return screen
