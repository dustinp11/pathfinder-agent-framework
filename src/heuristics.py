def heuristic(grid, point):
    """Returns manhattan distance of a point given a grid and goal."""
    goal = grid.goal
    
    return abs(goal[0] - point[0]) + abs(goal[1] - point[1])