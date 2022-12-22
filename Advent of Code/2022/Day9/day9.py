from typing import NamedTuple
from enum import Enum

sample = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".splitlines()


class Position(NamedTuple):
    x: int
    y: int

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def manhattan_distance(self, other):
        x, y = self - other
        return abs(x) + abs(y)

    def adjacent(self, other):
        x, y = self - other
        if abs(x) == 1 and abs(y) == 1:
            return True
        elif self.manhattan_distance(other) > 1:
            return False
        else:
            return True


class Direction(Enum):
    U = Position(0, 1)
    D = Position(0, -1)
    L = Position(-1, 0)
    R = Position(1, 0)


def part_one(my_list):
    head = Position(0, 0)
    tail = Position(0, 0)
    tail_positions = set()
    tail_positions.add(tail)

    for instr in my_list:
        move, _, count = instr.partition(" ")
        dxn = Direction[move].value
        for _ in range(int(count)):
            head += dxn
            if not head.adjacent(tail):
                tail = head - dxn
                tail_positions.add(tail)

    return len(tail_positions)


if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day9/input.txt",
        "r",
    ) as f:
        ...
        my_list = [line.rstrip() for line in f]
        # print(my_list[:10])
        # part 1
        print("Part 1: ", part_one(my_list))

        # part 2
