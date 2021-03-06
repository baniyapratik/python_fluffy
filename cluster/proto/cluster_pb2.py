# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cluster.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='cluster.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rcluster.proto\" \n\x04Node\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"/\n\x0b\x61\x63kResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"E\n\nNodeDetail\x12\x17\n\x08nodeInfo\x18\x01 \x01(\x0b\x32\x05.Node\x12\r\n\x05state\x18\x02 \x01(\t\x12\x0f\n\x07isAlive\x18\x03 \x01(\t\"\x14\n\x12getNeighborRequest\"\x12\n\x10getLeaderRequest\"1\n\x13getNeighborResponse\x12\x1a\n\x05nodes\x18\x01 \x03(\x0b\x32\x0b.NodeDetail2\xf1\x01\n\x0e\x43lusterService\x12(\n\x0fleader_initiate\x12\x05.Node\x1a\x0c.ackResponse\"\x00\x12%\n\x0c\x61\x64\x64_neighbor\x12\x05.Node\x1a\x0c.ackResponse\"\x00\x12(\n\x0fremove_neighbor\x12\x05.Node\x1a\x0c.ackResponse\"\x00\x12;\n\x0cgetNeighbors\x12\x13.getNeighborRequest\x1a\x14.getNeighborResponse\"\x00\x12\'\n\tgetLeader\x12\x11.getLeaderRequest\x1a\x05.Node\"\x00\x62\x06proto3')
)




_NODE = _descriptor.Descriptor(
  name='Node',
  full_name='Node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='Node.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='Node.port', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=49,
)


_ACKRESPONSE = _descriptor.Descriptor(
  name='ackResponse',
  full_name='ackResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='ackResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='ackResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=98,
)


_NODEDETAIL = _descriptor.Descriptor(
  name='NodeDetail',
  full_name='NodeDetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nodeInfo', full_name='NodeDetail.nodeInfo', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='NodeDetail.state', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isAlive', full_name='NodeDetail.isAlive', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=169,
)


_GETNEIGHBORREQUEST = _descriptor.Descriptor(
  name='getNeighborRequest',
  full_name='getNeighborRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=191,
)


_GETLEADERREQUEST = _descriptor.Descriptor(
  name='getLeaderRequest',
  full_name='getLeaderRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=193,
  serialized_end=211,
)


_GETNEIGHBORRESPONSE = _descriptor.Descriptor(
  name='getNeighborResponse',
  full_name='getNeighborResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nodes', full_name='getNeighborResponse.nodes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=213,
  serialized_end=262,
)

_NODEDETAIL.fields_by_name['nodeInfo'].message_type = _NODE
_GETNEIGHBORRESPONSE.fields_by_name['nodes'].message_type = _NODEDETAIL
DESCRIPTOR.message_types_by_name['Node'] = _NODE
DESCRIPTOR.message_types_by_name['ackResponse'] = _ACKRESPONSE
DESCRIPTOR.message_types_by_name['NodeDetail'] = _NODEDETAIL
DESCRIPTOR.message_types_by_name['getNeighborRequest'] = _GETNEIGHBORREQUEST
DESCRIPTOR.message_types_by_name['getLeaderRequest'] = _GETLEADERREQUEST
DESCRIPTOR.message_types_by_name['getNeighborResponse'] = _GETNEIGHBORRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), dict(
  DESCRIPTOR = _NODE,
  __module__ = 'cluster_pb2'
  # @@protoc_insertion_point(class_scope:Node)
  ))
_sym_db.RegisterMessage(Node)

ackResponse = _reflection.GeneratedProtocolMessageType('ackResponse', (_message.Message,), dict(
  DESCRIPTOR = _ACKRESPONSE,
  __module__ = 'cluster_pb2'
  # @@protoc_insertion_point(class_scope:ackResponse)
  ))
_sym_db.RegisterMessage(ackResponse)

NodeDetail = _reflection.GeneratedProtocolMessageType('NodeDetail', (_message.Message,), dict(
  DESCRIPTOR = _NODEDETAIL,
  __module__ = 'cluster_pb2'
  # @@protoc_insertion_point(class_scope:NodeDetail)
  ))
_sym_db.RegisterMessage(NodeDetail)

getNeighborRequest = _reflection.GeneratedProtocolMessageType('getNeighborRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETNEIGHBORREQUEST,
  __module__ = 'cluster_pb2'
  # @@protoc_insertion_point(class_scope:getNeighborRequest)
  ))
_sym_db.RegisterMessage(getNeighborRequest)

getLeaderRequest = _reflection.GeneratedProtocolMessageType('getLeaderRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETLEADERREQUEST,
  __module__ = 'cluster_pb2'
  # @@protoc_insertion_point(class_scope:getLeaderRequest)
  ))
_sym_db.RegisterMessage(getLeaderRequest)

getNeighborResponse = _reflection.GeneratedProtocolMessageType('getNeighborResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETNEIGHBORRESPONSE,
  __module__ = 'cluster_pb2'
  # @@protoc_insertion_point(class_scope:getNeighborResponse)
  ))
_sym_db.RegisterMessage(getNeighborResponse)



_CLUSTERSERVICE = _descriptor.ServiceDescriptor(
  name='ClusterService',
  full_name='ClusterService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=265,
  serialized_end=506,
  methods=[
  _descriptor.MethodDescriptor(
    name='leader_initiate',
    full_name='ClusterService.leader_initiate',
    index=0,
    containing_service=None,
    input_type=_NODE,
    output_type=_ACKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='add_neighbor',
    full_name='ClusterService.add_neighbor',
    index=1,
    containing_service=None,
    input_type=_NODE,
    output_type=_ACKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='remove_neighbor',
    full_name='ClusterService.remove_neighbor',
    index=2,
    containing_service=None,
    input_type=_NODE,
    output_type=_ACKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getNeighbors',
    full_name='ClusterService.getNeighbors',
    index=3,
    containing_service=None,
    input_type=_GETNEIGHBORREQUEST,
    output_type=_GETNEIGHBORRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getLeader',
    full_name='ClusterService.getLeader',
    index=4,
    containing_service=None,
    input_type=_GETLEADERREQUEST,
    output_type=_NODE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLUSTERSERVICE)

DESCRIPTOR.services_by_name['ClusterService'] = _CLUSTERSERVICE

# @@protoc_insertion_point(module_scope)
