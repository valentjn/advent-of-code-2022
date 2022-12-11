#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
from typing import List


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  xs = RunProgram(input)
  pixels = DrawPixels(xs)
  print("Solution of part 1: {}".format(sum((cycle + 1) * xs[cycle] for cycle in range(19, 240, 40))))
  print("Solution of part 2:\n{}".format(FormatPixels(pixels)))


def RunProgram(input: str) -> List[int]:
  x = 1
  xs = [x]

  for line in input.splitlines():
    if line == "noop":
      xs.append(x)
    else:
      xs.append(x)
      x += int(line.split()[1])
      xs.append(x)

  return xs


def DrawPixels(xs: List[int]) -> List[List[bool]]:
  numberOfRows = 6
  numberOfColumns = 40
  pixels = [[False for _ in range(numberOfColumns)] for _ in range(numberOfRows)]

  for cycle, x in enumerate(xs):
    rowIndex = cycle // numberOfColumns
    columnIndex = cycle % numberOfColumns
    if rowIndex >= numberOfRows: break
    if abs(x - columnIndex) <= 1: pixels[rowIndex][columnIndex] = True

  return pixels


def FormatPixels(pixels: List[List[bool]]) -> str:
  return "\n".join("".join("#" if pixel else "." for pixel in row) for row in pixels)


if __name__ == "__main__": Main()
