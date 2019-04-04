import grpc
import time
from concurrent import futures
from file_service import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50051


class FileUploadImplementation(fileservice_pb2_grpc.FilePostServiceServicer):

    def __init__(self, db=None):
        self.db = db

    def UploadFile(self, request, context):
        leader_address= '127.0.0.1'
        leader_port = '50051'

        user_name = request.username
        file_name = request.fileName
        data = request.data


        # save the file in mongo
        response = fileservice_pb2.ack()
        response.success = True
        response.message = file_name



def start_server():
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # server that can handle multiple requests, defining our threadpool
        file_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # adding the services that this server can serve
        #fileservice_pb2_grpc.add_FileGetServiceServicer_to_server(FileServer(), file_server)
        fileservice_pb2_grpc.add_FilePostServiceServicer_to_server(FileUploadImplementation(), file_server)

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
    file_server = FileServerImplementation(mg)
    file_server.start_server()