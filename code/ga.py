import numpy as np
import math

def ga(init_pop, fitness_sort, 
       fitness_func, pop_size, 
       max_generation, elitism_factor,
       crossover_op, mutation_op):

    # Initialize the population
    population = init_pop(pop_size)

    # Will be True if the solution is found
    solution_found = False
    # Keeps track of what generation we are at
    current_generation = 0

    # Loops until we found the solution or we hit the max generation limit
    while (not solution_found and current_generation < max_generation):
        # Calculates fitness and returns the population sorted by fitness
        sorted_population = fitness_sort(population, fitness_func)

        # If the first object in the sorted population has fitness of 0
        # we found the solution
        if (population[0].fitness == 0):
            found = True
            break

        # Calculates how many citizens will survive for the next generation
        # Using the formula for percentage
        # Part = (Whole * Percentage) / 100
        # Rounding up for nice integer numbers :)
        citizens_survived = math.ceil(((elitism_factor * pop_size) / 100))
        # The new population is the top performing citizens (from 0-citizens survived)
        new_population = sorted_population[0:citizens_survived]



        # Another generation passed
        current_generation += 1

    #print(population)  

class PuzzleChromosome:
    chromosome = np.empty(0)
    fitness = -1

    def __init__(self, chromosome, fitness):
        self.chromosome = chromosome
        self.fitness = fitness

    # ==
    def __eq__(self, value):
        if (type(value) is not PuzzleChromosome):
            return False
        return (self.fitness == value.fitness)

    # <
    def __lt__(self, value):
        if (type(value) is not PuzzleChromosome):
            return False
        return (self.fitness < value.fitness)

    # >
    def __gt__(self, value):
        if (type(value) is not PuzzleChromosome):
            return False
        return (self.fitness > value.fitness)

    def __repr__(self):
        return '({}, {})'.format(self.chromosome, self.fitness)

def init_pop(pop_size):
    population = np.empty(0, dtype=PuzzleChromosome)
    for i in range(0, pop_size):
        options = np.arange(9)
        np.random.shuffle(options)
        item = PuzzleChromosome(options, -1)
        population = np.append(population, item)

    return population.reshape(pop_size)
    print(population)

def fitness_func(chromosome):
    mul_vec = np.array([1, -1, 1, -1, 1, -1, 1, -1, 1]).reshape([9, 1])
    return (chromosome @ mul_vec)[0]

def fitness_sort(population, fitness_func):
    for pc in population:
        pc.fitness = fitness_func(pc.chromosome)

    return population[population.argsort()]

def crossover_op(parent1, parent2):
    from_parent1 = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1])
    np.random.shuffle(from_parent1)
    from_parent2 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1])
    from_parent2 = from_parent2 - from_parent1
    taken_from_p1 = parent1 * from_parent1
    taken_from_p2 = parent2 * from_parent2
    return (taken_from_p1 + taken_from_p2)


#ga(init_pop, fitness_sort, fitness_func, 3, 5, 10)
crossover_op(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))