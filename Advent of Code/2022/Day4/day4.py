sample = [
    "2-4,6-8",  # False
    "2-3,4-5",  # False
    "5-7,7-9",  # True
    "2-8,3-7",  # True
    "6-6,4-6",  # True
    "2-6,4-8",  # True
]


def part_one(my_list):
    score = 0
    for item in my_list:
        first_segment = item.split(",")[0].split("-")
        second_segment = item.split(",")[1].split("-")
        first_x, second_x = int(first_segment[0]), int(first_segment[1])
        third_x, fourth_x = int(second_segment[0]), int(second_segment[1])
        delta_one_three = first_x - third_x
        delta_two_four = second_x - fourth_x
        if delta_one_three <= 0 and delta_two_four >= 0:
            score += 1
        elif delta_one_three >= 0 and delta_two_four <= 0:
            score += 1
    return score


def part_two(my_list):
    score = 0
    for item in my_list:
        first_segment = item.split(",")[0].split("-")
        second_segment = item.split(",")[1].split("-")
        first_x, second_x = int(first_segment[0]), int(first_segment[1])
        third_x, fourth_x = int(second_segment[0]), int(second_segment[1])
        if second_x - third_x < 0 and first_x - fourth_x < 0:
            pass
        elif second_x - third_x > 0 and first_x - fourth_x > 0:
            pass
        else:
            score += 1

    return score


if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day4/input.txt",
        "r",
    ) as f:
        my_list = [line.rstrip() for line in f]
        # part 1
        print(part_one(my_list))

        # part 2
        print(part_two(my_list))
