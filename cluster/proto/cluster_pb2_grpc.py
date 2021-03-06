# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from cluster.proto import cluster_pb2 as cluster__pb2


class ClusterServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.leader_initiate = channel.unary_unary(
        '/ClusterService/leader_initiate',
        request_serializer=cluster__pb2.Node.SerializeToString,
        response_deserializer=cluster__pb2.ackResponse.FromString,
        )
    self.add_neighbor = channel.unary_unary(
        '/ClusterService/add_neighbor',
        request_serializer=cluster__pb2.Node.SerializeToString,
        response_deserializer=cluster__pb2.ackResponse.FromString,
        )
    self.remove_neighbor = channel.unary_unary(
        '/ClusterService/remove_neighbor',
        request_serializer=cluster__pb2.Node.SerializeToString,
        response_deserializer=cluster__pb2.ackResponse.FromString,
        )
    self.getNeighbors = channel.unary_unary(
        '/ClusterService/getNeighbors',
        request_serializer=cluster__pb2.getNeighborRequest.SerializeToString,
        response_deserializer=cluster__pb2.getNeighborResponse.FromString,
        )
    self.getLeader = channel.unary_unary(
        '/ClusterService/getLeader',
        request_serializer=cluster__pb2.getLeaderRequest.SerializeToString,
        response_deserializer=cluster__pb2.Node.FromString,
        )


class ClusterServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def leader_initiate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def add_neighbor(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def remove_neighbor(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getNeighbors(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getLeader(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ClusterServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'leader_initiate': grpc.unary_unary_rpc_method_handler(
          servicer.leader_initiate,
          request_deserializer=cluster__pb2.Node.FromString,
          response_serializer=cluster__pb2.ackResponse.SerializeToString,
      ),
      'add_neighbor': grpc.unary_unary_rpc_method_handler(
          servicer.add_neighbor,
          request_deserializer=cluster__pb2.Node.FromString,
          response_serializer=cluster__pb2.ackResponse.SerializeToString,
      ),
      'remove_neighbor': grpc.unary_unary_rpc_method_handler(
          servicer.remove_neighbor,
          request_deserializer=cluster__pb2.Node.FromString,
          response_serializer=cluster__pb2.ackResponse.SerializeToString,
      ),
      'getNeighbors': grpc.unary_unary_rpc_method_handler(
          servicer.getNeighbors,
          request_deserializer=cluster__pb2.getNeighborRequest.FromString,
          response_serializer=cluster__pb2.getNeighborResponse.SerializeToString,
      ),
      'getLeader': grpc.unary_unary_rpc_method_handler(
          servicer.getLeader,
          request_deserializer=cluster__pb2.getLeaderRequest.FromString,
          response_serializer=cluster__pb2.Node.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ClusterService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
