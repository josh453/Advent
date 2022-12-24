import math
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, repeat
from typing import List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Return the cross product"""
        return self.x * other.y - self.y * other.x

    def __and__(self, other):
        """Return the dot product"""
        return self.x * other.x + self.y * other.y

    @classmethod
    def from_str(cls, s: str):
        return cls(*map(int, s.split(",")))


@dataclass
class Line:
    start: Point
    end: Point

    @classmethod
    def from_string(cls, line: str):
        return cls(*sorted(map(Point.from_str, line.split("->"))))

    @staticmethod
    def determinant(a, b, c, d):
        """
        Return the determinant of a 2x2 matrix
        """
        return a * d - c * b

    @property
    def straight(self) -> bool:
        return self.start.x == self.end.x or self.start.y == self.end.y

    @property
    def end_start_diff(self) -> Point:
        return self.end - self.start

    @property
    def line_points(self):
        start_x, start_y = self.start.x, self.start.y
        end_x, end_y = self.end.x, self.end.y
        sdx = self.end.x - self.start.x
        sdy = self.end.y - self.start.y

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
        else:
            x_range = range(
                start_x, end_x + abs(slope.denominator), abs(slope.denominator)
            )

        # Determine the y coordinates
        if math.isclose(sdy, 0):
            y_range = repeat(start_y)
        elif sdy < 0:
            y_range = range(start_y, end_y - abs(slope.numerator), slope.numerator)
        else:
            y_range = range(start_y, end_y + abs(slope.numerator), abs(slope.numerator))

        return [Point(x, y) for x, y in zip(x_range, y_range)]

    def __mul__(self, p: Point):
        """
        Calculate the cross product of the line and Point p, useful for determining colinearity

        If the cross product == 0, then a scalar of Line exists that includes Point p
        """
        dx, dy = self.end.x - self.start.x, self.end.y - self.start.y
        return dx * (p.y - self.start.y) - (p.x - self.start.x) * dy

    def __and__(self, other):
        """
        Return True if the two lines intersect

        Adapted from:
        https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect

        """
        # * is the cross product for two Points
        # & is the dot product for two Points
        r = self.end_start_diff
        s = other.end_start_diff
        q = other.start
        p = self.start
        v = q - p
        r_cross_s = r * s
        r_dot_r = r & r
        s_dot_s = s & s
        q_minus_p_cross_r = (q - p) * r
        q_minus_p_cross_s = (q - p) * s

        # Lines are colinear
        if math.isclose(r_cross_s, 0) and math.isclose(q_minus_p_cross_r, 0):
            # print("Line segments are colinear")
            v_dot_r = v & r
            a_dot_s = (p - q) & s

            # They overlap
            if (0 <= v_dot_r <= r_dot_r) or (0 <= a_dot_s <= s_dot_s):
                # print("Line segments overlap")
                return set(self.line_points) & set(other.line_points)
            else:
                return False

        elif math.isclose(r_cross_s, 0) and q_minus_p_cross_r != 0:
            # print("Line segments are parallel and do not intersect")
            return False

        # Lines intersect at exactly one-point
        elif r_cross_s != 0:
            t = q_minus_p_cross_s / r_cross_s
            u = q_minus_p_cross_r / r_cross_s
            if (0 <= t <= 1) and (0 <= u <= 1):
                x1_diff_x2 = self.start.x - self.end.x
                x1_diff_x3 = self.start.x - other.start.x
                x3_diff_x4 = other.start.x - other.end.x

                y1_diff_y2 = self.start.y - self.end.y
                y1_diff_y3 = self.start.y - other.start.y
                y3_diff_y4 = other.start.y - other.end.y

                det = self.determinant(
                    x1_diff_x3, x3_diff_x4, y1_diff_y3, y3_diff_y4
                ) / self.determinant(x1_diff_x2, x3_diff_x4, y1_diff_y2, y3_diff_y4)
                x_intersect = self.start.x + det * (self.end.x - self.start.x)
                y_intersect = self.start.y + det * (self.end.y - self.start.y)

                # Check that diagonal lines intersect at integer coordinates
                if not (self.straight or other.straight):
                    sdx, sdy = self.end.x - self.start.x, self.end.y - self.start.y
                    odx, ody = other.end.x - other.start.x, other.end.y - other.start.y
                    sparity = (self.start.y + (sdy // sdx) * self.start.x) % 2
                    oparity = (other.start.y + (ody // odx) * other.start.x) % 2
                    if sparity != oparity:
                        return False

                return Point(round(x_intersect), round(y_intersect))

        # print("Line segments are not parallel and do not intersect")
        return False


def part1_solution(input):

    line_segments = map(Line.from_string, input)

    intersected_points = set()
    for segment_1, segment_2 in combinations(line_segments, 2):
        if segment_1.straight and segment_2.straight:
            overlapping_points = segment_1 & segment_2
            if overlapping_points:
                if isinstance(overlapping_points, Point):
                    overlapping_points = set([overlapping_points])
                    intersected_points |= overlapping_points
                else:
                    intersected_points |= overlapping_points

    return len(intersected_points)


def part2_solution(input):

    line_segments = map(Line.from_string, input)

    intersected_points = set()
    for segment_1, segment_2 in combinations(line_segments, 2):
        overlapping_points = segment_1 & segment_2
        if overlapping_points:
            if isinstance(overlapping_points, Point):
                overlapping_points = set([overlapping_points])
                intersected_points |= overlapping_points
            else:
                intersected_points |= overlapping_points

    return len(intersected_points)


sample = [
    "0,9 -> 5,9",  #
    "8,0 -> 0,8",
    "9,4 -> 3,4",  #
    "2,2 -> 2,1",  #
    "7,0 -> 7,4",  #
    "6,4 -> 2,0",
    "0,9 -> 2,9",  #
    "3,4 -> 1,4",  #
    "0,0 -> 8,8",  #
    "5,5 -> 8,2",  #
]

assert part1_solution(sample) == 5
assert part2_solution(sample) == 12

if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2021/Day5/input.txt", "r") as f:
        my_list = [line.rstrip() for line in f]
        print(f"Part 1: {part1_solution(my_list)}")
        print(f"Part 2: {part2_solution(my_list)}")
