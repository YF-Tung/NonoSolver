#!/usr/bin/env python3

import sys

N = None
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
    global GUESS_CNT
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
    global N
    def correct_vals(vals, N):
        if len(vals) == 0:
            return vals
        val = vals[0]
        if val > N:
            s = str(val)
            if len(s) >= 3:
                s1, s2 = s[0:2], s[2:]
                if int(s1) > N:
                    s1, s2 = s[0], s[1:]
            else:
                s1, s2 = s[0], s[1:]

            v1, v2 = int(s1), int(s2)
            vals[0] = v2
            return [v1] + correct_vals(vals, N)
        else:
            return [val] + correct_vals(vals[1:], N)


    with open(filename) as fin:
        rv = [[int(x) for x in line.strip().split()] for line in fin]
    rv = [vals for vals in rv if len(vals) > 0]
    rv = [correct_vals(vals, len(rv)) for vals in rv]
    N = len(rv)
    return rv

def init():
    global N, o_list, x_list
    for i in range(N+1):
        o_list.append(['o' for _ in range(i)])
    for i in range(N+1):
        x_list.append([' ' for _ in range(i)])


def pprint(dense, fat=False, convert=False):
    print (pretty(dense, fat, convert))

def pprint_arr(board, id, r_or_c):
    if r_or_c == 'r':
        pprint(get_current_col(board, id))
    else:
        pprint(get_current_row(board, id))

def pretty(dense, fat=False, convert=False):
    def c(x):
        if convert:
            if x == '?':
                return ' '
            elif x == ' ':
                return 'x'
        return x

    if fat:
        rv = '|'
        while len(dense) != 0:
            assert (len(dense) >= 5)
            for i in range(4):
                rv += ' ' + c(dense[i]) + '  '
            rv += ' ' + c(dense[4]) + ' |'
            dense = dense[5:]
        return rv
    else:
        return '|' + ''.join(dense) + '|'


def guess_aggregate(valid_guess_iterable):
    global N

    aggr = next(valid_guess_iterable).copy()
    cnt = 0
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


LAST_PRINT_LEN = 0
def show_status(board, arr1, arr2, no_new_line=True):
    global LAST_PRINT_LEN
    def show(s):
        global LAST_PRINT_LEN
        if no_new_line:
            print_len = len(s)
            if print_len < LAST_PRINT_LEN:
                d = LAST_PRINT_LEN - print_len
                s += ' ' * d + '\b' * d
            LAST_PRINT_LEN = print_len
            sys.stdout.write('\r' + s)
        else:
            print (s)
    total = len(board)*len(board)
    unsolved = sum(len([1 for v in row if v == '?']) for row in board)
    display_len = 40

    postfix = ', ' + str(sum(arr1)) + '/' + str(len(arr1)) \
            + ', ' + str(sum(arr2)) + '/' + str(len(arr2))


    if unsolved == 0:
        show(''.join(['='] * display_len) + postfix)
    else:
        unsolved_len = max(1, int(1.0 * display_len * unsolved / total))
        show(''.join(['='] * (display_len - unsolved_len) + ['-'] * unsolved_len) + postfix)


def pretty_print_board(board, convert=False):
    global N
    assert (N % 5 == 0)
    middle_line = '+                   ' * int(N/5) + '+'
    border_line = '---'.join(['+'] * (N + 1))
    print(border_line)
    for i, row in enumerate(board):
        if i != 0:
            if i % 5 == 0:
                print(border_line)
            else:
                print(middle_line)
        pprint(row, fat=True, convert=convert)
    print (border_line)



def solve(col_cons, row_cons, _N):
    global N
    N = _N
    assert (len(col_cons) == N)

    # Initiate board
    board = [['?' for _ in range(N)] for __ in range(N)]

    should_try_col = [True] * N
    should_try_row = [True] * N

    try:
        while any(should_try_col) or any(should_try_row):
            if any(should_try_col):
                col_id, min_par = -1, 1e8
                for i in range(N):
                    if should_try_col[i] and len(col_cons[i]) < min_par:
                        col_id = i

                current = get_current_col(board, col_id)
                after = solve_arr(col_cons[col_id], current)
                for i in range(N):
                    if current[i] != after[i]:
                        board[i][col_id] = after[i]
                        should_try_row[i] = True
                should_try_col[col_id] = False


            if any(should_try_row):
                row_id, min_par = -1, 1e8
                for i in range(N):
                    if should_try_row[i] and len(row_cons[i]) < min_par:
                        row_id = i

                current = get_current_row(board, row_id)
                after = solve_arr(row_cons[row_id], current)
                for i in range(N):
                    if current[i] != after[i]:
                        board[row_id][i] = after[i]
                        should_try_col[i] = True
                should_try_row[row_id] = False
            #show_status(board)

            if N >= 20:
                # May be slow
                show_status(board, should_try_col, should_try_row)
        print()
        pretty_print_board(board)
    except StopIteration:
        print()
        print('Failed to solve all entries! Only shows partial result.')
        pretty_print_board(board, convert=True)


def main():
    col_cons_file = 'col_cons.txt'
    row_cons_file = 'row_cons.txt'
    col_cons, row_cons = parse_cons_file(col_cons_file), parse_cons_file(row_cons_file)
    init()
    solve(col_cons, row_cons, len(col_cons))



if __name__ == '__main__':
    main()

