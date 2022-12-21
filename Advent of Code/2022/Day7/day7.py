from abc import ABC, abstractmethod
from collections import deque
from functools import cached_property
from dataclasses import dataclass, field
from typing import Iterable, Iterator, List, Union, Dict, Optional, Any, Self

sample = [
"$ cd /",
"$ ls",
"dir a",
"14848514 b.txt",
"8504156 c.dat",
"dir d",
"$ cd a",
"$ ls",
"dir e",
"29116 f",
"2557 g",
"62596 h.lst",
"$ cd e",
"$ ls",
"584 i",
"$ cd ..",
"$ cd ..",
"$ cd d",
"$ ls",
"4060174 j",
"8033020 d.log",
"5626152 d.ext",
"7214296 k",
]

example = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".splitlines()


"""
Supported commands:
cd / = go to outermost
cd .. = moves up a level
cd <name> = move to that directory
ls = list all files and directories in current
"""

@dataclass
class Entry(ABC):
    name: str

    @property
    @abstractmethod
    def size(self) -> int:
        ...

    @classmethod
    def from_ls_output(cls, size_or_dir: str, name: str) -> Self:
        return Directory(name) if size_or_dir == "dir" else File(name, int(size_or_dir))



@dataclass
class File(Entry):
    _size: int

    @property
    def size(self) -> int:
        return self._size

@dataclass
class Directory(Entry):
    entries: dict[str, Entry] = field(default_factory=dict)

    @cached_property
    def size(self) -> int:
        return sum(entry.size for entry in self.entries.values())
    
    def __iadd__(self, entry: Entry) -> Self:
        self.entries[entry.name] = entry
        return self
    
    def __contains__(self, name: str) -> bool:
        return name in self.entries
    
    def __getitem__(self, name: str) -> Entry:
        return self.entries[name]

# root = Directory(name='/')
# path = [root]
# print(path[-1])


@dataclass
class Filesystem:
    root: Directory

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        root = Directory("/")
        path = [root]
        for line in lines:
            cwd = path[-1]
            match line.split():
                case ["$", "ls"]:
                    continue
                case ["$", "cd", "/"]:
                    path = [root]
                case ["$", "cd", ".."]:
                    if cwd is not root:
                        path.pop()
                case ["$", "cd", name] if name in cwd and isinstance(cwd[name], Directory):
                    path.append(cwd[name])
                case ["$", "cd", name]:
                    raise ValueError(f"Invalid path: {name}")
                case ["$", *cmd]:
                    raise ValueError("Unknown command: {' '.join(cmd)}")
                case [size_or_dir, name]:
                    cwd += Entry.from_ls_output(size_or_dir, name)
                case _:
                    raise ValueError("Unknown output: {line}")
        return cls(root)

    def walk(self) -> Iterator[tuple[Directory, list[str]]]:
        """Traverse the filesystem directories in depth-first order.

        The second element is the list of subdirectory names; you can remove directories from this list
        to prune traversal.

        """
        stack = deque([self.root])
        while stack:
            cwd = stack.pop()
            names = [name for name, entry in cwd.entries.items() if isinstance(entry, Directory)]
            yield cwd, names
            for name in reversed(names):
                stack.append(cwd.entries[name])


AVAILABLE = 70000000
TARGET_FREE = 30000000
MAX_USED = AVAILABLE - TARGET_FREE

def find_space(filesystem: Filesystem) -> int:
    total = filesystem.root.size
    if total <= MAX_USED:
        return 0
    min_size = total - MAX_USED
    def dirsizes() -> Iterator[int]:
        for dir, dirnames in filesystem.walk():
            if dir.size < min_size:
                # prune search
                dirnames.clear()
                continue
            yield dir.size
    return min(dirsizes())


if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day7/input.txt", "r") as f:
        ...
        # part 1
        filesystem = Filesystem.from_lines(f.readlines())
        print("Part 1:", sum(size for dir, _ in filesystem.walk() if (size := dir.size) < 100000))

        # part 2
        print("Part 2:", find_space(filesystem))
        