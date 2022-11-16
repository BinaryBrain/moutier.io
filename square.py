import const
from color import Color, BackgroundColor
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
        color = self.get_color()
        if self.has_trail:
            if self.trail_direction is TrailDirection.HORIZONTAL:
                return color + const.TRAIL_HORIZONTAL
            elif self.trail_direction is TrailDirection.VERTICAL:
                return color + const.TRAIL_VERTICAL
            elif self.trail_direction is TrailDirection.LEFT_DOWN:
                return color + const.TRAIL_LEFT_DOWN
            elif self.trail_direction is TrailDirection.LEFT_UP:
                return color + const.TRAIL_LEFT_UP
            elif self.trail_direction is TrailDirection.RIGHT_DOWN:
                return color + const.TRAIL_RIGHT_DOWN
            elif self.trail_direction is TrailDirection.RIGHT_UP:
                return color + const.TRAIL_RIGHT_UP
        elif self.is_owned:
            return color + const.EMPTY_SQUARE
        else:
            return color + const.EMPTY_SQUARE

    def get_color(self):
        color = self.get_background_color()
        if self.has_trail:
            color += Color[self.trail_owner.color]
        return color

    def get_background_color(self):
        if self.is_owned:
            return BackgroundColor[self.owner.color]
        else:
            return BackgroundColor["BLACK"]

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
