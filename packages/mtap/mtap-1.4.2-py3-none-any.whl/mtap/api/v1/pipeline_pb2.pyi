from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessEventInPipelineRequest(_message.Message):
    __slots__ = ("pipeline_id", "event", "params", "keep_after")
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    KEEP_AFTER_FIELD_NUMBER: _ClassVar[int]
    pipeline_id: str
    event: _struct_pb2.Struct
    params: _struct_pb2.Struct
    keep_after: bool
    def __init__(self, pipeline_id: _Optional[str] = ..., event: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., keep_after: bool = ...) -> None: ...

class ProcessEventInPipelineResponse(_message.Message):
    __slots__ = ("event", "timing_info", "result")
    class ComponentResult(_message.Message):
        __slots__ = ("identifier", "result_dict", "timing_info")
        class TimingInfoEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: _duration_pb2.Duration
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
        IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        RESULT_DICT_FIELD_NUMBER: _ClassVar[int]
        TIMING_INFO_FIELD_NUMBER: _ClassVar[int]
        identifier: str
        result_dict: _struct_pb2.Struct
        timing_info: _containers.MessageMap[str, _duration_pb2.Duration]
        def __init__(self, identifier: _Optional[str] = ..., result_dict: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., timing_info: _Optional[_Mapping[str, _duration_pb2.Duration]] = ...) -> None: ...
    class PipelineResult(_message.Message):
        __slots__ = ("component_results", "elapsed_time")
        COMPONENT_RESULTS_FIELD_NUMBER: _ClassVar[int]
        ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
        component_results: _containers.RepeatedCompositeFieldContainer[ProcessEventInPipelineResponse.ComponentResult]
        elapsed_time: _duration_pb2.Duration
        def __init__(self, component_results: _Optional[_Iterable[_Union[ProcessEventInPipelineResponse.ComponentResult, _Mapping]]] = ..., elapsed_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
    class TimingInfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _duration_pb2.Duration
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
    EVENT_FIELD_NUMBER: _ClassVar[int]
    TIMING_INFO_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    event: _struct_pb2.Struct
    timing_info: _containers.MessageMap[str, _duration_pb2.Duration]
    result: ProcessEventInPipelineResponse.PipelineResult
    def __init__(self, event: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., timing_info: _Optional[_Mapping[str, _duration_pb2.Duration]] = ..., result: _Optional[_Union[ProcessEventInPipelineResponse.PipelineResult, _Mapping]] = ...) -> None: ...
