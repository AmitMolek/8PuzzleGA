import numpy as np
import random as rnd
import math

def ga(init_pop, fitness_sort, 
       fitness_func, pop_size, 
       max_generation, elitism_factor,
       crossover_op, mutation_op,
       mutation_factor):

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
        print("POP", population)
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

        # Count of how many offspring we need to create to repopulate the generation
        mate_count = pop_size - citizens_survived
        for i in range(mate_count):
            # Choosing the randomly the parents to mate
            parent_1 = np.random.choice(new_population, 1)[0]
            parent_2 = np.random.choice(new_population, 1)[0]
            # Creating the offspring using the parents genes
            offspring = crossover_op(parent_1.chromosome, parent_2.chromosome)
            # Inserting mutation (based on probability)
            if rnd.random() < mutation_factor:
                offspring.chromosome = mutation_op(offspring.chromosome)
            # Adding the new offspring to the new population
            new_population = np.append(new_population, offspring)

        print("Gen = {} | Fitness = {}".format(current_generation, population[0].fitness))
        # Making the new generation the current one
        population = new_population
        pop_size = np.size(population)
        # Another generation passed
        current_generation += 1

    print(population)

goal_state = np.array([1,2,3,4,5,6,7,8,0])

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

# Swaps index1 and index2, returns a copy of the swapped array
def swap(np_arr, index1, index2):
    np_arr_cpy = np.empty(9, dtype=np_arr.dtype)
    np.copyto(np_arr_cpy, np_arr)
    np_arr_cpy[[index1, index2]] = np_arr_cpy[[index2, index1]]
    return np_arr_cpy

# Creates a new possible move
# Returns a PuzzleChromosome object with the new chromosome move
def create_possible_move(p_chromosome, zero_placement, movement):
    offspring_chromosome = swap(p_chromosome.chromosome, zero_placement, zero_placement + movement)
    offspring = PuzzleChromosome(offspring_chromosome, -1)
    return offspring

# Returns an array filled with all the possible moves
# The array is filled with PuzzleChromosome objects
def possible_moves(puzzle_chromosome):
    # An empty array to store all the possible moves
    moves = np.empty(0, dtype=PuzzleChromosome)
    # The location of the zero in the chromosome
    zero_placement = np.where(puzzle_chromosome.chromosome == 0)[0][0]
    # Getting the row and col cords of the zero
    zero_row = int(zero_placement / 3)
    zero_col = zero_placement % 3

    # If zero can go DOWN
    if (zero_row + 1) < 3:
        moves = np.append(moves, create_possible_move(puzzle_chromosome, zero_placement, 3))
    # If zero can go UP
    if (zero_row - 1) > -1:
        moves = np.append(moves, create_possible_move(puzzle_chromosome, zero_placement, -3))
    # If zero can go RIGHT
    if (zero_col + 1) < 3:
        moves = np.append(moves, create_possible_move(puzzle_chromosome, zero_placement, 1))
    # If zero can go LEFT
    if (zero_col - 1) > -1:
        moves = np.append(moves, create_possible_move(puzzle_chromosome, zero_placement, -1))

    return moves

# Creates the initial population
# Randomly generate the initial state and adds the initial state and all the
# possible moves from the initial state to the initial population
def init_pop(pop_size):
    # The entire initial population
    population = np.empty(0, dtype=PuzzleChromosome)
    # Creating the initial state of the puzzle
    initial_state = np.array([0,1,2,3,4,5,6,7,8])
    # Randomizing the initial state
    np.random.shuffle(initial_state)

    initial_p_chromosome = PuzzleChromosome(initial_state, -1)
    # Adding the initial puzzle chromosome to the init population
    population = np.append(population, initial_p_chromosome)
    # Adding all the possible moves to the init population
    population = np.append(population, possible_moves(initial_p_chromosome))
    # Setting the initial population size
    pop_size = np.size(pop_size)
    return population

# The fitness function
# Calculates the fitness: F = SIGMA(i=0, i=8) n*i
# Where i is the index and n is the value of the gene
def fitness_func(puzzle_chromosome):
    sum = 0
    chromosome = puzzle_chromosome.chromosome
    for i in chromosome:
        sum += (chromosome[i] * i)
    return sum

def fitness_sort(population, fitness_func):
    for pc in population:
        pc.fitness = fitness_func(pc)

    return population[population.argsort()]

def crossover_op(parent1, parent2):
    #new_chromosome = np.empty(0, dtype=int)
    p1_chormo = parent1.chromosome
    p2_chromo = parent2.chromosome
    cross_point = rnd.randint(0, 8)
    new_chromosome = p1_chormo[0:cross_point]
    print(np.size(np.where(new_chromosome == 1)))
    for i in range(0, 9):
        if np.size(np.where(new_chromosome == p2_chromo[i])) == 0:
            new_chromosome = np.append(new_chromosome, p2_chromo[i])
    print("P1", p1_chormo)
    print("P2", p2_chromo)
    print("New", new_chromosome)

def mutation_op(chromosome):
    gene_1 = rnd.randint(0, np.size(chromosome) - 1)
    gene_2 = gene_1
    while (gene_1 == gene_2):
        gene_2 = rnd.randint(0, np.size(chromosome) - 1)

    # Switching gene 1 and gene 2
    chromosome[[gene_1, gene_2]] = chromosome[[gene_2, gene_1]]
    return chromosome

#c1 = np.array([0,1,2,3,4,5,6,7,8])
#pc1 = PuzzleChromosome(c1, -1)

#c2 = np.array([0,1,2,3,4,5,6,7,8])
#np.random.shuffle(c2)
#pc2 = PuzzleChromosome(c2, -1)

#swap(c1, 0, 5)
#print(possible_moves(pc1))
#print(possible_moves(pc1)[0])
#print(init_pop(0))
#possible_moves(c1)
#crossover_op(pc1, pc2)

ga(init_pop, fitness_sort, fitness_func, 0, 50, 0.1, crossover_op, mutation_op, 0.01)