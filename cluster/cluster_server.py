import grpc
import time
from utils.logger import Logger
from concurrent import futures
from cluster.proto import cluster_pb2, cluster_pb2_grpc
from cluster.libs.cluster import Cluster
from cluster.libs.node import Node
from random import randrange
from threading import Thread
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc

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
            leader_node = Node(request.ip, request.port)
            leader_node.setState("Leader")
            leader_node.isAlive = True
            node = self.cluster.add_node(leader_node)
            response = cluster_pb2.ackResponse(success=True, message='Node added')
            Logger.info("Node added.")
        else:
            response = cluster_pb2.ackResponse(success=False, message=f'Leader already exists. {leader}')
        Logger.info(f'Leader initiate. Response: {response}')
        return response

    def add_neighbor(self, request, context):
        neighbors = self.cluster.get_neighbors()
        node_search = [node for node in neighbors if node['ip'] == request.ip and node['port'] == request.port]
        if not node_search:
            ip = request.ip
            port = request.port
            Logger.info(f"Request received for adding neighbor. IP: {ip}, PORT: {port}")
            neighbor = self.cluster.add_neighbor(ip, port)
            neighbor.state = 'Follower'
            neighbor.state_data = ""
            response = cluster_pb2.ackResponse(success=True, message='Node added')
        else:
            response = cluster_pb2.ackResponse(success=False, message='Node already exists')

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
        node_list = [node for node in neighbors if node['state'] == 'Leader']
        leader = node_list[0]
        ip = leader['ip']
        port_number = leader['port']
        response = cluster_pb2.Node(ip=ip, port=port_number)
        Logger.info(f"Sending a response. {response}")
        return response

    def getNeighbors(self, request, context):
        Logger.info("Searching for all neighbors...")
        neighbors = self.cluster.get_neighbors()
        neighbors_list = []
        neighbor_list_response = cluster_pb2.getNeighborResponse();
        for neighbor in neighbors:
            neighbor_node_info = cluster_pb2.Node(ip=neighbor["ip"], port=neighbor["port"])
            state_data = neighbor["state_data"]
            if state_data is None:
                state_data = ""
            neighbor_info = cluster_pb2.NodeDetail(nodeInfo=neighbor_node_info, state=state_data, isAlive=neighbor["isAlive"])
            neighbors_list.append(neighbor_info)

        neighbor_list_response.nodes.extend(neighbors_list)
        Logger.info(f"Sending a neighbor response.")
        return neighbor_list_response

    def neighborHeartbeat(self):

        while True:
            # get neighbors[] from cluster
            neighbors = self.cluster.get_neighbors_objects()

            # sleep for random time between 2-13 seconds
            time.sleep(randrange(1, 4))
            print("We reached the heartbeat entry")

            for neighbor in neighbors:
                print(self.cluster.node_json(neighbor))
                #neighbor_ip = neighbor.nodeInfo.ip
                neighbor_ip = neighbor.ip
                #neighbor_port = neighbor.nodeInfo.port
                neighbor_port = neighbor.port

                # instantiate a communication channel
                channel = grpc.insecure_channel(
                    '{}:{}'.format(neighbor_ip, neighbor_port))

                # bind the client to the server channel
                stub = fileservice_pb2_grpc.FileServiceStub(channel)
                try:
                    stub.Heartbeat(fileservice_pb2.HeartbeatRequest())
                    neighbor.setIsAlive(True)
                    Logger.info("Node is alive")
                except:
                    neighbor.setIsAlive(False)
                    if neighbor.getState() == "Leader":
                        neighbor.setState("Follower")
                    Logger.info("Node is not alive")

            node_alive_list = [node for node in neighbors if node.getIsAlive() == True]


    def start_server(self):
        cluster_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

        # our cluster service
        cluster_pb2_grpc.add_ClusterServiceServicer_to_server(ClusterImplementation(self.node.ip, self.node.port), cluster_server)

        # bind the server to the described port
        cluster_server.add_insecure_port(f'[::]:{SERVER_PORT}')



        # start the server
        cluster_server.start()

        thread_1 = Thread(target=self.neighborHeartbeat)
        thread_1.start()


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
