from grid import Grid
from search import A_star, llm_search
from visualizer import compare_algos
import sys

def main(map_file, algo_A, algo_B):
    print(f"Loading map: {map_file}")
    grid = Grid(map_file)
    
    # 1. Ground Truth (A* with Admissible Heuristic)
    print("Running A* (Optimal Baseline)...")
    res_astar = A_star(grid)
    optimal_cost = res_astar[1]
    
    # 2. LLM Agent (Experimental)
    print("Running LLM Agent...")
    res_llm = llm_search(grid)
    agent_cost = res_llm[1]

    # 3. Compare Results
    print("\n--- BENCHMARK REPORT ---")
    print(f"Optimal Cost (A*): {optimal_cost}")
    print(f"Agent Cost (LLM):  {agent_cost}")
    
    if agent_cost == float('inf'):
        print("Result: Agent failed to reach the goal.")
    elif optimal_cost == 0:
         print("Result: Start is Goal.")
    else:
        # Lower cost is better, so efficiency is Optimal / Actual
        efficiency = (optimal_cost / agent_cost) * 100
        print(f"Efficiency:        {efficiency:.2f}%")
        
        if agent_cost == optimal_cost:
            print("Status:            PERFECT RUN")
        else:
            diff = agent_cost - optimal_cost
            print(f"Status:            +{diff} Cost over optimal")

    # 4. Visualize
    print("Opening visualization window...")
    compare_algos(grid, res_astar, res_llm, algo_A, algo_B)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/main.py data/map1.txt algo_A algo_B")
        sys.exit(1)
    main(*sys.argv[1:])