import utils
import random
import numpy as np
import copy
from city import City
from colors import bcolors
import time


def repair_crossover_chromosome(chromosome, gene_removed, gene_added):
    """
      Repairs a current solution, in case there are conflits
      Parameters:
          - chromosome: chromosome
          - gene_removed: gene removed
          - gene_added: gene added

      Returns feasible solution
    """
    equals = []
    for i in gene_added:
        if i in gene_removed:
            equals.append(i)
    gene_removed = [i for i in gene_removed if (i not in equals and i != 0)]
    gene_added = [i for i in gene_added if (i not in equals and i != 0)]
    for x in range(len(chromosome)):
        i = 0
        while i < len(chromosome[x]):
            if chromosome[x][i] in gene_added and len(gene_removed) > 0:
                gene_added.remove(chromosome[x][i])
                random_gene = random.choice(gene_removed)
                chromosome[x][i] = random_gene
                gene_removed.remove(random_gene)
                i += 1
            elif chromosome[x][i] in gene_added and len(gene_removed) == 0:
                gene_added.remove(chromosome[x][i])
                chromosome[x].remove(chromosome[x][i])
            elif len(gene_added) == 0:
                break
            else:
                i += 1

    if len(gene_removed) > 0:
        for i in range(len(gene_removed)):
            random_gene = random.choice(gene_removed)
            gene_removed.remove(random_gene)
            vehicle = min(chromosome, key=len)
            if len(vehicle) - 2 <= 1:
                vehicle.insert(1, random_gene)
            else:
                vehicle.insert(random.randint(1, len(vehicle) - 2), random_gene)
    return chromosome


def crossover_classical(parent1, parent2):
    """
       Generates two new offspring
       Parameters:
           - parent1: first parent
           - parent2: second parent

       Returns new parent
    """
    offspring_1 = copy.deepcopy(parent1)
    offspring_2 = copy.deepcopy(parent2)
    num_vehicles = len(offspring_1)
    num_vehicles = random.randint(int(num_vehicles * 0.05),
                                  int(num_vehicles * 0.15) if int(num_vehicles * 0.15) > 0 else 1)

    for i in range(1 if int(num_vehicles) == 0 else int(num_vehicles)):
        gene_1 = random.choice(offspring_1)
        gene_2 = random.choice(offspring_2)
        offspring_1.remove(gene_1)
        offspring_2.remove(gene_2)

        repair_crossover_chromosome(offspring_1, gene_1, gene_2)
        repair_crossover_chromosome(offspring_2, gene_2, gene_1)

        offspring_1.append(gene_2)
        offspring_2.append(gene_1)

    return offspring_1, offspring_2


def roulette_select(population, city, eval_func):
    """
       Selects new parent
       Parameters:
           - population: current population
           - city: The city with all establishments
           - eval_func: evaluation function

       Returns new parent
    """
    score_sum = sum([utils.evaluate_solution(city, solution, eval_func) for solution in population])
    selection_probs = [utils.evaluate_solution(city, solution, eval_func) / score_sum for solution in population]
    return population[np.random.choice(len(population), p=selection_probs)]


def remove_least_fit(population, city, eval_func, population_size):
    """
    Generates new population
    Parameters:
        - population: current population
        - city: The city with all establishments
        - eval_func: evaluation function
        - population_size: current population size

    Returns new fitter population
    """
    population = sorted(population, key=lambda x: utils.evaluate_solution(city, x, eval_func))
    population = population[0:population_size]
    return population


def genetic_algorithm(city: City, iterations, eval_func, crossover_func, neighbor_func, random_start,
                      population_size=100, population_reproduction=0.1):
    """
      Generates a neighbor feasible solution based on the simulated annealing algorithm

      Parameters:
          - city: The city with all establishments
          - iterations: maximum number of iterations we want the algorithm to do
          - eval_func: function to evaluate a solution
          - crossover_func: function to generate crossovers
          - neighbor_func: function to generate neighbor solutions from another solution
          - random_start: first generated solution is random or greedy
          - population_size: population size
          - population_reproduction: population reproduction

      Returns the best solution found
    """

    start_time = time.time()

    counter = 0
    population = []
    if random_start:
        for i in range(population_size):
            child = utils.generate_random_solution(city)
            population.append(child)
    else:
        for i in range(population_size - 1):
            child = utils.generate_random_solution(city)
            population.append(child)

        population.append(utils.generate_greedy_sol(city))

    best_solution = min(population, key=lambda x: utils.evaluate_solution(city, x, eval_func))
    initial = utils.evaluate_solution(city, best_solution, eval_func)
    print(f"\n\nInitial Solution: {best_solution} \nScore: {initial}\n")
    x_values = [counter]
    y_values = [utils.evaluate_solution(city, best_solution, eval_func)]

    while counter < iterations:
        first_offspring = best_solution
        population.remove(first_offspring)
        second_offspring = roulette_select(population, city, eval_func)
        cross_over_1, cross_over_2 = crossover_func(first_offspring, second_offspring)
        population.append(first_offspring)
        population.append(cross_over_1)
        population.append(cross_over_2)

        if random.randint(0, 10) < 5:
            mutation, _ = neighbor_func(city, first_offspring)
            population.append(mutation)
            mutation, _ = neighbor_func(city, cross_over_1)
            population.append(mutation)
            mutation, _ = neighbor_func(city, cross_over_2)
            population.append(mutation)

        for i in range(int(population_reproduction * population_size)):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child_1, child_2 = crossover_func(parent1, parent2)
            if random.randint(0, 10) < 5:
                mutation, _ = neighbor_func(city, child_1)
                population.append(mutation)
                mutation, _ = neighbor_func(city, child_2)
                population.append(mutation)
            population.append(child_1)
            population.append(child_2)

        counter += 1

        aux = utils.evaluate_solution(city, best_solution, eval_func)

        if (best_score := utils.evaluate_solution(city, min(population,
                                                            key=lambda x: utils.evaluate_solution(city, x, eval_func)),
                                                  eval_func)) < utils.evaluate_solution(city, best_solution, eval_func):
            print(f"Iteration {counter}: {bcolors.GREEN} upgrade {bcolors.WHITE}\n\t\tScore: {aux} -> {best_score}\n")
            best_time = time.time()

        best_solution = min(population, key=lambda x: utils.evaluate_solution(city, x, eval_func))
        population = remove_least_fit(population, city, eval_func, population_size)
        x_values.append(counter)
        y_values.append(utils.evaluate_solution(city, best_solution, eval_func))

    best_score = utils.evaluate_solution(city, best_solution, eval_func)
    print(f"\n\nFinal Solution: {best_solution} \nScore: {best_score}\n")

    end_time = time.time()
    best = best_time - start_time
    total = end_time - start_time

    print(f"\nOptimal solution execution time: {best} seconds")
    print(f"Total execution time: {total} seconds")
    #utils.write_results_file(best, total, initial, best_score)

    utils.plot_execution(x_values, y_values,
                         f'Minimum Duration: {utils.evaluate_solution(city, best_solution, eval_func)}')
    return best_solution
