from cluster.libs.node import Node

class Cluster:
    neighbors = []

    def add_node(self, node):
        self.neighbors.append(node)
        return self.node_json(node)

    def add_neighbor(self, host, port):
        node = Node(host, port)
        self.neighbors.append(node)
        return node

    def remove_neighbor(self, ip, port):
        for neighbor in self.neighbors:
            if neighbor.ip == ip and neighbor.port == port:
                self.neighbors.remove(neighbor)
                return neighbor
            else:
                return None

    def get_neighbors(self):
        my_neighbors = [self.node_json(neighbor) for neighbor in self.neighbors]
        return my_neighbors

    def node_json(self, node):
        return {
            "ip": node.ip,
            "port": node.port,
            "state": node.state,
            "state_data": node.state_data,
            "isAlive": node.isAlive
        }