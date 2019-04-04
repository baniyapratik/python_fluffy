import os
import math
from tqdm import tqdm
import grpc
from utils.logger import Logger
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

    def FileDelete(self, username, filename):
        request = fileservice_pb2.FileInfo()
        request.filename = "filename"
        request.user_info.username = 'prabaniy'
        self.stub.FileDelete(request)

    def UploadFile(self, _file):
        """
        Client function to call the rpc for GetDigest
        """
        Logger.info(f'Starting to stream the file...')
        chunk_iterator = self.chunk_bytes(_file)
        response = self.stub.UploadFile(chunk_iterator)
        Logger.info(f'File Uploaded. Response {response}')
        return response

    def fileExists(self, file_path):
        if os.path.exists(file_path):
            return True
        return False

    def get_file_size(self, file_path):
        if self.fileExists(file_path):
            file_size = os.path.getsize(file_path)
            Logger.info(f"File size is {file_size}")
            return file_size

    def chunk_bytes(self, _file):
        """Yield successive n-sized chunks"""
        # File size in megabytes
        _file_len = self.get_file_size(_file)
        print(f"{_file_len}")

        with open(_file, 'rb') as _file:
            if _file_len > THRESHHOLD:
                chunk_size = CHUNK_SIZE
                total_chunks = math.ceil(_file_len / chunk_size)
                index = 0
                for i in tqdm(range(0, total_chunks)):
                    _file.seek(index)
                    chunk = _file.read(index + chunk_size)
                    yield fileservice_pb2.FileData(username='ben', filename='_file', data=chunk)

                    index += chunk_size
            else:
                chunk = _file.read()
                yield fileservice_pb2.FileData(username='prabaniy',
                                               filename='_file.txt',
                                               data=chunk)

    def file_iterator(_file, index, chunk_size):
        yield _file.read(index + chunk_size)





if __name__ == '__main__':
    curr_client = FileClient()
    curr_client.UploadFile('/Users/prabaniy/Downloads/sample_data.txt')
    #curr_client.FileDelete('username', 'filename')