# -*- coding: utf-8 -*-
import pytest

from sourcelocation import FileLine


def test_fileline_equals():
    x = FileLine('foo.c', 1)
    y = FileLine('foo.c', 2)
    assert x != y
    assert x == x
    assert y == y

    a = FileLine('bar.c', 1)
    b = FileLine('foo.c', 1)
    assert a != b
