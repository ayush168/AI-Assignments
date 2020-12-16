# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:46:59 2018

@author: Ayush
"""

import numpy as np
import sys
import time

Inputs = sys.argv

N = int(Inputs[1])
T = int(Inputs[4])
MaxDepth = 7
MaxPlayer = Inputs[2]
BoardString = Inputs[3]

opponent = {'x' : 'o', 'o' : 'x'}
#creates a 2d matrix from the gievn input strin gas a board
def createBoardFromString(board_str, n):
    board = np.array(list(board_str)).reshape(n+3, n)
    return board

#checks whether the given state is the goal state or not
def isGoal(board, player1):
    board = board['board']
    if list(board.diagonal()).count(player1) == N:
        return True
    if list(np.flip(board, axis = 1).diagonal()).count(player1) == N:
        return True
    for i in range(0,N):
        #check for row
        if list(board[i,:]).count(player1) == N:
            return True
        #check for column
        if list(board[0:-3,i]).count(player1) == N:
            return True

    return False

#successor
def successors(initial_board, player):
    successors = []
    board = initial_board['board']
    for i in range(N):
        empty_spots = list(board[:,i]).count(".")
        #drop
        if empty_spots != 0:
            board_drop = np.array(board)
            board_drop[empty_spots-1,i] = player
            new_board = {'board': board_drop, 'currentDepth': initial_board['currentDepth'] + 1, \
                         'action' : initial_board['action'] + [i+1]}
            successors.append(new_board)
        #rotate
        if empty_spots != N+3:
            board_rotate = np.array(board)
            board_rotate[empty_spots:,i] = np.roll(board[empty_spots:,i],1)
            if not (board_rotate == board).all():
                new_board = {'board': board_rotate, 'currentDepth': initial_board['currentDepth'] + 1,\
                             'action' : initial_board['action'] + [-i-1]}
                successors.append(new_board)
    return np.array(successors)  
          
def checkInRows(board, currentPlayer):
    board_state = board['board']
    favourables = sum(int(list(board_state[i,:]).count(currentPlayer) in range(int((N+1)/2), N)) for i in range(N))
    notfavourables = sum(int(list(board_state[i,:]).count(opponent[currentPlayer]) in range(int((N+1)/2), N)) for i in range(N))
    return favourables - notfavourables

def checkInColumns(board, currentPlayer):
    board_state = board['board']
    favourables = sum(int(list(board_state[:,i]).count(currentPlayer) in range(int((N+4)/2), N)) for i in range(N))
    notfavourables = sum(int(list(board_state[:,i]).count(opponent[currentPlayer]) in range(int((N+4)/2), N)) for i in range(N))
    return favourables - notfavourables

def available_pos(curr_board, player):
    count_player = 0
    count_opp = 0
    board = curr_board['board']
    for i in range (N):
        #Row
        if list(board[i,:]).count(opponent[player]) == 0:
            count_player += 1
        #Row for opponent
        if list(board[i,:]).count(player) == 0:
            count_opp += 1
        #Column
        if list(board[0:-3,i]).count(opponent[player]) == 0:
            count_player += 1
        #Column for opponent
        if list(board[0:-3,i]).count(player) == 0:
            count_opp += 1
    #Diagonals
    if list(board.diagonal()).count(opponent[player]) == 0:
        count_player += 1
    if list(np.flip(board, axis = 1).diagonal()).count(opponent[player]) == 0:
        count_player += 1
    #Diagonals for opponent
    if list(board.diagonal()).count(player) == 0:
        count_opp += 1
    if list(np.flip(board, axis = 1).diagonal()).count(opponent[player]) == 0:
        count_opp += 1
    return count_player - count_opp

#This is the evaluation function which returns the value of the leaf node.
#If it is a goal state then the value will be the maximum else it will be some heuristic
def leafValue(board, currentPlayer):
    '''
    isGoalForMIN = isGoal(board, currentPlayer)
    isGoalForMAX = isGoal(board, currentPlayer)
    if MaxPlayer != currentPlayer and isGoalForMIN \
    and isGoalForMAX:
        return -1 * (N*(N+3) / board['currentDepth'])
    if isGoalForMAX:
        return 1 * (N*(N+3) / board['currentDepth'])
    else:
        if isGoalForMIN:
            return -1 * (N*(N+3) / board['currentDepth'])
    h_value = (checkInColumns(board, currentPlayer) + checkInRows(board, currentPlayer)) * (N*(N+3) / board['currentDepth'])
    return h_value
    '''
    return available_pos(board, currentPlayer)

def isLeafNode(board):
    #only for drop
    if '.' not in board['board']:
        return True
    if isGoal(board, 'o') or isGoal(board, 'x'):
        return True
    if board['currentDepth'] == MaxDepth:
       return True
    return False

def MAXValue(board, alpha, beta, player):
    if isLeafNode(board):
        return leafValue(board, player)
    for succ in successors(board, opponent[player]):
        alpha = max(alpha, MINValue(succ, alpha, beta, opponent[player]))
        if alpha >= beta:
            return alpha
    return alpha
    
def MINValue(board, alpha, beta, player):
    if isLeafNode(board):
        return leafValue(board, player)
    for succ in successors(board, opponent[player]):
        beta = min(beta, MAXValue(succ, alpha, beta, opponent[player]))
        if alpha >= beta:
            return beta
    return beta


def AlphaBetaDecision(board):
    #return a move that leads to the board corresponding to the maximum of the 
    #minimum values of the min successors
    pool_tuples = []
    pool_values = []
    alpha = -sys.maxsize
    beta = sys.maxsize
    board['currentDepth'] = 0
    bestmove = []
    #bestvalue = -sys.maxsize
    for succ in successors(board, MaxPlayer):
        current_value = MINValue(succ, alpha, beta, MaxPlayer)
        print("Min value = " + str(current_value))
        pool_tuples.append((current_value, succ))
        pool_values.append(current_value)
        if current_value > alpha:
            alpha = current_value
            bestmove = succ
    print ("maxvalue = " + str(alpha))
    return bestmove
initial_board = {'board' : createBoardFromString(BoardString, N),
                 'currentDepth' : 0, 'action' : []}  

start_time = time.time()
nextmove = AlphaBetaDecision(initial_board)
print(time.time() - start_time)
print(str(initial_board) + "\n\n" + str(nextmove))
print(str(nextmove['action'][-1]) + " " + ''.join(list(nextmove['board'].flatten())))