import time
import const
import collisions
from map import Map
from color import usable_colors
from screen import Screen
from trail_direction import TrailDirection
from direction import Direction
from heapq import heapify, heappush
from math import sqrt
from player import Player
from scores import Scores
from panel import Panel
from client_state import ClientState


class Game:
    def __init__(self, server):
        self.is_running = False
        self.fps = const.FPS
        self.map = Map(60, 30)
        self.scores = Scores(20, 20)
        self.server = server
        self.screen = Screen()
        self.timer = const.TIMER
        self.players = set()
        self.map_panel = Panel(60, 30, 0, 0, "Moutier.io")
        self.score_panel = Panel(20, 20, self.map_panel.width + 1, 0, "Scoreboard")

    def loop(self):
        if self.is_running:
            for player in self.players:
                player.update_direction()
                player.move(self.map)
                self.map.update(player)
                collisions.check_collisions(self, player)

            self.draw()

            self.timer -= 1
            if self.timer <= 0:
                self.timer = 0
                self.game_over()

    def draw(self):
        self.map_panel.title = str(self.timer)
        self.screen.draw_in_panel(self.map_panel, self.map.to_lines(self.players))
        max_score = self.map.width * self.map.height
        self.screen.draw_in_panel(
            self.score_panel, self.scores.to_lines(self.players, max_score)
        )
        self.screen.generate_next_display()
        self.sendScreen()

    def sendScreen(self):
        clients = map(lambda p: p.client, self.players)
        self.server.broadcast(clients, self.screen.getCurrentScreen())

    def add_player(self, client):
        client.state = ClientState.IN_GAME
        player = Player(
            client,
            next(
                c
                for c in usable_colors
                if not any(p for p in self.players if p.color is c)
            ),
        )
        self.players.add(player)

        self.score_panel.height = len(self.players) * 3
        self.screen.reset_panels()

        self.map.make_random_spawn(player)
        self.compute_scores()

        if not self.is_running and len(self.players) >= const.MIN_PLAYERS_TO_START:
            self.is_running = True

    def remove_player(self, client):
        player = next(p for p in self.players if p.client == client)
        self.players.remove(player)
        self.kill_player(player, player, False)
        self.score_panel.height = len(self.players) * 3
        self.screen.reset_panels()
        if len(self.players) == 0:
            self.game_over()

    def handle_input(self, client, key):
        if not self.is_running:
            return

        player = next(p for p in self.players if p.client == client)
        if key == const.KEY_UP and player.direction != Direction.DOWN:
            player.define_next_direction(Direction.UP)
        if key == const.KEY_DOWN and player.direction != Direction.UP:
            player.define_next_direction(Direction.DOWN)
        if key == const.KEY_LEFT and player.direction != Direction.RIGHT:
            player.define_next_direction(Direction.LEFT)
        if key == const.KEY_RIGHT and player.direction != Direction.LEFT:
            player.define_next_direction(Direction.RIGHT)

    def kill_player(self, dead_player, killer=None, respawn=True):
        dead_player.kill()
        self.remove_player_trail(dead_player)
        for x in range(len(self.map.squares)):
            for y in range(len(self.map.squares[x])):
                s = self.map.squares[x][y]
                if s.is_owned and s.owner is dead_player:
                    if killer is not dead_player:
                        s.owner = killer
                    else:
                        # suicide
                        s.is_owned = False
                        s.owner = None
        if respawn:
            self.map.make_random_spawn(dead_player)
        self.compute_scores(killer)

    def remove_player_trail(self, player):
        # This could be optimized by storing trails as a list of squares in Player
        player.has_trail = False
        for s in self.map.get_player_trail(player):
            s.has_trail = False
            s.trail_owner = None

    def convert_owned_zone(self, player):
        shortest_owned_path = self.a_star(player.trail_start, player.trail_end, player)
        if shortest_owned_path:
            squares = shortest_owned_path + self.map.get_player_trail(player)
            path_squares = self.convert_squares_to_path(player, squares)
            self.basic_fill_zone(player, path_squares)
            self.convert_trail_to_owned(player)
        else:
            self.convert_trail_to_owned(player)

        # Check if other players have at least one owned square or kill them
        self.compute_scores(player)

    def compute_scores(self, potential_killer=None):
        for p in self.players:
            p.score = 0
            for x in range(len(self.map.squares)):
                for y in range(len(self.map.squares[x])):
                    s = self.map.squares[x][y]
                    if s.is_owned and s.owner is p:
                        p.score += 1
            if p.score == 0:
                self.kill_player(p, potential_killer)

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
            if current_square.has_trail and current_square.trail_owner is player:
                path[current_square] = current_square.trail_direction
                continue

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

            # In some weird edge case, like player go out of the zone and back again
            if len(neighbors) < 2:
                continue

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
        # Two counters to double check my code :D
        # (I couldn't find the exact edge case)
        counter1 = 0
        counter2 = 0
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
                counter1 += 1

            if (
                direction is TrailDirection.VERTICAL
                or direction is TrailDirection.LEFT_DOWN
                or direction is TrailDirection.RIGHT_DOWN
            ):
                counter2 += 1

        return counter1 % 2 == 1 and counter2 % 2 == 1

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

    def game_over(self):
        self.is_running = False
        for p in self.players:
            p.define_next_direction(Direction.STOP)
            p.update_direction()

        self.draw()
        time.sleep(const.GAME_OVER_TIMER)  # FIXME this is blocking the loop
        self.server.game_over()
