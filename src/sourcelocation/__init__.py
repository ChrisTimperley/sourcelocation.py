"""Provides data structures for representing source code locations.

Implements data structures to represent, e.g., characters, character ranges, lines, etc.
"""
__all__ = (
    "__version__",
    "FileLine",
    "FileLineMap",
    "FileLineSet",
    "Location",
    "LocationRange",
    "FileLocation",
    "FileLocationRange",
    "FileLocationRangeSet",
)
__version__ = "1.1.5"

from .fileline import FileLine, FileLineMap, FileLineSet
from .location import FileLocation, FileLocationRange, FileLocationRangeSet, Location, LocationRange
