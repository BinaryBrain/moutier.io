from color import Color


class Scores:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.padding = 1

    def to_lines(self, players, max_score):
        lines = []
        for x in range(self.width):
            lines.append([])
            for y in range(self.height):
                lines[x].append(" ")

        y = 0
        for p in players:
            x = self.padding
            for i, c in enumerate(p.client.name):
                if x + i > self.width - 2:
                    break
                if i == 0:
                    lines[y][x + i] = Color[p.color] + c
                else:
                    lines[y][x + i] = c
            lines[y][x + i] = lines[y][x + i] + Color["RESET"]

            y += 1

            x = self.padding
            score = f"{p.score} {round(p.score * 100/max_score)}%"
            for i, c in enumerate(score):
                lines[y][x + i] = c

            y += 2

        for line in lines:
            line[0] = Color["RESET"] + line[0]
        return lines
