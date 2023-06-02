import utils
from city import City
from colors import bcolors
import time

def tabu_search(city: City, iterations, mutations_per_iteration, eval_func, neighbor_func, random_init, restrictive= True):
    """
      Generates a neighbor feasible solution based on the tabu search algorithm

      Parameters:
          - city: The city with all establishments
          - iterations: maximum number of iterations we want the algorithm to do
          - mutations_per_iteration: number of neighbors to explore
          - eval_func: function to evaluate a solution
          - neighbor_func: function to generate neighbor solutions from another solution
          - random_init: first generated solution is random or greedy
          - restrictive: whether it is restrictive or not

      Returns the best solution found
      """

    start_time = time.time()

    counter = 0
    tabu_tenure = 5
    tabu_list = {establishment.id_est: 0 for establishment in city.nodes if establishment.id_est != 0}

    best_sol = utils.generate_random_solution(city) if random_init else utils.generate_greedy_sol(city)
    best_score = utils.evaluate_solution(city, best_sol, eval_func)
    initial = best_score
    print(f"\n\nInitial Solution: {best_sol} \nScore: {best_score}")
    x_values = [counter]
    y_values = [best_score]
    while counter < iterations:

        iteration_neighbors = []
        curr_mutation = 0
        while curr_mutation < mutations_per_iteration:
            neighbor, nodes = neighbor_func(city, best_sol)
            if nodes == [0, 0]:
                continue

            if restrictive and (tabu_list[nodes[0]] <= 0 and tabu_list[nodes[1]] <= 0):
                score = utils.evaluate_solution(city, neighbor, eval_func)
                iteration_neighbors.append((neighbor, nodes))

            if not restrictive and (tabu_list[nodes[0]] <= 0 or tabu_list[nodes[1]] <= 0):
                score = utils.evaluate_solution(city, neighbor, eval_func)
                iteration_neighbors.append((neighbor, nodes))

            curr_mutation += 1

        curr_score = 9999
        best_neigh = None
        ex_nodes = []

        if not iteration_neighbors:
            counter += 1
            for i in range(1, len(tabu_list) + 1):
                tabu_list[i] -= 1
            continue


        for x in iteration_neighbors:
            if utils.evaluate_solution(city, x[0], eval_func) < curr_score:
                best_neigh = x[0]
                curr_score = utils.evaluate_solution(city, x[0], eval_func)
                ex_nodes = x[1]

        tabu_list[ex_nodes[0]] = tabu_tenure
        tabu_list[ex_nodes[1]] = tabu_tenure

        for i in range(1, len(tabu_list) + 1):
            tabu_list[i] -= 1

        cost = curr_score - best_score
        if cost < 0:
            aux = best_score
            best_sol = best_neigh
            best_score = curr_score
            print(f"Iteration {counter}: {bcolors.GREEN} upgrade {bcolors.WHITE}\n\t\tScore: {aux} -> {best_score}\n")
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