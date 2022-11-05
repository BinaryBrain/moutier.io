class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = ""
        self.loadAssets()

    def loadAssets(self):
        f = open("assets/frame.txt", "r")
        self.frame = f.read()

    def getCurrentScreen(self):
        return self.frame
