from collections import Counter

import numpy as np


def find_most_common_bit_position(array_of_binaries: np.array) -> dict:
    """
    Given an np.array, find the most common element in each character position
    """
    d = {}
    byte_size = len(array_of_binaries[0])
    for bin_pos in range(byte_size):
        A = array_of_binaries.view("<U1")[bin_pos::byte_size]
        c = Counter(A)
        d[bin_pos] = c.most_common(1)[0][0]

    return d


def find_oxygen_rating(array_of_binaries: np.array, position: int = 0) -> None:
    """
    Given an np.array find the rolling most common element
    """
    byte_size = len(array_of_binaries[0])

    A = array_of_binaries.view("<U1")[position::byte_size]
    c = Counter(A)
    most_common = c.most_common(2)
    if most_common[0][1] == most_common[1][1]:
        oxygen = array_of_binaries[A == "1"]
    else:
        oxygen = array_of_binaries[A == most_common[0][0]]

    if len(oxygen) == 1:
        return oxygen
    else:
        return find_oxygen_rating(oxygen, position + 1)


def find_carbon_rating(array_of_binaries: np.array, position: int = 0) -> None:
    """
    Given an np.array find the rolling least common element
    """
    byte_size = len(array_of_binaries[0])

    A = array_of_binaries.view("<U1")[position::byte_size]
    c = Counter(A)
    most_common = c.most_common(2)
    if most_common[0][1] == most_common[1][1]:
        carbon = array_of_binaries[A == "0"]
    else:
        carbon = array_of_binaries[A == most_common[1][0]]

    if len(carbon) == 1:
        return carbon
    else:
        return find_carbon_rating(carbon, position + 1)


if __name__ == "__main__":
    with open("Advent of Code/2021/Day3/input.txt", "r") as f:
        my_list = [line.rstrip() for line in f]
        my_array = np.array(my_list)

        # Part 1
        gamma_dict = find_most_common_bit_position(np.array(my_array))
        gamma_bin = gamma_dict.values()
        gamma_dec = int("".join(str(i) for i in gamma_bin), 2)
        epsilon_bin = [1 if i == "0" else 0 for i in gamma_bin]
        epsilon_dec = int("".join(str(i) for i in epsilon_bin), 2)
        print(f"{gamma_dec=} * {epsilon_dec=} = {gamma_dec*epsilon_dec}")

        # Part 2

        oxygen_rating = find_oxygen_rating(my_array)
        carbon_rating = find_carbon_rating(my_array)
        oxygen_rating = int(oxygen_rating[0], 2)
        carbon_rating = int(carbon_rating[0], 2)
        print(f"{oxygen_rating=} * {carbon_rating=} = {oxygen_rating*carbon_rating}")
