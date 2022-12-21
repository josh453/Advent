import operator
from itertools import accumulate, islice, starmap
from typing import Iterable, Iterator
from PIL import Image

large_example = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".splitlines()

def execute_video_instr(instructions):
    yield from (1,0)

    for instr in instructions:
        match instr.split():
            case ["noop"]:
                yield 0
            case ["addx", delta]:
                yield 0
                yield int(delta)

def part_one(instructions):
    register_x = accumulate(execute_video_instr(instructions))
    cycles_and_deltas = islice(enumerate(register_x), 20, None, 40)
    signal_strengths = starmap(operator.mul, cycles_and_deltas)

    return sum(list(signal_strengths))

def race_the_beam(instructions):
    register_x = accumulate(execute_video_instr(instructions))
    next(register_x)

    for cycle, x in enumerate(register_x):
        pos = cycle % 40
        yield pos - 1 <= x <= pos + 1

def crt_image_output(instructions: Iterable[str], scale: int = 10) -> Image:
    def to_bytes() -> Iterator[int]:
        value = 0
        for i, bit in enumerate(islice(race_the_beam(instructions), 240)):
            value = (value << 1) | int(bit)
            if i % 8 == 7:
                yield value
                value = 0
    
    data = bytes(to_bytes())
    img = Image.frombytes("1", (40, 6), data)
    return img.resize((img.size[0] * scale, img.size[1] * scale))




if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day10/input.txt", "r") as f:
        ...
        my_list = [line.rstrip() for line in f]
        # print(my_list[:10])
        # part 1
        print("Part 1: ", part_one(my_list))
        
        # part 2
        img = crt_image_output(my_list)
        img.show()
