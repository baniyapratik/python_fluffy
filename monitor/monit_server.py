import grpc
import time
import psutil
from utils.logger import Logger
from concurrent import futures
from monitor.proto import hearbeat_pb2_grpc, hearbeat_pb2

CPU_MAX = 20
SERVER_PORT = '50052'


class HeartBeatImplementation(hearbeat_pb2_grpc.HearBeatServiceServicer):
    '''
    This is the class for sending the heartbeat stats
    '''
    def update_warning(self, cpu_data):
        if cpu_data > CPU_MAX:
            return "high"
        else:
            return "normal"

    def isAlive(self, request, context):
        Logger.info(f"isAlive Request received.")

        cpu_data = psutil.cpu_percent()
        cpu_usage = self.update_warning(cpu_data)
        if cpu_usage == "high":
            Logger.warning(f"CPU Usage is High. {cpu_data}%")
        memory_swap_data = psutil.swap_memory().percent
        disk_available_data = psutil.swap_memory().percent

        response =  hearbeat_pb2.Stats(cpu_data=str(cpu_data), cpu_usage=str(cpu_usage),
                                       disk_space=str(disk_available_data), used_mem=str(memory_swap_data))
        Logger.info(f'is Alive Response. Stats: {response}')
        return response

    def start_server(self):
        heartbeat_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

        # our heartbeat service
        hearbeat_pb2_grpc.add_HearBeatServiceServicer_to_server(HeartBeatImplementation(), heartbeat_server)

        # bind the server to the described port
        heartbeat_server.add_insecure_port(f'[::]:{SERVER_PORT}')

        # start the server
        heartbeat_server.start()

        Logger.info(f'File Server running on port {SERVER_PORT}...')

        try:
            # Keep the program running unless keyboard interruption
            while True:
                time.sleep(60 * 60 * 60)
        except KeyboardInterrupt:
            heartbeat_server.stop(0)
            Logger.info('Heart beat Server Stopped ...')


if __name__ == "__main__":
    hear_beat_server = HeartBeatImplementation()
    hear_beat_server.start_server()