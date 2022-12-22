from collections import deque

sample = """\
1
2
-3
3
-2
0
4
""".splitlines()


def find_og_zero_idx(data: list[str]) -> tuple[int, int]:
    """Find the original location of the zero value and its index"""
    my_list = list(map(lambda x: int(x), data))

    return my_list.index(0), 0


def mix(data: list[str], rounds: int = 1, key: int = 1) -> deque:
    """Mix up the data for the number of rounds specified"""

    # Use enumerate to make a unique tuple of index, value to accommodate duplicate values
    enumerated_deque = deque(enumerate(map(lambda x: int(x) * key, data)))
    og_order = list(enumerated_deque)

    for _ in range(rounds):
        for item in og_order:

            # Rotate until we find the item we are looking for
            # placing it at the front of the queue
            num_rotations = enumerated_deque.index(item)
            enumerated_deque.rotate(-num_rotations)

            # Pop the item off and rotate that many times
            num_rotations = enumerated_deque.popleft()[1]
            enumerated_deque.rotate(-num_rotations)

            # Append the item back onto the queue after the rotation
            enumerated_deque.appendleft(item)

    return enumerated_deque


def part_one(data: list[str]) -> int:

    # We'll need to know where to find the zero later for the answer
    og_zero_idx = find_og_zero_idx(data)
    mixed_up_deque = mix(data)

    new_zero_idx = mixed_up_deque.index(og_zero_idx)
    answer = 0
    for offset in (1_000, 2_000, 3_000):
        val_idx = (new_zero_idx + offset) % len(mixed_up_deque)
        answer += mixed_up_deque[val_idx][1]

    return answer


def part_two(data: list[str]) -> int:

    # We'll need to know where to find the zero later for the answer
    og_zero_idx = find_og_zero_idx(data)
    mixed_up_deque = mix(data, rounds=10, key=811589153)

    new_zero_idx = mixed_up_deque.index(og_zero_idx)
    answer = 0
    for offset in (1_000, 2_000, 3_000):
        val_idx = (new_zero_idx + offset) % len(mixed_up_deque)
        answer += mixed_up_deque[val_idx][1]

    return answer


assert part_one(sample) == 3
assert part_two(sample) == 1623178306

if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day20/input.txt",
        "r",
    ) as f:
        data = f.read().splitlines()
        # print(my_list[:10])
        # part 1
        print("Part 1:", part_one(data))

        # # part 2
        print("Part 2:", part_two(data))
