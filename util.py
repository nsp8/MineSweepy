from platform import system
from random import randint
from math import floor
import re


def clear_console():
    os_ = system().lower()
    if os_ == "windows":
        return "cls"
    elif os_ in ["linux", "mac", "os x"]:
        return "clear"
    else:
        return ""


def map_headers(size):
    col_head, row_head = dict(), dict()
    for val in range(size):
        col_head[val] = chr(65 + val)
        row_head[val] = 1 + val
    return col_head, row_head


def reverse_mapping(object_map):
    return {v: k for k, v in object_map.items()}


def print_grid_skeleton(grid_object):
    display = ""
    grid, moves = grid_object.grid, grid_object.moves
    n = len(grid)
    col_id, row_id = map_headers(n)
    display += "\t{}\n".format(" ".join(col_id.values()))
    if len(moves) == 0:
        default_node_value = "* " * n
        for i in range(n):
            display += "{}\t{}\n".format(row_id[i], default_node_value)
    else:
        most_recent_move = moves[-1]
        row_mapped = reverse_mapping(row_id)[int(most_recent_move[1])]
        col_mapped = reverse_mapping(col_id)[most_recent_move[0]]
        grid_pos = grid[row_mapped][col_mapped]
        if grid_pos.value != "m":
            grid[row_mapped][col_mapped].facade = grid_pos.value
            for row in grid:
                val_ = " ".join(str(node.facade) for node in row)
                display += "{}\t{}\n".format(row_id[grid.index(row)], val_)
        else:
            for row in grid:
                val_ = " ".join(str(node.value) for node in row)
                display += "{}\t{}\n".format(row_id[grid.index(row)], val_)
            print("You hit a mine!\nX-P")
            grid_object.status = "detonated"
    return display


def define_mines(n=8):
    mines = list()
    while len(mines) != n:
        pos_x = randint(0, n - 1)
        pos_y = randint(0, n - 1)
        mine_pos = (pos_x, pos_y)
        if mine_pos not in mines:
            mines.append(mine_pos)
    return mines


def get_neighbours(node, n=8):
    x, y = node
    values = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y),
              (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    value_combos = []
    for value in values:
        xn, yn = value
        if xn in range(n) and yn in range(n):
            value_combos.append(value)
    return value_combos


def validate_user_selection(user_value, size):
    allowed_selection_length = 2 + floor(size / 10)
    if len(user_value) <= allowed_selection_length:
        match = re.search(r"(\w)(\d+)", user_value)
        if match:
            matches = match.groups()
            col_part, row_part = matches
            row_part = int(row_part)
            col_headers, _ = map_headers(size)
            col_headers_inv = reverse_mapping(col_headers)
            if row_part <= size and col_part in col_headers_inv.keys():
                return True
    return False


def re_prompt(preface=""):
    main_msg = "Press Return to play again, or any other key to exit"
    prompt_msg = "\n{}\n{}\n".format(preface, main_msg)
    action = input(prompt_msg)
    return action.strip()
