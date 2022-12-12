from nimply import Nimply
from nimply import Nim
from copy import deepcopy
import logging
import time

"""
Generic implementation

def minimax(currentpos,depth,maximizingplayer):
    if depth==0:
        return currentpos
    if maximizingplayer: #we want to get the max
        maxEval=-infinity
        for each child of position
            eval=minimax(child,depth-1,false)
            maxEval=max(maxEval,eval)
        return maxEval

    else
        minEval=+infinity
        for each child of position
            eval=minimax(minEval,eval)
            minEvail=min(minEval,eval)
        return minEval
"""

"""
With possible_new_states(),
you calculate the possible next states while making sure that a player can’t take more counters than those available on the board.
"""


def possible_moves(state: Nim):
    # retrieve all the possible moves
    # state is NIM so it is needed to explicitly use rows
    return [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]


def possible_new_states(state: Nim):
    # returns a list of outcome of all possible moves
    states = []
    # check available states
    for p in possible_moves(state):
        tmp = deepcopy(state)
        tmp.nimming(Nimply(p[0], p[1]))
        states.append(tmp)
    return states


"""
You evaluate a game position with evaluate().
If there are no counters left, then the function returns 1 if the maximizing player won the game and -1 if the other—minimizing—player won.
If the game isn’t over, execution will continue to the end of the function and implicitly return None.
"""


def evaluate(state, is_maximizing):
    if state == 0:
        return 1 if is_maximizing else -1


# understand the best possible move to do (highest in score)

# minmax strategy
def minimax(state: Nim, is_maximizing):
    # ending position
    if sum(r for r in state.rows) == 0:
        return -1 if is_maximizing else 1

    if is_maximizing:
        scores = [
            minimax(new_state, is_maximizing=False)
            for new_state in possible_new_states(state)
        ]
        return max(scores)
    else:
        scores = [
            minimax(new_state, is_maximizing=True)
            for new_state in possible_new_states(state)
        ]
        return min(scores)


# max_turn=is_maximizing

def minmax_strategy(state: Nim):
    for move in possible_moves(state):
        # from lecture code
        tmp = deepcopy(state)
        tmp.nimming(Nimply(move[0], move[1]))
        # calculate the score
        score = minimax(tmp, is_maximizing=False)
        if score > 0:
            break
    return Nimply(move[0], move[1])


# -------------------------- With alpha and beta pruning -----------------------------
"""
alpha will represent the minimum score that the maximizing player is ensured.
beta will represent the maximum score that the minimizing player is ensured.
"""


def minimax_pruning(state, is_maximizing, alpha=-0.5, beta=1):
    # ending position
    if sum(r for r in state.rows) == 0:
        return -1 if is_maximizing else 1

    scores = []
    for new_state in possible_new_states(state):
        scores.append(
            score := minimax_pruning(new_state, not is_maximizing, alpha, beta)
        )
        if is_maximizing:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
        if beta <= alpha:
            break
    return (max if is_maximizing else min)(scores)


def minmax_strategy_pruning(state: Nim):
    for move in possible_moves(state):
        # from lecture code
        tmp = deepcopy(state)
        tmp.nimming(Nimply(move[0], move[1]))
        # calculate the score
        score = minimax_pruning(tmp, False)
        if score > 0:
            break
    return Nimply(move[0], move[1])


def task_3_run(opponent_strategy, is_opponent_starting=False):
    start_time = time.time()
    logging.getLogger().setLevel(logging.INFO)

    strategy = (minmax_strategy, opponent_strategy)
    nim = Nim(3)

    logging.debug(f"status: Initial board  -> {nim}")
    player = int(is_opponent_starting)
    while nim:
        ply = strategy[player](nim)
        nim.nimming(ply)
        logging.debug(f"status: After player {player} -> {nim}")
        player = 1 - player
    winner = 1 - player
    if winner == 0:
        winner = 'Minmax'
    else:
        winner = 'Opponent'
    logging.info(f"status: {winner} won!")

    print("--- %s seconds ---" % (time.time() - start_time))
