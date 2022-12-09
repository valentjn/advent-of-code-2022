#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import math
import pathlib
from typing import List


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  treeHeights = ParseTreeHeights(input)
  visibleTrees = ComputeVisibleTrees(treeHeights)
  scenicScores = ComputeScenicScores(treeHeights)
  print("Solution of part 1: {}".format(sum(sum(row) for row in visibleTrees)))
  print("Solution of part 2: {}".format(max(max(row) for row in scenicScores)))


def ParseTreeHeights(input: str) -> List[List[int]]:
  return [[int(treeHeight) for treeHeight in line] for line in input.splitlines()]


def ComputeVisibleTrees(treeHeights: List[List[int]]) -> List[List[bool]]:
  numberOfRows = len(treeHeights)
  numberOfColumns = len(treeHeights[0])
  visibleTrees = [[True for _ in range(numberOfColumns)] for _ in range(numberOfRows)]

  for rowIndex in range(numberOfRows):
    for columnIndex in range(numberOfColumns):
      treeHeight = treeHeights[rowIndex][columnIndex]
      isTreeVisible = True

      for otherRowIndex in range(rowIndex):
        if treeHeights[otherRowIndex][columnIndex] >= treeHeight:
          isTreeVisible = False
          break

      if isTreeVisible: continue
      isTreeVisible = True

      for otherRowIndex in range(rowIndex + 1, numberOfRows):
        if treeHeights[otherRowIndex][columnIndex] >= treeHeight:
          isTreeVisible = False
          break

      if isTreeVisible: continue
      isTreeVisible = True

      for otherColumnIndex in range(columnIndex):
        if treeHeights[rowIndex][otherColumnIndex] >= treeHeight:
          isTreeVisible = False
          break

      if isTreeVisible: continue
      isTreeVisible = True

      for otherColumnIndex in range(columnIndex + 1, numberOfColumns):
        if treeHeights[rowIndex][otherColumnIndex] >= treeHeight:
          isTreeVisible = False
          break

      if isTreeVisible: continue
      visibleTrees[rowIndex][columnIndex] = False

  return visibleTrees


def ComputeScenicScores(treeHeights: List[List[int]]) -> List[List[int]]:
  numberOfRows = len(treeHeights)
  numberOfColumns = len(treeHeights[0])
  scenicScores = [[0 for _ in range(numberOfColumns)] for _ in range(numberOfRows)]

  for rowIndex in range(numberOfRows):
    for columnIndex in range(numberOfColumns):
      treeHeight = treeHeights[rowIndex][columnIndex]
      viewingDistances = [0, 0, 0, 0]

      for otherRowIndex in range(rowIndex - 1, -1, -1):
        viewingDistances[0] += 1
        if treeHeights[otherRowIndex][columnIndex] >= treeHeight: break

      for otherRowIndex in range(rowIndex + 1, numberOfRows):
        viewingDistances[1] += 1
        if treeHeights[otherRowIndex][columnIndex] >= treeHeight: break

      for otherColumnIndex in range(columnIndex - 1, -1, -1):
        viewingDistances[2] += 1
        if treeHeights[rowIndex][otherColumnIndex] >= treeHeight: break

      for otherColumnIndex in range(columnIndex + 1, numberOfColumns):
        viewingDistances[3] += 1
        if treeHeights[rowIndex][otherColumnIndex] >= treeHeight: break

      scenicScores[rowIndex][columnIndex] = math.prod(viewingDistances)

  return scenicScores


if __name__ == "__main__": Main()
