import numpy as np

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
    return PuzzleChromosome((taken_from_p1 + taken_from_p2), -1)

def mutation_op(chromosome):
    gene_1 = rnd.randint(0, np.size(chromosome) - 1)
    gene_2 = gene_1
    while (gene_1 == gene_2):
        gene_2 = rnd.randint(0, np.size(chromosome) - 1)

    # Switching gene 1 and gene 2
    chromosome[[gene_1, gene_2]] = chromosome[[gene_2, gene_1]]
    return chromosome