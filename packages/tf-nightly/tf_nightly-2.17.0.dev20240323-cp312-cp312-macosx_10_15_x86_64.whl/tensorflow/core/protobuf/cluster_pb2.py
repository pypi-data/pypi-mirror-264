# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/cluster.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&tensorflow/core/protobuf/cluster.proto\x12\ntensorflow\"r\n\x06JobDef\x12\x0c\n\x04name\x18\x01 \x01(\t\x12,\n\x05tasks\x18\x02 \x03(\x0b\x32\x1d.tensorflow.JobDef.TasksEntry\x1a,\n\nTasksEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"-\n\nClusterDef\x12\x1f\n\x03job\x18\x01 \x03(\x0b\x32\x12.tensorflow.JobDefB\x87\x01\n\x1aorg.tensorflow.distruntimeB\rClusterProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.protobuf.cluster_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032org.tensorflow.distruntimeB\rClusterProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'
  _JOBDEF_TASKSENTRY._options = None
  _JOBDEF_TASKSENTRY._serialized_options = b'8\001'
  _JOBDEF._serialized_start=54
  _JOBDEF._serialized_end=168
  _JOBDEF_TASKSENTRY._serialized_start=124
  _JOBDEF_TASKSENTRY._serialized_end=168
  _CLUSTERDEF._serialized_start=170
  _CLUSTERDEF._serialized_end=215
# @@protoc_insertion_point(module_scope)
