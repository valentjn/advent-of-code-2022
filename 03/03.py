#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
from typing import Collection, Iterable, Iterator, List, Optional, Set


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  rucksacks = input.splitlines()
  print("Solution of part 1: {}".format(sum(GetItemPriority(GetMisplacedItem(rucksack)) for rucksack in rucksacks)))
  print("Solution of part 2: {}".format(sum(GetItemPriority(GetBadge(group)) for group in GetGroups(rucksacks))))


def GetMisplacedItem(rucksack: str) -> str:
  firstCompartment = rucksack[:len(rucksack) // 2]
  secondCompartment = rucksack[len(rucksack) // 2:]
  intersection = set(firstCompartment).intersection(secondCompartment)
  return GetOnlyItem(intersection)


def GetGroups(rucksacks: Iterable[str]) -> Iterator[List[str]]:
  groupSize = 3
  group = []

  for rucksack in rucksacks:
    group.append(rucksack)

    if len(group) == groupSize:
      yield group
      group.clear()

  if len(group) > 0: yield group


def GetBadge(rucksacks: Iterable[str]) -> str:
  intersection: Optional[Set[str]] = None

  for rucksack in rucksacks:
    intersection = set(rucksack) if intersection is None else intersection.intersection(rucksack)

  assert intersection is not None
  return GetOnlyItem(intersection)


def GetOnlyItem(collection: Collection[str]) -> str:
  assert len(collection) == 1
  return next(item for item in collection)


def GetItemPriority(item: str) -> int:
  itemAsInt = ord(item)
  return itemAsInt - 38 if itemAsInt < 97 else itemAsInt - 96


if __name__ == "__main__": Main()
