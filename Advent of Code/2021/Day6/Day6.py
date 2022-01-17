from collections import deque
from typing import List


def solution(starting_ages: List[int], generations: int) -> int:
    fish, offspring = deque([0] * 7), deque([0, 0])
    for age in starting_ages:
        fish[age] += 1

    for _ in range(generations):
        fish.rotate(-1)
        offspring.append(fish[0])
        fish[0] += offspring.popleft()

    return sum(fish) + offspring.popleft()


if __name__ == "__main__":
    with open("Advent of Code/2021/Day6/input.txt", "r") as f:
        my_list = [int(age) for age in f.read().split(",")]
        part1 = solution(my_list, 80)
        print(f"Part 1: {part1}")

        part2 = solution(my_list, 256)
        print(f"Part 2: {part2}")
