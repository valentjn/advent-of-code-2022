#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
from typing import List, Tuple


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  assignmentPairs = [ParseAssignmentPair(line) for line in input.splitlines()]
  print("Solution of part 1: {}".format(
    sum(AreAssignmentsContainedInEachOther(assignment1, assignment2) for assignment1, assignment2 in assignmentPairs)))
  print("Solution of part 2: {}".format(
    sum(DoAssignmentsOverlap(assignment1, assignment2) for assignment1, assignment2 in assignmentPairs)))


gAssignment = Tuple[int, int]


def ParseAssignmentPair(string: str) -> List[gAssignment]:
  assignmentsParts = [assignmentString.split("-") for assignmentString in string.split(",")]
  return [(int(assignmentParts[0]), int(assignmentParts[1])) for assignmentParts in assignmentsParts]


def AreAssignmentsContainedInEachOther(assignment1: gAssignment, assignment2: gAssignment) -> bool:
  return (((assignment1[0] <= assignment2[0]) and (assignment1[1] >= assignment2[1]))
          or (assignment2[0] <= assignment1[0]) and (assignment2[1] >= assignment1[1]))


def DoAssignmentsOverlap(assignment1: gAssignment, assignment2: gAssignment) -> bool:
  return (assignment1[0] <= assignment2[0] <= assignment1[1]) or (assignment2[0] <= assignment1[0] <= assignment2[1])


if __name__ == "__main__": Main()
