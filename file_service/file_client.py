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

        # instantiate a communication channel
        self.cluster_channel = grpc.insecure_channel(
            '{}:{}'.format(self.cluster_ip, self.cluster_port))

        # bind the client to the server channel
        self.cluster_stub = cluster_pb2_grpc.ClusterServiceStub(self.cluster_channel)

    def FileDelete(self, filename, username):
        leader_response = self.cluster_stub.getLeader(cluster_pb2.getLeaderRequest())
        leader_channel = grpc.insecure_channel(
            '{}:{}'.format(leader_response.ip, leader_response.port))

        leader_stub = fileservice_pb2_grpc.FileServiceStub(leader_channel)
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

        leader_stub = fileservice_pb2_grpc.FileServiceStub(leader_channel)
        Logger.info(f'Starting to stream the file...')
        chunk_iterator = FileHandler.chunk_bytes(_file, username, fileservice_pb2)
        response = leader_stub.UploadFile(chunk_iterator)
        Logger.info(f'File Uploaded. Response {response}')

        return response

    def DownloadFile(self, _file, username):
        Logger.info(f'Starting to Download the file...')
        request = fileservice_pb2.FileInfo()
        request.user_info.username = username
        request.filename = _file
        # Check for the destination file
        destination_path = f"download_data_{self.server_port}/{username}"
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        f = open(f"{destination_path}/{_file}", 'bw+')
        self.stub.DownloadFile(request)
        try:

            for response in self.stub.DownloadFile(request):
                chunk = response.data
                f.write(chunk)
        except grpc.RpcError as err:
            Logger.warning(f"GRPC error. {err}")
        f.close()
        Logger.info(f'Downloading the file is complete...')

    def FileSearch(self, username, _file):
        Logger.info(f'Searching if the file exists...')
        request = fileservice_pb2.FileInfo()
        request.user_info.username = username
        request.filename = _file
        response = self.stub.FileSearch(request)
        Logger.info(f'File search complete...')
        return response

    def FileList(self, username):
        request = fileservice_pb2.UserInfo()
        request.username = username
        response = self.stub.FileList(request)
        return response

if __name__ == '__main__':
    curr_client = FileClient()
    #curr_client.UploadFile('1', 'ben')
    #curr_client.UploadFile('1', 'prabaniy')
    #curr_client.UploadFile('1_2', 'ben')
    #curr_client.UploadFile('1_2', 'prabaniy')
    #print(curr_client.FileList('prabaniy'))
    #print(curr_client.FileSearch('prabaniy', 'sample_data.txt'))
    curr_client.FileDelete('1', 'ben')