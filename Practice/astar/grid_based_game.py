import pygame
import heapq

# Grid Size
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // ROWS

# Directions for Movement
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Heuristic Function
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Algorithm for Game AI
def a_star_game(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))

    g_costs = {start: 0}
    came_from = {start: None}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] == 0:
                new_g_cost = g_costs[current] + 1
                if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_g_cost
                    f_cost = new_g_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_cost, neighbor))
                    came_from[neighbor] = current

    return None

# Example Grid (0 = Walkable, 1 = Obstacle)
game_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
game_grid[3][3] = 1  # Example obstacle

start, goal = (0, 0), (9, 9)
path = a_star_game(game_grid, start, goal)

print("Game AI Path:", path)
