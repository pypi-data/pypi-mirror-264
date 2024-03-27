from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Node2VecParameters(_message.Message):
    __slots__ = ("ndim", "num_walks", "walk_length", "window", "p", "q")
    NDIM_FIELD_NUMBER: _ClassVar[int]
    NUM_WALKS_FIELD_NUMBER: _ClassVar[int]
    WALK_LENGTH_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    ndim: int
    num_walks: int
    walk_length: int
    window: int
    p: float
    q: float
    def __init__(self, ndim: _Optional[int] = ..., num_walks: _Optional[int] = ..., walk_length: _Optional[int] = ..., window: _Optional[int] = ..., p: _Optional[float] = ..., q: _Optional[float] = ...) -> None: ...
