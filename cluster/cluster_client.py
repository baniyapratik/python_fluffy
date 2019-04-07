import grpc
from utils.logger import Logger
from cluster.proto import cluster_pb2, cluster_pb2_grpc

SERVER_PORT_1 = '50053'
SERVER_PORT_2 = '50054'


class ClusterClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = SERVER_PORT_1
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = cluster_pb2_grpc.ClusterServiceStub(self.channel)

    def leader_initiate(self, ip, port):
        Logger.info("Sending Request for leader initiate..")
        _node_info = cluster_pb2.Node(ip=ip, port=port)
        try:
            response = self.stub.leader_initiate(_node_info)
        except Exception as err:
            response = err
        Logger.info(f"Response for leader initiate. {response}")
        return response

    def add_neighbor(self, ip, port):
        Logger.info("Sending Request for add neighbor..")
        _node_info = cluster_pb2.Node(ip=ip, port=port)
        try:
            response = self.stub.add_neighbor(_node_info)
        except Exception as err:
            response = err
        Logger.info(f"Response for add neighbor. {response}")
        return response

    def remove_neighbor(self, ip, port):
        Logger.info("Sending Request for remove neighbor..")
        _node_info = cluster_pb2.Node(ip=ip, port=port)
        try:
            response = self.stub.remove_neighbor(_node_info)
        except Exception as err:
            response = err
        Logger.info(f"Response for remove neighbor. {response}")
        return response

    def getLeader(self):
        Logger.info("Sending Request for get leader..")
        try:
            response = self.stub.getLeader()
        except Exception as err:
            response = err
        Logger.info(f"Response for get leader. {response}")
        return response

    def getNeighbors(self):
        Logger.info("Sending Request for get neighbors..")
        try:
            response = self.stub.getNeighbors(cluster_pb2.getNeighborRequest())
        except Exception as err:
            response = err
        Logger.info(f"Response for get neighbors. {response}")
        return response


if __name__ == "__main__":
    cluster_client = ClusterClient()
    cluster_client.leader_initiate(ip="localhost", port=SERVER_PORT_1)
    cluster_client.add_neighbor(ip="localhost", port=SERVER_PORT_2)
    cluster_client.getNeighbors()