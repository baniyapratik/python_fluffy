import os
import math
from tqdm import tqdm
import grpc
from utils.logger import Logger
from utils import FileHandler
import utils.FileHandler as file_handler
from cluster.proto import cluster_pb2, cluster_pb2_grpc
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50053
CHUNK_SIZE = 4*1024
THRESHHOLD = 3500000


class FileClient(object):
    """
    Client for accessing the gRPC functionality
    """
    def __init__(self):
        # configure the host and the
        # the port to which the client should connect
        # to.
        self.cluster_ip = 'localhost'
        self.cluster_port = SERVER_PORT
        # self.cluster_ip = '192.168.0.9'
        # self.cluster_port = 9000

        # instantiate a communication channel
        self.cluster_channel = grpc.insecure_channel(
            '{}:{}'.format(self.cluster_ip, self.cluster_port))

        # bind the client to the server channel
        self.cluster_stub = cluster_pb2_grpc.ClusterServiceStub(self.cluster_channel)

    def FileDelete(self, filename, username):
        leader_response = self.cluster_stub.getLeader(cluster_pb2.getLeaderRequest())
        leader_channel = grpc.insecure_channel(
            '{}:{}'.format(leader_response.ip, leader_response.port))

        leader_stub = fileservice_pb2_grpc.FileserviceStub(leader_channel)
        Logger.info(f'Starting to delete the file...')
        request = fileservice_pb2.FileInfo()
        request.filename = filename
        request.user_info.username =username
        response = leader_stub.FileDelete(request)
        Logger.info(f'File deleted')
        return response

    def UploadFile(self, _file, username):
        """
        Client function to call the rpc for uploading a file, gets the leader from cluster_server then uploads the file to it
        """
        leader_response = self.cluster_stub.getLeader(cluster_pb2.getLeaderRequest())
        leader_channel = grpc.insecure_channel(
            '{}:{}'.format(leader_response.ip, leader_response.port))
        # cluster_channel = grpc.insecure_channel("192.168.0.9:9000")
        leader_stub = fileservice_pb2_grpc.FileserviceStub(leader_channel)
        Logger.info(f'Starting to stream the file...')
        chunk_iterator = FileHandler.chunk_bytes(_file, username, fileservice_pb2)
        response = leader_stub.UploadFile(chunk_iterator)
        Logger.info(f'File Uploaded. Response {response}')

        return response

    def DownloadFile(self, _file, username):
        # get read node from cluster server
        read_node = self.cluster_stub.getReadNode(cluster_pb2.getReadNodeRequest())
        read_node_channel = grpc.insecure_channel(
            '{}:{}'.format(read_node.ip, read_node.port))
        # cluster_channel = grpc.insecure_channel("192.168.0.9:9000")

        read_node_stub = fileservice_pb2_grpc.FileserviceStub(read_node_channel)
        Logger.info(f'Starting to Download the file...')
        request = fileservice_pb2.FileInfo()
        request.user_info.username = username
        request.filename = _file
        # Check for the destination file
        destination_path = f"download_data/{username}/"
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        f = open(f"{destination_path}/{_file}", 'bw+')
        read_node_stub.DownloadFile(request)
        try:

            for response in read_node_stub.DownloadFile(request):
                chunk = response.data
                f.write(chunk)
        except grpc.RpcError as err:
            Logger.warning(f"GRPC error. {err}")
        f.close()
        Logger.info(f'Downloading the file is complete...')

    def FileSearch(self, username, _file):
        read_node = self.cluster_stub.getReadNode(cluster_pb2.getReadNodeRequest())
        read_node_channel = grpc.insecure_channel(
            '{}:{}'.format(read_node.ip, read_node.port))

        read_node_stub = fileservice_pb2_grpc.FileserviceStub(read_node_channel)

        Logger.info(f'Searching if the file exists...')
        request = fileservice_pb2.FileInfo()
        request.user_info.username = username
        request.filename = _file
        response = read_node_stub.FileSearch(request)
        Logger.info(f'File search complete...')
        return response

    def FileList(self, username):
        read_node = self.cluster_stub.getReadNode(cluster_pb2.getReadNodeRequest())
        read_node_channel = grpc.insecure_channel(
            '{}:{}'.format(read_node.ip, read_node.port))

        read_node_stub = fileservice_pb2_grpc.FileserviceStub(read_node_channel)

        request = fileservice_pb2.UserInfo()
        request.username = username
        response = read_node_stub.FileList(request)
        return response

    def UsersList(self):
        read_node = self.cluster_stub.getReadNode(cluster_pb2.getReadNodeRequest())
        read_node_channel = grpc.insecure_channel(
            '{}:{}'.format(read_node.ip, read_node.port))

        read_node_stub = fileservice_pb2_grpc.FileserviceStub(read_node_channel)

        request = fileservice_pb2.UsersRequest()
        response = read_node_stub.GetUsers(request)
        return response

if __name__ == '__main__':
    curr_client = FileClient()

    # curr_client.UploadFile('/Users/sajan/Downloads/myfile.txt', 'sajan')
    curr_client.DownloadFile('myfile.txt', 'sajan')
    # read_node_channel = grpc.insecure_channel('192.168.0.9:9000')
    #
    # read_node_stub = fileservice_pb2_grpc.FileServiceStub(read_node_channel)
    # read_node_stub.UploadFile(fileservice_pb2.ClusterInfo(ip=str(121211212), port=str(43343), clusterName="easy_money"))
    #
    #curr_client.UploadFile('1', 'ben')
    #curr_client.UploadFile('1', 'prabaniy')
    #curr_client.UploadFile('1_2', 'ben')
    #curr_client.UploadFile('1_2', 'prabaniy')
    #curr_client.DownloadFile("1_2", "ben")
    #print(curr_client.UsersList())
    #print(curr_client.FileList('prabaniy'))
    #print(curr_client.FileSearch('prabaniy', '1_2'))
    #curr_client.FileDelete('1', 'ben')