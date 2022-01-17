from typing import Tuple


def find_x_y_position(iterable: list) -> Tuple[int, int]:
    """
    Given a list of directions, return the depth and horizontal position
    """
    x = int()
    y = int()
    for direction in iterable:
        if "forward" in direction:
            x += int(direction[-1])
        if "up" in direction:
            y -= int(direction[-1])
        if "down" in direction:
            y += int(direction[-1])

    return x, y


def find_x_y_position_with_aim(iterable: list) -> Tuple[int, int]:
    """
    Given a list of directions, return the depth and horizontal position using aim
    """
    x = int()
    y = int()
    aim = int()
    for direction in iterable:
        if "forward" in direction:
            x += int(direction[-1])
            y += int(direction[-1]) * aim
        if "up" in direction:
            aim -= int(direction[-1])
        if "down" in direction:
            aim += int(direction[-1])

    return x, y


if __name__ == "__main__":
    with open("Day2/input.txt", "r") as f:
        my_list = [line.rstrip() for line in f]

        # Part 1
        x, y = find_x_y_position(my_list)
        print(f"Part 1: {x*y}")

        # Part 2
        x, y = find_x_y_position_with_aim(my_list)
        print(f"Part 2: {x*y}")
