import utils
from city import City
from colors import bcolors
import time
from utils import write_results_file

def hill_climbing(city: City, iterations, eval_func, neighbor_func, random_init):
    """
      Generates a neighbor feasible solution

      Parameters:
          - city: The city with all establishments
          - iterations: maximum number of iterations we want the algorithm to do
          - eval_func: function to evaluate a solution
          - neighbor_func: function to generate neighbor solutions from another solution
          - random_init: first generated solution is random or greedy

      Returns the best solution found
      """

    start_time = time.time()

    # define initial random solution and its score
    counter = 0
    best_sol = utils.generate_random_solution(city) if random_init else utils.generate_greedy_sol(city)
    best_score = utils.evaluate_solution(city, best_sol, eval_func)
    initial = best_score
    x_values = [counter]
    y_values = [best_score]
    print(f"\n\nInitial Solution: {best_sol} \nScore: {best_score}\n")
    #print(f"\n\nInitial Score: {best_score}\n")

    # while didn't reach max iterations, try new solutions and update the best solution accordingly
    while counter < iterations:
        neighbor_sol, _ = neighbor_func(city, best_sol)
        neighbor_score = utils.evaluate_solution(city, neighbor_sol, eval_func)

        if neighbor_score < best_score:
            aux = best_score
            best_score = neighbor_score
            best_sol = neighbor_sol
            best_time = time.time()
            print(f"Iteration {counter}: {bcolors.GREEN} upgrade {bcolors.WHITE}\n\t\tScore: {aux} -> {best_score}\n")

        counter += 1
        x_values.append(counter)
        y_values.append(best_score)

    print(f"Final Solution: {best_sol}, \nScore: {best_score}")
    #print(f"Final Score: {best_score}\n")

    end_time = time.time()
    best = best_time-start_time
    total = end_time - start_time

    print(f"\nOptimal solution execution time: {best} seconds")
    print(f"Total execution time: {total} seconds")
    #write_results_file(best, total, initial, best_score)

    utils.plot_execution(x_values, y_values, f'Minimum Duration: {best_score}')
    return best_sol
