# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/log_file.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import claim_pb2 as proto_dot_claim__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/log_file.proto',
  package='gink',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14proto/log_file.proto\x12\x04gink\x1a\x11proto/claim.proto\"7\n\x07LogFile\x12\x0f\n\x07\x63ommits\x18\x01 \x03(\x0c\x12\x1b\n\x06\x63laims\x18\x02 \x03(\x0b\x32\x0b.gink.Claimb\x06proto3'
  ,
  dependencies=[proto_dot_claim__pb2.DESCRIPTOR,])




_LOGFILE = _descriptor.Descriptor(
  name='LogFile',
  full_name='gink.LogFile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='commits', full_name='gink.LogFile.commits', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='claims', full_name='gink.LogFile.claims', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=49,
  serialized_end=104,
)

_LOGFILE.fields_by_name['claims'].message_type = proto_dot_claim__pb2._CLAIM
DESCRIPTOR.message_types_by_name['LogFile'] = _LOGFILE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LogFile = _reflection.GeneratedProtocolMessageType('LogFile', (_message.Message,), {
  'DESCRIPTOR' : _LOGFILE,
  '__module__' : 'proto.log_file_pb2'
  # @@protoc_insertion_point(class_scope:gink.LogFile)
  })
_sym_db.RegisterMessage(LogFile)


# @@protoc_insertion_point(module_scope)
