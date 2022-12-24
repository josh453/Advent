from dataclasses import dataclass
from typing import Self, NamedTuple
from enum import Enum
from itertools import repeat, pairwise
import math
from fractions import Fraction

sample = [
"498,4 -> 498,6 -> 496,6",
# "503,4 -> 502,4 -> 502,9 -> 494,9"
]

# From day9
class Position(NamedTuple):
    x: int
    y: int

    def __sub__(self, other: Self) -> Self:
        return Position(self.x - other.x, self.y - other.y)

    def __add__(self, other: Self) -> Self:
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other:Self) -> bool:
        return self.x - other.x == 0 and self.y - other.y == 0

    def points_between(self, other: Self):

        start_x, start_y = self.x, self.y
        end_x, end_y = other.x, other.y
        sdx = other.x - self.x
        sdy = other.y - self.y

        try:
            slope = Fraction(sdy, sdx)
        except ZeroDivisionError:
            slope = Fraction(1, 1)

        # Determine the x coordinates
        if math.isclose(sdx, 0):
            x_range = repeat(start_x)
        elif sdx < 0:
            x_range = range(
                start_x, end_x - abs(slope.denominator), slope.denominator
            )
            print(slope.denominator)
        else:
            x_range = range(
                start_x, end_x + abs(slope.denominator), abs(slope.denominator)
            )
        print(x_range)

        # Determine the y coordinates
        if math.isclose(sdy, 0):
            y_range = repeat(start_y)
        elif sdy < 0:
            y_range = range(start_y, end_y - abs(slope.numerator), slope.numerator)
        else:
            y_range = range(start_y, end_y + abs(slope.numerator), abs(slope.numerator))
        print(y_range)

        return [Position(x, y) for x, y in zip(x_range, y_range)]

x = Position(498,6)
y = Position(496,6)

print(x.points_between(y))


class Direction(Enum):
    DOWN = Position(0, 1)
    DOWN_LEFT = Position(-1, 1)
    DOWN_RIGHT = Position(1, -1)

@dataclass
class CaveSystem:
    rocks = set[Position]

    @classmethod
    def from_text(cls, data: list[str]):
        for entry in data:
            for coordinate in data.split("->"):
                ...



# list(map(lambda x: int(x), data))
s = set()
l = []
for item in sample:
    for coord in item.split("->"):
        # print(coord)
        a = list(map(int, coord.strip().split(",")))
        l.append(Position(a[0], a[1]))
        # b = iter(map(int, a))
        # print(next(b))
        # print(next(b))

# print(l)
# for p in pairwise(l):
#     print(p[0].between(p[1]))


if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day14/input.txt",
        "r",
    ) as f:
        my_list = f.readlines()
        # print(my_list[0])
        # print(my_list[:10])
        # part 1
        # print("Part 1:", sum(i for i, (p1, p2) in enumerate(pairs, 1) if packet_analyzer(p1, p2) > 0))

        # # part 2
        # print("Part 2: ", decoder(my_list))
