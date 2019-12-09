# -*- coding: utf-8 -*-
"""
This module provides a simple set of data structures for representing source
code locations (e.g., characters, character ranges, lines, etc.).
"""
__all__ = (
    '__version__',
    'Location'
)
__version__ = '0.0.1'

import typing as _t
import attr as _attr


@_attr.s(frozen=True, str=False, auto_attribs=True)
class Location:
    """Represents a character location within an arbitrary file.

    Attributes
    ----------
    line: int
        A one-indexed line number.
    column: int
        A one-indexed column number.
    """
    line: int
    column: int

    @staticmethod
    def from_string(s: str) -> 'Location':
        line, _, column = s.partition(':')
        return Location(int(line), int(column))

    def __le__(self, other: _t.Any) -> bool:
        if not isinstance(other, Location):
            return False
        if self.line == other.line:
            return self.column < other.column
        return self.line < other.line

    def __str__(self) -> str:
        return f'{self.line}:{self.column}'
