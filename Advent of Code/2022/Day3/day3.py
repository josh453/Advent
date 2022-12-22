import string

scores = range(1, 53)
alphabet = string.ascii_letters
scoring_dict = dict(zip(alphabet, scores))

sample = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw",
]


def split_strings(s):
    first_half = s[: len(s) // 2]
    second_half = s[len(s) // 2 :]
    return first_half, second_half


def batch(iterable, n=2):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


def part_one(my_list):
    score = 0
    for item in my_list:
        first_rucksack, second_rucksack = split_strings(item)
        intersection = set(first_rucksack) & set(second_rucksack)
        unsetted_answer = next(iter(intersection))
        score += scoring_dict.get(unsetted_answer, 0)
    return score


def part_two(my_list):
    score = 0
    for item in batch(my_list, 3):
        one, two, three = item
        intersection = set(one) & set(two) & set(three)
        unsetted_answer = next(iter(intersection))
        score += scoring_dict.get(unsetted_answer, 0)
    return score


if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day3/input.txt",
        "r",
    ) as f:
        my_list = [line.rstrip() for line in f]
        # part 1
        print(part_one(my_list))

        # part 2
        print(part_two(my_list))
