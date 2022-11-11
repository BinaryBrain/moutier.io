import constants
from direction import Direction
from trail_direction import TrailDirection


class Square:
    def __init__(self, pos_x, pos_y, owner=None, trail_owner=None):
        self.owner = owner
        self.trail_owner = trail_owner
        self.is_owned = owner is not None
        self.has_trail = trail_owner is not None
        self.pos_x = pos_x
        self.pos_y = pos_y

        if self.has_trail:
            self.trail_direction = self.get_trail_direction(self.trail_owner)
        else:
            self.trail_direction = None

    def __str__(self):
        if self.has_trail:
            if self.trail_direction is TrailDirection.HORIZONTAL:
                return self.trail_owner.color + constants.TRAIL_HORIZONTAL
            elif self.trail_direction is TrailDirection.VERTICAL:
                return self.trail_owner.color + constants.TRAIL_VERTICAL
            elif self.trail_direction is TrailDirection.LEFT_DOWN:
                return self.trail_owner.color + constants.TRAIL_LEFT_DOWN
            elif self.trail_direction is TrailDirection.LEFT_UP:
                return self.trail_owner.color + constants.TRAIL_LEFT_UP
            elif self.trail_direction is TrailDirection.RIGHT_DOWN:
                return self.trail_owner.color + constants.TRAIL_RIGHT_DOWN
            elif self.trail_direction is TrailDirection.RIGHT_UP:
                return self.trail_owner.color + constants.TRAIL_RIGHT_UP
        # TODO Make this condition an if and have it has background color
        elif self.is_owned:
            return self.owner.color + constants.FULL_BLOCK
        else:
            return constants.EMPTY_SQUARE

    def get_trail_direction(self, player):
        pl = player.prev_direction is Direction.LEFT
        pr = player.prev_direction is Direction.RIGHT
        pu = player.prev_direction is Direction.UP
        pd = player.prev_direction is Direction.DOWN
        ps = player.prev_direction is Direction.STOP
        cl = player.direction is Direction.LEFT
        cr = player.direction is Direction.RIGHT
        cu = player.direction is Direction.UP
        cd = player.direction is Direction.DOWN

        if (pr and cu) or (pd and cl):
            return TrailDirection.LEFT_UP
        elif (pr and cd) or (pu and cl):
            return TrailDirection.LEFT_DOWN
        elif (pl and cu) or (pd and cr):
            return TrailDirection.RIGHT_UP
        elif (pl and cd) or (pu and cr):
            return TrailDirection.RIGHT_DOWN
        elif (pr and cl) or (pl and cr) or (pr and cr) or (pl and cl):
            return TrailDirection.HORIZONTAL
        elif (pu and cd) or (pd and cu) or (pu and cu) or (pd and cd):
            return TrailDirection.VERTICAL
        elif ps and (cl or cr):
            return TrailDirection.HORIZONTAL
        elif ps and (cu or cd):
            return TrailDirection.VERTICAL
        else:
            return TrailDirection.VERTICAL
