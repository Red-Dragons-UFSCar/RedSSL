# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_gc_rcon_remotecontrol.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_gc_common_pb2 as ssl__gc__common__pb2
import ssl_gc_rcon_pb2 as ssl__gc__rcon__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ssl_gc_rcon_remotecontrol.proto',
  package='',
  syntax='proto2',
  serialized_options=b'Z<github.com/RoboCup-SSL/ssl-game-controller/internal/app/rcon',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1fssl_gc_rcon_remotecontrol.proto\x1a\x13ssl_gc_common.proto\x1a\x11ssl_gc_rcon.proto\"O\n\x19RemoteControlRegistration\x12\x13\n\x04team\x18\x01 \x02(\x0e\x32\x05.Team\x12\x1d\n\tsignature\x18\x02 \x01(\x0b\x32\n.Signature\"\xbd\x02\n\x19RemoteControlToController\x12\x1d\n\tsignature\x18\x01 \x01(\x0b\x32\n.Signature\x12\x35\n\x07request\x18\x02 \x01(\x0e\x32\".RemoteControlToController.RequestH\x00\x12\x18\n\x0e\x64\x65sired_keeper\x18\x03 \x01(\x05H\x00\x12$\n\x1arequest_robot_substitution\x18\x04 \x01(\x08H\x00\x12\x19\n\x0frequest_timeout\x18\x05 \x01(\x08H\x00\x12 \n\x16request_emergency_stop\x18\x06 \x01(\x08H\x00\"F\n\x07Request\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04PING\x10\x01\x12\x12\n\x0e\x43HALLENGE_FLAG\x10\x02\x12\x10\n\x0cSTOP_TIMEOUT\x10\x03\x42\x05\n\x03msg\"o\n\x19\x43ontrollerToRemoteControl\x12*\n\x10\x63ontroller_reply\x18\x01 \x01(\x0b\x32\x10.ControllerReply\x12&\n\x05state\x18\x02 \x01(\x0b\x32\x17.RemoteControlTeamState\"\xbf\x03\n\x16RemoteControlTeamState\x12\x13\n\x04team\x18\x0c \x01(\x0e\x32\x05.Team\x12\x35\n\x12\x61vailable_requests\x18\x01 \x03(\x0e\x32\x19.RemoteControlRequestType\x12\x32\n\x0f\x61\x63tive_requests\x18\x02 \x03(\x0e\x32\x19.RemoteControlRequestType\x12\x11\n\tkeeper_id\x18\x03 \x01(\x05\x12\x19\n\x11\x65mergency_stop_in\x18\x04 \x01(\x02\x12\x15\n\rtimeouts_left\x18\x05 \x01(\x05\x12\x19\n\x11timeout_time_left\x18\n \x01(\x02\x12\x1c\n\x14\x63hallenge_flags_left\x18\x06 \x01(\x05\x12\x12\n\nmax_robots\x18\x07 \x01(\x05\x12\x17\n\x0frobots_on_field\x18\t \x01(\x05\x12\x18\n\x10yellow_cards_due\x18\x08 \x03(\x02\x12\x1c\n\x14\x63\x61n_substitute_robot\x18\x0b \x01(\x08\x12\x1e\n\x16\x62ot_substitutions_left\x18\r \x01(\r\x12\"\n\x1a\x62ot_substitution_time_left\x18\x0e \x01(\x02*\xa9\x01\n\x18RemoteControlRequestType\x12\x18\n\x14UNKNOWN_REQUEST_TYPE\x10\x00\x12\x12\n\x0e\x45MERGENCY_STOP\x10\x01\x12\x16\n\x12ROBOT_SUBSTITUTION\x10\x02\x12\x0b\n\x07TIMEOUT\x10\x03\x12\x12\n\x0e\x43HALLENGE_FLAG\x10\x04\x12\x14\n\x10\x43HANGE_KEEPER_ID\x10\x05\x12\x10\n\x0cSTOP_TIMEOUT\x10\x06\x42>Z<github.com/RoboCup-SSL/ssl-game-controller/internal/app/rcon'
  ,
  dependencies=[ssl__gc__common__pb2.DESCRIPTOR,ssl__gc__rcon__pb2.DESCRIPTOR,])

_REMOTECONTROLREQUESTTYPE = _descriptor.EnumDescriptor(
  name='RemoteControlRequestType',
  full_name='RemoteControlRequestType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_REQUEST_TYPE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EMERGENCY_STOP', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ROBOT_SUBSTITUTION', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TIMEOUT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CHALLENGE_FLAG', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CHANGE_KEEPER_ID', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STOP_TIMEOUT', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1040,
  serialized_end=1209,
)
_sym_db.RegisterEnumDescriptor(_REMOTECONTROLREQUESTTYPE)

