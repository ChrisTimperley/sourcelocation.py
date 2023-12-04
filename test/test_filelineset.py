# -*- coding: utf-8 -*-
from sourcelocation import FileLine, FileLineSet


def ln(num: int) -> FileLine:
    return FileLine('foo.c', num)


def contiguous_line_set(start: int, stop: int) -> FileLineSet:
    return FileLineSet.from_iter(ln(i) for i in range(start, stop))


def test_length():
    set_ = contiguous_line_set(1, 6)
    assert len(set_) == 5


def test_equals():
    set_x = contiguous_line_set(1, 6)
    set_y = contiguous_line_set(1, 6)
    set_z = contiguous_line_set(1, 3)
    assert set_x == set_x
    assert set_x == set_y
    assert set_y == set_x
    assert set_x != set_z
    assert set_y != set_z


def test_contains():
    set_ = contiguous_line_set(1, 6)
    assert ln(1) in set_
    assert ln(5) in set_
    assert ln(0) not in set_
    assert ln(6) not in set_
