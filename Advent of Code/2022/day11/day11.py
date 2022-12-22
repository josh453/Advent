import re
from typing import Final, Callable, Self
from functools import partial, reduce
from dataclasses import dataclass
import operator
from heapq import nlargest
import copy

sample = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".split("\n\n")

_parse: Final[re.Pattern[str]] = re.compile(
    r"\s*Starting items: (?P<items>[\d, ]*)\n"
    r"\s*Operation: new = old (?P<operation>[+*]) (?P<operand>\d+|old)\n"
    r"\s*Test: divisible by (?P<divisible_by>\d+)\n"
    r"\s*If true: throw to monkey (?P<if_true>\d)\n"
    r"\s*If false: throw to monkey (?P<if_false>\d)"
)

@dataclass
class Monkey:
    items: list[int]
    operation: Callable
    divisible_by: int
    if_true: int
    if_false: int
    relief: int = 3

    def __len__(self):
        return len(self.items)

    @classmethod
    def from_text(cls, text, relief=3):
        match = _parse.search(text)
        starting_items = [int(item) for item in match["items"].split(",")]
        divisible_by, if_true, if_false = map(int, match.group("divisible_by", "if_true", "if_false"))
        match (match["operation"], match["operand"]):     
            case ("*", "old"):
                operation = partial(pow, exp=2)
            case ("+", "old"):
                operation = partial(operator.mul, 2)
            case ("+", operand):
                operation = partial(operator.add, int(operand))
            case ("*", operand):
                operation = partial(operator.mul, int(operand))
        
        return cls(starting_items, operation, divisible_by, if_true, if_false, relief)
    
    def throw(self: Self, other: Self, val: int):
        self.items.pop(0)
        other.items.append(val)

def monkey_shenanigans(list_of_monkeys, relief=3, rounds=20):
    monkeys = [Monkey.from_text(item, relief) for item in list_of_monkeys]
    inspected = [0] * len(monkeys)
    lcm = reduce(operator.mul, (monkey.divisible_by for monkey in monkeys))
    for _ in range(rounds):
        for num, monkey in enumerate(monkeys):
            if len(monkey) == 0:
                # print(f"Monkey {num} has no items")
                continue
            for item in copy.deepcopy(monkey.items):
                # print(f"Monkey {num} inspects item with a worry level of {item}")
                item_worry_level = monkey.operation(item)
                item_worry_level = item_worry_level // monkey.relief
                inspected[num] += 1
                
                if item_worry_level % monkey.divisible_by == 0:
                    # print(f"Monkey {num} throws item with worry level {item_worry_level} to {monkey.if_true}")
                    monkey_to_throw_to = monkeys[monkey.if_true]
                    monkey.throw(monkey_to_throw_to, item_worry_level % lcm)
                else:
                    # print(f"Monkey {num} throws item with worry level {item_worry_level} to {monkey.if_false}")
                    monkey_to_throw_to = monkeys[monkey.if_false]
                    monkey.throw(monkey_to_throw_to, item_worry_level % lcm)
    
    return operator.mul(*nlargest(2, inspected))
    
        

if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day11/input.txt", "r") as f:
        ...
        my_list = f.read().split("\n\n")
        # print(my_list[:10])
        # part 1
        print("Part 1: ", monkey_shenanigans(my_list))
        
        # # part 2
        print("Part 2: ", monkey_shenanigans(my_list, relief=1, rounds=10_000))

