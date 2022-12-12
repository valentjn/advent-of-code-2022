#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
from typing import cast, Iterable, List, Optional, Tuple


class VMap(object):
  def __init__(self, heights: Iterable[Iterable[int]], start: Tuple[int, int], end: Tuple[int, int]) -> None:
    self.heights = [list(row) for row in heights]
    self.start = start
    self.end = end

  def __str__(self) -> str:
    string = ""

    for rowIndex, row in enumerate(self.heights):
      if rowIndex > 0: string += "\n"

      for columnIndex, height in enumerate(row):
        if (rowIndex, columnIndex) == self.start:
          string += "S"
        elif (rowIndex, columnIndex) == self.end:
          string += "E"
        else:
          string += chr(height + 97)

    return string

  @staticmethod
  def FromString(string: str) -> "VMap":
    lines = string.splitlines()
    numberOfRows = len(lines)
    numberOfColumns = len(lines[0])
    heights = [numberOfColumns * [0] for _ in range(numberOfRows)]

    for rowIndex in range(numberOfRows):
      for columnIndex in range(numberOfColumns):
        character = lines[rowIndex][columnIndex]

        if character == "S":
          height = 0
          start = (rowIndex, columnIndex)
        elif character == "E":
          height = 25
          end = (rowIndex, columnIndex)
        else:
          height = ord(character) - 97

        heights[rowIndex][columnIndex] = height

    return VMap(heights, start, end)

  def ComputeDistances(self) -> List[List[Optional[int]]]:
    numberOfRows = len(self.heights)
    numberOfColumns = len(self.heights[0])
    distances = cast(List[List[Optional[int]]], [numberOfColumns * [None] for _ in range(numberOfRows)])
    distances[self.end[0]][self.end[1]] = 0
    nextNodes = [self.end]

    while len(nextNodes) > 0:
      node = nextNodes.pop()

      possibleNeighborDistance = cast(int, distances[node[0]][node[1]]) + 1
      neighbors = []
      if node[0] > 0: neighbors.append((node[0] - 1, node[1]))
      if node[0] < numberOfRows - 1: neighbors.append((node[0] + 1, node[1]))
      if node[1] > 0: neighbors.append((node[0], node[1] - 1))
      if node[1] < numberOfColumns - 1: neighbors.append((node[0], node[1] + 1))

      for neighbor in neighbors:
        neighborDistance = distances[neighbor[0]][neighbor[1]]

        if ((self.heights[neighbor[0]][neighbor[1]] >= self.heights[node[0]][node[1]] - 1)
            and ((neighborDistance is None) or (possibleNeighborDistance < neighborDistance))):
          distances[neighbor[0]][neighbor[1]] = possibleNeighborDistance
          nextNodes.append(neighbor)

    return distances


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  map = VMap.FromString(input)
  distances = map.ComputeDistances()
  print("Solution of part 1: {}".format(distances[map.start[0]][map.start[1]]))
  print("Solution of part 2: {}".format(
    min(distance for heightsRow, distancesRow in zip(map.heights, distances)
        for height, distance in zip(heightsRow, distancesRow) if (height == 0) and (distance is not None))))


if __name__ == "__main__": Main()
