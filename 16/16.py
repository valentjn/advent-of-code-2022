#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import itertools
import pathlib
import re
from typing import Dict, FrozenSet, Iterable, Tuple


class VValve(object):
  def __init__(self, flowRate: int, connectedValves: Iterable[str]) -> None:
    self.flowRate = flowRate
    self.connectedValves = list(connectedValves)

  @staticmethod
  def CreateFromInputLine(inputLine: str) -> Tuple[str, "VValve"]:
    regexMatch = re.match(r"^Valve (.*) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)$", inputLine)
    assert regexMatch is not None
    valveName = regexMatch.group(1)
    valve = VValve(int(regexMatch.group(2)), regexMatch.group(3).split(", "))
    return (valveName, valve)


class VBoard(object):
  def __init__(self, valves: Dict[str, VValve], numberOfAgents: int) -> None:
    self.valves = valves
    self.relevantValves = frozenset(valveName for valveName, valve in valves.items() if valve.flowRate > 0)
    self.positionMap: Dict[Tuple[Tuple[str, ...], FrozenSet[str]], int] = {
      (tuple(numberOfAgents * ["AA"]), frozenset()): 0
    }

  def SimulateTimeSteps(self, numberOfTimeSteps: int) -> None:
    for time in range(numberOfTimeSteps):
      self.SimulateTimeStep(numberOfTimeSteps - time - 1)
      print(time, len(self.positionMap))

  def SimulateTimeStep(self, numberOfRemainingTimeSteps: int) -> None:
    newPositionMap: Dict[Tuple[Tuple[str, ...], FrozenSet[str]], int] = {}

    for (positions, openValves), pressure in self.positionMap.items():
      if openValves == self.relevantValves:
        candidateKey = (positions, openValves)

        if (candidateKey not in newPositionMap) or (pressure > newPositionMap[candidateKey]):
          newPositionMap[candidateKey] = pressure
          continue

      connectedValves = [self.valves[position].connectedValves + [position] for position in positions]

      for newPositions in itertools.product(*connectedValves):
        candidatePressure = pressure
        candidateOpenValves = set(openValves)
        isCandidateValid = True

        for position, newPosition in zip(positions, newPositions):
          if newPosition == position:
            if (newPosition not in candidateOpenValves) and (self.valves[newPosition].flowRate > 0):
              candidatePressure += numberOfRemainingTimeSteps * self.valves[newPosition].flowRate
              candidateOpenValves.add(newPosition)
            else:
              isCandidateValid = False
              break

        if isCandidateValid:
          candidateKey = (newPositions, frozenset(candidateOpenValves))

          if (candidateKey not in newPositionMap) or (candidatePressure > newPositionMap[candidateKey]):
            newPositionMap[candidateKey] = candidatePressure

    self.positionMap = newPositionMap

  def GetBestPressure(self) -> int:
    return max(self.positionMap.values())


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  valves = ParseValves(input)
  numbersOfAgents = [1, 2]
  numbersOfTimeSteps = [30, 26]
  bestPressures = []

  for numberOfAgents, numberOfTimeSteps in zip(numbersOfAgents, numbersOfTimeSteps):
    board = VBoard(valves, numberOfAgents)
    board.SimulateTimeSteps(numberOfTimeSteps)
    bestPressures.append(board.GetBestPressure())

  print("Solution of part 1: {}".format(bestPressures[0]))
  print("Solution of part 2: {}".format(bestPressures[1]))


def ParseValves(string: str) -> Dict[str, VValve]:
  valves = {}

  for line in string.splitlines():
    valveName, valve = VValve.CreateFromInputLine(line)
    valves[valveName] = valve

  return valves


if __name__ == "__main__": Main()
