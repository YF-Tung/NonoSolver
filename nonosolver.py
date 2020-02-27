#!/usr/bin/env python3

import sys

N = 15
o_list = []
x_list = []

""" 'o', ' ', '?' """

""" Return true iff solvable """
def solve_one_array(arr, label):
    if len(arr) == 0:
        return

def get_partition(label):
    global N
    k = len(label) + 1
    n = N - sum(label) - (len(label)-1)
    return partition(n, k, tuple())

""" Returns iterable of k-tuple non-neg integers that have sum n """
def partition(n, k, partial):
    if k == 1:
        yield partial + (n,)
    else:
        for i in range(n + 1):
            for result in partition(n-i, k-1, partial + (i,)):
                yield result

def generate_guess_by_partition(label, partition):
    global N
    assert(sum(label) + len(label) + sum(partition) == (N + 1))
    assert(len(partition) == len(label) + 1)
    first, partition = partition[0], partition[1:]
    partition = [x+1 for x in partition[:-1]] + [partition[-1]]
    rv = x_list[first].copy()
    for o, x in zip(label, partition):
        rv += o_list[o]
        rv += x_list[x]
    assert (len(rv) == N)
    return rv


""" current: o, ' ', ?, guess: o, ' '"""
def is_possible(current, guess):
    assert (len(current) == len(guess))
    return all((c == '?' or c == g) for c, g in zip(current, guess))



def parse_cons_file(filename):
    with open(filename) as fin:
        return [[int(x) for x in line.strip().split()] for line in fin]

def init():
    global N, o_list, x_list
    N = 15
    for i in range(N+1):
        o_list.append(['o' for _ in range(i)])
    for i in range(N+1):
        x_list.append([' ' for _ in range(i)])


def pprint(dense, fat=False):
    print (pretty(dense, fat))

def pprint_arr(board, id, r_or_c):
    if r_or_c == 'r':
        pprint(get_current_col(board, id))
    else:
        pprint(get_current_row(board, id))

def pretty(dense, fat=False):
    if fat:
        return '| ' + ' | '.join(dense) + ' |'
    else:
        return '|' + ''.join(dense) + '|'


def guess_aggregate(valid_guess_iterable):
    global N

    valid_guess_iterable = list(valid_guess_iterable)
    #print (valid_guess_iterable)
    valid_guess_iterable = (x for x in valid_guess_iterable)

    aggr = next(valid_guess_iterable).copy()
    for guess in valid_guess_iterable:
        aggr = ['?' if a != g else a for a, g in zip(aggr, guess)]

    return aggr

def solve_arr(label, current):
    guess_generator = (generate_guess_by_partition(label, par) for par in get_partition(label))
    valid_guess_generator = (guess for guess in guess_generator if is_possible(current, guess))
    aggr = guess_aggregate(valid_guess_generator)
    return aggr


""" board[r][c] """

def get_current_row(board, row_id):
    return board[row_id].copy()


def get_current_col(board, col_id):
    return [row[col_id] for row in board]


def show_status(board, no_new_line=True):
    def show(s):
        if no_new_line:
            sys.stdout.write('\r' + ''.join(s))
        else:
            print (''.join(s))
    total = len(board)*len(board)
    unsolved = sum(len([1 for v in row if v == '?']) for row in board)
    display_len = 40
    if unsolved == 0:
        show(['o'] * display_len)
    else:
        unsolved_len = max(1, int(1.0 * display_len * unsolved / total))
        show(['o'] * (display_len - unsolved_len) + ['?'] * unsolved_len)


def pretty_print_board(board):
    global N
    border_line = '+' + ''.join(['-'] * (4 * N - 1)) + '+'
    middle_line = '---'.join(['+'] * (N + 1))
    print (border_line)
    for i, row in enumerate(board):
        if i != 0:
            print(middle_line)
        pprint(row, fat=True)
    print (border_line)



def solve(col_cons, row_cons, _N):
    global N
    N = _N
    assert (len(col_cons) == N)

    # Initiate board
    board = [['?' for _ in range(N)] for __ in range(N)]

    should_try_col = [True] * N
    should_try_row = [True] * N

    while any(should_try_col) or any(should_try_row):
        if any(should_try_col):
            col_id = should_try_col.index(True)
            current = get_current_col(board, col_id)
            after = solve_arr(col_cons[col_id], current)
            for i in range(N):
                if current[i] != after[i]:
                    board[i][col_id] = after[i]
                    should_try_row[i] = True
            should_try_col[col_id] = False


        if any(should_try_row):
            row_id = should_try_row.index(True)
            current = get_current_row(board, row_id)
            after = solve_arr(row_cons[row_id], current)
            for i in range(N):
                if current[i] != after[i]:
                    board[row_id][i] = after[i]
                    should_try_col[i] = True
            should_try_row[row_id] = False
        #show_status(board)

        #show_status(board)
    print()
    print ('+' + ''.join(['-']*N) + '+')
    for row in board:
        pprint(row)
    print ('+' + ''.join(['-']*N) + '+')
    pretty_print_board(board)


def main():
    init()
    col_cons_file = 'col_cons.txt'
    row_cons_file = 'row_cons.txt'
    label = [3, 6]
    current = ['o','?','?','?','?','?','?', ' ', '?','?','?','?','o','?','?']
    col_cons, row_cons = parse_cons_file(col_cons_file), parse_cons_file(row_cons_file)
    solve(col_cons, row_cons, len(col_cons))



if __name__ == '__main__':
    main()

