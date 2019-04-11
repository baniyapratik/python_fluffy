import os
import math
from tqdm import tqdm
from utils.logger import Logger

CHUNK_SIZE = 4*1024
THRESHHOLD = 4000000


def fileExists(file_path):
    '''
    Check if a file exists
    '''
    if os.path.exists(file_path):
        return True
    return False


def get_file_size(file_path):
    '''
    Get the size of the file
    '''
    if fileExists(file_path):
        file_size = os.path.getsize(file_path)
        Logger.info(f"File size is {file_size}")
        return file_size


def chunk_bytes(_file, username, fileservice_pb2):
        """Yield successive n-sized chunks"""
        # File size in megabytes
        _file_len = get_file_size(_file)
        Logger.info(f"File is  {_file}")
        print(f"{_file_len}")
        filename = os.path.split(_file)[-1]
        with open(_file, 'rb') as _file:
            if _file_len > THRESHHOLD:
                chunk_size = CHUNK_SIZE
                total_chunks = math.ceil(_file_len / chunk_size)
                index = 0
                for i in tqdm(range(0, total_chunks)):
                    _file.seek(index)
                    chunk = _file.read(chunk_size)
                    yield fileservice_pb2.FileData(username=username, filename=filename, data=chunk)

                    index += chunk_size
            else:
                chunk = _file.read()
                yield fileservice_pb2.FileData(username=username,
                                               filename=filename,
                                               data=chunk)