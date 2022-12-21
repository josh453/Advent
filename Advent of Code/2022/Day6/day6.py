import collections
from itertools import islice

sample = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'

def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield set(window)
    for x in it:
        window.append(x)
        yield set(window)

def answer(s, n=4):
    for idx, item in enumerate(sliding_window(s, n)):
        if len(item) == n:
            return idx + n

# print(answer(sample, 14))

if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day6/input.txt", "r") as f:
        # part 1
        # print(type(f.readlines()))
        my_list = f.readlines()
        print(answer(my_list[0]))

        # part 2
        print(answer(my_list[0], 14))
        