#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  rounds = [line.split() for line in input.splitlines()]
  print("Solution of part 1: {}".format(sum(ComputeScoreForPart1(*round) for round in rounds)))
  print("Solution of part 2: {}".format(sum(ComputeScoreForPart2(*round) for round in rounds)))


def ComputeScoreForPart1(opponentMove: str, playerMove: str) -> int:
  winPoints = {("A", "Y"): 6, ("B", "Z"): 6, ("C", "X"): 6, ("A", "X"): 3, ("B", "Y"): 3, ("C", "Z"): 3}
  playerMovePoints = {"X": 1, "Y": 2, "Z": 3}
  return playerMovePoints[playerMove] + winPoints.get((opponentMove, playerMove), 0)


def ComputeScoreForPart2(opponentMove: str, outcome: str) -> int:
  playerMoves = {("A", "X"): "Z", ("A", "Y"): "X", ("A", "Z"): "Y", ("C", "X"): "Y", ("C", "Y"): "Z", ("C", "Z"): "X"}
  return ComputeScoreForPart1(opponentMove, playerMoves.get((opponentMove, outcome), outcome))


if __name__ == "__main__": Main()
