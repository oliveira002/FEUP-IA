import itertools
import os
import folium
import webbrowser
import utils

from city import City
from hill_climbing import hill_climbing
from tabu_search import tabu_search
from simulated_annealing import simulated_annealing
from genetic import genetic_algorithm, crossover_classical


def draw_map(solution, city: City):
    """
      Draws the solution on the map

      Parameters:
          - city: The city with all establishments
          - solution: The solution

      """
    colors = ['red', 'blue', 'gray', 'darkred', 'lightred', 'orange', 'beige', 'green', 'darkgreen', 'lightgreen',
              'darkblue', 'lightblue', 'purple', 'darkpurple', 'pink', 'cadetblue', 'lightgray', 'black']
    paths = []
    for x in solution:
        temp = []
        for y in x:
            temp.append((city.nodes[y].latitude, city.nodes[y].longitude))
        paths.append(temp)

    color_cycle = itertools.cycle(colors)
    mapa = folium.Map(location=[41.1, -7.8], zoom_start=9)
    feature_groups = []
    for i, path in enumerate(paths):
        feature_group = folium.FeatureGroup(name=f'Path {i + 1}')
        folium.PolyLine(path, color=colors[i % len(colors)], weight=2).add_to(feature_group)
        feature_group.add_to(mapa)
        feature_groups.append(feature_group)
    folium.LayerControl().add_to(mapa)

    mapa.save('my_map.html')
    webbrowser.open(os.path.abspath("my_map.html"))


