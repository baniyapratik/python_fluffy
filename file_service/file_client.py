import grpc
from  file_service import fileservice_pb2, fileservice_pb2_grpc

SERVER_PORT = 50051

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
        self.stub = fileservice_pb2_grpc.FilePostServiceStub(self.channel)

    def file_upload_chunk(self, file_path):

            import os
            if os.path.exists(file_path):

                print("Sending... Chunk: ", chunk_num, ", Seq: ", cur_seq_num)
                yield request

    def upload_files(self, file_path, file_name):
        """
        Client function to call the rpc for GetDigest
        """
        with grpc.insecure_channel(self.host + ':' + self.server_port) as channel:
            self.stub.UploadFile(self.file_upload_chunk(file_path))


if __name__ == '__main__':
    curr_client = FileClient()