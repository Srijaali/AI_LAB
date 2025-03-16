import heapq

# City Graph (Adjacency List)
graph = {
    'A': {'B': 4, 'C': 3},
    'B': {'A': 4, 'D': 5, 'E': 12},
    'C': {'A': 3, 'F': 7},
    'D': {'B': 5, 'E': 2},
    'E': {'B': 12, 'D': 2, 'F': 4},
    'F': {'C': 7, 'E': 4}
}

# Heuristic Estimates (Straight-line distance to goal)
heuristic = {
    'A': 10, 'B': 6, 'C': 8, 'D': 4, 'E': 2, 'F': 0  # Goal is 'F'
}

# A* Algorithm for Shortest Route
def a_star_city(graph, start, goal):
    open_set = []
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
            return path[::-1]

        for neighbor, cost in graph[current].items():
            new_g_cost = g_costs[current] + cost
            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic[neighbor]
                heapq.heappush(open_set, (f_cost, neighbor))
                came_from[neighbor] = current

    return None  # No path found

# Example Usage
start = 'A'
goal = 'F'
path = a_star_city(graph, start, goal)
print("Shortest Path:", path)
