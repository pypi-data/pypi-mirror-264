# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/image/opencv_encoded_image_to_image_frame_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nPmediapipe/calculators/image/opencv_encoded_image_to_image_frame_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xcd\x01\n/OpenCvEncodedImageToImageFrameCalculatorOptions\x12/\n apply_orientation_from_exif_data\x18\x01 \x01(\x08:\x05\x66\x61lse2i\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x8c\xfa\xd8\x90\x01 \x01(\x0b\x32:.mediapipe.OpenCvEncodedImageToImageFrameCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.image.opencv_encoded_image_to_image_frame_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_OPENCVENCODEDIMAGETOIMAGEFRAMECALCULATOROPTIONS']._serialized_start=134
  _globals['_OPENCVENCODEDIMAGETOIMAGEFRAMECALCULATOROPTIONS']._serialized_end=339
# @@protoc_insertion_point(module_scope)
