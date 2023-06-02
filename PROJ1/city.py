import ast
import csv
import math

from establishments import Establishment


class City:
    def __init__(self, data_size: int):
        """
        Constructor for city, reads from the files and creates the graph
        Parameters:
            data_size: City Size
        """
        data_size += 1
        matrix = [[0 for _ in range(data_size)] for _ in range(data_size)]
        vehicles = []
        nodes = []

        # parse input file
        distances_file = 'data/distances.csv'
        establishments_file = 'data/establishments.csv'
        counter = 0

        # add nodes
        with open(establishments_file,encoding="utf8") as file:
            read = csv.reader(file)
            next(read)
            for row in read:
                opening_hours = self.parse_open_hours(ast.literal_eval(row[9]))
                est = Establishment(int(row[0]), row[1], row[2], row[3], row[4], float(row[5]), float(row[6]),
                                    float(row[7]), int(row[8]) * 60, opening_hours)
                nodes.append(est)
                counter += 1
                if counter == data_size:
                    counter = 0
                    break

        # add edges
        with open(distances_file, encoding="utf8") as file:
            read = csv.reader(file)
            next(read)
            src_id = 0
            dest_id = 0
            for row in read:
                for i in range(data_size + 1):
                    if i == 0:
                        continue
                    else:
                        matrix[src_id][dest_id] = float(row[i])
                    dest_id += 1
                dest_id = 0
                src_id += 1
                counter += 1
                if counter == data_size:
                    break

        # add vehicles
        for i in range(math.floor(0.1 * (data_size - 1))):
            vehicles.append(Vehicle(nodes[0]))

        self.vehicles = vehicles
        self.edges = matrix
        self.nodes = nodes
        self.data_size = data_size

    def parse_open_hours(self, times: list[int]):
        """
            Parses the list of opening hours
            Parameters:
                - times: list of opening hours
            Returns list of tuples with open hours
        """
        result = []
        start = None
        for i in range(len(times)):
            if times[i] == 1:
                if start is None:
                    start = i
            else:
                if start is not None:
                    result.append((start * 3600, i * 3600))
                    start = None
        if start is not None:
            result.append((start * 3600, len(times) * 3600))
        return result

    """"
    def find_nearest(self, curr_node):
        res = []
        for edges in curr_node.edges:
            if(edges.dest != 0 and (not self.nodes[edges.dest].visited)):
                res.append((edges.weight, edges.dest))

        res.sort(key=lambda tup: tup[0])
        return res


    def find_furthest_n_establishment(self, exclude):
        result = []
        for i in range(len(self.nodes)):
            result.append([])
        for i in range(len(self.nodes)):
            if i in exclude:
                continue
            for j in range(len(self.nodes[i].edges)):
                if j in exclude:
                    continue
                result[i].append([self.nodes[i].edges[j].weight, j])
            r = max(result[i], key=lambda x: x[0])
            result[i] = r



        return result
    """""

    def all_visited(self):
        for node in self.nodes:
            if not node.visited:
                return False

        return True


class Node:
    def __init__(self, establishment, parent=None):
        self.establishment = establishment
        self.parent = parent
        self.visited = None


class Vehicle:
    def __init__(self, start_node: Establishment):
        self.path = [start_node]
        self.real_time = 32400.0  # day starts are 09:00 AM
        self.days = 1

    def update_time(self, time, set_time):
        if set_time:
            if time < self.real_time:
                self.days += 1
            self.real_time = time
        else:
            new_time = self.real_time + time
            self.real_time = new_time % (24 * 3600)
            if new_time >= 24 * 3600:
                self.days += 1
