"""
Tic Tac Toe Player
"""

import math
import copy

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
    values = {X: 0, O: 0, EMPTY: 0}

    for row in board:
        for elem in row:
            values[elem] = values[elem] + 1
    
    if values[X] > values[O]:
        return O
    
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError
    
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise ValueError
    
    tempBoard = copy.deepcopy(board)
    tempBoard[action[0]][action[1]] = player(board)
    return tempBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    diagonal = {X: 0, O: 0, EMPTY: 0}
    secondary_diagonal = {X: 0, O: 0, EMPTY: 0}

    for i in range(3):
        row = {X: 0, O: 0, EMPTY: 0}
        column = {X: 0, O: 0, EMPTY: 0}

        diagonal[board[i][i]] = diagonal[board[i][i]] + 1
        secondary_diagonal[board[i][-(i+1)]] = secondary_diagonal[board[i][-(i+1)]] + 1

        for j in range(3):
            row[board[i][j]] = row[board[i][j]] + 1
            column[board[j][i]] = column[board[j][i]] + 1

            if row[X] == 3 or column[X] == 3:
                return X
            elif row[O] == 3 or column[O] == 3:
                return O

    if diagonal[X] == 3 or secondary_diagonal[X] == 3:
        return X
    elif diagonal[O] == 3 or secondary_diagonal[O] == 3:
        return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # it means that there is no EMPTY on the board
    if not actions(board):
        return True
    
    # here we know that we have EMPTY on the board, so if there is no winner, the game is not over
    if winner(board) == None:
        return False
    
    # if there is EMPTY on the board, but there is a winner, the game is over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    if win == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        return max_value(board)[1]

    else:
        return min_value(board)[1]
    
    
def max_value(board):
    if terminal(board):
        return utility(board), None
    
    v = -math.inf

    for action in actions(board):
        before = v
        v = max(v, min_value(result(board, action))[0])

        if before != v:
            before = v
            optimal_action = action
    
    return v, optimal_action


def min_value(board):
    if terminal(board):
        return utility(board), None
    
    v = math.inf

    for action in actions(board):
        before = v
        v = min(v, max_value(result(board, action))[0])

        if before != v:
            before = v
            optimal_action = action

    return v, optimal_action