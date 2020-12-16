#!/usr/bin/env python3

import sys
from datetime import datetime

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 


# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "R" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors2(board):
    successors = []
    for c in range (count_pieces(board),N):
        for r in range (0,N):
            if (count_on_col(board, c) > 0):
                continue
            successors.append(add_piece(board, r,c))
    return successors

def successors3(board):
    successors = []
    if count_pieces(board) < N:
        for c in range (count_pieces(board),count_pieces(board) + 1):
            for r in range (0,N):
                if (count_on_col(board, c) > 0 or (count_on_row(board, r) > 0)):
                    continue
                successors.append(add_piece(board, r,c))
        return successors

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3(fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False


# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[1])

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
solution = solve(initial_board)
print (printable_board(solution) if solution else "Sorry, no solution found. :(")