import os
import grpc
import time
from tqdm import tqdm
import math
from utils import FileHandler
from utils.logger import Logger
from concurrent import futures
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50051
CHUNK_SIZE = 4*1024
THRESHHOLD = 3500000

def call_neghbor():
    return [
        {
            "ip": "127.0.0.1",
            "port": 50052,
        },
        {
            "ip": "127.0.0.1",
            "port": 50053
        }
    ]


class FileServiceImplementation(fileservice_pb2_grpc.FileServiceServicer):

    def __init__(self, port):
        self.port = port

    def ReplicateFile(self, request_iterator, context):
        Logger.info(f"Replicate request received. {self.port}")
        temp_file = f"replicate_{self.port}"
        Logger.info("Create temp file " + temp_file)
        f = open(temp_file, 'bw+')
        try:
            for request in request_iterator:
                user_name = request.username
                file_name = request.filename
                chunk = request.data
                f.write(chunk)

        finally:
            f.close()

        destination_path = f"file_data_{self.port}/{user_name}"
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        os.system(f"mv {temp_file} {destination_path}/{file_name}")
        return fileservice_pb2.ack(success=True, message="File Uploaded")


    def UploadFile(self, request_iterator, context):
        Logger.info("Upload request received.")
        temp_file = "temp"
        f = open(temp_file, 'bw+')
        try:
            for request in request_iterator:
                    user_name = request.username
                    file_name = request.filename
                    chunk = request.data
                    f.write(chunk)
        finally:
            f.close()

        destination_path = f"file_data_{self.port}/{user_name}"
        destination_file_path = f"{destination_path}/{file_name}"
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        os.system(f"mv {temp_file} {destination_path}/{file_name}")

        # After the file is saved send it to the neigbors
        Logger.info("Spawn thread to send " + destination_file_path + " to neighbors")
        Thread(target=self.replicate_to_neighbor, args=(destination_file_path, user_name)).start()

        Logger.info("File Upload Request Complete.")
        return fileservice_pb2.ack(success=True, message="File Uploaded")

    def replicate_to_neighbor(self, destination_path, user_name):
        Logger.info("Replicating the file")
        neighbors = call_neghbor()
        for neighbor in neighbors:
            # instantiate a communication channel
            channel = grpc.insecure_channel(
                '{}:{}'.format(neighbor['ip'], neighbor['port']))

            # bind the client to the server channel
            stub = fileservice_pb2_grpc.FileServiceStub(channel)
            Logger.info("ready for chunking to replicate")

            print("About to chunk")
            chunk_iterator = self.chunk_bytes(destination_path, user_name)

            Logger.info("Sending " + destination_path + " to " + neighbor['ip'] + ":" + str(neighbor['port']))
            stub.ReplicateFile(chunk_iterator)
            Logger.info("Files Replicated")

    def fileExists(self, file_path):
        if os.path.exists(file_path):
            return True
        return False

    def get_file_size(self, file_path):
        if self.fileExists(file_path):
            file_size = os.path.getsize(file_path)
            Logger.info(f"File size is {file_size}")
            return file_size

    def chunk_bytes(self, _file, username):
        """Yield successive n-sized chunks"""
        # File size in megabytes
        _file_len = self.get_file_size(_file)
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

    def FileDelete(self, request, context):
        Logger.info("Delete request received.")
        username = request.user_info.username
        filename = request.filename
        destination_path = f"file_data_{self.port}/{username}/{filename}"
        Logger.info(f"File to be deleted: {destination_path}")
        if not os.path.exists(destination_path):
            raise RuntimeError("File does not exist to delete")
        os.remove(destination_path)

        Thread(target=self.delete_from_neighbor, args=(filename, username)).start()

        Logger.info("File deleted")
        return fileservice_pb2.ack(success=True, message="File Deleted")

    def delete_from_neighbor(self, filename, user_name):
        Logger.info("Deleting the file from neighbors")
        neighbors = call_neghbor()
        for neighbor in neighbors:
            # instantiate a communication channel
            channel = grpc.insecure_channel(
                '{}:{}'.format(neighbor['ip'], neighbor['port']))
            # bind the client to the server channel
            stub = fileservice_pb2_grpc.FileServiceStub(channel)
            Logger.info("ready to delete from replicate")
            request = fileservice_pb2.FileInfo()
            request.user_info.username = user_name
            request.filename = filename
            stub.FileDelete(request)
            Logger.info("Files Deleted from Nodes.")


    def DownloadFile(self, request, context):
        username = request.user_info.username
        filename = request.filename
        Logger.info(f"Download request received from {username}.")

        destination_path = f"file_data_{self.port}/{username}/{filename}"
        if not os.path.exists(destination_path):
            raise RuntimeError("File does not exist")
        else:
            Logger.info(f"Starting chunking.")
            _file_len = self.get_file_size(destination_path)
            Logger.info(f"File is  {destination_path}")
            print(f"{_file_len}")
            filename = os.path.split(destination_path)[-1]

            with open(destination_path, 'rb') as _file:
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
        Logger.info(f"Chunking complete")

    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # server that can handle multiple requests, defining our threadpool
        file_server = grpc.server(futures.ThreadPoolExecutor(max_workers=100), options=(('grpc.max_message_length', 50 * 1024 * 1024,),('grpc.max_receive_message_length', 50 * 1024 * 1024)))

        # adding the services that this server can serve
        fileservice_pb2_grpc.add_FileServiceServicer_to_server(FileServiceImplementation(self.port), file_server)

        # bind the server to the described port
        file_server.add_insecure_port('[::]:{}'.format(self.port))

        # start the server
        file_server.start()

        print(f'File Server running on port {self.port}...')

        try:
            # Keep the program running unless keyboard interruption
            while True:
                time.sleep(60 * 60 * 60)
        except KeyboardInterrupt:
            file_server.stop(0)
            print('File Server Stopped ...')

if __name__ == '__main__':

    file_server_1 = FileServiceImplementation(50051)
    #file_server_1.start_server()
    file_server_2 = FileServiceImplementation(50052)
    #file_server_2.start_server()
    file_server_3 = FileServiceImplementation(50053)
    #file_server_3.start_server()
    from threading import Thread

    thread_1 = Thread(target=file_server_1.start_server)
    thread_2 = Thread(target=file_server_2.start_server)
    thread_3 = Thread(target=file_server_3.start_server)

    thread_1.start()
    thread_3.start()
    thread_2.start()