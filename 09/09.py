#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
from typing import Iterable, Tuple, List


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  headMoves = ParseHeadMoves(input)
  numberOfKnots = 10
  allKnotsPositions = [ExecuteHeadMoves(headMoves)]

  for _ in range(numberOfKnots - 1):
    allKnotsPositions.append(ExecuteKnotMoves(allKnotsPositions[-1]))

  print("Solution of part 1: {}".format(len(set(allKnotsPositions[1]))))
  print("Solution of part 2: {}".format(len(set(allKnotsPositions[-1]))))


def ParseHeadMoves(input: str) -> List[Tuple[str, int]]:
  parts = [line.split() for line in input.splitlines()]
  return [(line[0], int(line[1])) for line in parts]


def ExecuteHeadMoves(headMoves: Iterable[Tuple[str, int]]) -> List[Tuple[int, int]]:
  headPosition = [0, 0]
  headPositions = [(0, 0)]

  for headMove in headMoves:
    for _ in range(headMove[1]):
      if headMove[0] == "L":
        headPosition[0] -= 1
      elif headMove[0] == "R":
        headPosition[0] += 1
      elif headMove[0] == "D":
        headPosition[1] -= 1
      elif headMove[0] == "U":
        headPosition[1] += 1

      headPositions.append((headPosition[0], headPosition[1]))

  return headPositions


def ExecuteKnotMoves(otherKnotPositions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
  knotPosition = [0, 0]
  knotPositions = [(0, 0)]

  for otherKnotPosition in otherKnotPositions[1:]:
    if knotPosition[0] == otherKnotPosition[0]:
      if knotPosition[1] <= otherKnotPosition[1] - 2:
        knotPosition[1] = otherKnotPosition[1] - 1
      elif knotPosition[1] >= otherKnotPosition[1] + 2:
        knotPosition[1] = otherKnotPosition[1] + 1
    elif knotPosition[1] == otherKnotPosition[1]:
      if knotPosition[0] <= otherKnotPosition[0] - 2:
        knotPosition[0] = otherKnotPosition[0] - 1
      elif knotPosition[0] >= otherKnotPosition[0] + 2:
        knotPosition[0] = otherKnotPosition[0] + 1
    elif ((abs(knotPosition[0] - otherKnotPosition[0]) <= 1) and (abs(knotPosition[1] - otherKnotPosition[1]) <= 1)):
      pass
    else:
      knotPosition[0] += 2 * int(knotPosition[0] < otherKnotPosition[0]) - 1
      knotPosition[1] += 2 * int(knotPosition[1] < otherKnotPosition[1]) - 1

    knotPositions.append((knotPosition[0], knotPosition[1]))

  return knotPositions


if __name__ == "__main__": Main()
