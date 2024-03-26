from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Qos(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QOS_AT_MOST_ONCE: _ClassVar[Qos]
    QOS_AT_LEAST_ONCE: _ClassVar[Qos]
    QOS_EXACTLY_ONCE: _ClassVar[Qos]
QOS_AT_MOST_ONCE: Qos
QOS_AT_LEAST_ONCE: Qos
QOS_EXACTLY_ONCE: Qos

class TelemetryRequest(_message.Message):
    __slots__ = ("payload", "sub_topic", "qos")
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    SUB_TOPIC_FIELD_NUMBER: _ClassVar[int]
    QOS_FIELD_NUMBER: _ClassVar[int]
    payload: bytes
    sub_topic: str
    qos: Qos
    def __init__(self, payload: _Optional[bytes] = ..., sub_topic: _Optional[str] = ..., qos: _Optional[_Union[Qos, str]] = ...) -> None: ...
