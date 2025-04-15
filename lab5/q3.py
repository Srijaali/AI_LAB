import random
import math


city_names = ["karachi","lahore","islamabad","hyderabad","mumbai","dehli","pune","ahmedabad","istanbul","antalya"]
city_coords = [
    (0, 0), (1, 5), (5, 2), (6, 6), (8, 3),
    (2, 9), (3, 4), (7, 8), (9, 1), (4, 7)
]


def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def total_distance(route, coords):
    return sum(distance(coords[route[i]], coords[route[(i+1)%len(route)]]) for i in range(len(route)))

def fitness(route, coords):
    return 1 / total_distance(route, coords)  

def create_individual(n):
    route = list(range(n))
    random.shuffle(route)
    return route

def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[start:end] = parent1[start:end]

    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    return child

def mutate(route, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

def select_parents(population, coords):
    scores = [(fitness(ind, coords), ind) for ind in population]
    scores.sort(reverse=True)
    return [ind for _, ind in scores[:len(population)//2]]

def gene_algo(coords, population_size=50, generations=200, mutation_rate=0.1):
    n = len(coords)
    population = [create_individual(n) for _ in range(population_size)]

    best_route = None
    best_fit = 0

    for gen in range(generations):
        fitness_scores = [fitness(ind, coords) for ind in population]
        current_best_fit = max(fitness_scores)
        current_best_route = population[fitness_scores.index(current_best_fit)]

        if current_best_fit > best_fit:
            best_fit = current_best_fit
            best_route = current_best_route

        parents = select_parents(population, coords)
        next_generation = []

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            next_generation.append(mutate(child, mutation_rate))

        population = next_generation
        print(f"Generation {gen+1}: Best Distance = {round(1/best_fit, 2)}")

    return best_route, 1 / best_fit


best_route, distance_val = gene_algo(city_coords)
print("\nBest Route:", " → ".join(city_names[i] for i in best_route))
print("Total Distance:", round(distance_val, 2))
