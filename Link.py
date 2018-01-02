import numpy as np


class Link:
    _counter = 0
    biggest = 0

    def __init__(self, start, end, length, cores):
        self.start = start
        self.end = end
        self.length = length
        self.core_num = cores
        self.cores = [0 for x in range(cores)]
        self.biggest_taken = [0, 0]

        self.id = Link._counter
        Link._counter += 1

    def can_add(self, slices):
        for i in range(len(self.cores)):
            if self.cores[i] == 0 or (self.cores[i] + slices) < self.biggest_taken[1]:
                return i
            else:
                return -1

    def assign_core(self, core, slices):
        if core == -1:
            index = self.cores.index(min(self.cores))
            self.cores[index] += slices
            if self.cores[index] > self.biggest_taken[1]:
                self.biggest_taken = [index, self.cores[index]]
            if self.cores[index] > Link.biggest:
                Link.biggest = self.cores[index]
        else:
            self.cores[core] = self.cores[core] + slices
            if self.cores[core] > self.biggest_taken[1]:
                self.biggest_taken = [core, self.cores[core]]
            if self.cores[core] > Link.biggest:
                Link.biggest = self.cores[core]
