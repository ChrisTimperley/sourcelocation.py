# -*- coding: utf-8 -*-
"""
This module provides a simple set of data structures for representing source
code locations (e.g., characters, character ranges, lines, etc.).
"""
__all__ = (
    '__version__',
    'FileLine',
    'FileLineMap',
    'FileLineSet',
    'Location',
    'LocationRange',
    'FileLocation',
    'FileLocationRange',
    'FileLocationRangeSet'
)
__version__ = '1.0.2'

from .fileline import FileLine, FileLineMap, FileLineSet
from .location import (Location, LocationRange,
                       FileLocation, FileLocationRange, FileLocationRangeSet)
