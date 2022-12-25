from dataclasses import dataclass, field
from typing import Self, List
from enum import Enum
from itertools import repeat, pairwise
import math
from fractions import Fraction

sample = ["498,4 -> 498,6 -> 496,6", "503,4 -> 502,4 -> 502,9 -> 494,9"]

# From day9
@dataclass
class Position:
    x: int
    y: int

    def __sub__(self, other: Self) -> Self:
        return Position(self.x - other.x, self.y - other.y)

    def __add__(self, other: Self) -> Self:
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other: Self) -> bool:
        return self.x - other.x == 0 and self.y - other.y == 0

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # From 2021, day5
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
            x_range = range(start_x, end_x - abs(slope.denominator), -slope.denominator)
        else:
            x_range = range(
                start_x, end_x + abs(slope.denominator), abs(slope.denominator)
            )

        # Determine the y coordinates
        if math.isclose(sdy, 0):
            y_range = repeat(start_y)
        elif sdy < 0:
            y_range = range(start_y, end_y - abs(slope.numerator), -slope.numerator)
        else:
            y_range = range(start_y, end_y + abs(slope.numerator), abs(slope.numerator))

        return {Position(x, y) for x, y in zip(x_range, y_range)}


class Direction(Enum):
    DOWN = Position(0, 1)
    DOWN_LEFT = Position(-1, 1)
    DOWN_RIGHT = Position(1, 1)


@dataclass
class CaveSystem:
    rocks: set[Position]
    sand_path: List[Position] = field(default_factory=lambda: [Position(500, 0)])

    @classmethod
    def from_text(cls, data: list[str]) -> Self:
        rocks = set()
        for entry in data:
            temp_list = []
            for coordinate in entry.split("->"):
                line_segment = list(map(int, coordinate.strip().split(",")))
                temp_list.append(Position(line_segment[0], line_segment[1]))

                for pair in pairwise(temp_list):
                    rocks |= pair[0].points_between(pair[1])

        return cls(rocks)

    @property
    def floor(self):
        return max(pos.y for pos in self.rocks)

    def find_single_grain_resting_position(
        self, occupied: set[Position], floor: int, position: Position = Position(500, 0)
    ):
        """Find the resting position of a single grain of sand given the occupied spaces"""
        while True:
            for d in Direction:
                if (position + d.value) not in occupied:
                    if position.y <= floor:
                        position = position + d.value
                        # Append to the path the previous position before resting
                        # We can use this to traverse up the path instead of following
                        # every grain from the top
                        self.sand_path.append(position - d.value)
                        # print(self.sand_path)
                        break
                    else:
                        # Sand has hit the floor
                        # print(f"Sand has hit the floor at {self.sand_path[-1]}")
                        return
            else:
                return position

    def full_simulation(self, occupied=None, floor=None, has_floor=False):
        """Simulate all grains of sand

        Algorithm steps:

            1. Take the grain of sand and find it's resting position while saving all the positions it traversed on it's way down
                - Check to see if the grain is in free fall
                    - If has_floor is False then stop the simulation and return the difference between the starting number of rocks
                      and the now occuppied spaces
                    - If has_floor is true, add a rock in it's path and continue
            2. Add the final resting position to the set of occuppied positions
            3. Take the last element of the traversal path and use that as the starting position for the next grain
            4.

        """
        if occupied is None:
            occupied = set(self.rocks)

        if floor is None:
            floor = self.floor

        resting_pos = self.find_single_grain_resting_position(
            occupied=occupied, floor=floor
        )

        if not has_floor:
            while True:
                if resting_pos is None:
                    break
                occupied.add(resting_pos)
                next_sand = self.sand_path.pop()
                resting_pos = self.find_single_grain_resting_position(
                    occupied=occupied, floor=floor, position=next_sand
                )

        if has_floor:
            while True:

                if not self.sand_path:
                    return len(occupied) - len(self.rocks)

                # Sand is free falling, so we add a rock to in it's way
                if resting_pos is None:
                    self.rocks.add(self.sand_path.pop())
                    occupied = set(self.rocks)
                else:
                    occupied.add(resting_pos)

                next_sand = self.sand_path.pop()
                resting_pos = self.find_single_grain_resting_position(
                    occupied=occupied, floor=floor + 2, position=next_sand
                )

        return len(occupied) - len(self.rocks)


test = CaveSystem.from_text(sample)


assert test.full_simulation() == 24
assert test.full_simulation(has_floor=True) == 93

if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day14/input.txt",
        "r",
    ) as f:
        my_list = f.readlines()
        cave = CaveSystem.from_text(my_list)
        # part 1
        print("Part 1:", cave.full_simulation())

        # # part 2
        print("Part 2:", cave.full_simulation(has_floor=True))
