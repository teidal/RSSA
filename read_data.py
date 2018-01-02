import Link
import Path
import numpy as np
import pandas as pd
import itertools
from operator import methodcaller, attrgetter, itemgetter


def read_network(filename):
    with open('Euro16/' + filename) as f:
        lines = f.readlines()
        nodes = int(lines[0])
        links = int(lines[1])
        network = []
        l = []
        x = 0
        for line in lines[2:]:
            network.append([int(x) for x in line.split('\t')])

        for i in range(2, len(lines)):
            n = lines[i].split('\t')
            for j in range(len(n)):
                if int(n[j]) != 0:
                    l.append(Link.Link(x, j, int(n[j]), cores_num))
            x += 1
        return nodes, links, network, l


def read_paths(filename1, filename2):
    with open('Euro16/' + filename1) as f1, open('Euro16/' + filename2) as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        net_matrix = np.zeros((nodes_num, nodes_num), dtype=object)
        p = []
        x = 0
        y = 1
        for i in range(len(lines1)):
            if i > 0 and i % 30 == 0:
                net_matrix[x][y] = p
                p = []
                y += 1
                if y == nodes_num:
                    y = 0
                    x += 1
                if y == x:
                    y += 1

            n = lines1[i].split()
            slices = list(map(int, lines2[i].split()))
            l = []
            for j in range(len(n)):
                if int(n[j]):
                    l.append(j)
            length = 0
            for t in l:
                length += links[t].length
            p.append(Path.Path(x, y, l, slices, length))
            if i == 7199:
                net_matrix[x][y] = p
                break
        return net_matrix


def read_demands(filename):
    with open('Euro16/' + filename) as f:
        lines = f.readlines()
        dems = []
        for line in lines[1:]:
            dems.append([int(x) for x in line.split(' ')])
        return dems


def find_shortest(start, end, distance, tabu=[]):
    paths = matrix[start][end]
    # shortest = min(paths, key=attrgetter('length'))[0]
    length = 20000
    shortest = None
    for path in paths:
        if path not in tabu and path.length < length:
            length = path.length
            shortest = path
    slices = shortest.calc_slices(distance)
    return shortest, slices


def sort_demands(dems):
    for demand in dems:
        shortest, slices = find_shortest(demand[0], demand[1], demand[2])
        demand.append(shortest)
        demand.append(slices)
        # start, end, gbps, path, slices
    return sorted(dems, key=itemgetter(4, 2), reverse=True)


def execute():
    for demand in dems_sorted:
        to_add = []
        forbidden = [demand[3]]
        default = demand[3].links
        for j in default:
            index = links[j].can_add(demand[4])
            to_add.append([j, index, demand[4]])
        for l in itertools.count():
            if (-1 not in (z[1] for z in to_add)) or l > 28:
                break
            to_add = []
            shortest, slices = find_shortest(demand[0], demand[1], demand[2], forbidden)
            for k in shortest.links:
                index2 = links[k].can_add(slices)
                to_add.append([k, index2, slices])
            forbidden.append(shortest)

        if -1 in to_add:  # no available cores = add to default path
            for j in default:
                links[j].assign_core(-1, demand[4])
        else:  # available core found
            for j in to_add:
                links[j[0]].assign_core(j[1], j[2])

    print("done")


def export(data):
    filename = 'results.csv'
    # filename = 'results.csv'
    head = ['Cores number', 'Demand file', 'Most slices']
    my_df = pd.DataFrame(data)
    my_df.to_csv(filename, index=False, header=head, sep=';')


if __name__ == "__main__":
    filename = "ee.net"
    filename1 = "e30.pat"
    filename2 = "e30.spec"
    dems_file = "01.dem"
    cores_num = 7
    results = []

    nodes_num, links_num, net, links = read_network(filename)
    matrix = read_paths(filename1, filename2)
    demands = read_demands(dems_file)

    dems_sorted = sort_demands(demands)
    execute()
    #  export([cores_num, dems_file, links[0].biggest])
    print(links[0].biggest)
