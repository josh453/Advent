from typing import NamedTuple
from dataclasses import dataclass
from itertools import combinations

class Point(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

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

    @property
    def straight(self) -> bool:
        return self.start.x == self.end.x or self.start.y == self.end.y
    

class LineIntersection:

    def __init__(self, AB:Line, CD:Line) -> None:
        self.AB = AB
        self.CD = CD
    
    @staticmethod
    def is_counter_clockwise(A:Point,B: Point,C: Point) -> bool:
        """
        Given 3 points, determine if they are listed in counter-clockwise order

        If slope of AB is less than slope of AC then the points are counter-clockwise
        """
        slope_ab = (C.y-A.y)*(B.x-A.x)
        slope_ac = (B.y-A.y)*(C.x-A.x)
        
        return slope_ab > slope_ac
    
    @staticmethod
    def determinant(a,b,c,d):
        """
        Return the determinant of a 2x2 matrix
        """
        return a * d - c * b
    
    @property
    def is_intersected(self) -> bool:
        """
        Given line segments AB and CD determine if they intersect

        If AB intersects CD then either ACD or BCD should be in counter-clockwise orientation
        """
        A = self.AB.start
        B = self.AB.end
        C = self.CD.start
        D = self.CD.end

        acd_not_bcd = self.is_counter_clockwise(A,C,D) != self.is_counter_clockwise(B,C,D)
        abc_not_abd = self.is_counter_clockwise(A,B,C) != self.is_counter_clockwise(A,B,D)
        
        return acd_not_bcd and abc_not_abd
    
    @property
    def intersection_point(self) -> Point:
        """
        Based on https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
        """

        x1_diff_x2 = self.AB.start.x - self.AB.end.x
        x1_diff_x3 = self.AB.start.x - self.CD.start.x
        x3_diff_x4 = self.CD.start.x - self.CD.end.x

        y1_diff_y2 = self.AB.start.y - self.AB.end.y
        y1_diff_y3 = self.AB.start.y - self.CD.start.y
        y3_diff_y4 = self.CD.start.y - self.CD.end.y

        t = self.determinant(x1_diff_x3, x3_diff_x4, y1_diff_y3, y3_diff_y4) / self.determinant(x1_diff_x2, x3_diff_x4, y1_diff_y2, y3_diff_y4)
        x_intersect = self.AB.start.x + t * (self.AB.end.x - self.AB.start.x)
        y_intersect = self.AB.start.y + t * (self.AB.end.y - self.AB.start.y)

        return Point(x_intersect, y_intersect)
    

sample = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]

A = Point(0,9)
B = Point(5,9)
C = Point(0,9)
D = Point(2,9)

AB = Line(A, B)
CD = Line(C, D)

dx, dy = AB.end.x - AB.start.x, AB.end.y - AB.start.y
print(dx * (p.y - AB.start.y) - (p.x - AB.start.x) * dy)

intersection = LineIntersection(AB,CD)

print(intersection.is_intersected)

# def part1_solution(input):

#     line_segments = map(Line.from_string, input)

#     intersected_points = set()
#     for AB, CD in combinations(line_segments, 2):
#         if AB.straight and CD.straight:
#             print(AB, CD)
#             inter = LineIntersection(AB, CD)
#             print(inter.is_intersected)
#             if inter.is_intersected:
#                 intersected_points |= {inter.intersection_point}

#     return len(intersected_points)

# print(part1_solution(sample))
# for line in line_segments:
#     if line.straight:
#         print(line)


# if __name__ == "__main__":
#     with open("Day5/input.txt", "r") as f:
#         my_list = [line.rstrip() for line in f]
#         print(my_list)