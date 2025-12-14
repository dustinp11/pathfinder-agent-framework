from grid import Grid
from search import search_algorithm
import json
import sys

def main(map_file):
    grid = Grid(map_file)
    path, cost, nodes_expanded = search_algorithm(grid)
    output = {
        "path": path,
        "cost": cost,
        "nodes_expanded": nodes_expanded
    }
    print(output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py maps/map1.txt")
        sys.exit(1)
    main(sys.argv[1])
