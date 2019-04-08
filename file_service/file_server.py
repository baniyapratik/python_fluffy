import os
import grpc
import time
import math
import sys
import psutil
import ast
from tqdm import tqdm
from utils import FileHandler
from utils.logger import Logger
from concurrent import futures
from threading import Thread
from file_service.proto import fileservice_pb2, fileservice_pb2_grpc
from cluster.proto import cluster_pb2, cluster_pb2_grpc
import json

SERVER_PORT = 50051
CHUNK_SIZE = 4*1024
THRESHHOLD = 3500000

class FileServiceImplementation(fileservice_pb2_grpc.FileServiceServicer):

    def __init__(self, port, cluster_server_ip, cluster_server_port):
        self.ip = "localhost"
        self.port = port
        self.cluster_server_stub = cluster_pb2_grpc.ClusterServiceStub(grpc.insecure_channel(f'{cluster_server_ip}:{cluster_server_port}'))

    def ReplicateFile(self, request_iterator, context):
        Logger.info(f"Replicate request received. {self.port}")
        f = None
        destination_path = None
        temp_file = None
        file_name = None
        try:
            for request in request_iterator:
                if f is None:
                    file_name = request.filename
                    destination_path = f"file_data_{self.port}/{request.username}"
                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)
                    temp_file = f"{destination_path}/replicate_{file_name}"
                    Logger.info("Create temp file " + temp_file)
                    f = open(temp_file, 'bw+')
                chunk = request.data
                f.write(chunk)

        finally:
            if f is not None:
                f.close()


        os.system(f"mv {temp_file} {destination_path}/{file_name}")
        return fileservice_pb2.ack(success=True, message="File Uploaded")

    def FileSearch(self, request, context):
        Logger.info("File search request received.")
        username = request.user_info.username
        filename = request.filename

        file_path = f"file_data_{self.port}/{username}/{filename}"
        if os.path.exists(file_path):
            Logger.info("File search request complete.")
            return fileservice_pb2.ack(success=True, message=f"{filename} File exists")
        else:
            Logger.info("File search request complete.")
            return fileservice_pb2.ack(success=False, message="File does not exists")

    def FileList(self, request, context):
        Logger.info("File list request received.")
        username = request.username
        directory_path = f"file_data_{self.port}/{username}"
        onlyfiles = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        print(onlyfiles)
        Logger.info("File list request complete.")
        return fileservice_pb2.FileListResponse(filenames=str(onlyfiles))

    def GetUsers(self, request, context):
        Logger.info("Users request received.")
        directory_path = f"file_data_{self.port}"
        if os.path.exists(directory_path):
            # get list of directories in top level folder which is simply the list of user names as each user has own directory
            users = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) is False]
            print(users)
            Logger.info("Users request complete.")
        else:
            users = []
        return fileservice_pb2.UsersResponse(users_list=str(users))

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
        neighbors = self.get_neighbors()
        print(neighbors)
        for neighbor in neighbors:
            neighbor_ip = neighbor.nodeInfo.ip
            neighbor_port = neighbor.nodeInfo.port
            is_alive = neighbor.isAlive
            if neighbor_port != self.port and is_alive == 'True':
                # instantiate a communication channel
                channel = grpc.insecure_channel(
                    '{}:{}'.format(neighbor_ip, neighbor_port))

                # bind the client to the server channel
                stub = fileservice_pb2_grpc.FileServiceStub(channel)
                Logger.info("ready for chunking to replicate")

                print("About to chunk")
                chunk_iterator = FileHandler.chunk_bytes(destination_path, user_name, fileservice_pb2)

                Logger.info("Sending " + destination_path + " to " + neighbor_ip + ":" + neighbor_port)
                stub.ReplicateFile(chunk_iterator)
                Logger.info("Files Replicated")

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
        neighbors = self.get_neighbors()
        for neighbor in neighbors:
            neighbor_ip = neighbor.nodeInfo.ip
            neighbor_port = neighbor.nodeInfo.port
            if int(neighbor_port) != self.port and neighbor.isAlive:
                # instantiate a communication channel
                channel = grpc.insecure_channel(
                    '{}:{}'.format(neighbor_ip, neighbor_port))
                # bind the client to the server channel
                stub = fileservice_pb2_grpc.FileServiceStub(channel)
                Logger.info("ready to delete from replicate")
                request = fileservice_pb2.FileInfo()
                request.user_info.username = user_name
                request.filename = filename
                stub.FileDelete(request)
                Logger.info("Files Deleted from Nodes.")

    def get_neighbors(self):
        # obtain list of neighbors from cluster_server
        neighbors = self.cluster_server_stub.getNeighbors(cluster_pb2.getNeighborRequest())
        return neighbors.nodes

    def DownloadFile(self, request, context):
        username = request.user_info.username
        filename = request.filename
        Logger.info(f"Download request received from {username}.")

        destination_path = f"file_data_{self.port}/{username}/{filename}"
        if not os.path.exists(destination_path):
            raise RuntimeError("File does not exist")
        else:
            Logger.info(f"Starting chunking.")
            _file_len = FileHandler.get_file_size(destination_path)
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

    def Heartbeat(self, request, context):
        Logger.info("got heartbeat")
        return fileservice_pb2.HeartbeatResponse(response="ok")

    def Stats(self, request, context):
        cpu_data = psutil.cpu_percent()
        swap_memory_data = psutil.swap_memory().percent
        return fileservice_pb2.StatsResponse(cpuutil=cpu_data, swap_memory=swap_memory_data)

    def initiate_data(self):
        # get read_node to get files from
        read_node = self.cluster_server_stub.getReadNode(cluster_pb2.getReadNodeRequest())

        if read_node.ip != "-1":
            # nodes exist, so get list of users

            read_node_channel = grpc.insecure_channel(
                '{}:{}'.format(read_node.ip, read_node.port))
            read_node_stub = fileservice_pb2_grpc.FileServiceStub(read_node_channel)

            users = read_node_stub.GetUsers(fileservice_pb2.UsersRequest())
            users_list = ast.literal_eval(users.users_list)
            print(users_list)

            # get uploaded files node may have missed out on from other nodes, also delete old files node may have
            for user in users_list:
                # obtain list of files for user
                users_files = read_node_stub.FileList(fileservice_pb2.UserInfo(username=user))
                print(users_files)
                users_files_list = ast.literal_eval(users_files.filenames)
                destination_path = f"file_data_{self.port}/{user}"
                # download needed files
                for users_file in users_files_list:
                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)

                    f = open(f"{destination_path}/{users_file}", 'bw+')
                    try:
                        for response in read_node_stub.DownloadFile(fileservice_pb2.FileInfo(user_info=fileservice_pb2.UserInfo(username=user), filename=users_file)):
                            chunk = response.data
                            f.write(chunk)
                    except grpc.RpcError as err:
                        Logger.warning(f"GRPC error. {err}")
                    f.close()

                # remove old file not found on neighbor node
                if os.path.exists(destination_path):
                    for filename in os.listdir(destination_path):
                        if filename not in users_files_list:
                            os.remove(f"{destination_path}/{filename}")



    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # server that can handle multiple requests, defining our threadpool
        file_server = grpc.server(futures.ThreadPoolExecutor(max_workers=100), options=(('grpc.max_message_length', 50 * 1024 * 1024,),('grpc.max_receive_message_length', 50 * 1024 * 1024)))

        # adding the services that this server can serve
        fileservice_pb2_grpc.add_FileServiceServicer_to_server(self, file_server)

        # bind the server to the described port
        file_server.add_insecure_port('[::]:{}'.format(self.port))

        # start the server
        file_server.start()
        node_message = cluster_pb2.Node(ip=self.ip, port=str(self.port))

        self.initiate_data()
        # try to initiate itself as leader
        leader_response = self.cluster_server_stub.leader_initiate(node_message)
        print(self.cluster_server_stub.getNeighbors(cluster_pb2.getNeighborRequest()))
        if not leader_response.success:
            # if node is not able to add itself as leader simply add itself as a neighbor to cluster_server
            self.cluster_server_stub.add_neighbor(node_message)

        print(f'File Server running on port {self.port}...\n')

        try:
            # Keep the program running unless keyboard interruption
            while True:
                time.sleep(60 * 60 * 60)
        except KeyboardInterrupt:
            file_server.stop(0)
            print('File Server Stopped ...')

if __name__ == '__main__':
    # argument 1: port node runs on
    # argument 2: ip cluster_server runs on
    # argument 3: port cluster_server runs on
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    file_server = FileServiceImplementation(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    file_server.start_server()
