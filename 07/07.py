#!/usr/bin/python3

# Copyright (C) 2022 Julian Valentin
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pathlib
from typing import Dict, Optional


class VDirectory(object):
  def __init__(self, parentDirectory: Optional["VDirectory"]) -> None:
    self.parentDirectory = parentDirectory
    self.files: Dict[str, int] = {}
    self.subDirectories: Dict[str, VDirectory] = {}

  def GetAllTransitiveSubDirectories(self) -> Dict["VDirectory", int]:
    selfSize = sum(fileSize for fileSize in self.files.values())
    result: Dict[VDirectory, int] = {}

    for subDirectory in self.subDirectories.values():
      subSubDirectories = subDirectory.GetAllTransitiveSubDirectories()
      selfSize += subSubDirectories[subDirectory]
      result.update(subSubDirectories)

    result[self] = selfSize
    return result


def Main() -> None:
  input = pathlib.Path(__file__).with_name("input.txt").read_text()
  rootDirectory = ParseDirectoryTree(input)
  subDirectories = rootDirectory.GetAllTransitiveSubDirectories()
  totalSpace = 70000000
  requiredSpace = 30000000
  freeSpace = totalSpace - subDirectories[rootDirectory]
  print("Solution of part 1: {}".format(sum(size for size in subDirectories.values() if size <= 100000)))
  print("Solution of part 2: {}".format(
    min(size for size in subDirectories.values() if size >= requiredSpace - freeSpace)))


def ParseDirectoryTree(input: str) -> VDirectory:
  rootDirectory = VDirectory(None)
  currentDirectory = rootDirectory

  for line in input.splitlines():
    if line == "$ cd ..":
      assert currentDirectory.parentDirectory is not None
      currentDirectory = currentDirectory.parentDirectory
    elif line == "$ cd /":
      currentDirectory = rootDirectory
    elif line.startswith("$ cd "):
      subDirectoryName = line[5:]

      if subDirectoryName not in currentDirectory.subDirectories:
        currentDirectory.subDirectories[subDirectoryName] = VDirectory(currentDirectory)

      currentDirectory = currentDirectory.subDirectories[subDirectoryName]
    elif (line == "$ ls") or line.startswith("dir "):
      pass
    else:
      size, fileName = line.split()
      currentDirectory.files[fileName] = int(size)

  return rootDirectory


if __name__ == "__main__": Main()
