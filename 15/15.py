#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
import re
from typing import Dict, List, Optional, Sequence, Tuple


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  sensors = ParseSensors(input)
  y = 2000000
  coverageIntervalsAtY = [
    ComputeCoverageIntervalAtY(sensor, nearestBeacon, y) for sensor, nearestBeacon in sensors.items()
  ]
  lower = (0, 0)
  upper = (4000000, 4000000)
  distressBeacon = FindFirstMissingCoveragePoint(sensors, lower, upper)
  assert distressBeacon is not None
  print("Solution of part 1: {}".format(ComputeAreaOfIntervalUnion(coverageIntervalsAtY)))
  print("Solution of part 2: {}".format(ComputeTuningFrequency(distressBeacon)))


def ParseSensors(string: str) -> Dict[Tuple[int, int], Tuple[int, int]]:
  matchesGroups = re.findall(r"Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)",
                             string)
  return {(int(matchGroups[0]), int(matchGroups[1])): (int(matchGroups[2]), int(matchGroups[3]))
          for matchGroups in matchesGroups}


def ComputeCoverageIntervalAtY(sensor: Tuple[int, int], nearestBeacon: Tuple[int, int], y: int) -> Tuple[int, int]:
  distance = abs(sensor[0] - nearestBeacon[0]) + abs(sensor[1] - nearestBeacon[1])
  intervalWidth = distance - abs(sensor[1] - y)
  return (sensor[0] - intervalWidth, sensor[0] + intervalWidth) if intervalWidth >= 0 else (0, -1)


def ComputeAreaOfIntervalUnion(intervals: Sequence[Tuple[int, int]]) -> int:
  events = sorted(event for interval in intervals for event in ((interval[0], True), (interval[1], False))
                  if interval[0] < interval[1])
  area = 0
  numberOfCurrentIntervals = 0
  previousX = 0

  for x, isStart in events:
    if numberOfCurrentIntervals > 0: area += x - previousX
    previousX = x

    if isStart:
      numberOfCurrentIntervals += 1
    else:
      numberOfCurrentIntervals -= 1

  return area


def FindFirstMissingCoveragePoint(
  sensors: Dict[Tuple[int, int], Tuple[int, int]],
  lower: Tuple[int, int],
  upper: Tuple[int, int],
) -> Optional[Tuple[int, int]]:
  for y in range(lower[1], upper[1] + 1):
    coverageIntervals = [
      ComputeCoverageIntervalAtY(sensor, nearestBeacon, y) for sensor, nearestBeacon in sensors.items()
    ]
    missingCoverageEnd, missingCoverageIntervals, missingCoverageStart = ComputeComplementOfIntervalUnion(
      coverageIntervals)

    if missingCoverageEnd >= lower[0]:
      return (lower[0], y)
    elif missingCoverageStart <= lower[1]:
      return (missingCoverageStart, y)
    elif len(missingCoverageIntervals) > 0:
      return (missingCoverageIntervals[0][0], y)

  return None


def ComputeComplementOfIntervalUnion(intervals: Sequence[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]], int]:
  if len(intervals) == 0: return 0, [], 0
  events = sorted(event for interval in intervals for event in ((interval[0], True), (interval[1], False))
                  if interval[0] < interval[1])
  complementIntervals: List[Tuple[int, int]] = []
  numberOfCurrentIntervals = 0
  previousX = None

  for x, isStart in events:
    if (numberOfCurrentIntervals == 0) and (previousX is not None) and (x - previousX >= 2):
      complementIntervals.append((previousX + 1, x - 1))

    previousX = x

    if isStart:
      numberOfCurrentIntervals += 1
    else:
      numberOfCurrentIntervals -= 1

  return events[0][0] - 1, complementIntervals, events[-1][0] + 1


def ComputeTuningFrequency(point: Tuple[int, int]) -> int:
  return 4000000 * point[0] + point[1]


if __name__ == "__main__": Main()
