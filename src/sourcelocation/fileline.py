# -*- coding: utf-8 -*-
__all__ = (
    'FileLine',
)

import attr as _attr
import collections as _collections
import typing as _t

T = _t.TypeVar('T')

# see: https://github.com/python/mypy/issues/5446
if _t.TYPE_CHECKING:
    BaseSet = _t.Set[FileLine]
    BaseMap = _t.MutableMapping[FileLine, T]
else:
    BaseSet = _collections.abc.Set
    BaseMap = _collections.abc.MutableMapping


@_attr.s(frozen=True, slots=True, auto_attribs=True)
class FileLine:
    """Represents a one-indexed line within a specific file."""
    filename: str
    num: int

    @staticmethod
    def from_string(s: str) -> 'FileLine':
        fn, _, s_num = s.rpartition(':')
        num = int(s_num)
        return FileLine(fn, num)

    def __str__(self) -> str:
        return f'{self.filename}:{self.num}'


class FileLineMap(BaseMap):
    """
    An efficient implementation of maps indexed by file lines.
    Note that operations on instances of this class are NOT thread safe.
    """
    def __init__(self, contents: _t.Mapping[FileLine, T]) -> None:
        self.__contents: _t.Dict[str, _t.Dict[int, T]] = {}
        self.__length = 0
        for line, val in contents.items():
            self[line] = val

    def __iter__(self) -> _t.Iterator[FileLine]:
        for filename in self.__contents:
            for line_number in self.__contents[filename]:
                yield FileLine(filename, line_number)

    def __len__(self) -> int:
        return self.__length

    def __getitem__(self, line: FileLine) -> T:
        return self.__contents[line.filename][line.num]

    def __setitem__(self, line: FileLine, val: T) -> None:
        if line.filename not in self.__contents:
            self.__contents[line.filename] = {}
        if line.num not in self.__contents[line.filename]:
            self.__length += 1
        self.__contents[line.filename][line.num] = val

    def __delitem__(self, line: FileLine) -> None:
        del self.__contents[line.filename][line.num]
        if not self.__contents[line.filename]:
            del self.__contents[line.filename]
        self.__length -= 1
