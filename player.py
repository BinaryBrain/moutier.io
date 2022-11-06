from direction import Direction


class Player:
    def __init__(self, conn, name, symbol, color):
        self.conn = conn
        self.name = name
        self.symbol = symbol
        self.color = color
        self.posX = 0
        self.posY = 0
        self.direction = Direction.STOP

    def __str__(self):
        return f"{self.name} [{self.symbol}]"

    def move(self, worldMap):
        if self.direction is Direction.LEFT:
            self.posX -= 1
        if self.direction is Direction.RIGHT:
            self.posX += 1
        if self.direction is Direction.UP:
            self.posY -= 1
        if self.direction is Direction.DOWN:
            self.posY += 1

        if self.posX < 0:
            self.posX = 0
            self.direction = Direction.STOP
        if self.posX > worldMap.width - 1:
            self.posX = worldMap.width - 1
            self.direction = Direction.STOP
        if self.posY < 0:
            self.posY = 0
            self.direction = Direction.STOP
        if self.posY > worldMap.height - 1:
            self.posY = worldMap.height - 1
            self.direction = Direction.STOP
