# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/core/bypass_calculator.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2mediapipe/calculators/core/bypass_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xa3\x01\n\x17\x42ypassCalculatorOptions\x12\x19\n\x11pass_input_stream\x18\x01 \x03(\t\x12\x1a\n\x12pass_output_stream\x18\x02 \x03(\t2Q\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x9d\xe1\xbd\xe5\x01 \x01(\x0b\x32\".mediapipe.BypassCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.core.bypass_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BYPASSCALCULATOROPTIONS']._serialized_start=104
  _globals['_BYPASSCALCULATOROPTIONS']._serialized_end=267
# @@protoc_insertion_point(module_scope)
