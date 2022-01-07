import math
from fractions import Fraction
from itertools import repeat

from Day5 import Line

# # Diagonal intersection at non-integers
# # AB, CD = Line.from_string("10,0 -> 7,4"), Line.from_string("9,0 -> 9,4")
# # assert AB & CD == False

# # Straight intersection at integers
# AB, CD = Line.from_string("12,4 -> 7,4"), Line.from_string("9,0 -> 9,4")
# assert AB & CD == Point(9, 4)

# # Intersect at end point
# AB, CD = Line.from_string("12,4 -> 9,4"), Line.from_string("9,0 -> 9,4")
# assert AB & CD == Point(9, 4)

# # Intersect at end point
# CD, AB = Line.from_string("12,4 -> 9,4"), Line.from_string("9,0 -> 9,4")
# assert AB & CD == Point(9, 4)

# # Diagonal and straight intersection at end point
# AB, CD = Line.from_string("11,2 -> 7,6"), Line.from_string("9,0 -> 9,4")
# assert AB & CD == Point(9, 4)

# # Straight overlap
# AB, CD = Line.from_string("11,6 -> 7,6"), Line.from_string("8,6 -> 13,6")
# assert AB & CD == {Point(8, 6), Point(9, 6), Point(10, 6), Point(11, 6)}

# # Disjoint straight
# AB, CD = Line.from_string("2,6 -> 5,6"), Line.from_string("8,6 -> 13,6")
# assert AB & CD == False
AB = "591,357 -> 30,918"
CD = "25,923 -> 904,44"
start_x, start_y = 25, 923
end_x, end_y = 904, 44
sdy = end_y - start_y
sdx = end_x - start_x

try:
    slope = Fraction(sdy, sdx)
except ZeroDivisionError as e:
    slope = Fraction(1, 1)

# if sdx < 0:
#     start_x, end_x = end_x, start_x
# if sdy < 0:
#     start_y, end_y = end_y, start_y

print(slope.numerator, slope.denominator)
# Determine the x coordinates
if math.isclose(sdx, 0):
    x_range = repeat(start_x)
elif sdx < 0:
    x_range = range(start_x, start_x - abs(slope.denominator), slope.denominator)
else:
    x_range = range(start_x, end_x + abs(slope.denominator), abs(slope.denominator))

# Determine the y coordinates
if math.isclose(sdy, 0):
    y_range = repeat(start_y)
elif sdy < 0:
    y_range = range(start_y, end_y - abs(slope.numerator), slope.numerator)
else:
    y_range = range(start_y, end_y + abs(slope.numerator), abs(slope.numerator))


# x_range = [xs for xs in x_range]
# y_range = [ys for ys in y_range]
points = [(x, y) for x, y in zip(x_range, y_range)]
print("X Coordinates")
print(x_range)
print("Y Coordinates")
print(y_range)
# print(points)

# print(len(list(x_range)))
# print(len(list(y_range)))
# CD = "25,923 -> 904,44"
# AB = Line.from_string("591,357 -> 30,918")
# # AB = Line.from_string("4,7 -> 1,1")
# print(AB.line_points)
