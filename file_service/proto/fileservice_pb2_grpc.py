# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from file_service.proto import fileservice_pb2 as fileService__pb2


class FileServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.DownloadFile = channel.unary_stream(
        '/fileservice.FileService/DownloadFile',
        request_serializer=fileService__pb2.FileInfo.SerializeToString,
        response_deserializer=fileService__pb2.FileData.FromString,
        )
    self.FileSearch = channel.unary_unary(
        '/fileservice.FileService/FileSearch',
        request_serializer=fileService__pb2.FileInfo.SerializeToString,
        response_deserializer=fileService__pb2.ack.FromString,
        )
    self.FileList = channel.unary_unary(
        '/fileservice.FileService/FileList',
        request_serializer=fileService__pb2.UserInfo.SerializeToString,
        response_deserializer=fileService__pb2.FileListResponse.FromString,
        )
    self.ReplicateFile = channel.stream_unary(
        '/fileservice.FileService/ReplicateFile',
        request_serializer=fileService__pb2.FileData.SerializeToString,
        response_deserializer=fileService__pb2.ack.FromString,
        )
    self.UploadFile = channel.stream_unary(
        '/fileservice.FileService/UploadFile',
        request_serializer=fileService__pb2.FileData.SerializeToString,
        response_deserializer=fileService__pb2.ack.FromString,
        )
    self.FileDelete = channel.unary_unary(
        '/fileservice.FileService/FileDelete',
        request_serializer=fileService__pb2.FileInfo.SerializeToString,
        response_deserializer=fileService__pb2.ack.FromString,
        )
    self.UpdateFile = channel.stream_unary(
        '/fileservice.FileService/UpdateFile',
        request_serializer=fileService__pb2.FileData.SerializeToString,
        response_deserializer=fileService__pb2.ack.FromString,
        )
    self.Heartbeat = channel.unary_unary(
        '/fileservice.FileService/Heartbeat',
        request_serializer=fileService__pb2.HeartbeatRequest.SerializeToString,
        response_deserializer=fileService__pb2.HeartbeatResponse.FromString,
        )
    self.Stats = channel.unary_unary(
        '/fileservice.FileService/Stats',
        request_serializer=fileService__pb2.StatsRequest.SerializeToString,
        response_deserializer=fileService__pb2.StatsResponse.FromString,
        )
    self.GetUsers = channel.unary_unary(
        '/fileservice.FileService/GetUsers',
        request_serializer=fileService__pb2.UsersRequest.SerializeToString,
        response_deserializer=fileService__pb2.UsersResponse.FromString,
        )
    self.getClusterStats = channel.unary_unary(
        '/fileservice.FileService/getClusterStats',
        request_serializer=fileService__pb2.Empty.SerializeToString,
        response_deserializer=fileService__pb2.ClusterStats.FromString,
        )
    self.getLeaderInfo = channel.unary_unary(
        '/fileservice.FileService/getLeaderInfo',
        request_serializer=fileService__pb2.ClusterInfo.SerializeToString,
        response_deserializer=fileService__pb2.ack.FromString,
        )


class FileServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def DownloadFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def FileSearch(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def FileList(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReplicateFile(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UploadFile(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def FileDelete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateFile(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Heartbeat(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Stats(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUsers(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getClusterStats(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getLeaderInfo(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_FileServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'DownloadFile': grpc.unary_stream_rpc_method_handler(
          servicer.DownloadFile,
          request_deserializer=fileService__pb2.FileInfo.FromString,
          response_serializer=fileService__pb2.FileData.SerializeToString,
      ),
      'FileSearch': grpc.unary_unary_rpc_method_handler(
          servicer.FileSearch,
          request_deserializer=fileService__pb2.FileInfo.FromString,
          response_serializer=fileService__pb2.ack.SerializeToString,
      ),
      'FileList': grpc.unary_unary_rpc_method_handler(
          servicer.FileList,
          request_deserializer=fileService__pb2.UserInfo.FromString,
          response_serializer=fileService__pb2.FileListResponse.SerializeToString,
      ),
      'ReplicateFile': grpc.stream_unary_rpc_method_handler(
          servicer.ReplicateFile,
          request_deserializer=fileService__pb2.FileData.FromString,
          response_serializer=fileService__pb2.ack.SerializeToString,
      ),
      'UploadFile': grpc.stream_unary_rpc_method_handler(
          servicer.UploadFile,
          request_deserializer=fileService__pb2.FileData.FromString,
          response_serializer=fileService__pb2.ack.SerializeToString,
      ),
      'FileDelete': grpc.unary_unary_rpc_method_handler(
          servicer.FileDelete,
          request_deserializer=fileService__pb2.FileInfo.FromString,
          response_serializer=fileService__pb2.ack.SerializeToString,
      ),
      'UpdateFile': grpc.stream_unary_rpc_method_handler(
          servicer.UpdateFile,
          request_deserializer=fileService__pb2.FileData.FromString,
          response_serializer=fileService__pb2.ack.SerializeToString,
      ),
      'Heartbeat': grpc.unary_unary_rpc_method_handler(
          servicer.Heartbeat,
          request_deserializer=fileService__pb2.HeartbeatRequest.FromString,
          response_serializer=fileService__pb2.HeartbeatResponse.SerializeToString,
      ),
      'Stats': grpc.unary_unary_rpc_method_handler(
          servicer.Stats,
          request_deserializer=fileService__pb2.StatsRequest.FromString,
          response_serializer=fileService__pb2.StatsResponse.SerializeToString,
      ),
      'GetUsers': grpc.unary_unary_rpc_method_handler(
          servicer.GetUsers,
          request_deserializer=fileService__pb2.UsersRequest.FromString,
          response_serializer=fileService__pb2.UsersResponse.SerializeToString,
      ),
      'getClusterStats': grpc.unary_unary_rpc_method_handler(
          servicer.getClusterStats,
          request_deserializer=fileService__pb2.Empty.FromString,
          response_serializer=fileService__pb2.ClusterStats.SerializeToString,
      ),
      'getLeaderInfo': grpc.unary_unary_rpc_method_handler(
          servicer.getLeaderInfo,
          request_deserializer=fileService__pb2.ClusterInfo.FromString,
          response_serializer=fileService__pb2.ack.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'fileservice.FileService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
