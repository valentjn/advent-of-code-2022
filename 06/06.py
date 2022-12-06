#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib


def Main() -> None:
  signal = pathlib.Path(__file__).with_name("input.txt").read_text()
  print("Solution of part 1: {}".format(FindStartOfPacket(signal, 4)))
  print("Solution of part 2: {}".format(FindStartOfPacket(signal, 14)))


def FindStartOfPacket(signal: str, length: int) -> int:
  return next(index for index in range(length, len(signal)) if len(set(signal[index - length:index])) == length)


if __name__ == "__main__": Main()
