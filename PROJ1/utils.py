import copy
import math
import random
import numpy
import numpy as np

from city import City, Vehicle
from random import choice
import matplotlib.pyplot as plt


def evaluate_solution(city: City, solution, eval_func):
    """
    Evaluate a given solution
    Parameters:
        city: the city with all establishments
        solution: solution to be evaluated
        eval_func: evaluation function

    Returns the solution value

    """
    max_time = -9999
    for i in range(len(solution)):
        path = solution[i]
        curr_time = eval_func(city, path)
        # print(f'Vehicle {i + 1} total evaluation: {curr_time} hours')
        if curr_time > max_time:
            max_time = curr_time

    # print(f'Total evaluation: {max_time} hours')
    return max_time


def vehicle_time(city: City, path):
    """
    Function that given a certain path calculates the total duration of a vehicle from the depot until it comes back

    Parameters:
        - city: The city with all establishments
        - path: path of a vehicle

    Returns total path duration

    """
    day_time = 9 * 3600
    days = 1
    for i in range(len(path) - 1):
        src_node = city.nodes[path[i]]
        dst_node = city.nodes[path[i + 1]]
        day_time += city.edges[path[i]][path[i + 1]]
        if day_time >= 24 * 3600:
            days += 1
            day_time = day_time % (24 * 3600)
        if i == len(path) - 2:
            break
        next_opening = dst_node.next_opening_2(day_time)
        if next_opening < day_time:
            days += 1
        day_time = next_opening + dst_node.inspection_time
        if day_time >= 24 * 3600:
            days += 1
            day_time = day_time % (24 * 3600)
    if days == 1:
        return (day_time - 9 * 3600) / 3600

    return (24 * 3600 * (days - 2) + day_time + (24 * 3600 - 9 * 3600)) / 3600


def path_duration(city: City, path):
    """
       Function that given a certain path calculates the total duration of a vehicle from the depot until it comes back

       Parameters:
           - city: The city with all establishments
           - path: path of a vehicle

       Returns total path duration

       """
    size = len(path)
    days = 1
    curr_time = 9 * 3600
    for i in range(size):
        if i == size - 1:
            break

        idx = path[i]
        src_node = city.nodes[idx]
        idx = path[i + 1]
        dest_node = city.nodes[idx]

        travel_time = city.edges[src_node.id_est][dest_node.id_est]
        arrival_time = travel_time + curr_time
        inspection_time = dest_node.inspection_time

        if arrival_time >= 24 * 3600:
            days += 1

        arrival_time = arrival_time % (24 * 3600)

        # print(f'Leave NODE: {src_node.id_est}')
        # print(f'Current Time: {curr_time}')
        # print(f'Arrival Time: {arrival_time}')

        if dest_node.is_open(arrival_time):
            # print(f'It is OPEN')
            if i == size - 2:
                new_time = arrival_time
            else:
                new_time = arrival_time + inspection_time
            curr_time = new_time % (24 * 3600)

            if new_time >= (24 * 3600):
                # print("New day")
                days += 1

        else:
            opens_at = dest_node.next_opening(arrival_time)
            new_time = opens_at + inspection_time
            if opens_at < arrival_time:
                # print("New day")
                days += 1
            if new_time >= (24 * 3600):
                days += 1
            new_time = new_time % (24 * 3600)
            curr_time = new_time
            # print(f'It will open at {opens_at}')

    if days == 1:
        dur = curr_time - (9 * 3600)
    else:
        dur = (24 * 3600 - 9 * 3600) + ((days - 2) * 24 * 3600) + curr_time

    # print(f' ola {curr_time}')
    dur = dur / 3600
    # print(f"Inspections occurred within {days} days")
    # print(f"Duration of {dur}hours")
    return dur


def generate_random_solution(city: City):
    """
       Generates a random feasible solution, meaning in the end all nodes will be visited

       Parameters:
           - city: The city with all establishments

       Returns list with paths of each vehicle

       """
    all_stores = [x for x in city.nodes if x.id_est != 0]
    vehicles = []
    for i in range(math.floor(0.1 * (len(city.nodes) - 1))):
        vehicles.append(Vehicle(city.nodes[0]))

    while all_stores:
        # randomly choose node & vehicle
        vec = choice(vehicles)
        dest_node = choice(all_stores)

        src_node = vec.path[-1]
        travel_time = city.edges[src_node.id_est][dest_node.id_est]
        arrival_dest_time = travel_time + vec.real_time

        if arrival_dest_time >= 24 * 3600:
            vec.days += 1

        arrival_dest_time = arrival_dest_time % (24 * 3600)

        # visit the node right away
        if dest_node.is_open(arrival_dest_time):
            new_time = arrival_dest_time + dest_node.inspection_time
            if new_time >= (24 * 3600):
                vec.days += 1
            new_time = new_time % (24 * 3600)
            vec.update_time(new_time, True)

        # wait until its open
        else:
            opens_at = dest_node.next_opening(arrival_dest_time)
            if opens_at < arrival_dest_time:
                vec.days += 1
            vec.real_time = opens_at
            vec.update_time(dest_node.inspection_time, False)

        vec.path.append(dest_node)
        dest_node.visited = True
        all_stores.remove(dest_node)

    # all nodes have been visited
    for vec in vehicles:
        src_node = vec.path[-1]
        travel_time = city.edges[src_node.id_est][0]
        vec.path.append(city.nodes[0])
        vec.update_time(travel_time, False)

    res = []

    for vec in vehicles:
        vec_path = [x.id_est for x in vec.path]
        res.append(vec_path)

    return res


