#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import itertools
import pathlib
from typing import Dict, List, Sequence, Set, Tuple


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  cubes = ParseCubes(input)
  allAdjacentCubeIndices = ComputeAllAdjacentCubeIndices(cubes)
  interiorCubes = ComputeInteriorCubes(cubes)
  cubesWithoutHoles = cubes + list(interiorCubes)
  allAdjacentCubeIndicesWithoutHoles = ComputeAllAdjacentCubeIndices(cubesWithoutHoles)
  print("Solution of part 1: {}".format(ComputeSurfaceArea(allAdjacentCubeIndices)))
  print("Solution of part 2: {}".format(ComputeSurfaceArea(allAdjacentCubeIndicesWithoutHoles)))


def ParseCubes(string: str) -> List[Tuple[int, int, int]]:
  linesParts = [line.split(",") for line in string.splitlines()]
  return [(int(lineParts[0]), int(lineParts[1]), int(lineParts[2])) for lineParts in linesParts]


def ComputeAllAdjacentCubeIndices(cubes: Sequence[Tuple[int, int, int]]) -> List[Set[int]]:
  allAdjacentCubes: Dict[Tuple[int, int, int], Set[int]] = {cube: set() for cube in cubes}

  for cubeIndex, cube in enumerate(cubes):
    for candidateAdjacentCube in GetAdjacentCubes(cube):
      if candidateAdjacentCube in allAdjacentCubes:
        allAdjacentCubes[candidateAdjacentCube].add(cubeIndex)

  return [allAdjacentCubes[cube] for cube in cubes]


def GetAdjacentCubes(cube: Tuple[int, int, int]) -> Set[Tuple[int, int, int]]:
  return {
    (cube[0] - 1, cube[1], cube[2]),
    (cube[0] + 1, cube[1], cube[2]),
    (cube[0], cube[1] - 1, cube[2]),
    (cube[0], cube[1] + 1, cube[2]),
    (cube[0], cube[1], cube[2] - 1),
    (cube[0], cube[1], cube[2] + 1),
  }


def ComputeSurfaceArea(allAdjacentCubes: Sequence[Set[int]]) -> int:
  return 6 * len(allAdjacentCubes) - sum(len(adjacentCubes) for adjacentCubes in allAdjacentCubes)


def ComputeInteriorCubes(cubes: Sequence[Tuple[int, int, int]]) -> Set[Tuple[int, int, int]]:
  lowerBoundCube = (
    min(cube[0] for cube in cubes) - 1,
    min(cube[1] for cube in cubes) - 1,
    min(cube[2] for cube in cubes) - 1,
  )
  upperBoundCube = (
    max(cube[0] for cube in cubes) + 1,
    max(cube[1] for cube in cubes) + 1,
    max(cube[2] for cube in cubes) + 1,
  )
  cubesSet = set(cubes)
  exteriorCubes = set()
  surfaceCubes = set()
  reaminingExteriorCubes = {lowerBoundCube}

  while len(reaminingExteriorCubes) > 0:
    cube = reaminingExteriorCubes.pop()

    if cube in cubesSet:
      surfaceCubes.add(cube)
      continue

    if ((cube in exteriorCubes) or (not ((lowerBoundCube[0] <= cube[0] <= upperBoundCube[0]) and
                                         (lowerBoundCube[1] <= cube[1] <= upperBoundCube[1]) and
                                         (lowerBoundCube[2] <= cube[2] <= upperBoundCube[2])))):
      continue

    exteriorCubes.add(cube)
    reaminingExteriorCubes.update(GetAdjacentCubes(cube))

  allCubes = set(
    itertools.product(range(lowerBoundCube[0], upperBoundCube[0] + 1), range(lowerBoundCube[1], upperBoundCube[1] + 1),
                      range(lowerBoundCube[2], upperBoundCube[2] + 1)))
  return allCubes - exteriorCubes - surfaceCubes - cubesSet


if __name__ == "__main__": Main()
