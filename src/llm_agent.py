import os
import random
from dotenv import load_dotenv
from openai import OpenAI

# Load env vars from .env file
load_dotenv()

class LLMAgent:
    def __init__(self, grid):
        self.grid = grid
        # initialize client using the key from environment
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_valid_moves(self, current_pos, visited):
        """Returns list of (neighbor_pos, cost, direction_name)"""
        r, c = current_pos
        moves = []
        candidates = [
            ((r-1, c), "North"), 
            ((r+1, c), "South"), 
            ((r, c+1), "East"), 
            ((r, c-1), "West")
        ]
        
        for pos, name in candidates:
            if self.grid.in_bounds(pos) and self.grid.passable(pos):
                # avoid immediate backtracking
                if pos not in visited:
                    cost = self.grid.cost(pos)
                    moves.append((pos, cost, name))
        return moves

    def _construct_prompt(self, current_pos, valid_moves):
        grid_info = f"Grid Size: {len(self.grid.grid)}x{len(self.grid.grid[0])}"
        status = f"Current Position: {current_pos}. Goal: {self.grid.goal}."
        
        options = ""
        for _, cost, name in valid_moves:
            options += f"- {name}: Terrain Cost {cost}\n"
            
        return f"""
                You are a tactical pathfinding AI.
                {grid_info}
                {status}

                Available Moves:
                {options}

                Thinking Process:
                1. Identify moves with Cost 1 (Road).
                2. Identify moves with Cost greater than 1 (Mud).
                3. ELIMINATE moves that are EXPENSIVE (greater than 1) unless no other option exists.
                4. Pick the direction that is CHEAPEST.

                Which move do you choose? Reply with JUST the direction name.
                """

    def choose_move(self, current_pos, visited):
        valid_moves = self.get_valid_moves(current_pos, visited)
        
        if not valid_moves:
            return None
        try:
            prompt = self._construct_prompt(current_pos, valid_moves)
            
            response = self.client.chat.completions.create(
                model="gpt-5-nano", 
                messages=[{"role": "user", "content": prompt}]
            )
            
            decision = response.choices[0].message.content.strip()
            
            # parse response
            for pos, cost, name in valid_moves:
                if name.lower() in decision.lower():
                    print(f"Agent chose: {name}") 
                    return pos
            
            # fallback if LLM hallucinates a bad direction
            print(f"LLM Invalid Output: {decision}. Falling back to random.")
            return valid_moves[0][0]

        except Exception as e:
            print(f"API Error: {e}")
            return None