RemoteControlRequestType = enum_type_wrapper.EnumTypeWrapper(_REMOTECONTROLREQUESTTYPE)
UNKNOWN_REQUEST_TYPE = 0
EMERGENCY_STOP = 1
ROBOT_SUBSTITUTION = 2
TIMEOUT = 3
CHALLENGE_FLAG = 4
CHANGE_KEEPER_ID = 5
STOP_TIMEOUT = 6


_REMOTECONTROLTOCONTROLLER_REQUEST = _descriptor.EnumDescriptor(
  name='Request',
  full_name='RemoteControlToController.Request',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PING', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CHALLENGE_FLAG', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STOP_TIMEOUT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=397,
  serialized_end=467,
)
_sym_db.RegisterEnumDescriptor(_REMOTECONTROLTOCONTROLLER_REQUEST)


_REMOTECONTROLREGISTRATION = _descriptor.Descriptor(
  name='RemoteControlRegistration',
  full_name='RemoteControlRegistration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='RemoteControlRegistration.team', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature', full_name='RemoteControlRegistration.signature', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=154,
)


_REMOTECONTROLTOCONTROLLER = _descriptor.Descriptor(
  name='RemoteControlToController',
  full_name='RemoteControlToController',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='signature', full_name='RemoteControlToController.signature', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request', full_name='RemoteControlToController.request', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='desired_keeper', full_name='RemoteControlToController.desired_keeper', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_robot_substitution', full_name='RemoteControlToController.request_robot_substitution', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_timeout', full_name='RemoteControlToController.request_timeout', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_emergency_stop', full_name='RemoteControlToController.request_emergency_stop', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REMOTECONTROLTOCONTROLLER_REQUEST,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='msg', full_name='RemoteControlToController.msg',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=157,
  serialized_end=474,
)


_CONTROLLERTOREMOTECONTROL = _descriptor.Descriptor(
  name='ControllerToRemoteControl',
  full_name='ControllerToRemoteControl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='controller_reply', full_name='ControllerToRemoteControl.controller_reply', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='ControllerToRemoteControl.state', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=476,
  serialized_end=587,
)


_REMOTECONTROLTEAMSTATE = _descriptor.Descriptor(
  name='RemoteControlTeamState',
  full_name='RemoteControlTeamState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='RemoteControlTeamState.team', index=0,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='available_requests', full_name='RemoteControlTeamState.available_requests', index=1,
      number=1, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='active_requests', full_name='RemoteControlTeamState.active_requests', index=2,
      number=2, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keeper_id', full_name='RemoteControlTeamState.keeper_id', index=3,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='emergency_stop_in', full_name='RemoteControlTeamState.emergency_stop_in', index=4,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeouts_left', full_name='RemoteControlTeamState.timeouts_left', index=5,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeout_time_left', full_name='RemoteControlTeamState.timeout_time_left', index=6,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='challenge_flags_left', full_name='RemoteControlTeamState.challenge_flags_left', index=7,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_robots', full_name='RemoteControlTeamState.max_robots', index=8,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='robots_on_field', full_name='RemoteControlTeamState.robots_on_field', index=9,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='yellow_cards_due', full_name='RemoteControlTeamState.yellow_cards_due', index=10,
      number=8, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='can_substitute_robot', full_name='RemoteControlTeamState.can_substitute_robot', index=11,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bot_substitutions_left', full_name='RemoteControlTeamState.bot_substitutions_left', index=12,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bot_substitution_time_left', full_name='RemoteControlTeamState.bot_substitution_time_left', index=13,
      number=14, type=2, cpp_type=6, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=590,
  serialized_end=1037,
)

_REMOTECONTROLREGISTRATION.fields_by_name['team'].enum_type = ssl__gc__common__pb2._TEAM
_REMOTECONTROLREGISTRATION.fields_by_name['signature'].message_type = ssl__gc__rcon__pb2._SIGNATURE
_REMOTECONTROLTOCONTROLLER.fields_by_name['signature'].message_type = ssl__gc__rcon__pb2._SIGNATURE
_REMOTECONTROLTOCONTROLLER.fields_by_name['request'].enum_type = _REMOTECONTROLTOCONTROLLER_REQUEST
_REMOTECONTROLTOCONTROLLER_REQUEST.containing_type = _REMOTECONTROLTOCONTROLLER
_REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg'].fields.append(
  _REMOTECONTROLTOCONTROLLER.fields_by_name['request'])
