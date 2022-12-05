#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
import pathlib
import re
from typing import List, Tuple


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  board, moves = ParseInput(input)
  boardWithCrateMover9000 = copy.deepcopy(board)
  boardWithCrateMover9001 = copy.deepcopy(board)

  for move in moves:
    PerformMoveWithCrateMover9000(move, boardWithCrateMover9000)
    PerformMoveWithCrateMover9001(move, boardWithCrateMover9001)

  print("Solution of part 1: {}".format("".join(stack[-1] for stack in boardWithCrateMover9000)))
  print("Solution of part 2: {}".format("".join(stack[-1] for stack in boardWithCrateMover9001)))


def ParseInput(input: str) -> Tuple[List[List[str]], List[Tuple[int, int, int]]]:
  boardString, movesString = input.split("\n\n")
  boardLines = boardString.splitlines()
  numberOfStacks = int(boardLines[-1].split()[-1])
  boardLines.pop()
  board: List[List[str]] = [[] for _ in range(numberOfStacks)]

  for line in boardLines:
    for stackIndex in range(numberOfStacks):
      characterIndex = 4 * stackIndex + 1
      if characterIndex >= len(line): break
      crate = line[characterIndex]
      if crate != " ": board[stackIndex].insert(0, crate)

  movesMatches = [re.findall(r"^move ([0-9]+) from ([0-9]+) to ([0-9]+)$", line) for line in movesString.splitlines()]
  moves = [(int(match[0]), int(match[1]) - 1, int(match[2]) - 1) for match, in movesMatches]
  return board, moves


def PerformMoveWithCrateMover9000(move: Tuple[int, int, int], board: List[List[str]]) -> None:
  for _ in range(move[0]):
    board[move[2]].append(board[move[1]].pop())


def PerformMoveWithCrateMover9001(move: Tuple[int, int, int], board: List[List[str]]) -> None:
  board[move[2]].extend(board[move[1]][-move[0]:])
  del board[move[1]][-move[0]:]


if __name__ == "__main__": Main()
