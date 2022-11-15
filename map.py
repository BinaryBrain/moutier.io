from constants import SPAWN_MARGINS
import random
from square import Square
from direction import Direction
from color import Color


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = []
        for x in range(width):
            self.squares.append([])
            for y in range(height):
                self.squares[x].append(Square(x, y))

    def __str__(self):
        asciiMap = ""
        for x in range(self.width):
            for y in range(self.height):
                asciiMap += str(self.squares[x][y])
            asciiMap += "\r\n"
        return asciiMap

    def to_lines(self, players):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(str(self.squares[x][y]))
            lines.append(line)

        for player in players:
            s = self.squares[player.pos_x][player.pos_y]
            if s.is_owned and s.owner is player:
                color = s.get_background_color() + Color["BLACK"]
            else:
                color = s.get_background_color() + Color[player.color]
            lines[player.pos_y][player.pos_x] = color + str(player)
        return lines

    def update(self, player):
        square = self.squares[player.prev_pos_x][player.prev_pos_y]
        if square.is_owned and square.owner is player:
            pass
        else:
            self.squares[player.prev_pos_x][player.prev_pos_y] = Square(
                player.prev_pos_x, player.prev_pos_y, square.owner, player
            )

    def get_player_trail(self, player):
        trail = []
        for x in range(self.width):
            for y in range(self.height):
                square = self.squares[x][y]
                if square.has_trail and square.trail_owner is player:
                    trail.append(square)
        return trail

    def make_random_spawn(self, player):
        if self.width >= self.height:
            ratio = self.height / self.width
            if random.random() > ratio:
                pos = random.randint(SPAWN_MARGINS, self.width - SPAWN_MARGINS - 1)
                if random.randint(0, 1) == 0:
                    side = Direction.UP
                else:
                    side = Direction.DOWN
            else:
                pos = random.randint(SPAWN_MARGINS, self.height - SPAWN_MARGINS - 1)
                if random.randint(0, 1) == 0:
                    side = Direction.LEFT
                else:
                    side = Direction.RIGHT

        if side is Direction.UP:
            spawn = self.squares[pos][SPAWN_MARGINS]
        elif side is Direction.DOWN:
            spawn = self.squares[pos][self.height - SPAWN_MARGINS - 1]
        elif side is Direction.LEFT:
            spawn = self.squares[SPAWN_MARGINS][pos]
        else:
            spawn = self.squares[self.width - SPAWN_MARGINS - 1][pos]

        player.pos_x = spawn.pos_x
        player.pos_y = spawn.pos_y
        for x in range(spawn.pos_x - SPAWN_MARGINS, spawn.pos_x + SPAWN_MARGINS + 1):
            for y in range(
                spawn.pos_y - SPAWN_MARGINS, spawn.pos_y + SPAWN_MARGINS + 1
            ):
                self.squares[x][y] = Square(x, y, player)
