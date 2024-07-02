## 1.1.8 (2024-07-01)

* added `FileHunk` data structure and ability to build `Diff` from `FileHunk`s
* added `with_relative_location` and `with_relative_locations` to all data structures

## 1.1.7 (2024-06-05)

* added `Diff` and `FileDiff` data structures

## 1.1.6 (2024-06-04)

* added `__lt__` and `__le__` to FileLine, Location, LocationRange, FileLocation, and FileLocationRange

## 1.1.5 (2024-05-31)

* updated to require Python 3.9 or greater
* replaced travis CI with GitHub Actions workflows
* switched from Pipenv to Poetry
* dropped dependency on attrs (replaced by dataclasses)
* added Makefile for development tasks

## 1.0.5 (2022-08-09)

* Updated FileLineSet.to_dict to return line numbers in ascending order

## 1.0.4 (2022-06-29)

* Added py.typed to support checking of type annotations

## 1.0.3 (2022-06-29)

* Relaxed attrs dependency requirements

## 1.0.2 (2019-12-10)

### Features

* Added a basic FileLocationRangeSet data structure

## 1.0.1 (2019-12-09)

### Bug Fixes

* Fixed missing import of LocationRange and FileLocationRange

## 1.0.0 (2019-12-09)

* Initial package release
* Data structures taken from BugZoo, Darjeeling, and Boggart