def neighbors_1(city: City, solution):
    """
      Generates a neighbor feasible solution. Remove a random node from the slowest vehicle and add it to a random vehicle at a random position

      Parameters:
          - solution: which we generate the neighbors from

      Returns neighbor solution (list with paths of each vehicle)
    """

    neighbor = copy.deepcopy(solution)
    num_vehicles = len(solution)

    fst_vec_aux = max(solution, key=lambda x: vehicle_time(city, x))
    fst_vec = [ind for ind, x in enumerate(solution) if x == fst_vec_aux][0]

    while True:
        snd_vec = random.randint(0, num_vehicles - 1)

        if fst_vec != snd_vec:
            break

    fst_node = random.randint(1, len(solution[fst_vec]) - 2)

    first_path, snd_path = list(solution[fst_vec]), list(solution[snd_vec])
    first_path.remove(solution[fst_vec][fst_node])

    insertion_idx = random.randint(1, len(solution[snd_vec]) - 2)
    snd_path.insert(insertion_idx, solution[fst_vec][fst_node])

    neighbor[fst_vec] = first_path
    neighbor[snd_vec] = snd_path

    return neighbor, []


def neighbors_2(city: City, solution):
    """
      Generates a neighbor feasible solution. Switches two 2 randoms nodes between worst vehicle and a random one.

      Parameters:
          - solution: which we generate the neighbors from

      Returns neighbor solution (list with paths of each vehicle)

    """
    neighbor = copy.deepcopy(solution)
    num_vehicles = len(solution)

    fst_vec_aux = max(solution, key=lambda x: vehicle_time(city, x))
    fst_vec = [ind for ind, x in enumerate(solution) if x == fst_vec_aux][0]

    while True:
        snd_vec = random.randint(0, num_vehicles - 1)

        if fst_vec != snd_vec and len(solution[fst_vec]) > 2 and len(solution[snd_vec]) > 2:
            break

    changes = []

    fst_node = random.randint(1, len(solution[fst_vec]) - 2)
    snd_node = random.randint(1, len(solution[snd_vec]) - 2)

    neighbor[fst_vec][fst_node] = solution[snd_vec][snd_node]
    neighbor[snd_vec][snd_node] = solution[fst_vec][fst_node]

    changes = [solution[fst_vec][fst_node], solution[snd_vec][snd_node]]

    return neighbor, changes


def neighbors_3(city: City, solution):
    """
      Generates a neighbor feasible solution. For the worse vehicle, changes 2 nodes order in the Path

      Parameters:
          - solution: which we generate the neighbors from

      Returns neighbor solution (list with paths of each vehicle)

    """

    # define neighbor
    neighbor = copy.deepcopy(solution)
    num_vehicles = len(solution)
    fst_vec = max(solution, key=lambda x: vehicle_time(city, x))
    random_vehicle = [ind for ind, x in enumerate(solution) if x == fst_vec][0]

    if len(solution[random_vehicle]) <= 3:
        return solution, [0, 0]

    # while didn't choose the same establishment twice
    changes = []
    while True:
        first_establishment = random.randint(1, len(solution[random_vehicle]) - 2)
        second_establishment = random.randint(1, len(solution[random_vehicle]) - 2)

        if first_establishment != second_establishment:
            neighbor[random_vehicle][first_establishment] = neighbor[random_vehicle][second_establishment]
            neighbor[random_vehicle][second_establishment] = solution[random_vehicle][first_establishment]
            changes = [solution[random_vehicle][first_establishment], solution[random_vehicle][second_establishment]]
            break

    return neighbor, changes


