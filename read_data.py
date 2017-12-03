import Link
import Path
import numpy as np


def read_network(filename):
    with open('Euro16/' + filename) as f:
        lines = f.readlines()
        nodes = int(lines[0])
        links = int(lines[1])
        network = []
        l = []
        for line in lines[2:]:
            network.append([int(x) for x in line.split('\t')])

        for i in range(2, len(lines)):
            n = lines[i].split('\t')
            for j in range(len(n)):
                if n[j] != 0:
                    l.append(Link.Link(i, j, int(n[j])))
        return nodes, links, network, l


def read_paths(filename1, filename2):
    with open('Euro16/' + filename1) as f1, open('Euro16/' + filename2) as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        paths = lines1[0]
        net_matrix = np.zeros((nodes, nodes))
        p = []
        x = 0
        y = 1
        l = []
        for i in range(1, len(lines1)):
            if i > 0 and i % 30 == 0:
                net_matrix[x][y] = p
                p.clear()
                y += 1
                if y == x:
                    y += 1
                if y == nodes:
                    y = 0
                    x += 1

            n = lines1[i].split('\t')
            slices = list(map(int, lines2[i].split('\t')))
            for j in range(len(n)):
                if int(n[j]):
                    l.append(j)
            p.append(Path.Path(x, y, l, slices))
        return net_matrix


filename = "ee.net"
filename1 = "ee30.pat"
filename2 = "ee30.spec"

nodes, links_num, net, links = read_network(filename)
matrix = read_paths(filename1, filename2)
