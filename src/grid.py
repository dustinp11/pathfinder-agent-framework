class Grid:
    def __init__(self, filename):
        self.grid = []
        self.start = None
        self.goal = None

        with open(filename) as f:
            for r, line in enumerate(f):
                row = []
                for c, char in enumerate(line.strip()):
                    if char == 'S':
                        self.start = (r, c)
                        row.append(0)
                    elif char == 'G':
                        self.goal = (r, c)
                        row.append(1)
                    elif char == '#':
                        row.append(None)  # Obstacle
                    elif char == '.':
                        row.append(1)
                    else:
                        row.append(int(char))
                self.grid.append(row)

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])

    def passable(self, pos):
        r, c = pos
        return self.grid[r][c] is not None

    def neighbors(self, pos):
        r, c = pos
        candidates = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        return [p for p in candidates if self.in_bounds(p) and self.passable(p)]

    def cost(self, pos):
        r, c = pos
        return self.grid[r][c]
