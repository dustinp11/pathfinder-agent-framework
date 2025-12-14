import matplotlib.pyplot as plt
import numpy as np

def plot_grid(ax, grid, path, visited, title):
    rows = len(grid.grid)
    cols = len(grid.grid[0])
    
    # create map
    map_display = np.ones((rows, cols, 3))
    
    # visited nodes == yellow
    if visited:
        for r, c in visited:
            if 0 <= r < rows and 0 <= c < cols:
                map_display[r, c] = [1, 1, 0.7]

    # walls == black
    for r in range(rows):
        for c in range(cols):
            if grid.grid[r][c] is None:
                map_display[r, c] = [0, 0, 0] 

    ax.imshow(map_display)
    
    # grid lines 
    ax.set_xticks(np.arange(-0.5, cols, 1))
    ax.set_yticks(np.arange(-0.5, rows, 1))
    ax.grid(color='black', linestyle='-', linewidth=1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # cost numbers in top right
    for r in range(rows):
        for c in range(cols):
            val = grid.grid[r][c]
            if val is not None:
                ax.text(c + 0.4, r - 0.4, str(val), 
                        ha='right', va='top', 
                        color='black', fontsize=9)

    # paths == blue line
    if path:
        py, px = zip(*path)
        ax.plot(px, py, color='blue', linewidth=4, alpha=0.4, label='Path')
        ax.scatter(px, py, color='blue', s=30, zorder=5)

    # start == green square, goal == red star
    sr, sc = grid.start
    gr, gc = grid.goal
    ax.scatter([sc], [sr], c='lime', s=150, marker='s', edgecolors='black', label='Start', zorder=10)
    ax.scatter([gc], [gr], c='red', s=180, marker='*', edgecolors='black', label='Goal', zorder=10)

    ax.set_title(title)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

def compare_algos(grid, result_a, result_b, name_a="Algorithm A", name_b="Algorithm B"):
    # unpack results
    path_a, cost_a, nodes_a, visited_a = result_a
    path_b, cost_b, nodes_b, visited_b = result_b

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # plot algo a
    title_a = f"{name_a}\nTotal Cost: {cost_a} | Nodes Visited: {nodes_a}"
    plot_grid(ax1, grid, path_a, visited_a, title_a)

    # plot algo b
    title_b = f"{name_b}\nTotal Cost: {cost_b} | Nodes Visited: {nodes_b}"
    plot_grid(ax2, grid, path_b, visited_b, title_b)

    plt.suptitle(f"Algorithm Comparison: {name_a} vs {name_b}", fontsize=14)
    plt.tight_layout()
    plt.show()