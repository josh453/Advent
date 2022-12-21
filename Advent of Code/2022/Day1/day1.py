def find_top_n_calories(calorie_list, n=1):
    cal_list = []
    temp_cals = 0
    for item in calorie_list:
        if item == '':
            cal_list.append(temp_cals)
            temp_cals = 0
        else:
            temp_cals += int(item)
    
    return sum(sorted(cal_list, reverse=True)[:n])


"""
74394
212836
"""



if __name__ == "__main__":
    with open("C:/Users/joshu/OneDrive/Desktop/Advent of Code 2022/Day1/input.txt", "r") as f:
        my_list = [line.rstrip() for line in f]

        # part 1
        print(find_top_n_calories(my_list))

        # part 2
        print(find_top_n_calories(my_list, 3))