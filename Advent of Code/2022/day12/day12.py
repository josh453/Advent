import numpy as np
import networkx as nx

sample = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".splitlines()


def list_to_2d_array(my_list):
    for idx, tree_line in enumerate(my_list):
        if idx == 0:
            arr = np.fromiter(tree_line, "U8")
        else:
            arr = np.append(arr, np.fromiter(tree_line, "U8"), axis=0)

    return np.reshape(arr, (len(my_list), len(my_list[0])))


def find_start_end(arr, start_char="S", end_char="E"):
    start_row, start_col = (
        np.nonzero(arr == start_char)[0][0],
        np.nonzero(arr == start_char)[1][0],
    )
    end_row, end_col = (
        np.nonzero(arr == end_char)[0][0],
        np.nonzero(arr == end_char)[1][0],
    )

    return start_row, start_col, end_row, end_col


def convert_str_to_int(arr, func=ord):
    return np.vectorize(ord)(arr)


def create_graph(arr):
    """This assumes a numpy array of ints"""
    i_end = arr.shape[0] - 1
    j_end = arr.shape[1] - 1
    G = nx.DiGraph(directed=True)

    for (i, j), ele in np.ndenumerate(arr):
        right_row, right_col = min(i + 1, i_end), j
        right = arr[right_row][right_col]

        left_row, left_col = max(i - 1, 0), j
        left = arr[left_row][left_col]

        bottom_row, bottom_col = i, min(j + 1, j_end)
        bottom = arr[bottom_row][bottom_col]

        top_row, top_col = i, max(j - 1, 0)
        top = arr[top_row][top_col]

        if ele - right >= 0 or ele - right == -1:
            G.add_edge(f"{i,j}", f"{right_row,right_col}")
        if ele - left >= 0 or ele - left == -1:
            G.add_edge(f"{i,j}", f"{left_row,left_col}")
        if ele - top >= 0 or ele - top == -1:
            G.add_edge(f"{i,j}", f"{top_row,top_col}")
        if ele - bottom >= 0 or ele - bottom == -1:
            G.add_edge(f"{i,j}", f"{bottom_row,bottom_col}")

    G.remove_edges_from(nx.selfloop_edges(G))

    return G


def part_one(my_list):
    A = list_to_2d_array(my_list)
    start_row, start_col, end_row, end_col = find_start_end(A)

    A[start_row][start_col] = "a"
    A[end_row][end_col] = "z"

    A = convert_str_to_int(A)
    G = create_graph(A)

    shortest_path = G.subgraph(
        nx.astar_path(G, f"{start_row,start_col}", f"{end_row,end_col}")
    )

    return len(shortest_path) - 1


def part_two(my_list):
    A = list_to_2d_array(my_list)
    start_row, start_col, end_row, end_col = find_start_end(A)

    A[start_row][start_col] = "a"
    A[end_row][end_col] = "z"

    A = convert_str_to_int(A)
    G = create_graph(A)
    start_row, start_col = np.nonzero(A == 97)[0], np.nonzero(A == 97)[1]
    answer = np.inf
    for i, j in zip(start_row, start_col):
        try:
            shortest_path = G.subgraph(nx.astar_path(G, f"{i,j}", f"{end_row,end_col}"))
        except nx.NetworkXNoPath:
            continue
        if len(shortest_path) < answer:
            answer = len(shortest_path)

    return answer - 1


if __name__ == "__main__":
    with open(
        "C:/Users/joshu/OneDrive/Desktop/Github/Advent/Advent of Code/2022/Day12/input.txt",
        "r",
    ) as f:
        ...
        my_list = f.read().splitlines()
        # part 1
        print("Part 1: ", part_one(my_list))

        # # part 2
        print("Part 2: ", part_two(my_list))
