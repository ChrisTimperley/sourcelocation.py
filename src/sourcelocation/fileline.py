# -*- coding: utf-8 -*-
__all__ = (
    'FileLine',
)

import typing as _t
import attr as _attr


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
