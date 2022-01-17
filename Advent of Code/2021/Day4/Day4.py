from typing import List

import numpy as np


class BingoBoard:
    def __init__(self, arr) -> None:
        self.arr = arr
        self.board = arr
        self.board_copy = self.board.copy()

    def __repr__(self) -> None:
        return f"{self.__class__.__name__}({self.arr})"

    # For testing
    @classmethod
    def from_string(cls, data):
        _array_from_string = np.fromstring(data, dtype=int, sep="\n")
        board = np.reshape(_array_from_string, (5, 5))
        return cls(board)

    def update(self, number) -> None:
        self.board = np.select([self.board == number], [-1], default=self.board)

    def check_win(self) -> bool:
        self.marked_spots = self.board != -1
        check_rows = np.sum(self.board, axis=1)
        check_cols = np.sum(self.board, axis=0)
        if -5 in check_rows or -5 in check_cols:
            return True
        else:
            return False

    def final_score(self, last_draw) -> int:
        self.marked_spots = self.board != -1
        board_sum = np.sum(self.board, where=self.marked_spots)
        return board_sum * last_draw

    def reset(self):
        self.board = self.board_copy


def part1_solution(draws: List[str], boards: List[BingoBoard]):
    _boards = boards.copy()
    _draws = draws.copy()
    for draw in _draws:
        draw = int(draw)
        for board in _boards:
            board.update(draw)
            if board.check_win():
                print("Found a winner!")
                print(f"Number drawn: {draw}")
                print(board.board_copy)

                return board.final_score(draw)


def part2_solution(draws: List[str], boards: List[BingoBoard]):
    _boards = boards.copy()
    _draws = draws.copy()
    for draw in _draws:
        draw = int(draw)
        for idx, board in enumerate(_boards):
            board.update(draw)

        for idx, board in enumerate(_boards):
            if board.check_win():
                winning_board = _boards.pop(idx)
                winning_draw = draw

    print("Found a winner!")
    print(f"Number drawn: {winning_draw}")
    print(winning_board.board_copy)

    return winning_board.final_score(winning_draw)


if __name__ == "__main__":
    with open("Advent of Code/2021/Day5/input.txt", "r") as f:
        my_list = [line.rstrip() for line in f]
        draws = my_list[0].split(",")
        list_of_boards = [
            my_list[i + 1 : i + 6] for i, line in enumerate(my_list) if line == ""
        ]

        arr_of_boards = []
        for board in list_of_boards:
            arr = np.array([[int(i) for i in j.split()] for j in board])
            arr_of_boards.append(BingoBoard(arr))

        # Part 1
        solution = part1_solution(draws, arr_of_boards)
        print(f"Part 1: {solution}")

        for board in arr_of_boards:
            board.reset()

        # Part 2
        solution2 = part2_solution(draws, arr_of_boards)
        print(f"Part 2: {solution2}")
