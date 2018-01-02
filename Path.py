class Path:
    def __init__(self, start, end, links, slices, length):
        self.start = start
        self.end = end
        self.links = links
        self.slices = slices
        self.length = length

    def calc_slices(self, speed):
        return self.slices[((speed - 1) // 50)]