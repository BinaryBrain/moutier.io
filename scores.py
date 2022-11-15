from color import Color


class Scores:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def to_lines(self, players, max_score):
        lines = []
        for x in range(self.width):
            lines.append([])
            for y in range(self.height):
                lines[x].append(" ")

        y = 0
        for p in players:
            x = 0
            for i, c in enumerate(p.client.name):
                lines[y][x + i] = c

            y += 1

            x = 0
            score = f"{p.score} {round(p.score * 100/max_score)}%"
            for i, c in enumerate(score):
                lines[y][x + i] = c

            y += 2

        for line in lines:
            line[0] = Color["RESET"] + line[0]
        return lines
