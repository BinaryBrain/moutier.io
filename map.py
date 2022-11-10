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
        # Check if other players have at least one owned square or kill them
        if self.is_trail_close_path(player):
            self.basic_fill_zone(player)
            # (x, y) = self.find_square_in_player_trail(player)
            # self.fill_zone(player, x, y)
        else:
            # TODO convert only the Trail
            pass

    def is_trail_close_path(self, player):
        # TODO
        return True

    # This method is not really optimized but should work
    def basic_fill_zone(self, player):
        # Optimize by taking only bounding box?
        squares_to_be_filled = []
        for x in range(len(self.squares)):
            for y in range(len(self.squares[x])):
                if self.is_square_inside_player_trail(player, x, y):
                    squares_to_be_filled.append(self.squares[x][y])
        for square in squares_to_be_filled:
            square.is_owned = True
            square.owner = player

    def is_square_inside_player_trail(self, player, pos_x, pos_y):
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
                if self.is_square_connected_to_trail(player, x, y):
                    counter += 1
        return counter

    def is_square_connected_to_trail(self, player, pos_x, pos_y):
        # TODO BFS to say if the trail is connected to a square or not
        return True

    # def find_square_in_player_trail(self, player):
    #    (x, y) = self.find_approximative_center_of_trail(player)
    #    if self.is_square_inside_player_trail(player, x, y):
    #        print("Square is in trail")
    #        return (x, y)
    #    else:
    #        print("Square is not in trail")
    #        # TODO find next intersection and cross it to be inside trail

    # def find_approximative_center_of_trail(self, player):
    #     counter = 0
    #     add_x = 0
    #     add_y = 0
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             square = self.squares[x][y]
    #             if square.has_trail and square.trail_owner is player:
    #                 counter += 1
    #                 add_x += x
    #                 add_y += y
    #     return (round(add_x / counter), round(add_y / counter))
