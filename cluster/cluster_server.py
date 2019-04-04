import grpc
import time
from utils.logger import Logger
from concurrent import futures
from cluster.proto import cluster_pb2, cluster_pb2_grpc
from cluster.libs.cluster import Cluster
from cluster.libs.node import Node

from monitor.monit_client import HeartbeatClient

CPU_MAX = 20
SERVER_PORT = '50053'


class ClusterImplementation(cluster_pb2_grpc.ClusterServiceServicer):

    def __init__(self, ip, port):
        self.cluster = Cluster()
        self.node = Node(ip, port)
        self.hearbeat_client = HeartbeatClient()

    def leader_initiate(self, request, context):
        Logger.info("Request received for initiating leader.")
        # check if there is already leader in the cluster
        neighbors = self.cluster.get_neighbors()

        leader = [node for node in neighbors if node['state'] == 'Leader']
        if not leader:
            self.node.setState('Leader')
            self.node.setIsAlive(True)
            self.cluster.add_node(self.node)
            response = cluster_pb2.ackResponse(success=True, message='Node added')
            Logger.info("Node added.")
        else:
            response = cluster_pb2.ackResponse(success=False, message=f'Leader already exists. {leader}')
        Logger.info(f'Leader initiate. Response: {response}')
        return response

    def add_neighbor(self, request, context):
        ip = request.ip
        port = request.port
        Logger.info(f"Request received for adding neighbor. IP: {ip}, PORT: {port}")
        if self.node.state == 'Leader':
            neighbor = self.cluster.add_neighbor(ip, port)
            neighbor.state = 'Follower'
            is_alive = self.hearbeat_client.send_isalive(dest_ip=ip, dest_port=port)
            if is_alive:
                neighbor.state = True
                neighbor.state_data = is_alive
            else:
                neighbor.state_data = None

            response = cluster_pb2.ackResponse(success=True, message='Node added')
        else:
            response = cluster_pb2.ackResponse(success=False,
                                       message='Current node is not a leader. Only leader can add neighbors.')
        Logger.info(f"Sending a response. {response}")
        return response

    def remove_neighbor(self, request, context):
        ip = request.ip
        port = request.port
        Logger.info(f"Request received for removing neighbor. IP: {ip}, PORT: {port}")
        if self.node.state == 'Leader':
            neighbor = self.cluster.remove_neighbor(ip, port)
            if neighbor:
                response = cluster_pb2.ackResponse(success=True, message=f'Neighbor removed. {neighbor}')
            else:
                response = cluster_pb2.ackResponse(success=False, message=f'Neighbor not found. Is the ip and port correct?')
        else:
            response = cluster_pb2.ackResponse(success=False,
                                       message='Current node is not a leader. Only leader can remove neighbors.')
        Logger.info("Sending a response")
        return response

    def getLeader(self, request, context):
        Logger.info("Searching for the Leader...")
        neighbors = self.cluster.get_neighbors()
        leader = [node for node in neighbors if node['state'] == 'Leader']
        response = cluster_pb2.getLeaderRequest(ip=leader.ip, port=leader.port)
        Logger.info(f"Sending a response. {response}")
        return response

    def getNeighbors(self, request, context):
        Logger.info("Searching for all neighbors...")
        neighbors = self.cluster.get_neighbors()
        response =  cluster_pb2.getNeighborRequest(neighbors)
        Logger.info(f"Sending a response. {response}")
        return response

    def start_server(self):
        cluster_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

        # our cluster service
        cluster_pb2_grpc.add_ClusterServiceServicer_to_server(ClusterImplementation(self.node.ip, self.node.port), cluster_server)

        # bind the server to the described port
        cluster_server.add_insecure_port(f'[::]:{SERVER_PORT}')

        # start the server
        cluster_server.start()

        Logger.info(f'Cluster Server running on port {SERVER_PORT}...')

        try:
            # Keep the program running unless keyboard interruption
            while True:
                time.sleep(60 * 60 * 60)
        except KeyboardInterrupt:
            cluster_server.stop(0)
            Logger.info('Cluster  Server Stopped ...')


if __name__ == '__main__':
    cluster_server = ClusterImplementation(ip='localhost', port=SERVER_PORT)
    cluster_server.start_server()