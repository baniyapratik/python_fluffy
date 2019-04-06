import os
import math
from tqdm import tqdm
import grpc
from utils.logger import Logger
from utils import FileHandler
import utils.FileHandler as file_handler
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50051
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
        self.host = 'localhost'
        self.server_port = SERVER_PORT

        # instantiate a communication channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client to the server channel
        self.stub = fileservice_pb2_grpc.FileServiceStub(self.channel)

    def FileDelete(self, filename, username):
        Logger.info(f'Starting to delete the file...')
        request = fileservice_pb2.FileInfo()
        request.filename = filename
        request.user_info.username =username
        response = self.stub.FileDelete(request)
        Logger.info(f'File deleted')
        return response

    def UploadFile(self, _file, username):
        """
        Client function to call the rpc for GetDigest
        """
        Logger.info(f'Starting to stream the file...')
        chunk_iterator = FileHandler.chunk_bytes(_file, username, fileservice_pb2)
        response = self.stub.UploadFile(chunk_iterator)
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
    curr_client.UploadFile('1', 'prabaniy')
    print(curr_client.FileList('prabaniy'))
    #print(curr_client.FileSearch('prabaniy', 'sample_data.txt'))
    #curr_client.FileDelete('username', 'filename')