from functools import cmp_to_key
from ast import literal_eval

sample = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".split("\n\n")



def packet_analyzer(p1, p2):
    p1 = p1 if isinstance(p1, list) else [p1]
    p2 = p2 if isinstance(p2, list) else [p2]

    for left,right in zip(p1, p2):
        # print(left, right)
        match (left, right):
            case (list(), _) | (_, list()) :
                comparison = packet_analyzer(left, right)
            case _:
                comparison = right - left
        
        if comparison != 0:
            return comparison
    
    return len(p2) - len(p1)
                
        
def pairings(input):
    pairing = []
    for pair in input:
        p1, p2 = pair.splitlines()
        p1, p2 = literal_eval(p1), literal_eval(p2)
        pairing.append((p1,p2))

    return pairing

def single_list(input):
    singlet = []
    for pair in input:
        # print(pair)
        p1, p2 = pair.splitlines()
        p1, p2 = literal_eval(p1), literal_eval(p2)
        singlet.extend([p1,p2])
    
    return singlet

def decoder(input):
    singlet= single_list(input)
    singlet.extend([[[2]], [[6]]])
    sorted_answer = sorted(singlet, key=cmp_to_key(packet_analyzer), reverse=True)
    answer = (sorted_answer.index([[2]]) + 1) * (sorted_answer.index([[6]]) + 1 )
    
    return answer




pairs = pairings(sample)

assert sum(i for i, (p1, p2) in enumerate(pairs, 1) if packet_analyzer(p1, p2) > 0) == 13
assert decoder(sample) == 140



if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day13/input.txt", "r") as f:
        my_list = f.read().split("\n\n")
        pairs = pairings(my_list)
        # print(my_list[:10])
        # part 1
        print("Part 1:", sum(i for i, (p1, p2) in enumerate(pairs, 1) if packet_analyzer(p1, p2) > 0))
        
        # # part 2
        print("Part 2: ", decoder(my_list)) 


