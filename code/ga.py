import numpy as np
import math
import random as rnd

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

        # Making the new generation the current one
        population = new_population
        # Another generation passed
        current_generation += 1

    print(population)


#ga(init_pop, fitness_sort, fitness_func, 20, 5, 10, crossover_op, mutation_op, 1)

#c1 = np.array([1,2,3,4,5,6,7,8,9])
#np.random.shuffle(c1)
#crossover_op(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))
#mutation_op(c1)