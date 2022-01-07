import math
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, count, repeat
from typing import List, NamedTuple

from num import count_crossings, read_file


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
                start_x, start_x - abs(slope.denominator), slope.denominator
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
        # eps = 10e-5
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

                t = self.determinant(
                    x1_diff_x3, x3_diff_x4, y1_diff_y3, y3_diff_y4
                ) / self.determinant(x1_diff_x2, x3_diff_x4, y1_diff_y2, y3_diff_y4)
                x_intersect = self.start.x + t * (self.end.x - self.start.x)
                y_intersect = self.start.y + t * (self.end.y - self.start.y)

                # Check that diagonal lines intersect at integer coordinates
                if not (self.straight or other.straight):
                    # intercepts of the diagonals must both be odd or even
                    sdx, sdy = self.end.x - self.start.x, self.end.y - self.start.y
                    odx, ody = other.end.x - other.start.x, other.end.y - other.start.y
                    sparity = (self.start.y + (sdy // sdx) * self.start.x) % 2
                    oparity = (other.start.y + (ody // odx) * other.start.x) % 2
                    if sparity != oparity:
                        return False

                return Point(x_intersect, y_intersect)

        # print("Line segments are not parallel and do not intersect")
        return False


class LineIntersection:
    def __init__(self, AB: Line, CD: Line) -> None:
        self.AB = AB
        self.CD = CD

    @staticmethod
    def is_counter_clockwise(A: Point, B: Point, C: Point) -> bool:
        """
        Given 3 points, determine if they are listed in counter-clockwise order

        If slope of AB is less than slope of AC then the points are counter-clockwise
        """
        slope_ab = (C.y - A.y) * (B.x - A.x)
        slope_ac = (B.y - A.y) * (C.x - A.x)

        return slope_ab > slope_ac

    @staticmethod
    def determinant(a, b, c, d):
        """
        Return the determinant of a 2x2 matrix
        """
        return a * d - c * b

    @property
    def is_intersected(self) -> bool:
        """
        Given line segments AB and CD determine if they intersect at a single point

        If AB intersects CD then either ACD or BCD should be in counter-clockwise orientation
        """
        A = self.AB.start
        B = self.AB.end
        C = self.CD.start
        D = self.CD.end

        acd_not_bcd = self.is_counter_clockwise(A, C, D) != self.is_counter_clockwise(
            B, C, D
        )
        abc_not_abd = self.is_counter_clockwise(A, B, C) != self.is_counter_clockwise(
            A, B, D
        )

        return acd_not_bcd and abc_not_abd

    @property
    def intersection_point(self) -> Point:
        """
        Based on https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
        """

        # A: (x1, y1)
        # B: (x2, y2)
        # C: (x3, y3)
        # D: (x4, y4)
        x1_diff_x2 = self.AB.start.x - self.AB.end.x
        x1_diff_x3 = self.AB.start.x - self.CD.start.x
        x3_diff_x4 = self.CD.start.x - self.CD.end.x

        y1_diff_y2 = self.AB.start.y - self.AB.end.y
        y1_diff_y3 = self.AB.start.y - self.CD.start.y
        y3_diff_y4 = self.CD.start.y - self.CD.end.y

        t = self.determinant(
            x1_diff_x3, x3_diff_x4, y1_diff_y3, y3_diff_y4
        ) / self.determinant(x1_diff_x2, x3_diff_x4, y1_diff_y2, y3_diff_y4)
        x_intersect = self.AB.start.x + t * (self.AB.end.x - self.AB.start.x)
        y_intersect = self.AB.start.y + t * (self.AB.end.y - self.AB.start.y)

        # Check that diagonal lines intersect at integer coordinates
        if not x_intersect.is_integer() or not y_intersect.is_integer():
            return None

        return Point(x_intersect, y_intersect)

    @property
    def is_overlap(self) -> bool:
        """
        Given line segments AB and CD determine if they are colinear and overlap
        """
        cross_start = self.AB * self.CD.start
        cross_end = self.AB * self.CD.end
        # Colinear
        if cross_start == 0 and cross_end == 0:
            return True
        else:
            return False

    @property
    def overlapping_points(self):
        return set(self.AB.line_points) & set(self.CD.line_points)


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


# AB = "600,773 -> 546,773"
# CD = "831,773 -> 32,773"


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


# def part1_solution(input):

#     line_segments = map(Line.from_string, input)

#     intersected_points = set()
#     for segment_1 in line_segments:
#         for segment_2 in line_segments:
#             if segment_1 == segment_2:
#                 pass
#             elif segment_1.straight and segment_2.straight:
#                 overlapping_points = segment_1 & segment_2
#                 if overlapping_points:
#                     if isinstance(overlapping_points, Point):
#                         overlapping_points = set([overlapping_points])
#                         intersected_points |= overlapping_points
#                     else:
#                         intersected_points |= overlapping_points

#     return len(intersected_points)


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


def turn_to_example(arr: List):
    lines = [line.split(" -> ") for line in arr]
    return [
        [(int(s[0]), int(s[1])) for s in (x.split(",") for x in line)] for line in lines
    ]


print(part1_solution(sample))

if __name__ == "__main__":
    AB = "591,357 -> 30,918"
    CD = "25,923 -> 904,44"

    # sample = [AB, CD]
    # temp_vals = turn_to_example(sample)
    # print("Example function:")
    # print(count_crossings(temp_vals, allow_diagonal=True))

    # LINE_AB = Line.from_string(CD)  # (0,9), (1,9), (2,9), (3,9), (4,9), (5,9)
    # LINE_CD = Line.from_string(AB)  # (0,9), (1,9), (2,9)
    # print("My function")
    # if LINE_AB & LINE_CD:
    #     print(len(LINE_AB & LINE_CD))
    with open("Advent of Code/2021/Day5/input.txt", "r") as f:
        my_list = [line.rstrip() for line in f]
    #     # print(part1_solution(my_list))
    #     # print(part2_solution(my_list))
    sample_counter = int()
    my_counter = int()
    for seg1, seg2 in combinations(my_list, 2):
        sample = [seg1, seg2]
        temp_vals = turn_to_example(sample)
        sample_counts = count_crossings(temp_vals, allow_diagonal=True)
        my_counts = part2_solution(sample)
        sample_counter += sample_counts
        my_counter += my_counts
        if sample_counts != my_counts:
            print(f"Do not align:\n{sample}")
            break
    print(f"{sample_counter=}")
    print(f"{my_counter=}")

# Answer: 7318
# sol = part1_solution(my_list)

# # print(part1_solution(my_list))

# # Guesses: 14955, 14954, 16360
# # Answer: 19939
# print(part2_solution(my_list))

# text_chunk_size = 29

# for idx in range(len(s) // text_chunk_size):
#     # 15 .. 0,1,2,3
#     first_idx = idx * text_chunk_size
#     second_idx = first_idx + text_chunk_size
#     print(s[first_idx:second_idx])
