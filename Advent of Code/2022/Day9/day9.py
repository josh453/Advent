from typing import Iterable, Iterator, NamedTuple, Self
from enum import Enum

sample = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".splitlines()

class Position(NamedTuple):
    x: int
    y: int

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def manhattan_distance(self, other):
        x, y = self - other
        return abs(x) + abs(y)
    
    def adjacent(self, other):
        x, y = self - other
        if abs(x) == 1 and abs(y) == 1:
            return True
        elif self.manhattan_distance(other) > 1:
            return False
        else:
            return True

class Direction(Enum):
    U = Position(0,1)
    D = Position(0,-1)
    L = Position(-1,0)
    R = Position(1,0)


def part_one(my_list):
    head = Position(0, 0)
    tail = Position(0, 0)
    tail_positions = set()
    tail_positions.add(tail)

    for instr in my_list:      
        move, _, count = instr.partition(" ")
        dxn = Direction[move].value
        for _ in range(int(count)):
            head += dxn
            # print("\nNext")
            # print(f"Head: {head}")
            if not head.adjacent(tail):
                tail = head - dxn
                tail_positions.add(tail)
            # print(f"Tail: {tail}")
    # print(tail_positions)
    
    return len(tail_positions)

print(part_one(sample))

head = Position(1,3)
tail = Position(2,4)
# print(head - tail)
# print(head.manhattan_distance(tail))
# print(head.adjacent(tail))

class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x - other.x, self.y - other.y)

    def __or__(self, other: Self) -> bool:
        """Are two positions adjacent?"""
        if not isinstance(other, Position):
            return NotImplemented
        return all(abs(v) <= 1 for v in self - other)

    def __pos__(self) -> Self:
        """Unit vector"""
        return Position(*(v // abs(v or 1) for v in self))

    def __and__(self, other: Self) -> Self:
        """Move self towards other

        Moves diagonally if other is not in line (same row or column)

        """
        if not isinstance(other, Position):
            return NotImplemented
        unit = +(other - self)
        return self + unit

    def __len__(self) -> int:
        """Manhattan distance from origin"""
        return abs(self.x) + abs(self.y)


class Direction(Enum):
    U = Position(0, -1)
    D = Position(0, 1)
    L = Position(-1, 0)
    R = Position(1, 0)


class Rope:
    _head: Position = Position(0, 0)
    _tail: Position = Position(0, 0)

    @property
    def head(self) -> Position:
        return self._head
    
    @property
    def tail(self) -> Position:
        return self._tail

    def __init__(self, head: Position | None = None, tail: Position | None = None):
        if head is not None:
            self._head = head
        if tail is not None:
            self._tail = tail

    def __add__(self, dir: Direction) -> Self:
        head, tail = self.head + dir.value, self.tail
        if not head | tail:
            # if the head moved too far away from the tail, move the tail to
            # the previous head position.
            tail = self.head
        return __class__(head, tail)

    def move(self, instructions: Iterable[str]) -> Iterator[Self]:
        rope = self
        for line in instructions:
            move, _, count = line.partition(" ")
            dir = Direction[move]
            for _ in range(int(count)):
                rope += dir
                yield rope


def count_tail_positions(rope: Rope, instructions: Iterable[str]) -> int:
    return len(set(rope.tail for rope in rope.move(instructions)))

class LongRope(Rope):
    knots: tuple[Position, ...]

    def __init__(self, *knots: Position, length: int = 10):
        if length is not None and len(knots) < length:
            knots = (*knots, *(Position(0, 0) for _ in range(length - len(knots))))
        self.knots = knots

    @property
    def head(self) -> Position:
        return self.knots[0]

    @property
    def tail(self) -> Position:
        return self.knots[-1]

    def __add__(self, dir: Direction) -> Self:
        curr, *remainder = self.knots
        curr += dir.value
        knots: list[Position] = []
        it = iter(remainder)
        for knot in it:
            knots.append(curr)
            if curr | knot:
                # done, remainder won't have to move
                curr = knot
                break
            curr = knot & curr
        return __class__(*knots, curr, *it)

if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day9/input.txt", "r") as f:
        ...
        my_list = [line.rstrip() for line in f]
        # print(my_list[:10])
        # part 1
        # print("Part 1: ", part_one(my_list))
        
        # part 2
        print("Part 2:", count_tail_positions(LongRope(), my_list))
