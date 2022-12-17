#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
from typing import Dict, FrozenSet, Optional, Tuple


class VBoard(object):
  def __init__(self, jetPattern: str) -> None:
    self.jetSigns = [2 * int(character == ">") - 1 for character in jetPattern]
    self.jetIndex = 0
    self.occupiedTiles: FrozenSet[Tuple[int, int]] = frozenset()
    self.rockIndex = 0
    self.rocksTiles = [
      frozenset([(0, 0), (1, 0), (2, 0), (3, 0)]),
      frozenset([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
      frozenset([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
      frozenset([(0, 0), (0, 1), (0, 2), (0, 3)]),
      frozenset([(0, 0), (1, 0), (0, 1), (1, 1)]),
    ]
    self.width = 7

  def __str__(self) -> str:
    return "\n".join("".join("#" if (x, y) in self.occupiedTiles else "." for x in range(self.width))
                     for y in range(self.GetHeightOfOccupiedTiles() - 1,
                                    min([y for _, y in self.occupiedTiles] + [0]) - 1, -1))

  def SimulateRocks(self,
                    numberOfRocks: int,
                    pruneHeight: Optional[int] = None,
                    cacheHeight: Optional[int] = None) -> int:
    rockNumber = 0
    cache: Dict[Tuple[FrozenSet[Tuple[int, int]], int], Tuple[int, int]] = {}

    while rockNumber < numberOfRocks:
      self.SimulatePiece()
      rockNumber += 1
      if pruneHeight is not None: self.occupiedTiles = self.Prune(pruneHeight)

      if (cacheHeight is not None) and (self.rockIndex == 0):
        cacheKey = (self.Prune(cacheHeight, makeRelativeToTop=True), self.jetIndex)
        heightOfOccupiedTiles = self.GetHeightOfOccupiedTiles()

        if cacheKey in cache:
          cachedRockNumber, cachedHeightOfOccupiedTiles = cache[cacheKey]
          cycleLength = rockNumber - cachedRockNumber
          numberOfCycles = (numberOfRocks - rockNumber) // cycleLength
          rockNumber += numberOfCycles * cycleLength
          yOffset = numberOfCycles * (heightOfOccupiedTiles - cachedHeightOfOccupiedTiles)
          self.occupiedTiles = frozenset((x, y + yOffset) for x, y in self.occupiedTiles)
          cacheHeight = None
        else:
          cache[cacheKey] = (rockNumber, heightOfOccupiedTiles)

    return self.GetHeightOfOccupiedTiles()

  def SimulatePiece(self) -> None:
    rockTiles = self.rocksTiles[self.rockIndex]
    self.rockIndex = (self.rockIndex + 1) % len(self.rocksTiles)
    rockOffset = (2, self.GetHeightOfOccupiedTiles() + 3)

    while True:
      jetSign = self.jetSigns[self.jetIndex]
      self.jetIndex = (self.jetIndex + 1) % len(self.jetSigns)
      newRockOffset = (rockOffset[0] + jetSign, rockOffset[1])
      if not self.DoesRockCollide(rockTiles, newRockOffset): rockOffset = newRockOffset

      newRockOffset = (rockOffset[0], rockOffset[1] - 1)

      if self.DoesRockCollide(rockTiles, newRockOffset):
        break
      else:
        rockOffset = newRockOffset

    self.occupiedTiles |= frozenset((x + rockOffset[0], y + rockOffset[1]) for x, y in rockTiles)

  @staticmethod
  def GetHeightOfTiles(tiles: FrozenSet[Tuple[int, int]]) -> int:
    return max([y for _, y in tiles] + [-1]) + 1

  def GetHeightOfOccupiedTiles(self) -> int:
    return VBoard.GetHeightOfTiles(self.occupiedTiles)

  def DoesRockCollide(self, rockTiles: FrozenSet[Tuple[int, int]], offset: Tuple[int, int]) -> bool:
    for x, y in rockTiles:
      actualX = x + offset[0]
      actualY = y + offset[1]

      if (actualX < 0) or (actualX >= self.width) or (actualY < 0) or ((actualX, actualY) in self.occupiedTiles):
        return True

    return False

  def Prune(self, height: int, makeRelativeToTop: bool = False) -> FrozenSet[Tuple[int, int]]:
    heightOfOccupiedTiles = self.GetHeightOfOccupiedTiles()
    return frozenset((x, y - (heightOfOccupiedTiles if makeRelativeToTop else 0)) for x, y in self.occupiedTiles
                     if y >= heightOfOccupiedTiles - height)


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  jetPattern = input.strip()
  board1 = VBoard(jetPattern)
  board1.SimulateRocks(2022)
  board2 = VBoard(jetPattern)
  board2.SimulateRocks(1000000000000, pruneHeight=100, cacheHeight=10)
  print("Solution of part 1: {}".format(board1.GetHeightOfOccupiedTiles()))
  print("Solution of part 2: {}".format(board2.GetHeightOfOccupiedTiles()))


if __name__ == "__main__": Main()
