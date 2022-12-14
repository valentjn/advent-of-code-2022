#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
import enum
import pathlib
from typing import Optional, Set, Tuple


class VSandEvents(enum.Enum):
  success = 0
  abyss = 1
  sourceBlocked = 2


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  sandPoint = (500, 0)
  cave = ParseCave(input)
  floorY = max(point[1] for point in cave) + 2
  print("Solution of part 1: {}".format(AddSand(sandPoint, copy.deepcopy(cave))))
  print("Solution of part 2: {}".format(AddSand(sandPoint, copy.deepcopy(cave), floorY)))


def ParseCave(string: str) -> Set[Tuple[int, int]]:
  cave = set()

  for line in string.splitlines():
    points = line.split(" -> ")

    for previousPointString, currentPointString in zip(points[:-1], points[1:]):
      previousPoint = ParsePoint(previousPointString)
      currentPoint = ParsePoint(currentPointString)

      if previousPoint[0] != currentPoint[0]:
        for intermediateX in range(min(previousPoint[0], currentPoint[0]), max(previousPoint[0], currentPoint[0]) + 1):
          cave.add((intermediateX, currentPoint[1]))
      else:
        for intermediateY in range(min(previousPoint[1], currentPoint[1]), max(previousPoint[1], currentPoint[1]) + 1):
          cave.add((currentPoint[0], intermediateY))

  return cave


def AddSand(sandPoint: Tuple[int, int], cave: Set[Tuple[int, int]], floorY: Optional[int] = None) -> int:
  numberOfUnitsOfSand = 0

  while AddUnitOfSand(sandPoint, cave, floorY=floorY) == VSandEvents.success:
    numberOfUnitsOfSand += 1

  return numberOfUnitsOfSand


def AddUnitOfSand(sandPoint: Tuple[int, int], cave: Set[Tuple[int, int]], floorY: Optional[int] = None) -> VSandEvents:
  if sandPoint in cave: return VSandEvents.sourceBlocked
  maximumY = floorY if floorY is not None else max(point[1] for point in cave)

  while sandPoint[1] <= maximumY:
    isStepSuccessful = False

    for possibleNextSandPoint in [(sandPoint[0], sandPoint[1] + 1), (sandPoint[0] - 1, sandPoint[1] + 1),
                                  (sandPoint[0] + 1, sandPoint[1] + 1)]:
      if (possibleNextSandPoint not in cave) and ((floorY is None) or (possibleNextSandPoint[1] < floorY)):
        sandPoint = possibleNextSandPoint
        isStepSuccessful = True
        break

    if not isStepSuccessful:
      cave.add(sandPoint)
      return VSandEvents.success

  return VSandEvents.abyss


def ParsePoint(string: str) -> Tuple[int, int]:
  items = string.split(",")
  return (int(items[0]), int(items[1]))


if __name__ == "__main__": Main()