def neighbors_rm_add(city: City, solution):
    """
      Generates a neighbor feasible solution. Remove a random node from a random vehicle and add it into a random position at other random vehicle

      Parameters:
          - solution: which we generate the neighbors from

      Returns neighbor solution (list with paths of each vehicle)
    """

    neighbor = copy.deepcopy(solution)
    num_vehicles = len(solution)

    while True:
        fst_vec = random.randint(0, num_vehicles - 1)
        snd_vec = random.randint(0, num_vehicles - 1)

        if fst_vec != snd_vec:
            break

    fst_node = random.randint(1, len(solution[fst_vec]) - 2)

    first_path, snd_path = list(solution[fst_vec]), list(solution[snd_vec])
    first_path.remove(solution[fst_vec][fst_node])

    insertion_idx = random.randint(1, len(solution[snd_vec]) - 2)
    snd_path.insert(insertion_idx, solution[fst_vec][fst_node])

    neighbor[fst_vec] = first_path
    neighbor[snd_vec] = snd_path

    return neighbor, []


def neighbors_diff_vec_nodes(city: City, solution):
    """
      Generates a neighbor feasible solution. Switches two 2 randoms nodes between 2 random vehicles

      Parameters:
          - solution: which we generate the neighbors from

      Returns neighbor solution (list with paths of each vehicle)

    """
    neighbor = copy.deepcopy(solution)
    num_vehicles = len(solution)

    while True:
        fst_vec = random.randint(0, num_vehicles - 1)
        snd_vec = random.randint(0, num_vehicles - 1)

        if fst_vec != snd_vec and len(solution[fst_vec]) > 2 and len(solution[snd_vec]) > 2:
            break

    changes = []

    fst_node = random.randint(1, len(solution[fst_vec]) - 2)
    snd_node = random.randint(1, len(solution[snd_vec]) - 2)

    neighbor[fst_vec][fst_node] = solution[snd_vec][snd_node]
    neighbor[snd_vec][snd_node] = solution[fst_vec][fst_node]

    changes = [solution[fst_vec][fst_node], solution[snd_vec][snd_node]]

    return neighbor, changes


def neighbors_diff_sorting(city: City, solution):
    """
      Generates a neighbor feasible solution. For the same vehicles, changes 2 nodes order in the Path

      Parameters:
          - solution: which we generate the neighbors from

      Returns neighbor solution (list with paths of each vehicle)

    """

    # define neighbor
    neighbor = copy.deepcopy(solution)
    num_vehicles = len(solution)
    random_vehicle = random.randint(0, num_vehicles - 1)

    if len(solution[random_vehicle]) <= 3:
        return solution, [0, 0]

    # while didn't choose the same establishment twice
    changes = []
    while True:
        first_establishment = random.randint(1, len(solution[random_vehicle]) - 2)
        second_establishment = random.randint(1, len(solution[random_vehicle]) - 2)

        if first_establishment != second_establishment:
            neighbor[random_vehicle][first_establishment] = neighbor[random_vehicle][second_establishment]
            neighbor[random_vehicle][second_establishment] = solution[random_vehicle][first_establishment]
            changes = [solution[random_vehicle][first_establishment], solution[random_vehicle][second_establishment]]
            break

    return neighbor, changes


def heuristic_func(city: City, src_node, dest_node):
    return 0.6 * city.nodes[dest_node].inspection_time + 0.4 * city.edges[src_node][dest_node]


def get_closest_node(city: City, src_node, available_nodes):
    heuristic_list = [(x, heuristic_func(city, src_node, x)) for x in available_nodes]
    heuristic_list = sorted(heuristic_list, key=lambda k: k[1])
    return heuristic_list[0][0]


def generate_greedy_sol(city: City):
    """
      Generates a greedy solution for the current city

      Parameters:
          - city: current city

      Returns the greedy solution
    """
    all_stores = [x.id_est for x in city.nodes if x.id_est != 0]
    vehicles = []

    for i in range(math.floor(0.1 * (len(city.nodes) - 1))):
        vehicles.append(Vehicle(city.nodes[0]))

    while all_stores:
        for vec in vehicles:
            curr_node = vec.path[-1].id_est
            closest_node = get_closest_node(city, curr_node, all_stores)
            vec.path.append(city.nodes[closest_node])
            all_stores.remove(closest_node)

    # all nodes have been visited
    for vec in vehicles:
        vec.path.append(city.nodes[0])

    res = []

    for vec in vehicles:
        vec_path = [x.id_est for x in vec.path]
        res.append(vec_path)

    return res


def write_results_file(time1, time2, initial, final, file_name='data_out/export.txt'):
    """
      Writes data to the respective algorithm file

      Parameters:
          - file_name: name of the file
          - initial: initial solution value
          - final: final solution value
          - time: time taken to execute the algorithm

      Returns 1 if success in writing to file
      """
    with open(file_name, 'a') as f:
        f.write(f'{time1}\n{time2}\n{initial}\n{final}\n\n')
    return 1


def plot_execution(x_values, y_values, title):
    plt.plot(x_values, y_values)
    plt.xlabel('Number Iterations')
    plt.ylabel('Solution Evaluation')
    plt.title(title)
    plt.show()
