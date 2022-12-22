import numpy as np


sample = [
    "30373",
    "25512",
    "65332",
    "33549",
    "35390",
]


def list_to_2d_array(my_list):
    for idx, tree_line in enumerate(my_list):
        if idx == 0:
            arr = np.fromiter(tree_line, int)
        else:
            arr = np.append(arr, np.fromiter(tree_line, int), axis=0)

    return np.reshape(arr, (len(my_list[0]), len(my_list)))


def count_cross_trees(arr):
    visible_trees = 0
    for (i, j), value in np.ndenumerate(arr):
        if i == 0 or i == arr.shape[0] - 1:
            pass
        elif j == 0 or j == arr.shape[1] - 1:
            pass
        else:
            if all(value > arr[0:i, j]):
                visible_trees += 1
            elif all(value > arr[i + 1 : arr.shape[0], j]):
                visible_trees += 1
            elif all(value > arr[i, 0:j]):
                visible_trees += 1
            elif all(value > arr[i, j + 1 : arr.shape[1]]):
                visible_trees += 1

    return visible_trees


def scenic_score_helper(arr, value):
    score = 0
    for item in arr:
        if item < value:
            score += 1
        elif item == value:
            score += 1
            break
        elif item > value:
            score += 1
            break

    return score


def scenic_score(arr):
    scenic_score = 0
    for (i, j), value in np.ndenumerate(arr):
        temp_score = 0
        if i == 0 or i == arr.shape[0] - 1:
            pass
        elif j == 0 or j == arr.shape[1] - 1:
            pass
        else:
            up_arr = arr[0:i, j][::-1]
            up = scenic_score_helper(up_arr, value)

            down_arr = arr[i + 1 : arr.shape[0], j]
            down = scenic_score_helper(down_arr, value)

            left_arr = arr[i, 0:j][::-1]
            left = scenic_score_helper(left_arr, value)

            right_arr = arr[i, j + 1 : arr.shape[1]]
            right = scenic_score_helper(right_arr, value)

            temp_score = up * down * left * right
        if temp_score > scenic_score:
            scenic_score = temp_score

    return scenic_score


def part_one(my_list):
    arr = list_to_2d_array(my_list)
    visible_trees = count_cross_trees(arr)
    visible_trees += len(my_list) * 2 + len(my_list[0]) * 2 - 4

    return visible_trees


def part_two(my_list):
    arr = list_to_2d_array(my_list)

    return scenic_score(arr)


if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day8/input.txt",
        "r",
    ) as f:
        ...
        my_list = [line.rstrip() for line in f]
        # part 1
        print("Part 1: ", part_one(my_list))

        # part 2
        print("Part 2: ", part_two(my_list))
