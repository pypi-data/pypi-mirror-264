from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Collection(_message.Message):
    __slots__ = ("shortcode", "name", "description", "path", "created_at", "modified_at", "files")
    SHORTCODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    shortcode: str
    name: str
    description: str
    path: str
    created_at: str
    modified_at: str
    files: _containers.RepeatedCompositeFieldContainer[File]
    def __init__(self, shortcode: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., path: _Optional[str] = ..., created_at: _Optional[str] = ..., modified_at: _Optional[str] = ..., files: _Optional[_Iterable[_Union[File, _Mapping]]] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ("guid", "name", "path", "description", "magic", "checksum", "size", "created_at", "modified_at", "indexed_at")
    GUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    INDEXED_AT_FIELD_NUMBER: _ClassVar[int]
    guid: str
    name: str
    path: str
    description: str
    magic: str
    checksum: str
    size: int
    created_at: str
    modified_at: str
    indexed_at: str
    def __init__(self, guid: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., description: _Optional[str] = ..., magic: _Optional[str] = ..., checksum: _Optional[str] = ..., size: _Optional[int] = ..., created_at: _Optional[str] = ..., modified_at: _Optional[str] = ..., indexed_at: _Optional[str] = ...) -> None: ...

class Intelligence(_message.Message):
    __slots__ = ("source", "summary", "faq")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    FAQ_FIELD_NUMBER: _ClassVar[int]
    source: str
    summary: str
    faq: _containers.RepeatedCompositeFieldContainer[QnA]
    def __init__(self, source: _Optional[str] = ..., summary: _Optional[str] = ..., faq: _Optional[_Iterable[_Union[QnA, _Mapping]]] = ...) -> None: ...

class QnA(_message.Message):
    __slots__ = ("question", "answer")
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    question: str
    answer: str
    def __init__(self, question: _Optional[str] = ..., answer: _Optional[str] = ...) -> None: ...
