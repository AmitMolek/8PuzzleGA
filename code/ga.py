import numpy as np

def ga(gaObj, init_pop, 
       fitness_sort, fitness_func, 
       pop_size, max_generation, 
       elitism_factor):

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
        if (population[0].fitness <= 0):
            found = True
            break

        # Calculates how many citizens will survive for the next generation
        # Using the formula for percentage
        # Part = (Whole * Percentage) / 100
        citizens_survived = (elitism_factor * pop_size) / 100
        new_population = sorted_population[0:citizens_survived]
        

    print(population)  

class PuzzleChromosome:
    chromosome = np.empty(0)
    fitness = -1

    def __init__(self, chromosome, fitness):
        self.chromosome = chromosome
        self.fitness = fitness

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

    print(population)

#ga(int)
pop = init_pop(3)
fitness_sort(pop, fitness_func)
