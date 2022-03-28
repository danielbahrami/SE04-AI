import random
from queens_fitness import *

p_mutation = 0.2
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    """
    Reproduce two individuals with single-point crossover
    Return the child individual
    """

    number = random.randint(0, len(father) - 1)
    child = [0] * len(father)

    for i in range(0, number):
        child[i] = mother[i]

    for i in range(number, 0):
        child[i] = father[i]

    # return child
    return tuple(child)


def mutate(individual):
    """
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    """

    if len(individual) > 0:
        number = random.randint(0, len(individual) - 1)
        mutation = [0] * len(individual)
        for i in range(0, len(individual)):
            if i != number:
                mutation[i] = individual[i]
            else:
                mutation[i] = random.randint(0, 1)

        # return mutation
        return tuple(mutation)


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    ordered_population = list(population)
    total_fitness = 0
    fitness_population = []

    for individual in ordered_population:
        total_fitness += fitness_fn(individual)

    for individual in ordered_population:
        fitness_population.append(fitness_fn(individual))

    stagnate_value = random.randint(0, 100)
    mother_index = 0
    father_index = fitness_population.index(max(fitness_population))

    fitness_population.remove(max(fitness_population))

    if stagnate_value > p_mutation * 100:
        mother_index = fitness_population.index(max(fitness_population))
    else:
        while mother_index != father_index:
            mother_index = random.randint(0, len(ordered_population))

    # return selected
    return ordered_population[mother_index], ordered_population[father_index]


def fitness_function(individual):
    """
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    """

    reversed_individuals = individual[::-1]
    fitness = 0

    for i in range(0, len(reversed_individuals)):
        fitness += (2 ** i) * reversed_individuals[i]

    # return fitness
    return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    """
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    """
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (5, 6, 2, 3, 5, 8, 6, 1),
        (7, 3, 6, 6, 4, 6, 8, 1)
    }
    initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


# fitness_fn_negative()


if __name__ == '__main__':
    pass
    main()
