# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_visualization.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ssl_visualization.proto',
  package='',
  syntax='proto3',
  serialized_options=b'Z:github.com/RoboCup-SSL/ssl-vision-client/pkg/visualization',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17ssl_visualization.proto\"6\n\x08RgbColor\x12\t\n\x01r\x18\x01 \x01(\r\x12\t\n\x01g\x18\x02 \x01(\r\x12\t\n\x01\x62\x18\x03 \x01(\r\x12\t\n\x01\x61\x18\x04 \x01(\x02\"\x82\x01\n\x08Metadata\x12\r\n\x05layer\x18\x01 \x03(\t\x12\x18\n\x10visibleByDefault\x18\x02 \x01(\x08\x12\r\n\x05order\x18\x03 \x01(\x05\x12\x1d\n\ncolor_fill\x18\x04 \x01(\x0b\x32\t.RgbColor\x12\x1f\n\x0c\x63olor_stroke\x18\x05 \x01(\x0b\x32\t.RgbColor\"j\n\x0bLineSegment\x12\x1b\n\x08metadata\x18\x01 \x01(\x0b\x32\t.Metadata\x12\x0f\n\x07start_x\x18\x02 \x01(\x02\x12\x0f\n\x07start_y\x18\x03 \x01(\x02\x12\r\n\x05\x65nd_x\x18\x04 \x01(\x02\x12\r\n\x05\x65nd_y\x18\x05 \x01(\x02\"Y\n\x06\x43ircle\x12\x1b\n\x08metadata\x18\x01 \x01(\x0b\x32\t.Metadata\x12\x10\n\x08\x63\x65nter_x\x18\x02 \x01(\x02\x12\x10\n\x08\x63\x65nter_y\x18\x03 \x01(\x02\x12\x0e\n\x06radius\x18\x04 \x01(\x02\"^\n\x12VisualizationFrame\x12\x11\n\tsender_id\x18\x01 \x01(\t\x12\x1b\n\x05lines\x18\x02 \x03(\x0b\x32\x0c.LineSegment\x12\x18\n\x07\x63ircles\x18\x03 \x03(\x0b\x32\x07.CircleB<Z:github.com/RoboCup-SSL/ssl-vision-client/pkg/visualizationb\x06proto3'
)




_RGBCOLOR = _descriptor.Descriptor(
  name='RgbColor',
  full_name='RgbColor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='r', full_name='RgbColor.r', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='g', full_name='RgbColor.g', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='b', full_name='RgbColor.b', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='a', full_name='RgbColor.a', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=27,
  serialized_end=81,
)


_METADATA = _descriptor.Descriptor(
  name='Metadata',
  full_name='Metadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='layer', full_name='Metadata.layer', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='visibleByDefault', full_name='Metadata.visibleByDefault', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order', full_name='Metadata.order', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='color_fill', full_name='Metadata.color_fill', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='color_stroke', full_name='Metadata.color_stroke', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=84,
  serialized_end=214,
)


_LINESEGMENT = _descriptor.Descriptor(
  name='LineSegment',
  full_name='LineSegment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='LineSegment.metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_x', full_name='LineSegment.start_x', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_y', full_name='LineSegment.start_y', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_x', full_name='LineSegment.end_x', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_y', full_name='LineSegment.end_y', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=216,
  serialized_end=322,
)


_CIRCLE = _descriptor.Descriptor(
  name='Circle',
  full_name='Circle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='Circle.metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='center_x', full_name='Circle.center_x', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='center_y', full_name='Circle.center_y', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='Circle.radius', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=324,
  serialized_end=413,
)


_VISUALIZATIONFRAME = _descriptor.Descriptor(
  name='VisualizationFrame',
  full_name='VisualizationFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender_id', full_name='VisualizationFrame.sender_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lines', full_name='VisualizationFrame.lines', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='circles', full_name='VisualizationFrame.circles', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=415,
  serialized_end=509,
)

_METADATA.fields_by_name['color_fill'].message_type = _RGBCOLOR
_METADATA.fields_by_name['color_stroke'].message_type = _RGBCOLOR
_LINESEGMENT.fields_by_name['metadata'].message_type = _METADATA
_CIRCLE.fields_by_name['metadata'].message_type = _METADATA
_VISUALIZATIONFRAME.fields_by_name['lines'].message_type = _LINESEGMENT
_VISUALIZATIONFRAME.fields_by_name['circles'].message_type = _CIRCLE
DESCRIPTOR.message_types_by_name['RgbColor'] = _RGBCOLOR
DESCRIPTOR.message_types_by_name['Metadata'] = _METADATA
DESCRIPTOR.message_types_by_name['LineSegment'] = _LINESEGMENT
DESCRIPTOR.message_types_by_name['Circle'] = _CIRCLE
DESCRIPTOR.message_types_by_name['VisualizationFrame'] = _VISUALIZATIONFRAME
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RgbColor = _reflection.GeneratedProtocolMessageType('RgbColor', (_message.Message,), {
  'DESCRIPTOR' : _RGBCOLOR,
  '__module__' : 'ssl_visualization_pb2'
  # @@protoc_insertion_point(class_scope:RgbColor)
  })
_sym_db.RegisterMessage(RgbColor)

Metadata = _reflection.GeneratedProtocolMessageType('Metadata', (_message.Message,), {
  'DESCRIPTOR' : _METADATA,
  '__module__' : 'ssl_visualization_pb2'
  # @@protoc_insertion_point(class_scope:Metadata)
  })
_sym_db.RegisterMessage(Metadata)

LineSegment = _reflection.GeneratedProtocolMessageType('LineSegment', (_message.Message,), {
  'DESCRIPTOR' : _LINESEGMENT,
  '__module__' : 'ssl_visualization_pb2'
  # @@protoc_insertion_point(class_scope:LineSegment)
  })
_sym_db.RegisterMessage(LineSegment)

Circle = _reflection.GeneratedProtocolMessageType('Circle', (_message.Message,), {
  'DESCRIPTOR' : _CIRCLE,
  '__module__' : 'ssl_visualization_pb2'
  # @@protoc_insertion_point(class_scope:Circle)
  })
_sym_db.RegisterMessage(Circle)

VisualizationFrame = _reflection.GeneratedProtocolMessageType('VisualizationFrame', (_message.Message,), {
  'DESCRIPTOR' : _VISUALIZATIONFRAME,
  '__module__' : 'ssl_visualization_pb2'
  # @@protoc_insertion_point(class_scope:VisualizationFrame)
  })
_sym_db.RegisterMessage(VisualizationFrame)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
