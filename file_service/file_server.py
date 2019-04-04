import grpc
import time
from utils.logger import Logger
from concurrent import futures
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50051


class FileServiceImplementation(fileservice_pb2_grpc.FileServiceServicer):

    def __init__(self, db=None):
        self.db = db

    def UploadFile(self, request_iterator, context):
        Logger.info("Upload request received.")
        for request in request_iterator:
            user_name = request.username
            file_name = request.filename
            chunk = request.data
        Logger.info("File Upload Request Complete.")
        return fileservice_pb2.ack(success=True, message="File Uploaded")

    def FileDelete(self, request, context):
        Logger.info("Delete request received.")
        username = request.username
        filename = request.filename


    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # server that can handle multiple requests, defining our threadpool
        file_server = grpc.server(futures.ThreadPoolExecutor(max_workers=100), options=(('grpc.max_message_length', 50 * 1024 * 1024,),('grpc.max_receive_message_length', 50 * 1024 * 1024)))

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