# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tensor/tensors_to_detections_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCmediapipe/calculators/tensor/tensors_to_detections_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\x95\n\n$TensorsToDetectionsCalculatorOptions\x12\x13\n\x0bnum_classes\x18\x01 \x01(\x05\x12\x11\n\tnum_boxes\x18\x02 \x01(\x05\x12\x12\n\nnum_coords\x18\x03 \x01(\x05\x12\x1d\n\x15keypoint_coord_offset\x18\t \x01(\x05\x12\x18\n\rnum_keypoints\x18\n \x01(\x05:\x01\x30\x12\"\n\x17num_values_per_keypoint\x18\x0b \x01(\x05:\x01\x32\x12\x1b\n\x10\x62ox_coord_offset\x18\x0c \x01(\x05:\x01\x30\x12\x12\n\x07x_scale\x18\x04 \x01(\x02:\x01\x30\x12\x12\n\x07y_scale\x18\x05 \x01(\x02:\x01\x30\x12\x12\n\x07w_scale\x18\x06 \x01(\x02:\x01\x30\x12\x12\n\x07h_scale\x18\x07 \x01(\x02:\x01\x30\x12,\n\x1d\x61pply_exponential_on_box_size\x18\r \x01(\x08:\x05\x66\x61lse\x12#\n\x14reverse_output_order\x18\x0e \x01(\x08:\x05\x66\x61lse\x12\x16\n\x0eignore_classes\x18\x08 \x03(\x05\x12\x19\n\rallow_classes\x18\x15 \x03(\x05\x42\x02\x10\x01\x12\x1c\n\rsigmoid_score\x18\x0f \x01(\x08:\x05\x66\x61lse\x12\x1d\n\x15score_clipping_thresh\x18\x10 \x01(\x02\x12\x1e\n\x0f\x66lip_vertically\x18\x12 \x01(\x08:\x05\x66\x61lse\x12\x18\n\x10min_score_thresh\x18\x13 \x01(\x02\x12\x17\n\x0bmax_results\x18\x14 \x01(\x05:\x02-1\x12U\n\x0etensor_mapping\x18\x16 \x01(\x0b\x32=.mediapipe.TensorsToDetectionsCalculatorOptions.TensorMapping\x12\x66\n\x16\x62ox_boundaries_indices\x18\x17 \x01(\x0b\x32\x44.mediapipe.TensorsToDetectionsCalculatorOptions.BoxBoundariesIndicesH\x00\x12Z\n\nbox_format\x18\x18 \x01(\x0e\x32\x39.mediapipe.TensorsToDetectionsCalculatorOptions.BoxFormat:\x0bUNSPECIFIED\x1a\xae\x01\n\rTensorMapping\x12\x1f\n\x17\x64\x65tections_tensor_index\x18\x01 \x01(\x05\x12\x1c\n\x14\x63lasses_tensor_index\x18\x02 \x01(\x05\x12\x1b\n\x13scores_tensor_index\x18\x03 \x01(\x05\x12#\n\x1bnum_detections_tensor_index\x18\x04 \x01(\x05\x12\x1c\n\x14\x61nchors_tensor_index\x18\x05 \x01(\x05\x1aZ\n\x14\x42oxBoundariesIndices\x12\x0f\n\x04ymin\x18\x01 \x01(\x05:\x01\x30\x12\x0f\n\x04xmin\x18\x02 \x01(\x05:\x01\x31\x12\x0f\n\x04ymax\x18\x03 \x01(\x05:\x01\x32\x12\x0f\n\x04xmax\x18\x04 \x01(\x05:\x01\x33\":\n\tBoxFormat\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04YXHW\x10\x01\x12\x08\n\x04XYWH\x10\x02\x12\x08\n\x04XYXY\x10\x03\x32^\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xaf\x8d\x8c\xa0\x01 \x01(\x0b\x32/.mediapipe.TensorsToDetectionsCalculatorOptionsB\r\n\x0b\x62ox_indices')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tensor.tensors_to_detections_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS'].fields_by_name['allow_classes']._options = None
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS'].fields_by_name['allow_classes']._serialized_options = b'\020\001'
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS']._serialized_start=121
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS']._serialized_end=1422
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS_TENSORMAPPING']._serialized_start=985
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS_TENSORMAPPING']._serialized_end=1159
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS_BOXBOUNDARIESINDICES']._serialized_start=1161
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS_BOXBOUNDARIESINDICES']._serialized_end=1251
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS_BOXFORMAT']._serialized_start=1253
  _globals['_TENSORSTODETECTIONSCALCULATOROPTIONS_BOXFORMAT']._serialized_end=1311
# @@protoc_insertion_point(module_scope)
