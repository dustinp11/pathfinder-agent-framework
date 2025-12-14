import heapq
from collections import deque
from heuristics import heuristic






def A_star(grid):
    start, goal = grid.start, grid.goal
    min_heap = []
    # we want higher g value to be chosen in case of ties, so our tuple in our min heap is:
    # (f value, -(g value), node) so that lower f-value chosen first, bigger g => lower -g => is chosen first
    heapq.heappush(min_heap, (0, 0, start))
    came_from = {start: None}
    total_cost = {start: 0}
    nodes_expanded = 0
    


    while min_heap:
        current = heapq.heappop(min_heap)[2]
    
        if current == goal:
            break

        nodes_expanded += 1
        for neighbor in grid.neighbors(current):
            if neighbor not in came_from:
                # update total cost 
                total_cost[neighbor] = total_cost[current] + grid.cost(neighbor)

                # compute g values and f value
                g_val = heuristic(grid, neighbor)
                f_val = total_cost[neighbor] + g_val
                heapq.heappush(min_heap, (f_val, -g_val, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return [], float('inf'), nodes_expanded

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    cost = sum(grid.cost(p) for p in path)

    return path, cost, nodes_expanded






def bfs_search(grid):
    start, goal = grid.start, grid.goal
    frontier = deque([start])
    came_from = {start: None}
    nodes_expanded = 0

    while frontier:
        current = frontier.popleft()
        nodes_expanded += 1

        if current == goal:
            break

        for neighbor in grid.neighbors(current):
            if neighbor not in came_from:
                frontier.append(neighbor)
                came_from[neighbor] = current

    # Reconstruct path
    if goal not in came_from:
        return [], float('inf'), nodes_expanded

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    cost = sum(grid.cost(p) for p in path)
    return path, cost, nodes_expanded





search_algorithm = A_star

