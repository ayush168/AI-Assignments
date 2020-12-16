#!/usr/bin/env python2
# Reference(s): http://aima.eecs.berkeley.edu/python/games.html
#               https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning 

import sys
import time
import copy
from types import NoneType

n = int(sys.argv[1])
max_player = sys.argv[2]
initial_board = sys.argv[3]
stop = int(sys.argv[4])

start = time.time()

B = [[0]*n for N in range(0,(n+3))]

A = []
l = 0

parent = {}

while l < len(initial_board):
    A += [initial_board[l:l+3]]
    l = l + 3

p = -1
q = -1

last_row = n+3-1
last_col = n-1
first_row = -1
first_col = -1

for i in A:
    p += 1
    q = -1
    for j in i:
        q += 1
        B[p][q] = j

def ef_poss_mvs(board):
    count = 0
    for col in range(last_col, -1, -1):
        for row in range(last_row, n-(n+1), -1):
            if(row == n):
                continue
            elif (board[row][col] == '.' and board[row-1][col] == '.'):
                count = count + 1
                break
            elif ((board[row][col] == 'x' and board[row-1][col] == '.') or (board[row][col] == 'o' and board[row-1][col] == '.')):
                count = count + 1
                break
    return count

def ef_rem_sqr(board):
    count = 0
    for col in range(last_col, -1, -1):
        for row in range(last_row, n-1, -1):
            if board[row][col] == '.':
                count = count + 1
    return count

def ef_nxn(board, player):
    val = 0
    # row check 
    for row in range(0,n):
        flag = 0
        for col in range(0,n):
            if(board[row][col] == "." or board[row][col] == player ):
                flag += 1
            if(flag == n):
                val = val + 1

    # col check
    for col in range(0,n):
        flag = 0
        for row in range(0,n):
            if(board[row][col] == "." or board[row][col] == player):
                flag += 1
            if(flag == n):
                val = val + 1
            
    # diag check
    flag = True
    for diag in range(0,n):
        if(board[diag][diag] == "." or board[diag][diag] == player):
            continue
        else:
            flag = False
        if flag == False:
            break
    if(flag):
        val = val + 1
        
    # Top Right - Bottom Left Empty Check
    flag = True
    for row in range(0,n):
        col = n - row - 1
        if(board[row][col] == "." or board[row][col] == player):
            continue
        else:
            flag = False
        if flag == False:
            break
    if(flag):
        val = val + 1
        
    return val

def eval_func(board, player):
    if player == 'x':
        nxn = ef_nxn(board, 'x') - ef_nxn(board, 'o')
    else:
        nxn = ef_nxn(board, 'o') - ef_nxn(board, 'x')
    e = 3*(nxn + ef_poss_mvs(board)) - 2*(ef_rem_sqr(board))
    return e

def mov_row(board, col, player):
    new_board = copy.deepcopy(board)
    for row in range (last_row, first_row, -1):
        if new_board[first_row+1][col] != ".":
            return
        if(new_board[row][col] == "."):
            new_board[row][col] = player
            break
    return new_board

def mov_col(board, col):
    new_board = copy.deepcopy(board)
    for row in range (last_row,first_row,-1):
        if(row == first_row+1):
            break
        else:
            temp = 0
            if(new_board[row][col] == "."):
                break
            else:
                temp = new_board[row][col]
                if(new_board[row - 1][col] == "."):
                    break
                else:
                    new_board[row][col] = new_board[row - 1][col]
                    new_board[row - 1][col] = temp
    return new_board

def successors(board, player):
    succ_board = []
    for col in range (last_col, first_col, -1):
        temp_board = mov_row(board, col, player)
        if type(temp_board) != NoneType:
            succ_board += [temp_board]
        else:
            continue
    for col in range (last_col, first_col,-1):
        temp_board = mov_col(board, col)
        if board != temp_board:
            succ_board += [temp_board]
        else:
            continue
    return succ_board
        
def is_goal(b):
    for row in range (0, n):                    # check for each row for top n rows
        flag = 0                                # initialize flag to 0 for each check
        for col in range(0, n):                 # increment column by 1
            if(b[row][col] == max_player):      # if pebble already there
                flag += 1                       # increment flag by 1 
        if flag == n:                           # when flag = n, 3 pebbles for player exist
            return True                         # terminal state (player wins)
    
    for col in range(0, n):                     # check for each column
        flag = 0                                # initialize flag to 0 for each check
        for row in range (0, n):                # increment row by 1
            if(b[row][col] == max_player):      # if pebble already exists in square
                flag += 1                       # increment flag by 1 
        if flag == n:                           # when flag = n, n pebbles for player exist
            return True                         # terminal state (player wins)
    
    flag = 0
    x = range(0, n)
    y = range(n-1, -1, -1)
    for row, col in zip(x, x):                  # left-to-right diagonal check
        if b[row][col] == max_player:
            flag += 1
        if flag == n:
            return True
    
    flag = 0
    for row, col in zip(x, y):
        if b[row][col] == max_player:           # right-to-left diagonal check
            flag += 1
        if flag == n:
            return True
        
    return False    

def successors_root(board, player):
    succ_board = []
    for col in range (last_col, first_col, -1):
        temp_board = mov_row(board, col, player)
        if type(temp_board) != NoneType:
            succ_board += [(col+1, temp_board)]
        else:
            continue
    for col in range (last_col, first_col,-1):
        temp_board = mov_col(board, col)
        if board != temp_board:
            succ_board += [(-(col+1), temp_board)]
        else:
            continue
    return succ_board

def max_val(board, depth, alpha, beta, player):
    if depth == 0 or is_goal(board):
        e = eval_func(board, player)
        return  e
    val = float('-inf')
    for s in successors(board, player):
        val = max(val, min_val(s, depth-1, alpha, beta, 'x'))
        if (val <= beta):
            return val
        alpha = max(alpha, val)
    return val

def min_val(board, depth, alpha, beta, player):
    if depth == 0 or is_goal(board) or time.time() > start + (stop-2):
        e = eval_func(board, player)
        return e
    val = float('inf')
    for s in successors(board, player):
        val = min(val, max_val(s, depth-1, alpha, beta, 'o'))
        if (val >= alpha):
            return val
        beta = min(beta, val)
    return val

def betsy(board, depth, alpha, beta, player):
    action = []
    for (mov, s) in successors_root(board, player):
        if depth == 0 or is_goal(s):
            m = eval_func(s, player)
            return mov, s
        elif player == 'x':
            m = min_val(s, depth, alpha, beta, 'o')
        else:
            m = min_val(s, depth, alpha, beta, 'x')
        action.append([mov, s, m])

    max_e = max(l[2] for l in action)
    
    for a in action:
        if a[2] == max_e:
            return a[0], a[1]
    
    
if is_goal(B):
    print "You've already won!"
    exit()

d = 1
while time.time() != start + stop:
    d = d + 1
    mov, res_board = betsy(B,d,float('-inf'), float('inf'), max_player)
    print mov, "".join("".join(col for col in row) for row in res_board)