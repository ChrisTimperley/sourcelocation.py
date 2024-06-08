"""Provides data structures for representing source code locations.

Implements data structures to represent, e.g., characters, character ranges, lines, etc.
"""
__all__ = (
    "__version__",
    "Diff",
    "FileDiff",
    "FileLine",
    "FileLineMap",
    "FileLineSet",
    "Location",
    "LocationRange",
    "FileLocation",
    "FileLocationRange",
    "FileLocationRangeSet",
)
__version__ = "1.1.7"

from sourcelocation.diff import (
    Diff,
    FileDiff,
)
from sourcelocation.fileline import (
    FileLine,
    FileLineMap,
    FileLineSet,
)
from sourcelocation.location import (
    FileLocation,
    FileLocationRange,
    FileLocationRangeSet,
    Location,
    LocationRange,
)
