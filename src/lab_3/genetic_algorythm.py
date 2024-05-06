#########################################################
#                         import                        #
#########################################################

import numpy as np
import random


#########################################################
#                          rules                        #
#########################################################
def fitness(x):
    return 2 * x[0] ** 2 + x[1] ** 3 - x[2] ** 2 + 7 * x[3] ** 2 - 2 * x[4] ** 5


def generate_individual():
    return np.array([
        random.randint(0, 10),  # x0, constrained to <= 10
        random.choice([i for i in range(1, 26) if i % 10 in range(1, 8)]),  # x1, mod 10 in {1,...,7}
        random.randint(1, 25),  # x2, >= 1
        random.randint(0, 20),  # x3, <= 20
        random.randint(6, 25)  # x4, > 5
    ])


def crossover(parent_x, parent_y):
    # Uniform crossover for diversity
    child1 = np.array([p1 if random.random() < 0.5 else p2 for p1, p2 in zip(parent_x, parent_y)])
    child2 = np.array([p2 if random.random() < 0.5 else p1 for p1, p2 in zip(parent_x, parent_y)])
    return [child1, child2]


def mutate(child, mutation_rate=0.2):  # Increased mutation rate
    print(f"Child: {child}")
    for i in range(len(child)):
        if random.random() < mutation_rate:
            child[i] = generate_individual()[i]
    print(f"Mutated child: {child}")
    return child


def tournament_selection(population, fitness_t, k=3):  # Changed fitnesses to fitnesses_t to avoid shadowing
    selected_indices = np.random.choice(len(population), k)
    selected_fitness_t = [fitness_t[i] for i in selected_indices]
    best_index_t = np.argmax(selected_fitness_t)
    return population[selected_indices[best_index_t]]


#########################################################
#                           Main                        #
#########################################################

# Initialize population
POP_SIZE = 20
GEN_MAX = 20
population = [generate_individual() for _ in range(POP_SIZE)]

best_global_fitness = -np.inf  # Changed to negative infinity to ensure that the first individual is selected
best_global_individual = None

for generation in range(GEN_MAX):
    fitnesses = [fitness(ind) for ind in population]
    best_index = np.argmax(fitnesses)
    best_fitness = fitnesses[best_index]

    # Elitism: Preserve the top 10% of individuals
    num_elites = int(0.1 * POP_SIZE)
    elites = sorted(population, key=lambda x: fitness(x), reverse=True)[:num_elites] # Changed to reverse=True1

    if best_fitness > best_global_fitness:
        best_global_fitness = best_fitness
        best_global_individual = population[best_index]

    new_population = elites.copy()  # Start new population with the elites

    while len(new_population) < POP_SIZE:
        parent1 = tournament_selection(population, fitnesses)
        parent2 = tournament_selection(population, fitnesses)
        children = crossover(parent1, parent2)
        children = [mutate(child) for child in children]
        new_population.extend(children)

    population = new_population[:POP_SIZE]
    # print(f"Generation {generation}, Best fitness: {best_fitness}, set: {best_global_individual}")
    print(f"Generation {generation}, Best fitness: {best_fitness}, set: {best_global_individual}")


print("Best individual:", best_global_individual, "Fitness:", best_global_fitness)


