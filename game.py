import time
import asyncio
import constants
import collisions
from map import Map
from screen import Screen
from square import Square
from trail_direction import TrailDirection
from direction import Direction
from heapq import heapify, heappush
from math import sqrt


class Game:
    def __init__(self, server):
        self.fps = constants.FPS
        self.map = Map(40, 40)
        self.server = server
        self.screen = Screen(40, 40)
        self.t = 0

    async def loop(self):
        while True:
            start_timer = time.time()
            for player in self.server.players:
                player.move(self.map)
                self.map.update(player)
                player.define_direction(player.direction)
                collisions.check_collisions(self, player)

            self.draw()
            end_timer = time.time()
            await asyncio.sleep(1 / constants.FPS - (end_timer - start_timer))
            self.t = self.t + 1

    def draw(self):
        self.screen.draw(self.map.to_lines(), 0, 0)
        for player in self.server.players:
            self.screen.draw([[str(player)]], player.pos_x, player.pos_y)
        self.sendScreen()

    def sendScreen(self):
        self.server.broadcast(self.screen.getCurrentScreen())

    def initialize_game(self):
        for i, player in enumerate(self.server.players):
            player.pos_x = 1
            player.pos_y = 1
            for x in range(3):
                for y in range(3):
                    self.map.squares[x][y] = Square(x, y, player)

    def remove_player_trail(self, player):
        # This could be optimized by storing trails as a list of squares in Player
        player.has_trail = False
        for s in self.map.get_player_trail(player):
            s.has_trail = False
            s.trail_owner = None

    def convert_owned_zone(self, player):
        # TODO Convert to owned zone
        # Check if other players have at least one owned square or kill them
        shortest_owned_path = self.a_star(player.trail_start, player.trail_end, player)
        if shortest_owned_path:
            squares = shortest_owned_path + self.map.get_player_trail(player)
            path_squares = self.convert_squares_to_path(player, squares)
            self.basic_fill_zone(player, path_squares)
            # (x, y) = self.find_square_in_player_trail(player)
            # self.fill_zone(player, x, y)
            self.convert_trail_to_owned(player)
        else:
            self.convert_trail_to_owned(player)
            print("Zone is not closed")

    def convert_trail_to_owned(self, player):
        player.has_trail = False
        for s in self.map.get_player_trail(player):
            s.has_trail = False
            s.trail_owner = None
            s.is_owned = True
            s.owner = player

    # This method is not really optimized but should work
    def basic_fill_zone(self, player, path_squares):
        # Optimize by taking only bounding box?
        squares_to_be_filled = []
        for x in range(len(self.map.squares)):
            for y in range(len(self.map.squares[x])):
                s = self.map.squares[x][y]
                if self.is_square_inside_player_trail(path_squares, s):
                    squares_to_be_filled.append(s)
        for square in squares_to_be_filled:
            square.is_owned = True
            square.owner = player

    def convert_squares_to_path(self, player, squares):
        path = {}
        for current_square in squares:

            def condition_func(s):
                return (s[0].is_owned and s[0].owner is player) or (
                    s[0].has_trail and s[0].trail_owner is player
                )

            neighbors = list(
                filter(
                    lambda n: n[0] in squares,
                    self.get_neighbors(current_square, condition_func),
                )
            )

            has_l = (
                neighbors[0][1] is Direction.LEFT or neighbors[1][1] is Direction.LEFT
            )
            has_r = (
                neighbors[0][1] is Direction.RIGHT or neighbors[1][1] is Direction.RIGHT
            )
            has_u = neighbors[0][1] is Direction.UP or neighbors[1][1] is Direction.UP
            has_d = (
                neighbors[0][1] is Direction.DOWN or neighbors[1][1] is Direction.DOWN
            )

            if has_l and has_u:
                path[current_square] = TrailDirection.LEFT_UP
            elif has_l and has_d:
                path[current_square] = TrailDirection.LEFT_DOWN
            elif has_r and has_u:
                path[current_square] = TrailDirection.RIGHT_UP
            elif has_r and has_d:
                path[current_square] = TrailDirection.RIGHT_DOWN
            elif has_l and has_r:
                path[current_square] = TrailDirection.HORIZONTAL
            elif has_u and has_d:
                path[current_square] = TrailDirection.VERTICAL

        return path

    def is_square_inside_player_trail(self, path_squares, candidate):
        counter = 0
        y = candidate.pos_y
        for x in range(candidate.pos_x, self.map.width):
            square = self.map.squares[x][y]
            if square not in path_squares:
                continue

            direction = path_squares[square]
            if (
                direction is TrailDirection.VERTICAL
                or direction is TrailDirection.LEFT_UP
                or direction is TrailDirection.RIGHT_UP
            ):
                counter += 1

        return counter % 2 == 1

    def a_star(self, start_square, end_square, player):
        discovered_squares = []
        heapify(discovered_squares)
        heappush(discovered_squares, (0, id(start_square), start_square))
        came_from = {}
        cost_from_start = {start_square: 0}
        cost_through_square = {start_square: self.h_func(start_square, end_square)}

        while len(discovered_squares) > 0:
            current = discovered_squares[0][2]
            if current is end_square:
                return self.reconstruct_path(came_from, end_square)

            discovered_squares.remove(discovered_squares[0])

            def condition_func(s):
                return s[0].is_owned and s[0].owner is player

            neighbors = self.get_neighbors(current, condition_func)
            for neighbor, direction in neighbors:
                tentative_cost_from_start = cost_from_start[current] + 1
                if (
                    neighbor not in cost_from_start
                    or tentative_cost_from_start < cost_from_start[neighbor]
                ):
                    came_from[neighbor] = current
                    cost_from_start[neighbor] = tentative_cost_from_start
                    cost_through_square[
                        neighbor
                    ] = tentative_cost_from_start + self.h_func(neighbor, end_square)
                    tup = (cost_from_start[neighbor], id(neighbor), neighbor)
                    if tup not in discovered_squares:
                        heappush(discovered_squares, tup)

        return None

    def h_func(self, square1, square2):
        return sqrt(
            abs(square1.pos_x - square2.pos_x) ** 2
            + abs(square1.pos_y - square2.pos_y) ** 2
        )

    def reconstruct_path(self, came_from, end_square):
        path = [end_square]
        should_continue = True
        while should_continue:
            if end_square in came_from:
                previous_square = came_from[end_square]
                path.insert(0, previous_square)
                end_square = previous_square
            else:
                should_continue = False
        return path

    def get_neighbors(self, square, condition_func):
        neighbors = []
        x = square.pos_x
        y = square.pos_y
        if x >= 1:
            neighbors.append((self.map.squares[x - 1][y], Direction.LEFT))
        if x < self.map.width - 1:
            neighbors.append((self.map.squares[x + 1][y], Direction.RIGHT))
        if y >= 1:
            neighbors.append((self.map.squares[x][y - 1], Direction.UP))
        if y < self.map.height - 1:
            neighbors.append((self.map.squares[x][y + 1], Direction.DOWN))

        neighbors = filter(condition_func, neighbors)

        return list(neighbors)
