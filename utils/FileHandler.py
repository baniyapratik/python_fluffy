import os
import math
import itertools
from tqdm import tqdm
from utils.logger import Logger


def fileExists(file_path):
    if os.path.exists(file_path):
        return True
    return False


def get_file_size(file_path):
    if fileExists(file_path):
        file_size = os.path.getsize(file_path)
        Logger.info(f"File size is {file_size}")
        return file_size


def chunk_bytes(_file):
    """Yield successive n-sized chunks"""
    # File size in megabytes
    _file_len = get_file_size(_file)
    with open(_file, 'rb') as _file:
        if _file_len > 4000000:
            chunk_size = 4
            total_chunks = math.ceil(_file_len/chunk_size)
            index = 0
            for i in tqdm(range(0, total_chunks, chunk_size)):
                _file.seek(index)
                yield (_file.read(index+chunk_size))
                index += chunk_size
        else:

            yield _file.read()

data = next(chunk_bytes(_file='/Users/prabaniy/Downloads/ECN2k18-183of213.jpg'))



