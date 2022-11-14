from direction import Direction
import constants


class Player:
    def __init__(self, client, color):
        self.client = client
        self.color = color
        self.prev_pos_x = 0
        self.prev_pos_y = 0
        self.pos_x = 0
        self.pos_y = 0
        self.prev_direction = Direction.STOP
        self.direction = Direction.STOP
        self.has_trail = False
        self.alive = True
        self.trail_start = None
        self.trail_end = None
        self.score = 0

    def __str__(self):
        if self.direction is Direction.UP:
            return constants.PLAYER_UP
        elif self.direction is Direction.DOWN:
            return constants.PLAYER_DOWN
        elif self.direction is Direction.LEFT:
            return constants.PLAYER_LEFT
        elif self.direction is Direction.RIGHT:
            return constants.PLAYER_RIGHT
        else:
            return constants.PLAYER_STOP

    def define_direction(self, direction):
        if self.direction is not Direction.STOP:
            self.prev_direction = self.direction
        self.direction = direction

    def move(self, worldMap):
        self.prev_pos_x = self.pos_x
        self.prev_pos_y = self.pos_y

        if self.direction is Direction.LEFT:
            self.pos_x -= 1
        if self.direction is Direction.RIGHT:
            self.pos_x += 1
        if self.direction is Direction.UP:
            self.pos_y -= 1
        if self.direction is Direction.DOWN:
            self.pos_y += 1

        if self.pos_x < 0:
            self.pos_x = 0
            self.direction = Direction.STOP
        if self.pos_x > worldMap.width - 1:
            self.pos_x = worldMap.width - 1
            self.direction = Direction.STOP
        if self.pos_y < 0:
            self.pos_y = 0
            self.direction = Direction.STOP
        if self.pos_y > worldMap.height - 1:
            self.pos_y = worldMap.height - 1
            self.direction = Direction.STOP

    def kill(self):
        self.alive = False
