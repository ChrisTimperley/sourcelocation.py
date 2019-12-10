# -*- coding: utf-8 -*-
"""
This module provides a simple set of data structures for representing source
code locations (e.g., characters, character ranges, lines, etc.).
"""
__all__ = (
    '__version__',
    'FileLine',
    'Location',
    'FileLocation'
)
__version__ = '0.0.1'

import typing as _t
import attr as _attr

from .fileline import FileLine


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


@_attr.s(frozen=True, str=False, auto_attribs=True)
class FileLocation:
    """Represents a character location within a particular file.

    Attributes
    ----------
    filename: str
        The name of the file to which the character belongs.
    location: Location
        The location of the character within the given file.
    """
    filename: str
    location: Location

    @property
    def line(self) -> int:
        """The one-indexed line number for this location."""
        return self.location.line

    @property
    def column(self) -> int:
        """The one-indexed column number for this location."""
        return self.location.column

    @staticmethod
    def from_string(s: str) -> 'FileLocation':
        filename, _, location_string = s.rpartition('@')
        location = Location.from_string(location_string)
        return FileLocation(filename, location)

    def __str__(self) -> str:
        return f'{self.filename}@{str(self.location)}'
