#!/usr/bin/env python3

N = 30
p = 0.6


import random
from argparse import ArgumentParser

def to_sparse(arr):
    s = ''.join([str(x) for x in arr]).strip('0').split('0')
    s = [x for x in s if x != '']
    return ' '.join([str(len(w)) for w in s])


def gen_board():
    return [[1 if random.random() < p else 0 for _ in range(N)] for __ in range(N)]

def is_valid_board(board):
    global N
    return not (
            any([sum(row) == 0 for row in board])
            or
            any([sum([row[i] for row in board]) == 0 for i in range(N)])
            )

def main():
    board = gen_board()
    while not is_valid_board(board):
        print ('retry')
        board = gen_board()

    board = [[1 if random.random() < p else 0 for _ in range(N)] for __ in range(N)]

    with open('col_cons.txt', 'w') as fout:
        for i in range(N):
            fout.write(to_sparse([row[i] for row in board]) + '\n')
    with open('row_cons.txt', 'w') as fout:
        for i in range(N):
            fout.write(to_sparse(board[i]) + '\n')

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('-N', type=int, default=30)
    ap.add_argument('-p', type=float, default=0.6)
    args = ap.parse_args()
    N = args.N
    p = args.p
    main()
