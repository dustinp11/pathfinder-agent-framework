import heapq
from collections import deque
from heuristics import heuristic

from llm_agent import LLMAgent # Import the class

def llm_search(grid):
    """
    Standard search interface for the LLM Agent.
    """
    start, goal = grid.start, grid.goal
    
    # Instantiate the 'Brain'
    agent = LLMAgent(grid)
    
    # Standard tracking structures
    came_from = {start: None}
    nodes_expanded = 0
    current = start
    
    # Safety break for LLMs (they can get into infinite loops)
    max_steps = 100 

    while current != goal and nodes_expanded < max_steps:
        nodes_expanded += 1
        
        # Ask the agent for the single next step
        # We pass 'came_from' keys as 'visited' so it avoids backtracking
        next_node = agent.choose_move(current, visited=came_from)
        
        if next_node:
            # Register the move
            came_from[next_node] = current
            current = next_node
        else:
            # Agent got stuck or trapped
            break

    if goal not in came_from:
        return [], float('inf'), nodes_expanded, list(came_from.keys())

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    cost = sum(grid.cost(p) for p in path)
    
    visited_nodes = list(came_from.keys())

    return path, cost, nodes_expanded, visited_nodes



def A_star(grid):
    start, goal = grid.start, grid.goal
    min_heap = []
    # (f, -g, node)
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
            new_cost = total_cost[current] + grid.cost(neighbor)
            
            if neighbor not in total_cost or new_cost < total_cost[neighbor]:
                total_cost[neighbor] = new_cost
                
                # h(n)
                h_val = heuristic(grid, neighbor) 
                # f(n) = g(n) + h(n)
                f_val = new_cost + h_val
                
                heapq.heappush(min_heap, (f_val, -new_cost, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return [], float('inf'), nodes_expanded, []

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    cost = sum(grid.cost(p) for p in path)
    
    visited_nodes = list(came_from.keys())

    return path, cost, nodes_expanded, visited_nodes


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

    if goal not in came_from:
        return [], float('inf'), nodes_expanded, []

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    cost = sum(grid.cost(p) for p in path)
    
    visited_nodes = list(came_from.keys())
    
    return path, cost, nodes_expanded, visited_nodes


search_algorithm = A_star