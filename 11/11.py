#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import math
import pathlib
import re
from typing import Iterable, List, Optional, Sequence


class VMonkey(object):
  def __init__(self,
               startingItems: List[int],
               operation: str,
               rightOperand: Optional[int],
               divisor: int,
               divisibleTargetMonkeyIndex: int,
               notDivisibleTargetMonkeyIndex: int,
               divideBy3: bool,
               modulus: int = 0) -> None:
    self.startingItems = startingItems
    self.items = list(startingItems)
    self.operation = operation
    self.rightOperand = rightOperand
    self.divisor = divisor
    self.divisibleTargetMonkeyIndex = divisibleTargetMonkeyIndex
    self.divisibleTargetMonkey: Optional[VMonkey] = None
    self.notDivisibleTargetMonkeyIndex = notDivisibleTargetMonkeyIndex
    self.notDivisibleTargetMonkey: Optional[VMonkey] = None
    self.divideBy3 = divideBy3
    self.modulus = modulus
    self.numberOfInspectedItems = 0

  @staticmethod
  def FromString(string: str, divideBy3: bool) -> "VMonkey":
    regexMatch = re.search(r"Starting items:(.*)", string)
    assert regexMatch is not None
    startingItems = [int(item) for item in regexMatch.group(1).split(",")]

    regexMatch = re.search(r"Operation: new = old (.) (.+)", string)
    assert regexMatch is not None
    operation = regexMatch.group(1)
    rightOperand = None if regexMatch.group(2) == "old" else int(regexMatch.group(2))

    regexMatch = re.search(r"Test: divisible by (.+)", string)
    assert regexMatch is not None
    divisor = int(regexMatch.group(1))

    regexMatch = re.search(r"If true: throw to monkey (.+)", string)
    assert regexMatch is not None
    divisibleTargetMonkeyIndex = int(regexMatch.group(1))

    regexMatch = re.search(r"If false: throw to monkey (.+)", string)
    assert regexMatch is not None
    notDivisibleTargetMonkeyIndex = int(regexMatch.group(1))

    return VMonkey(startingItems, operation, rightOperand, divisor, divisibleTargetMonkeyIndex,
                   notDivisibleTargetMonkeyIndex, divideBy3)

  def PlayTurn(self) -> None:
    for oldItem in self.items:
      rightOperand = self.rightOperand if self.rightOperand is not None else oldItem

      if self.operation == "+":
        newItem = oldItem + rightOperand
      elif self.operation == "*":
        newItem = oldItem * rightOperand
      else:
        raise RuntimeError(f"Unknown operation {self.operation!r}.")

      if self.divideBy3: newItem //= 3
      if self.modulus > 0: newItem %= self.modulus
      targetMonkey = self.divisibleTargetMonkey if newItem % self.divisor == 0 else self.notDivisibleTargetMonkey
      assert targetMonkey is not None
      targetMonkey.items.append(newItem)

    self.numberOfInspectedItems += len(self.items)
    self.items.clear()


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  monkeysWithDivideBy3 = CreateMonkeys(input, True)
  PlayRounds(monkeysWithDivideBy3, 20)
  monkeysWithoutDivideBy3 = CreateMonkeys(input, False)
  PlayRounds(monkeysWithoutDivideBy3, 10000)
  print("Solution of part 1: {}".format(GetScore(monkeysWithDivideBy3)))
  print("Solution of part 2: {}".format(GetScore(monkeysWithoutDivideBy3)))


def CreateMonkeys(input: str, divideBy3: bool) -> List[VMonkey]:
  monkeys = [VMonkey.FromString(monkeyString, divideBy3) for monkeyString in input.split("\n\n")]
  modulus = math.prod(monkey.divisor for monkey in monkeys)

  for monkey in monkeys:
    monkey.divisibleTargetMonkey = monkeys[monkey.divisibleTargetMonkeyIndex]
    monkey.notDivisibleTargetMonkey = monkeys[monkey.notDivisibleTargetMonkeyIndex]
    monkey.modulus = modulus

  return monkeys


def PlayRounds(monkeys: Sequence[VMonkey], numberOfRounds: int) -> None:
  for _ in range(numberOfRounds):
    for monkey in monkeys:
      monkey.PlayTurn()


def GetScore(monkeys: Iterable[VMonkey]) -> int:
  sortedMonkeys = sorted(monkeys, key=lambda monkey: monkey.numberOfInspectedItems, reverse=True)
  return sortedMonkeys[0].numberOfInspectedItems * sortedMonkeys[1].numberOfInspectedItems


if __name__ == "__main__": Main()
