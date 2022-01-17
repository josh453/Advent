from math import ceil
from statistics import mean, median
from typing import List


def triangle_cost(num: int):
    return (num ** 2 + num) // 2


def part1(start_positions: List[int]) -> int:
    target = int(median(start_positions))
    fuel_needed = int()

    for position in start_positions:
        fuel_needed += abs(position - target)

    return fuel_needed


def part2(start_positions: List[int]) -> int:
    # It's unclear whether rounding up or down will cost more fuel, so we calculate both
    target = mean(start_positions)
    fuel_needed_up, fuel_needed_down = int(), int()

    for position in start_positions:
        fuel_needed_up += triangle_cost(abs(position - int(target)))
        fuel_needed_down += triangle_cost(abs(position - ceil(target)))

    return min(fuel_needed_up, fuel_needed_down)


if __name__ == "__main__":
    with open("Advent of Code/2021/Day7/input.txt", "r") as f:
        my_list = [int(pos) for pos in f.read().split(",")]

        part1 = part1(my_list)
        print(f"Part 1: {part1}")

        part2 = part2(my_list)
        print(f"Part 2: {part2}")
