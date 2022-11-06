from color import Color


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = ""
        self.loadAssets()

    def loadAssets(self):
        with open("assets/frame.txt", "r") as f:
            self.frame = f.read()

    def getCurrentScreen(self, worldMap):
        # screen = self.frame
        screen = str(worldMap)
        screen += Color["RESET"]  # Don't bleed on the rest of the terminal
        return screen
