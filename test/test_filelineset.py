# -*- coding: utf-8 -*-
import pytest

from sourcelocation import FileLine, FileLineSet


def ln(num: int) -> FileLine:
    return FileLine('foo.c', num)


def contiguous_line_set(start: int, stop: int) -> FileLineSet:
    return FileLineSet.from_iter(ln(i) for i in range(start, stop))


def test_length():
    set_ = contiguous_line_set(1, 6)
    assert len(set_) == 5
