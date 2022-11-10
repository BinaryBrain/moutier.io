from square import Square
from trail_direction import TrailDirection


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.squares = []
        for x in range(width):
            self.squares.append([])
            for y in range(height):
                self.squares[x].append(Square())

    def __str__(self):
        asciiMap = ""
        for y in range(self.height):
            for x in range(self.width):
                asciiMap += str(self.squares[x][y])
            asciiMap += "\r\n"
        return asciiMap

    def to_lines(self):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(str(self.squares[x][y]))
            lines.append(line)
        return lines

    def update(self, player):
        square = self.squares[player.prev_pos_x][player.prev_pos_y]
        if square.is_owned and square.owner is player:
            pass
        else:
            self.squares[player.prev_pos_x][player.prev_pos_y] = Square(
                square.owner, player
            )

    def remove_player_trail(self, player):
        # This could be optimized by storing trails as a list of squares in Player
        for y in range(self.height):
            for x in range(self.width):
                square = self.squares[x][y]
                if square.has_trail and square.trail_owner is player:
                    self.squares[x][y].has_trail = False
                    self.squares[x][y].trail_owner = None

    def convert_owned_zone(self, player):
        # TODO Convert to owned zone
        # Optimize by taking only bounding box?
        # Check if other players have at least one owned square or kill them
        if self.is_trail_close_path(player):
            (x, y) = self.find_square_in_player_trail(player)
            self.fill_zone(player, x, y)
        else:
            # TODO convert only the Trail
            pass

    def find_square_in_player_trail(self, player):
        (x, y) = self.find_approximative_center_of_trail(player)
        if self.is_square_in_player_trail(player, x, y):
            print("Square is in trail")
            return (x, y)
        else:
            print("Square is not in trail")
            # TODO find next intersection and cross it to be inside trail

    def is_square_in_player_trail(self, player, pos_x, pos_y):
        counter = self.count_intersection_from_square(player, pos_x, pos_y)
        return counter % 2 == 1

    def count_intersection_from_square(self, player, pos_x, pos_y):
        counter = 0
        y = pos_y
        for x in range(pos_x, self.width):
            square = self.squares[x][y]

            if square.has_trail and square.trail_owner is player:
                direction = square.trail_direction
                if (
                    direction is TrailDirection.VERTICAL
                    or direction is TrailDirection.LEFT_UP
                    or direction is TrailDirection.RIGHT_UP
                ):
                    counter += 1

            if square.is_owned and square.owner is player:
                if self.is_connected_to_trail(player, x, y):
                    counter += 1
        return counter

    def is_connected_to_trail(self, player, pos_x, pos_y):
        # TODO BFS to say if the trail is connected or not
        return True

    def find_approximative_center_of_trail(self, player):
        counter = 0
        add_x = 0
        add_y = 0
        for y in range(self.height):
            for x in range(self.width):
                square = self.squares[x][y]
                if square.has_trail and square.trail_owner is player:
                    counter += 1
                    add_x += x
                    add_y += y
        return (round(add_x / counter), round(add_y / counter))

    def is_trail_close_path(self, player):
        # TODO
        return True

    def fill_zone(self, player, pos_x, pos_y):
        isLeftFree = True
        isRightFree = True
        x = pos_x
        y = pos_y
        # Scan line on the left side
        while isLeftFree and x >= 0:
            square = self.squares[x][y]
            print("isLeftFree", x, y, player.pos_x, player.pos_y)
            if square.trail_owner is not player:
                self.fill_square(player, x, y)
                x = x - 1
            else:
                isLeftFree = False
        most_left_x = x
        x = pos_x + 1
        # Scan line on the right side
        while isRightFree and x < self.width:
            square = self.squares[x][y]
            if square.trail_owner is not player:
                self.fill_square(player, x, y)
                x = x + 1
            else:
                isRightFree = False
        most_right_x = x

        # loop on line below and line above from min and max,
        # taking care of walls and if there is some,
        # cut in multiple line that will be called individually
        # TODO find a way to make it recursive or loop

    def fill_square(self, player, x, y):
        self.squares[x][y].is_owned = True
        self.squares[x][y].owner = player
