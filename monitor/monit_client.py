import grpc
from utils.logger import Logger
from monitor.proto import hearbeat_pb2_grpc, hearbeat_pb2

SERVER_PORT = 50052


class HeartbeatClient():
    def __init__(self):
        self.host = 'localhost'
        self.port = SERVER_PORT
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = hearbeat_pb2_grpc.HearBeatServiceStub(self.channel)

    def send_isalive(self, dest_ip, dest_port):
        Logger.info(f'Sending HeartBeat Request...')
        isalive = hearbeat_pb2.NodeInfo(
            ip = dest_ip, port = dest_port
        )
        try:
            response = self.stub.isAlive(isalive)
        except:
            response = None
        Logger.info(f'Heartbeat response is: {response}')
        return response


if __name__ == "__main__":
    heart_beat_client = HeartbeatClient()
    heart_beat_client.send_isalive(dest_ip='localhost', dest_port='50052')