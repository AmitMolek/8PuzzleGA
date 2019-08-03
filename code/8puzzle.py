import numpy as np

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
    return population

# The fitness function
# Calculates the fitness: F = SIGMA(i=0, i=8) n*i
# Where i is the index and n is the value of the gene
def fitness_func(puzzle_chromosome):
    sum = 0
    chromosome = puzzle_chromosome.chromosome
    for i in np.size(chromosome):
        sum += (chromosome[i] * i)
    return sum

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

#c1 = np.array([0,1,2,3,4,5,6,7,8])
#pc1 = PuzzleChromosome(c1, -1)
#swap(c1, 0, 5)
#print(possible_moves(pc1))
#print(possible_moves(pc1)[0])
print(init_pop(0))
#possible_moves(c1)