def menu():
    while True:
        print("\n1. Hill climbing")
        print("2. Simulated annealing")
        print("3. Tabu search")
        print("4. Genetic algorithm")
        print("0. Exit")
        n = int(input("Select an algorithm to run: "))

        if n == 0:
            break
        elif n not in [1, 2, 3, 4]:
            print("Not a valid option! \n")
            continue

        size = int(input("\nSize of the city (number of establishments) (20-1000): "))  # Tested with 200
        city = City(size)

        if n == 1:
            iterations = int(input("Number of iterations: "))  # Tested with 1000

            while True:
                print(
                    "\n1. Greedy: Remove a random node from the slowest vehicle and add it to a random vehicle at a random position")  # neighbors_1
                print("2. Greedy: Switches two 2 randoms nodes between worst vehicle and a random one.")  # neighbors_2
                print("3. Greedy: For the worse vehicle, changes 2 nodes order in the Path")  # neighbors_3
                print(
                    "4. Random: Remove a random node from a random vehicle and add it into a random position at other random vehicle")  # neighbors_rm_add
                print("5. Random: Switches two 2 randoms nodes between 2 random vehicles")  # neighbors_diff_vec_nodes
                print("6. Random: For the same vehicles, changes 2 nodes order in the Path")  # neighbors_diff_sorting
                n = int(input("Select an algorithm to run: "))

                if n not in [1, 2, 3, 4, 5, 6]:
                    print("Not a valid option! \n")
                    continue
                elif n == 1:
                    neighbor_func = utils.neighbors_1
                    break
                elif n == 2:
                    neighbor_func = utils.neighbors_2
                    break
                elif n == 3:
                    neighbor_func = utils.neighbors_3
                    break
                elif n == 4:
                    neighbor_func = utils.neighbors_rm_add
                    break
                elif n == 5:
                    neighbor_func = utils.neighbors_diff_vec_nodes
                    break
                elif n == 6:
                    neighbor_func = utils.neighbors_diff_sorting
                    break

            random_init = bool(input("\nRandom start (True/False)?: "))  # Tested with True

            sol = hill_climbing(city=city,
                                iterations=iterations,
                                eval_func=utils.vehicle_time,
                                neighbor_func=neighbor_func,
                                random_init=random_init)

        elif n == 2:
            iterations = int(input("Number of iterations: "))  # Tested with 1000
            initial_temp = int(input("Initial temperature: "))  # Tested with 1000

            while True:
                print(
                    "\n1. Greedy: Remove a random node from the slowest vehicle and add it to a random vehicle at a random position")  # neighbors_1
                print("2. Greedy: Switches two 2 randoms nodes between worst vehicle and a random one.")  # neighbors_2
                print("3. Greedy: For the worse vehicle, changes 2 nodes order in the Path")  # neighbors_3
                print(
                    "4. Random: Remove a random node from a random vehicle and add it into a random position at other random vehicle")  # neighbors_rm_add
                print("5. Random: Switches two 2 randoms nodes between 2 random vehicles")  # neighbors_diff_vec_nodes
                print("6. Random: For the same vehicles, changes 2 nodes order in the Path")  # neighbors_diff_sorting
                n = int(input("Select an algorithm to run: "))

                if n not in [1, 2, 3, 4, 5, 6]:
                    print("Not a valid option! \n")
                    continue
                elif n == 1:
                    neighbor_func = utils.neighbors_1
                    break
                elif n == 2:
                    neighbor_func = utils.neighbors_2
                    break
                elif n == 3:
                    neighbor_func = utils.neighbors_3
                    break
                elif n == 4:
                    neighbor_func = utils.neighbors_rm_add
                    break
                elif n == 5:
                    neighbor_func = utils.neighbors_diff_vec_nodes
                    break
                elif n == 6:
                    neighbor_func = utils.neighbors_diff_sorting
                    break

            random_init = bool(input("\nRandom start (True/False)?: "))  # Tested with True
            min_temp = int(input("Minimum temperature: "))  # Tested with 1

            sol = simulated_annealing(city=city,
                                      iterations=iterations,
                                      initial_temp=initial_temp,
                                      eval_func=utils.vehicle_time,
                                      neighbor_func=neighbor_func,
                                      random_init=random_init,
                                      min_temp=min_temp)

        elif n == 3:
            iterations = int(input("Number of iterations: "))  # Tested with 1000
            mutations_per_iteration = int(input("Number of mutations per iteration: "))  # Tested with 20

            while True:
                print("\n1. Greedy: Switches two 2 randoms nodes between worst vehicle and a random one.")  # neighbors_2
                print("2. Greedy: For the worse vehicle, changes 2 nodes order in the Path")  # neighbors_3
                print("3. Random: Switches two 2 randoms nodes between 2 random vehicles")  # neighbors_diff_vec_nodes
                print("4. Random: For the same vehicles, changes 2 nodes order in the Path")  # neighbors_diff_sorting
                n = int(input("Select an algorithm to run: "))

                if n not in [1, 2, 3, 4]:
                    print("Not a valid option! \n")
                    continue
                elif n == 1:
                    neighbor_func = utils.neighbors_2
                    break
                elif n == 2:
                    neighbor_func = utils.neighbors_3
                    break
                elif n == 3:
                    neighbor_func = utils.neighbors_diff_vec_nodes
                    break
                elif n == 4:
                    neighbor_func = utils.neighbors_diff_sorting
                    break

            random_init = bool(input("\nRandom start (True/False)?: "))  # Tested with True
            restrictive = bool(input("Restrictive (True/False)?: "))  # Tested with False

            sol = tabu_search(city=city,
                              iterations=iterations,
                              mutations_per_iteration=mutations_per_iteration,
                              eval_func=utils.vehicle_time,
                              neighbor_func=neighbor_func,
                              random_init=random_init,
                              restrictive=restrictive)

        elif n == 4:
            iterations = int(input("Number of iterations: "))  # Tested with 1000

            while True:
                print(
                    "\n1. Greedy: Remove a random node from the slowest vehicle and add it to a random vehicle at a random position")  # neighbors_1
                print("2. Greedy: Switches two 2 randoms nodes between worst vehicle and a random one.")  # neighbors_2
                print("3. Greedy: For the worse vehicle, changes 2 nodes order in the Path")  # neighbors_3
                print("4. Random: Remove a random node from a random vehicle and add it into a random position at other random vehicle")  # neighbors_rm_add
                print("5. Random: Switches two 2 randoms nodes between 2 random vehicles")  # neighbors_diff_vec_nodes
                print("6. Random: For the same vehicles, changes 2 nodes order in the Path")  # neighbors_diff_sorting
                n = int(input("Select an algorithm to run: "))

                if n not in [1, 2, 3, 4, 5, 6]:
                    print("Not a valid option! \n")
                    continue
                elif n == 1:
                    neighbor_func = utils.neighbors_1
                    break
                elif n == 2:
                    neighbor_func = utils.neighbors_2
                    break
                elif n == 3:
                    neighbor_func = utils.neighbors_3
                    break
                elif n == 4:
                    neighbor_func = utils.neighbors_rm_add
                    break
                elif n == 5:
                    neighbor_func = utils.neighbors_diff_vec_nodes
                    break
                elif n == 6:
                    neighbor_func = utils.neighbors_diff_sorting
                    break

            random_init = bool(input("\nRandom start (True/False)?: "))  # Tested with True
            pop_size = int(input("Population size: "))  # Tested with 20
            pop_rep = float(input("Population reproduction rate: "))  # Tested with 0.1

            sol = genetic_algorithm(city=city,
                                    iterations=iterations,
                                    eval_func=utils.vehicle_time,
                                    crossover_func=crossover_classical,
                                    neighbor_func=neighbor_func,
                                    random_start=random_init,
                                    population_size=pop_size,
                                    population_reproduction=pop_rep)

        draw_map(sol, city)


if __name__ == '__main__':
    menu()

