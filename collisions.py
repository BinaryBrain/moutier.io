from direction import Direction


def check_collisions(game, player):
    square = game.map.squares[player.pos_x][player.pos_y]
    check_conquest(game, player, square)
    check_kill(game, player, square)
    check_new_trail(game, player, square)


def check_kill(game, killer, square):
    if square.has_trail:
        if killer is not square.trail_owner or killer.direction is not Direction.STOP:
            dead_player = square.trail_owner
            game.kill_player(dead_player, killer)


def check_conquest(game, player, square):
    if player.has_trail and square.is_owned and square.owner is player:
        player.trail_end = square
        game.convert_owned_zone(player)
        game.remove_player_trail(player)
        pass


def check_new_trail(game, player, square):
    if not square.is_owned or square.owner is not player:
        if not player.has_trail:
            player.has_trail = True
            player.trail_start = game.map.squares[player.prev_pos_x][player.prev_pos_y]
