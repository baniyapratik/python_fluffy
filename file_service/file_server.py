import grpc
import time
from utils.logger import Logger
from concurrent import futures
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50051


class FileServiceImplementation(fileservice_pb2_grpc.FileServiceServicer):

    def __init__(self, db=None):
        self.db = db

    def UploadFile(self, chunk_iterator, context):
        print('hello')
        for chunk in chunk_iterator:
            user_name = chunk.username
            file_name = chunk.filename
            print(chunk.data)
        return fileservice_pb2.ack(success=True, message="received")

    def fileExists(file_path):
        if os.path.exists(file_path):
            return True
        return False

    def get_file_size(file_path):
        if fileExists(file_path):
            file_size = os.path.getsize(file_path)
            Logger.info(f"File size is {file_size}")
            return file_size

    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # server that can handle multiple requests, defining our threadpool
        file_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # adding the services that this server can serve
        fileservice_pb2_grpc.add_FileServiceServicer_to_server(FileServiceImplementation(), file_server)

        # bind the server to the described port
        file_server.add_insecure_port('[::]:{}'.format(SERVER_PORT))

        # start the server
        file_server.start()

        print(f'File Server running on port {SERVER_PORT}...')

        try:
            # Keep the program running unless keyboard interruption
            while True:
                time.sleep(60 * 60 * 60)
        except KeyboardInterrupt:
            file_server.stop(0)
            print('File Server Stopped ...')

if __name__ == '__main__':
    from database import mg
    mg.init_app()
    file_server = FileServiceImplementation(mg)
    file_server.start_server()