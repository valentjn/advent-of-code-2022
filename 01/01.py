#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  elves = [[int(calories) for calories in elf.splitlines()] for elf in input.split("\n\n")]
  elfSums = sorted((sum(elf) for elf in elves), reverse=True)
  print("Solution of part 1: {}".format(max(elfSums)))
  print("Solution of part 2: {}".format(sum(elfSums[:3])))


if __name__ == "__main__": Main()
