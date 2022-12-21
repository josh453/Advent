from collections import deque
from itertools import repeat

sample = [
['move', '1', 'from', '2', 'to', '1'], #1, 3, -1
['move', '3', 'from', '1', 'to', '3'],
['move', '2', 'from', '2', 'to', '1'],
['move', '1', 'from', '1', 'to', '2'],
]

cols = [
    deque("ZN"),
    deque("MCD"),
    deque("P"),
]


def multi_pop(db_queue, n, one_time=True):
    popped_elements = str()
    if one_time:
        for i in range(n):
            popped_elements += db_queue.pop()
        return popped_elements
    else:
        for i in range(n):
            popped_elements += db_queue.pop()
        return popped_elements[::-1]

    

def part_one(instructions, cols):
    answer = str()
    for item in instructions:
        # print(item)
        quantity_to_move = int(item[1])
        pickup = int(item[3]) - 1 # List indexing
        destination = int(item[-1]) - 1
        popped_elements = multi_pop(cols[pickup], quantity_to_move)
        cols[destination].extend(popped_elements)
    
    for crate in cols:
        answer += crate[-1]
    
    return answer

def part_two(instructions, cols):
    answer = str()
    for item in instructions:
        quantity_to_move = int(item[1])
        pickup = int(item[3]) - 1 # List indexing
        destination = int(item[-1]) - 1
        popped_elements = multi_pop(cols[pickup], quantity_to_move, one_time=False)
        cols[destination].extend(popped_elements)

    for crate in cols:
        answer += crate[-1]
    
    return answer

# print(part_two(sample, cols))

if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day5/input.txt", "r") as f:
        cols = [
            deque("PFMQWGRT"),
            deque("HFR"),
            deque("PZRVGHSD"),
            deque("QHPBFWG"),
            deque("PSMJH"),
            deque("MZTHSRPL"),
            deque("PTHNML"),
            deque("FDQR"),
            deque("DSCNLPH"),
        ]
        my_list = [line.split() for line in f]
        # print(my_list[:18])
        # part 1
        # print(part_one(my_list, cols))

        # part 2
        print(part_two(my_list, cols))