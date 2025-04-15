import random
import math


def distance(a, b):
    #euclideam
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def total_route_distance(route, locations):
    #round trip
    total = 0
    for i in range(len(route)):
        total += distance(locations[route[i]], locations[route[(i + 1) % len(route)]])
    return total

def get_neighbors(route):
    #swapped to generate neighbours
    neighbors = []
    for i in range(len(route)):
        for j in range(i + 1, len(route)):
            new_route = route[:]
            new_route[i], new_route[j] = new_route[j], new_route[i]
            neighbors.append(new_route)
    return neighbors

def hill_climbing(locations):
    n = len(locations)
    current = list(range(n))
    random.shuffle(current)
    current_distance = total_route_distance(current, locations)

    while True:
        neighbors = get_neighbors(current)
        improved = False
        for neighbor in neighbors:
            d = total_route_distance(neighbor, locations)
            if d < current_distance:
                current = neighbor
                current_distance = d
                improved = True
                break  
        if not improved:
            break 

    return current, current_distance


locations = [
        (0, 0), (1, 4), (4, 2), (9, 6), (8, 3)
    ]

best_route, best_distance = hill_climbing(locations)

print("Route Coordinates:", [locations[i] for i in best_route])
print("Total Distance:", round(best_distance, 2))
