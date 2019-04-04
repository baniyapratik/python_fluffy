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


def uploadFiles(stub, _file):
    """
    Client function to call the rpc for GetDigest
    """
    Logger.info(f'Starting to stream the file...')
    chunk_iterator = chunk_bytes(_file)
    response = stub.UploadFile(chunk_iterator)
    return response


def chunk_bytes(_file):
    """Yield successive n-sized chunks"""
    # File size in megabytes
    _file_len = get_file_size(_file)
    print("doing something ")
    with open(_file, 'rb') as _file:
        if _file_len > THRESHHOLD:
            chunk_size = CHUNK_SIZE
            total_chunks = math.ceil(_file_len / chunk_size)
            index = 0
            for i in tqdm(range(0, _file_len, chunk_size)):
                _file.seek(index)
                print("doing something ")
                chunk = _file.read(index + chunk_size)
                file_data = fileservice_pb2.FileData(username='ben', filename='_file', data=chunk)
                print(file_data)
                yield file_data
                index += chunk_size
                print("Done")
        else:
            chunk = _file.read()
            yield fileservice_pb2.FileData(username='prabaniy',
                                                             filename='_file.txt',
                                                             data=chunk)

def fileExists(file_path):
    if os.path.exists(file_path):
        return True
    return False

def get_file_size(file_path):
    if fileExists(file_path):
        file_size = os.path.getsize(file_path)
        Logger.info(f"File size is {file_size}")
        return file_size

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = fileservice_pb2_grpc.FileServiceStub(channel)
        uploadFiles(stub, '1')