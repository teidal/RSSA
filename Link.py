class Link:
    _counter = 0

    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.length = length
        self.cores = []

        self.id = Link._counter
        Link._counter += 1

