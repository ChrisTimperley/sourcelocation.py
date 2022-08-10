# -*- coding: utf-8 -*-
__all__ = (
    'FileLine',
    'FileLineMap',
    'FileLineSet'
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
        self._contents: _t.Dict[str, _t.Dict[int, T]] = {}
        self._length = 0
        for line, val in contents.items():
            self[line] = val

    def __hash__(self) -> int:
        return hash(self._contents)

    def __eq__(self, other: _t.Any) -> bool:
        if not isinstance(other, FileLineMap):
            return False
        return self._contents == other._contents

    def __iter__(self) -> _t.Iterator[FileLine]:
        for filename in self._contents:
            for line_number in self._contents[filename]:
                yield FileLine(filename, line_number)

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, line: FileLine) -> T:
        return self._contents[line.filename][line.num]

    def __setitem__(self, line: FileLine, val: T) -> None:
        if line.filename not in self._contents:
            self._contents[line.filename] = {}
        if line.num not in self._contents[line.filename]:
            self._length += 1
        self._contents[line.filename][line.num] = val

    def __delitem__(self, line: FileLine) -> None:
        del self._contents[line.filename][line.num]
        if not self._contents[line.filename]:
            del self._contents[line.filename]
        self._length -= 1


class FileLineSet(BaseSet):
    """A set of file lines."""
    @staticmethod
    def from_dict(d: _t.Dict[str, _t.Iterable[int]]) -> 'FileLineSet':
        contents = {fn: set(lines) for (fn, lines) in d.items()}
        return FileLineSet(contents)

    @staticmethod
    def from_list(lst: _t.List[FileLine]) -> 'FileLineSet':
        """Converts a list of file lines into a FileLineSet."""
        return FileLineSet.from_iter(lst)

    @staticmethod
    def from_iter(itr: _t.Iterable[FileLine]) -> 'FileLineSet':
        d: _t.Dict[str, _t.Set[int]] = {}
        for line in itr:
            if line.filename not in d:
                d[line.filename] = set()
            d[line.filename].add(line.num)
        return FileLineSet(d)

    def __init__(self,
                 contents: _t.Optional[_t.Dict[str, _t.Set[int]]] = None
                 ) -> None:
        if contents is None:
            contents = {}
        self._contents: _t.Dict[str, _t.FrozenSet[int]] = \
            {fn: frozenset(line_nums) for (fn, line_nums) in contents.items()}

    def __iter__(self) -> _t.Iterator[FileLine]:
        for filename in self._contents:
            for line_number in self._contents[filename]:
                yield FileLine(filename, line_number)

    def __repr__(self) -> str:
        output = []
        for (fn, set_lines) in self._contents.items():
            lines = sorted(set_lines)
            if lines == []:
                continue

            ranges = [[lines[0], lines[0]]]
            for num in lines[1:]:
                if num == ranges[-1][1] + 1:
                    ranges[-1][1] = num
                else:
                    ranges.append([num, num])

            range_strs = []
            for (start, stop) in ranges:
                if start == stop:
                    range_strs.append(str(start))
                else:
                    range_strs.append("{}..{}".format(start, stop))

            output.append("{}: {}".format(fn, '; '.join(range_strs)))
        return '\n'.join(output)

    def __len__(self) -> int:
        return sum(len(lines) for lines in self._contents.values())

    def __getitem__(self, filename: str) -> _t.Iterator[FileLine]:
        """
        Returns an iterator over all lines contained in this set that belong
        to a given file.
        """
        if filename not in self._contents:
            raise StopIteration
        for line_number in self._contents[filename]:
            yield FileLine(filename, line_number)

    def __contains__(self, elem: _t.Any) -> bool:
        if not isinstance(elem, FileLine):
            return False
        return elem.filename in self._contents and \
            elem.num in self._contents[elem.filename]

    def filter(self,
               predicate: _t.Callable[[FileLine], 'FileLineSet']
               ) -> 'FileLineSet':
        """
        Returns a subset of the file lines within this set that satisfy a given
        filtering criterion.
        """
        return FileLineSet.from_iter(filter(predicate, self))

    def union(self, *others: _t.Iterable[FileLine]) -> "FileLineSet":
        """
        Returns a set that contains the union of the file lines contained
        within this set and the given collections of file lines.
        """
        sources: _t.Tuple[_t.Iterable[FileLine], ...] = (self,) + others
        return FileLineSet.from_iter(l for src in sources for l in src)

    def intersection(self, *others: _t.Iterable[FileLine]) -> "FileLineSet":
        """
        Returns a set of file lines that contains the intersection of the lines
        within this set and a given set.
        """
        lines = set(self)
        for src in others:
            lines &= set(src)
        return FileLineSet.from_iter(lines)

    def restricted_to_files(self, filenames: _t.List[str]) -> 'FileLineSet':
        """
        Returns a variant of this set that only contains lines that occur in
        any one of the given files. (I.e., returns the intersection of this set
        and the set of all lines from a given set of files.)
        """
        restricted: _t.Dict[str, _t.Set[int]] = {}
        for filename in filenames:
            if filename in self._contents:
                restricted[filename] = set(self._contents[filename])
        return FileLineSet(restricted)

    @property
    def files(self) -> _t.List[str]:
        """
        A list of the names of the files that are represented by the file lines
        in this set.
        """
        return list(self._contents.keys())

    def to_dict(self) -> _t.Dict[str, _t.List[int]]:
        return {
            filename: list(sorted(lines))
            for (filename, lines) in self._contents.items()
        }
