# main_maze.py
import time
from maze import Maze
from collections import deque
from typing import Tuple 

def solve_maze_with_stack(maze: Maze, start_pos: Tuple[int, int]) -> bool:
    stack = deque()
    visited = set()

    stack.append(start_pos)

    while stack:
        current = stack.pop()
        x, y = current

        if current in visited:
            continue
        visited.add(current)

        if maze.find_prize(current):
            print("Prêmio encontrado em:", current)
            maze.mov_player(current)
            return True

        maze.mov_player(current)
        time.sleep(0.01)

        # cima, baixo, esquerda, direita
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.M.shape[0] and 0 <= ny < maze.M.shape[1]:
                if maze.is_free((nx, ny)) and (nx, ny) not in visited:
                    stack.append((nx, ny))

    print("Caminho não encontrado.")
    return False


if __name__ == "__main__":
    maze_csv_path = "labirinto1.txt"
    maze = Maze()

    maze.load_from_csv(maze_csv_path)
    maze.run()
    maze.init_player()

    start = maze.get_init_pos_player()
    maze.mov_player(start)

    # Executa o algoritmo de backtracking
    solve_maze_with_stack(maze, start)