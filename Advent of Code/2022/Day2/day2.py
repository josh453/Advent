"""
1 for rock
2 for paper
3 for scissors

0 for losing
6 for winning
3 for drawing
"""
from enum import Enum

practice = [['A', 'Y'], ['B', 'X'], ['C', 'Z']]

class Choices(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

class Points(Enum):
    WIN = 6
    LOSE = 0
    DRAW = 3

winning_scenarios = {
    Choices.Rock : Choices.Scissors,
    Choices.Paper : Choices.Rock,
    Choices.Scissors : Choices.Paper,
}

encrypted_choices = {
    'A': Choices.Rock,
    'B': Choices.Paper,
    'C': Choices.Scissors,
    'X': Choices.Rock,
    'Y': Choices.Paper,
    'Z': Choices.Scissors,
}

def determine_p1_score(encrypted_strategy_guide):
    score = 0
    for item in encrypted_strategy_guide:
        elf_choice = encrypted_choices[item[0]]  
        my_choice = encrypted_choices[item[1]]
        score += my_choice.value
        if elf_choice == winning_scenarios[my_choice]:
            score += Points.WIN.value
        elif my_choice == winning_scenarios[elf_choice]:
            score += Points.LOSE.value
        else:
            score += Points.DRAW.value
    
    return score

def determine_p2_score(encrypted_strategy_guide):
    """
    X means lose
    Y means draw
    Z means win
    """
    score = 0
    for item in encrypted_strategy_guide:
        elf_choice = encrypted_choices[item[0]]  
        my_strategy = item[1]
        if my_strategy == 'X':
            my_choice = winning_scenarios[elf_choice]
            score += my_choice.value
            score += Points.LOSE.value
        elif my_strategy == 'Y':
            my_choice = elf_choice         
            score += my_choice.value
            score += Points.DRAW.value
        else:
            my_choice = list(winning_scenarios.keys())[list(winning_scenarios.values()).index(elf_choice)]
            score += my_choice.value
            score += Points.WIN.value


    return score




if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day2/input.txt", "r") as f:
        my_list = [line.rstrip().split(' ') for line in f]
        # part 1
        print(determine_p1_score(my_list))
        # part 2
        print(determine_p2_score(my_list))