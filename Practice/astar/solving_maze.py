import heapq

# Directions for movement (Right, Left, Down, Up)
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Heuristic Function: Manhattan Distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Algorithm for Maze
def a_star_maze(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = []  # Priority queue for nodes
    heapq.heappush(open_set, (0, start))  # (f(n), node)
    
    g_costs = {start: 0}
    came_from = {start: None}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Reverse path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                new_g_cost = g_costs[current] + 1
                if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_g_cost
                    f_cost = new_g_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_cost, neighbor))
                    came_from[neighbor] = current

    return None  # No path found

# Example Maze (0 = Open Path, 1 = Wall)
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

path = a_star_maze(maze, start, goal)
print("Path:", path)
