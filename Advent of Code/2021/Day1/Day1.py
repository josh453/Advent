def greater_than_previous_counter(iterable: list) -> int:
    """
    Return a count of the number of times the i + 1 > i
    """
    ctr = int()
    for i, j in zip(iterable, iterable[1:]):
        if int(j) > int(i):
            ctr += 1

    return ctr


def divide_and_sum(iterable: list, n: int) -> list:
    """
    Group and sum N elements into a list
    """
    # Could be a list comprehension but this is more readable
    new = []
    for idx in range(len(iterable)):
        if idx + n > len(iterable):
            break
        new.append(sum(iterable[idx : idx + n]))

    return new


if __name__ == "__main__":
    with open("Advent of Code/2021/Day1/input.txt", "r") as f:
        my_list = [int(line.rstrip()) for line in f]
        # Part 1
        print(greater_than_previous_counter(my_list))

        # Part 2
        grouped_list = divide_and_sum(my_list, 3)
        print(greater_than_previous_counter(grouped_list))
