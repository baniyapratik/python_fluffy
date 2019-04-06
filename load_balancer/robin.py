
"""
Round-robin
"""


class RoundRobin:

    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.count = 0

    def add(self, node):
        self.nodes.append(node)

    def remove(self, node):
        # Reset count to zero
        self.nodes.remove(node)
        self.count = 0

    def get(self):
        node = self.nodes[self.count]
        self.count = (self.count + 1) % (len(self.nodes))
        return node

    def set(self, nodes=[]):
        self.nodes = nodes
        self.count = 0

if __name__ == '__main__':
    rr = RoundRobin(nodes=[('localhost', i) for i in range(5000, 5005)])

    print(rr.nodes)
    rr.remove(('localhost', 5000))

    print(rr.nodes)

    for j in range(10):
        print(rr.get())
