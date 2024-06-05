from sourcelocation import FileLine


def test_equals():
    x = FileLine('foo.c', 1)
    y = FileLine('foo.c', 2)
    assert x != y
    assert x == x
    assert y == y

    a = FileLine('bar.c', 1)
    b = FileLine('foo.c', 1)
    assert a != b


def test_comparison():
    x = FileLine('foo.c', 1)
    y = FileLine('foo.c', 2)
    assert x < y
    assert y > x
    assert x <= y
    assert y >= x

    a = FileLine('bar.c', 1)
    b = FileLine('foo.c', 1)
    assert a < b
    assert b > a
    assert a <= b
    assert b >= a
