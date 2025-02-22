import heapq
from collections import deque
# a dictionary has been made which is storing the city name where key:value pair is city:(neighbour,cost) 
cities = {
    "Arad": {"Zerind": 75, "Timisoara": 118, "Sibiu": 140},
    "Zerind": {"Oradea": 71, "Arad": 75},
    "Oradea": {"Sibiu": 151, "Zerind": 71},
    "Timisoara": {"Lugoj": 111, "Arad": 118},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Pitesti": 138, "Rimnicu Vilcea": 146},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Rimnicu Vilcea": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}

#another dictionary which store the heuristics of each city from 
heuristic_value = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242,
    "Eforie": 161, "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151,
    "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234,
    "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193,
    "Sibiu": 253, "Timisoara": 329, "Urziceni": 80,
    "Vaslui": 199, "Zerind": 374
}

def bfs(start_city, goal_city):
    queue = deque([(start_city, [start_city], 0)])
    visited = set()
    while queue:
        node, path, cost = queue.popleft()
        if node == goal:
            return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, step_cost in cities[node].items():
                queue.append((neighbor, path + [neighbor], cost + step_cost))
    return None, float('inf')

def uniform_cost_search(start_city, goal_city):
    queue = [(0, start_city, [start_city])]
    visited = set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == goal:
            return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, step_cost in cities[node].items():
                heapq.heappush(queue, (cost + step_cost, neighbor, path + [neighbor]))
    return None, float('inf')

def greedy_best_first(start_city, goal_city):
    queue = [(heuristic_value[start_city], start_city, [start_city], 0)]
    visited = set()
    while queue:
        _, node, path, cost = heapq.heappop(queue)
        if node == goal:
            return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, step_cost in data[node].items():
                heapq.heappush(queue, (heuristic_value[neighbor], neighbor, path + [neighbor], cost + step_cost))
    return None, float('inf')

def iterative_deepening_dfs(start_city, goal_city, max_depth=10):
    def dls(node, path, depth, cost):
        if depth == 0 and node == goal:
            return path, cost
        if depth > 0:
            for neighbor, step_cost in cities[node].items():
                new_path, new_cost = dls(neighbor, path + [neighbor], depth - 1, cost + step_cost)
                if new_path:
                    return new_path, new_cost
        return None, float('inf')
    
    for depth in range(max_depth):
        result, cost = dls(start_city, [start_city], depth, 0)
        if result:
            return result, cost
    return None, float('inf')

start_city = input("Enter start city: ")
goal_city = input("Enter goal city: ")

print("\nBreadth-First Search:")
print(bfs(start_city, goal_city))

print("\nUniform Cost Search:")
path, cost = uniform_cost_search(start_city, goal_city)
print(path, "Cost:", cost)

print("\nGreedy Best-First Search:")
print(greedy_best_first(start_city, goal_city))

print("\nIterative Deepening DFS:")
print(iterative_deepening_dfs(start_city, goal_city))
