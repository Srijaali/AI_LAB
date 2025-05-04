#tsp

import random
import math


# Locations with (x, y) coordinates
locations = [(0, 0), (1, 5), (2, 3), (5, 2), (6, 6)]


# Fitness function: Calculate the total distance of a route
def calculate_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):      #looping over locations
        x1, y1 = locations[route[i]]     #coordinates at i
        x2, y2 = locations[route[i + 1]] #coordinates at j
        #distance between the above two cities
        total_distance += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return total_distance

# Generate a random route
def create_random_route():
    route = list(range(len(locations)))
    random.shuffle(route)
    return route

# Initialize population
population_size = 10
population = [create_random_route() for _ in range(population_size)]
print("Initial Population:\n", population)

# Evaluate fitness for each route in the population
fitness_scores = [calculate_distance(route) for route in population]
print("\nFitness Scores:\n", fitness_scores)

# Select the best routes (parents) based on fitness
def select_parents(population, fitness_scores):
    # Select top 50% of the population
    sorted_population = [route for _, route in sorted(zip(fitness_scores, population))]
    return sorted_population[:len(population)//2]


parents = select_parents(population, fitness_scores)
print("\nSelected Parents:\n", parents)

# Combine two parents to create offspring
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = parent1[start:end]
    for gene in parent2:
        if gene not in child:
            child.append(gene)
    return child

# Create new population using crossover
new_population = []
for i in range(population_size):
    parent1, parent2 = random.sample(parents, 2)
    child = crossover(parent1, parent2)
    new_population.append(child)
print("\nNew Population after Crossover:\n", new_population)

# Randomly swap two locations in a route
def mutate(route):
    idx1, idx2 = random.sample(range(len(route)), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

mutation_rate = 0.1
for i in range(len(new_population)):
    if random.random() < mutation_rate:
        new_population[i] = mutate(new_population[i])
print("\nPopulation after Mutation:\n", new_population)

# Convergence criteria: Stop if no improvement for 10 generations
best_fitness = min(fitness_scores)
no_improvement_count = 0
max_generations = 100
generation = 0


while generation < max_generations and no_improvement_count < 10:
    # Evaluate fitness of new population in each generation
    fitness_scores = [calculate_distance(route) for route in new_population]
    current_best_fitness = min(fitness_scores)

    # Updates best_fitness if a better route is found
    if current_best_fitness < best_fitness:
        best_fitness = current_best_fitness
        no_improvement_count = 0
    else:
        no_improvement_count += 1

    # Selects parents from current population based on fitness
    parents = select_parents(new_population, fitness_scores)


    # Generates new population using crossover
    new_population = [crossover(random.choice(parents), random.choice(parents)) for _ in range(population_size)]




    # Applies mutation to the new population with a small probability
    for i in range(len(new_population)):
        if random.random() < mutation_rate:
            new_population[i] = mutate(new_population[i])
    # Proceed to next generation
    generation += 1


print("Best Route:", new_population[fitness_scores.index(min(fitness_scores))])
print("Best Distance:", min(fitness_scores))
