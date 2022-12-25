from typing import List

sample = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".splitlines()


def convert_snafu_to_dec(snafu: str, base=5) -> int:

    if "-" in snafu or "=" in snafu:
        ans = 0
        encoding_scheme = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}

        for idx, digit in enumerate(reversed(snafu)):
            ans += encoding_scheme[digit] * pow(base, idx)
        return ans

    else:
        return int(snafu, base)


def convert_dec_to_snafu(dec: int) -> str:
    snafu = ""
    encoding_scheme = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}

    # Recursively divide and utilize the remainder
    while dec > 0:
        snafu += encoding_scheme[(dec + 2) % 5 - 2]
        dec = round(dec / 5)
        # print(f"{dec=}")
    return snafu[::-1]


def part_one(data: List[str]) -> str:
    ans = 0
    for item in data:
        ans += convert_snafu_to_dec(item)

    return convert_dec_to_snafu(ans)


assert part_one(sample) == "2=-1=0"

if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day25/input.txt",
        "r",
    ) as f:
        data = f.read().splitlines()
        # print(my_list[:10])
        # part 1
        print("Part 1:", part_one(data))

        # # part 2
        # print("Part 2:", part_two(data))
