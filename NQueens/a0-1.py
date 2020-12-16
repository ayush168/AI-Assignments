#!/usr/bin/env python3

import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

def check_top_left_diagonal(board, row, col):
    while(row >= 0 and col >= 0):
        if ((board[row][col]) == 1):
            return False
        row = row - 1
        col = col - 1
    return True

def check_top_right_diagonal(board, row, col):
    while(row >= 0 and col < N):
        if ((board[row][col]) == 1):
            return False
        row = row - 1
        col = col + 1
    return True

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    str = ''
    for row in range (N):
        for col in range (N):
            if (row,col) in block:
                str = str + 'X '
            elif board[row][col] == 0:
                str = str + '_ '
        str = str + '\n'
    return str

def printable_board_R(board):
    str = ''
    for row in range (N):
        for col in range (N):
            if (row,col) in block:
                str = str + 'X '
            elif board[row][col] == 0:
                str = str + '_ '
            elif board[row][col] == 1:
                str = str + 'R '
        str = str + '\n'
    return str

def printable_board_Q(board):
    str = ''
    for row in range (N):
        for col in range (N):
            if (row,col) in block:
                str = str + 'X '
            elif board[row][col] == 0:
                str = str + '_ '
            elif board[row][col] == 1:
                str = str + 'Q '
        str = str + '\n'
    return str

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors_R(board):
    successors = []
    if count_pieces(board) < N:
        for c in range (count_pieces(board),count_pieces(board) + 1):
            for r in range (0,N):
                if (count_on_col(board, c) > 0 or (count_on_row(board, r) > 0) or (r,c) in block):
                    continue
                successors.append(add_piece(board, r,c))
    return successors
    
def successors_Q(board):
    successors = []
    r = count_pieces(board)
    if r < N:
        for c in range (0,N):
            if ((check_top_left_diagonal(board,r,c) and check_top_right_diagonal(board,r,c)) and (r,c) not in block and count_on_col(board, c) < 1):
                successors.append(add_piece(board, r,c))
    return successors

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks/n-queens!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        if (inp == 1):
            for s in successors_R(fringe.pop() ):
                if is_goal(s):
                    return(s)
                fringe.append(s)
        elif (inp == 2):
            for s in successors_Q(fringe.pop() ):
                if is_goal(s):
                    return(s)
                fringe.append(s)
        else:
            print('Wrong input. Plese select either 1 or 2')
            break
    return False


# This is N, the size of the board. It is passed through command line arguments.
inp = 0

a = sys.argv
a.pop(0)
problem_type = a.pop(0)
if (problem_type == 'nrook'):
    inp = 1
elif (problem_type == 'nqueen'):
    inp = 2

N = int(a.pop(0))
no_blocked = int(a.pop(0))
block = []
for i in range (no_blocked):
    x = int(a.pop(0))
    y = int(a.pop(0))
    block.append((x-1,y-1))

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
solution = solve(initial_board)
if (inp == 1):
    print (printable_board_R(solution) if solution else "Sorry, no solution found. :(")
elif (inp == 2):
    print (printable_board_Q(solution) if solution else "Sorry, no solution found. :(")