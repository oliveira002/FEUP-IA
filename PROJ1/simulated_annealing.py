import utils
import random
import math
from city import City
from colors import bcolors
import time

def simulated_annealing(city: City, iterations, initial_temp, eval_func, neighbor_func, random_init, min_temp= 1):
    """
    Generates a neighbor feasible solution based on the simulated annealing algorithm

    Parameters:
        - city: The city with all establishments
        - iterations: maximum number of iterations we want the algorithm to do
        - initial_temp: initial temperature of the algorithm, should be high
        - eval_func: function to evaluate a solution
        - neighbor_func: function to generate neighbor solutions from another solution
        - random_init: first generated solution is random or greedy
        - min_temp: minimum temperature of the algorithm

    Returns the best solution found
    """

    start_time = time.time()

    # define initial random solution and its score
    temperature = initial_temp
    counter = 0
    best_sol = utils.generate_random_solution(city) if random_init else utils.generate_greedy_sol(city)
    best_score = utils.evaluate_solution(city, best_sol, eval_func)
    initial = best_score
    print(f"\n\nInitial Solution: {best_sol} \nScore: {best_score}")
    x_values = [counter]
    y_values = [best_score]

    while counter < iterations:

        if temperature <= min_temp:
            break

        neighbor_sol, _ = neighbor_func(city, best_sol)
        neighbor_score = utils.evaluate_solution(city, neighbor_sol, eval_func)
        delta_score = neighbor_score - best_score

        temperature = temp_sched(temperature)

        if delta_score == 0:
            counter += 1
            continue

        
        # if the new solution is better or the calculated probability for a worse solution is greater than a random number between 0 and 1, accept new solution
        if((upgrade:= delta_score < 0) or (probability := prob(delta_score, temperature)) >= random.random()):
            aux = best_score
            best_score = neighbor_score
            best_sol = neighbor_sol

            if upgrade: 
                print(f"Iteration {counter}: {bcolors.GREEN} upgrade {bcolors.WHITE}\n\t\tScore: {aux} -> {best_score}\n")
            else: 
                print(f"Iteration {counter}: {bcolors.RED} downgrade {bcolors.WHITE}\n\t\tScore: {aux} -> {best_score} \n\t\tProbability: {probability}\n")
            best_time = time.time()

        counter += 1
        x_values.append(counter)
        y_values.append(best_score)

    print(f"Final Solution: {best_sol}, \nScore: {best_score}")

    end_time = time.time()
    best = best_time-start_time
    total = end_time - start_time

    print(f"\nOptimal solution execution time: {best} seconds")
    print(f"Total execution time: {total} seconds")
    #utils.write_results_file(best, total, initial, best_score)

    utils.plot_execution(x_values, y_values, f'Minimum Duration: {best_score}')

    return best_sol

def temp_sched(temperature):
    """ 
    Cools down the system by a random amount between 0.001% and 0.005%

    Parameters:
        - temperature: The temperature of the system

    Returns a new, lower temperature
    """
    temperature *= random.uniform(0.995, 0.999)
    return temperature

def prob(delta_score,temperature):
    """ 
    Calculates the probability of accepting a new solution based on the temperature

    Parameters:
        - current_score: The score of the current solution
        - new_score: The score of the new solution
        - temperature: The temperature of the algorithm

    Returns the probability
    """
    probability = math.e**(-delta_score/temperature)
    return probability