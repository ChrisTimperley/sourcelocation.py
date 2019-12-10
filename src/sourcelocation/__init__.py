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
    'FileLocation'
)
__version__ = '0.0.1'

from .fileline import FileLine, FileLineMap, FileLineSet
from .location import Location, FileLocation
