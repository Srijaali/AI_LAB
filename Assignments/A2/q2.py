import random

tasks = [5,8, 4,7,6,3,9]
capacities = [24,30,28]
cost_matrix = [
    [10,12,9],
    [15,14,16],
    [8,9,7],
    [12,10,13],
    [14,13,12],
    [9,8,10],
    [11,12,13]
]
PENALTY = 1000

pop =6
cross_rate =0.8
mute_rte =0.2

def gen_chrom():
    return [random.randint(1,3) for _ in range(len(tasks))]

def fitness(chrom):
    time_used = [0,0,0]
    cost = 0
    for i, facility in enumerate(chrom):
        f = facility - 1
        time_used[f] += tasks[i]
        cost += cost_matrix[i][f] * tasks[i]
    penalty = sum(
        max(0, time_used[i] - capacities[i]) * PENALTY
        for i in range(3)
    )
    return cost + penalty

def roulette_selection(pop,fits):
    total = sum(1/f for f in fits)
    pick = random.uniform(0, total)
    current =0
    for chrom, fit in zip(pop,fits):
        current+=1/fit
        if current>=pick:
            return chrom[:]

def crossover(p1, p2):
    if random.random() > cross_rate:
        return p1[:], p2[:]
    point = random.randint(1, len(p1)-2)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

def mutate(chrom):
    if random.random() >mute_rte:
        return chrom
    i, j = random.sample(range(len(chrom)), 2)
    chrom[i], chrom[j] = chrom[j], chrom[i]
    return chrom

population = [gen_chrom() for _ in range(pop)]
fitnesses = [fitness(c) for c in population]
print("initial population and fitness:")
for i in range(pop):
    print(f"p{i+1}: {population[i]}  --> fitness: {fitnesses[i]}")
new_population = []
while len(new_population) < pop:
    p1 = roulette_selection(population, fitnesses)
    p2 = roulette_selection(population, fitnesses)
    c1, c2 = crossover(p1, p2)
    new_population.append(mutate(c1))
    if len(new_population) < pop:
        new_population.append(mutate(c2))

print("\nnew pop:")
for i, chrom in enumerate(new_population):
    print(f"new p{i+1}: {chrom}")
new_fitnesses = [fitness(c) for c in new_population]
best_index = new_fitnesses.index(min(new_fitnesses))
best_chrom = new_population[best_index]
best_fit = new_fitnesses[best_index]


print(f"best chromosome: {best_chrom}")
print(f"best fitness: {best_fit}")
