import os
import math
from tqdm import tqdm
import grpc
from utils.logger import Logger
import utils.FileHandler as file_handler
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50051
CHUNK_SIZE = 4*1024
THRESHHOLD = 4000000

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


    def uploadFiles(self, _file):
        """
        Client function to call the rpc for GetDigest
        """
        Logger.info(f'Starting to stream the file...')
        response = next(self.chunk_bytes(_file))
        return response

    def chunk_bytes(self, _file):
        """Yield successive n-sized chunks"""
        # File size in megabytes
        _file_len = self.get_file_size(_file)
        print("doing something ")
        with open(_file, 'rb') as _file:
            if _file_len > THRESHHOLD:
                chunk_size = CHUNK_SIZE
                total_chunks = math.ceil(_file_len / chunk_size)
                index = 0
                for i in tqdm(range(0, total_chunks, chunk_size)):
                    _file.seek(index)
                    print("doing something ")
                    yield self.stub.UploadFile(fileservice_pb2.FileData(username='prabaniy',
                                                                 filename='_file.txt',
                                                                 data=_file.read(index + chunk_size)))
                    index += chunk_size
                    print("Done")
            else:
                yield self.stub.UploadFile(fileservice_pb2.FileData(username='prabaniy',
                                                                 filename='_file.txt',
                                                                 data=_file.read()))

    def fileExists(self, file_path):
        if os.path.exists(file_path):
            return True
        return False

    def get_file_size(self, file_path):
        if self.fileExists(file_path):
            file_size = os.path.getsize(file_path)
            Logger.info(f"File size is {file_size}")

            return file_size
if __name__ == '__main__':
    curr_client = FileClient()
    curr_client.uploadFiles('/Users/prabaniy/Downloads/ECN2k18-183of213.jpg')