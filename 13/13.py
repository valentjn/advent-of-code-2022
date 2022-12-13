#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import functools
import math
import pathlib
from typing import Any, List, Optional, Sequence, Tuple


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  packetPairs = ParsePacketPairs(input)
  arePacketPairsEqual = [AreDataInRightOrder(left, right) for left, right in packetPairs]
  dividerPackets = [[[2]], [[6]]]
  packets = [packet for left, right in packetPairs for packet in [left, right]] + dividerPackets
  packets.sort(key=functools.cmp_to_key(CompareData))
  print("Solution of part 1: {}".format(
    sum(packetPairIndex + 1 for packetPairIndex, isPacketPairEqual in enumerate(arePacketPairsEqual)
        if isPacketPairEqual)))
  print("Solution of part 2: {}".format(ComputeDecoderKey(packets, dividerPackets)))


def ParsePacketPairs(string: str) -> List[Tuple[Any, Any]]:
  pairsLines = [pair.splitlines() for pair in string.split("\n\n")]
  return [(ParseData(pairLines[0]), ParseData(pairLines[1])) for pairLines in pairsLines]


def ParseData(string: str) -> Any:
  if string[0] == "[":
    assert string[-1] == "]"
    item = ""
    items = []
    level = 0

    for character in string:
      if character == "[":
        if level > 0: item += "["
        level += 1
      elif character == "]":
        level -= 1
        if level > 0: item += "]"
      elif character == ",":
        if level <= 1:
          items.append(item)
          item = ""
        else:
          item += character
      else:
        item += character

    if item != "": items.append(item)
    return [ParseData(item) for item in items]
  else:
    return int(string)


def AreDataInRightOrder(left: Any, right: Any) -> Optional[bool]:
  if isinstance(left, int) and isinstance(right, int):
    return left < right if left != right else None
  elif isinstance(left, int):
    return AreDataInRightOrder([left], right)
  elif isinstance(right, int):
    return AreDataInRightOrder(left, [right])
  else:
    for leftItem, rightItem in zip(left, right):
      areItemsEqual = AreDataInRightOrder(leftItem, rightItem)
      if areItemsEqual is not None: return areItemsEqual

    return len(left) < len(right) if len(left) != len(right) else None


def CompareData(left: Any, right: Any) -> int:
  areDataInRightOrder = AreDataInRightOrder(left, right)
  assert areDataInRightOrder is not None
  return -1 if areDataInRightOrder else 1


def ComputeDecoderKey(packets: Sequence[Any], dividerPackets: Sequence[Any]) -> int:
  return math.prod(packets.index(dividerPacket) + 1 for dividerPacket in dividerPackets)


if __name__ == "__main__": Main()