_REMOTECONTROLTOCONTROLLER.fields_by_name['request'].containing_oneof = _REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg']
_REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg'].fields.append(
  _REMOTECONTROLTOCONTROLLER.fields_by_name['desired_keeper'])
_REMOTECONTROLTOCONTROLLER.fields_by_name['desired_keeper'].containing_oneof = _REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg']
_REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg'].fields.append(
  _REMOTECONTROLTOCONTROLLER.fields_by_name['request_robot_substitution'])
_REMOTECONTROLTOCONTROLLER.fields_by_name['request_robot_substitution'].containing_oneof = _REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg']
_REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg'].fields.append(
  _REMOTECONTROLTOCONTROLLER.fields_by_name['request_timeout'])
_REMOTECONTROLTOCONTROLLER.fields_by_name['request_timeout'].containing_oneof = _REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg']
_REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg'].fields.append(
  _REMOTECONTROLTOCONTROLLER.fields_by_name['request_emergency_stop'])
_REMOTECONTROLTOCONTROLLER.fields_by_name['request_emergency_stop'].containing_oneof = _REMOTECONTROLTOCONTROLLER.oneofs_by_name['msg']
_CONTROLLERTOREMOTECONTROL.fields_by_name['controller_reply'].message_type = ssl__gc__rcon__pb2._CONTROLLERREPLY
_CONTROLLERTOREMOTECONTROL.fields_by_name['state'].message_type = _REMOTECONTROLTEAMSTATE
_REMOTECONTROLTEAMSTATE.fields_by_name['team'].enum_type = ssl__gc__common__pb2._TEAM
_REMOTECONTROLTEAMSTATE.fields_by_name['available_requests'].enum_type = _REMOTECONTROLREQUESTTYPE
_REMOTECONTROLTEAMSTATE.fields_by_name['active_requests'].enum_type = _REMOTECONTROLREQUESTTYPE
DESCRIPTOR.message_types_by_name['RemoteControlRegistration'] = _REMOTECONTROLREGISTRATION
DESCRIPTOR.message_types_by_name['RemoteControlToController'] = _REMOTECONTROLTOCONTROLLER
DESCRIPTOR.message_types_by_name['ControllerToRemoteControl'] = _CONTROLLERTOREMOTECONTROL
DESCRIPTOR.message_types_by_name['RemoteControlTeamState'] = _REMOTECONTROLTEAMSTATE
DESCRIPTOR.enum_types_by_name['RemoteControlRequestType'] = _REMOTECONTROLREQUESTTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RemoteControlRegistration = _reflection.GeneratedProtocolMessageType('RemoteControlRegistration', (_message.Message,), {
  'DESCRIPTOR' : _REMOTECONTROLREGISTRATION,
  '__module__' : 'ssl_gc_rcon_remotecontrol_pb2'
  # @@protoc_insertion_point(class_scope:RemoteControlRegistration)
  })
_sym_db.RegisterMessage(RemoteControlRegistration)

RemoteControlToController = _reflection.GeneratedProtocolMessageType('RemoteControlToController', (_message.Message,), {
  'DESCRIPTOR' : _REMOTECONTROLTOCONTROLLER,
  '__module__' : 'ssl_gc_rcon_remotecontrol_pb2'
  # @@protoc_insertion_point(class_scope:RemoteControlToController)
  })
_sym_db.RegisterMessage(RemoteControlToController)

ControllerToRemoteControl = _reflection.GeneratedProtocolMessageType('ControllerToRemoteControl', (_message.Message,), {
  'DESCRIPTOR' : _CONTROLLERTOREMOTECONTROL,
  '__module__' : 'ssl_gc_rcon_remotecontrol_pb2'
  # @@protoc_insertion_point(class_scope:ControllerToRemoteControl)
  })
_sym_db.RegisterMessage(ControllerToRemoteControl)

RemoteControlTeamState = _reflection.GeneratedProtocolMessageType('RemoteControlTeamState', (_message.Message,), {
  'DESCRIPTOR' : _REMOTECONTROLTEAMSTATE,
  '__module__' : 'ssl_gc_rcon_remotecontrol_pb2'
  # @@protoc_insertion_point(class_scope:RemoteControlTeamState)
  })
_sym_db.RegisterMessage(RemoteControlTeamState)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)