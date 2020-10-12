"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]



def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if any(None in row for row in board):
        xcount = sum(row.count(X) for row in board)
        ocount = sum(row.count(O) for row in board)

        if xcount == ocount:
            return X
        else:
            return O
    else:
        return

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i,j))

    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i < 3 and j < 3 and board[i][j] is EMPTY:
        player_name = player(board)
        new_board =  deepcopy(board)
        new_board[i][j] = player_name
        return new_board
    else:
        raise Exceptcion("Invalid Action")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Checking for rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == X:
            return X
        elif board[i][0] == board[i][1] == board[i][2] == O:
            return O

    #Checking Columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == X:
            return X
        elif board[0][i] == board[1][i] == board[2][i] == O:
            return O

    #Checking for diagonals
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    if board[0][2] == board[1][1] == board[2][0] == X:
        return X

    if board[0][0] == board[1][1] == board[2][2] == O:
        return O
    if board[0][2] == board[1][1] == board[2][0] == O:
        return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    if any(None in row for row in board):
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):

    if terminal(board):
        return None

    if player(board) == X:
        
        best_val = -1 
        best_move = (-1,1)
        c = sum(row.count(EMPTY) for row in board)
        if c == 9:
            return best_move
        for action in actions(board):
            move_value = min_value(result(board,action))
            if move_value == 1:
                best_move = action
                break
            if move_value > best_val:
                best_move = action
        return best_move

    if player(board) == O:
        best_val = 1
        best_move = (-1,1)
        for action in actions(board):
            move_value = max_value(result(board,action))
            if move_value == -1:
                best_move = action
                break
            if move_value < best_val:
                best_move = action
        return best_move

def min_value(board):
    if terminal(board):
        return utility(board)
    v = 1
    for action in actions(board):
        v = min(v,max_value(result(board,action)))
        if v == -1:
            break
    return v







def max_value(board):
    if terminal(board):
        return utility(board)
    v = -1
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
        if v == 1:
            break
    return v