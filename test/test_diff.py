from __future__ import annotations

from sourcelocation.diff import (
    Diff,
    FileDiff,
    Hunk,
)
from sourcelocation.utils import dedent


def test_hunk_read_next() -> None:
    before = """
    @@ -1,7 +1,6 @@
    -The Way that can be told of is not the eternal Way;
    -The name that can be named is not the eternal name.
     The Nameless is the origin of Heaven and Earth;
    -The Named is the mother of all things.
    +The named is the mother of all things.
    +
     Therefore let there always be non-being,
       so we may see their subtlety,
     And let there always be being,
    """
    before = dedent(before)[1:-1]
    lines = before.split('\n')

    hunk = Hunk.read_next(lines)
    assert not lines
    assert str(hunk) == before


def test_file_patch_read_next() -> None:
    before = """
    diff --git a/file-two.txt b/file-two.txt
    new file mode 100644
    index 0000000..2990e5b
    --- /dev/null
    +++ b/file-two.txt
    @@ -0,0 +1,2 @@
    +This is file two.
    +How do you do?
    diff --git a/testfile.c b/testfile.c
    index f50a1fc..60ed6ff 100644
    --- a/testfile.c
    +++ b/testfile.c
    @@ -6,6 +6,8 @@
     int testfun(int a, int b)
       x = a + b;
       x *= x;
     
    +  int z = 10000;
    +
       int y;
       y = x * 2;
    """
    before = dedent(before)[1:-1]
    lines = before.split("\n")

    expected_l1 = lines[8:]
    expected_s1 = "\n".join(lines[3:8])
    expected_s2 = "\n".join(lines[10:])

    file_diff = FileDiff.read_next(lines)
    assert str(file_diff) == expected_s1
    assert lines == expected_l1

    file_diff = FileDiff.read_next(lines)
    assert str(file_diff) == expected_s2
    assert not lines


def test_diff_from_unidiff() -> None:
    before = """
    diff --git a/file-two.txt b/file-two.txt
    new file mode 100644
    index 0000000..2990e5b
    --- /dev/null
    +++ b/file-two.txt
    @@ -0,0 +1,2 @@
    +This is file two.
    +How do you do?
    diff --git a/testfile.c b/testfile.c
    index f50a1fc..60ed6ff 100644
    --- a/testfile.c
    +++ b/testfile.c
    @@ -6,6 +6,8 @@
     int testfun(int a, int b)
       x = a + b;
       x *= x;
     
    +  int z = 10000;
    +
       int y;
       y = x * 2;
    """
    before = dedent(before)[1:-1]
    print(before)
    lines = before.split('\n')
    expected = "\n".join(lines[3:8] + lines[10:] + [""])

    diff = Diff.from_unidiff(before)
    assert str(diff) == expected

    # produced using 'svn diff'
    before = """
    Index: src/joblist.c
    ===================================================================
    --- src/joblist.c	(revision 1794)
    +++ src/joblist.c	(working copy)
    @@ -7,7 +7,7 @@
     
     int joblist_append(server *srv, connection *con) {
       if (con->in_joblist) return 0;
    -  con->in_joblist = 1;
    +  con->in_joblist = 10000;
     
       if (srv->joblist->size == 0) {
         srv->joblist->size  = 16;
    @@ -19,7 +19,7 @@
     
       srv->joblist->ptr[srv->joblist->used++] = con;
     
    -  return 0;
    +  return 3300;
     }
     
     void joblist_free(server *srv, connections *joblist) {
    Index: tests/core-request.t
    ===================================================================
    --- tests/core-request.t	(revision 2792)
    +++ tests/core-request.t	(working copy)
    @@ -246,7 +246,7 @@
     ok($tf->handle_http($t) == 0, 'Content-Type - image/jpeg');
     
     $t->{REQUEST}  = ( <<EOF
    - GET /image.JPG HTTP/1.0
    + GET /image.jpg HTTP/1.0
     EOF
     );
     $t->{RESPONSE} = [ { 'HTTP-Protocol' => 'HTTP/1.0', 'HTTP-Status' => 200, 'Content-Type' => 'image/jpeg' } ];
    """
    before = dedent(before)[1:-1]
    lines = before.split("\n")
    expected = "\n".join(lines[2:22] + lines[24:] + [""])

    diff = Diff.from_unidiff(before)
    assert str(diff) == expected


def test_diff_from_file_hunks() -> None:
    before = """
    diff --git a/file-two.txt b/file-two.txt
    new file mode 100644
    index 0000000..2990e5b
    --- /dev/null
    +++ b/file-two.txt
    @@ -0,0 +1,2 @@
    +This is file two.
    +How do you do?
    diff --git a/testfile.c b/testfile.c
    index f50a1fc..60ed6ff 100644
    --- a/testfile.c
    +++ b/testfile.c
    @@ -6,6 +6,8 @@
     int testfun(int a, int b)
       x = a + b;
       x *= x;
     
    +  int z = 10000;
    +
       int y;
       y = x * 2;
    """
    before = dedent(before)[1:-1]
    print(before)
    lines = before.split('\n')

    diff = Diff.from_unidiff(before)
    file_hunks = list(diff.file_hunks)
    diff_from_file_hunks = Diff.from_file_hunks(file_hunks)
    assert str(diff) == str(diff_from_file_hunks)
