# Lab 3 - Giuseppe Atanasio

You can find the solution in the `taskN_lib` for each task.

## **Problem**

Create four different agents for the game `Nim`, you can find the full description in `lab3_nim.ipynb`

## **Task 3.1 - Hard-coded rules-based strategy**

The hardcoded strategy tries to exploit the number of object we could take depending on the number of `active_rows` left.
It is more of a late game oriented and it can easily lose versus early game strategy (check `nim-sum` based strategies).

Here is the workflow of the algorithm:
```
    if number of rows is odd:
        take all objects from a random row
    else if the number of rows is even and the longest row has more than one object:
        take objects-1 from a random row with more than one object
    else:
        take all objects from a random row
```

## **Task 3.2 - Genetic Algorithm-based strategies** 

### **Strategy 0**
It tries to tune three parameters:
1) **alpha**: it is employed until 'mid-game' finishes. It tries to guide the choice of `num_objects`.
2) **beta**: employed only in 'end-game'. It tries to guide the choice of `num_objects`.
3) **gamma**: employed only in 'end-game'. It guides whether picking a row with `num_objects` over the average (otherwise below).

### **Strategy 1**
The idea behind this strategy is to use the parameters `alpha` and `beta` to tune the two part of the strategy:

```
    if cooked["num_obj"] / cooked["active_rows_number"] * alpha > beta:
```
The metric `cooked["num_obj"] / cooked["active_rows_number"]` is the non-weighted distribution of the objects over the rows, which means it doesn't take into account that the higher is the index of a row, the higher is the possibility that more object are in there.

The two branches of this strategy exploit the hard-coded strategy in `Task 3.1` but it changes the number of objects to take or from which row the objects have to be taken.

In the end it can achieves 100% winrate over 100 games versus the `pure_random`, and the average win rate is 95%.
It doesn't beat the `optimal_strategy` and that makes sense because we don't exploit `xor` operations or `nim-sum`.

### **Strategy 2**
There are four parameters in this case.

The concept is computing a different accumulation operation (and - or - xor),
randomly picked according to the weight parameters (alpha - beta - gamma).
The 'percentage' parameter is employed to choose how many objects must be selected.

The choice is made initializing (with 'percentage')
an array sorted with a lambda where the elements are put in the array according to their distance from the num_objects of the
longest row; 'perc' determines how much the points must be distant from the longest_row.

After some generations, it will learn to exploit xor only (and it retrieves the optimal-strategy).

## **Task 3.3 MinMax strategy**

Behind the implementation of the `nim` with `minmax` there is the basic structure of the algorithm `minmax`:

```
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
            minEval=min(minEval,eval)
        return minEval
```

There are few main solutions:
- `possible_new_states`: understand the next state
- `evaluate`: understand if the game is over
- `possible_moves`: calculate all the moves for the program

### **Alpha Beta Pruning**

Basically you consider branches from left to right and sto exploring subtrees once the minimax score of a node is decided. In this way the game become much smaller. 

Alpha-beta pruning is a search algorithm that seeks to decrease the number of nodes that are evaluated by the minmax algorithm. 

To implement the algorithm we refactored the `minimax()` function and add a criterion to the to know when we can stop exploring:

- `alpha`: will represent the minimum score that the maximizing player is ensured.
- `beta`: will represent the maximum score that the minimizing player is ensured.

```
if beta < alpha: stop exploring -> means that the minimax has already found a better option
```

This is implemented with an explicit `for` loop. The scores of child nodes are in the `scores` variable. Also, each `minimax()` iteration, `alpha` and `beta` are changed:

```
if is_maximizing:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
```

Note that this is only optimization and does not change the output of the minmax algorithm, so the results are the same. We can also see that the execution time is better with the alpha-beta pruning.

| **Alpha** | **Beta** | **Time**             |
|-----------|----------|----------------------|
| -1        | 1        | 0.08599638938903809  |
| -0.5      | 1        | 0.033998727798461914 |
| -0.5      | 0.5      | 0.06699728965759277  |
| -1        | 0.5      | 0.053972721099853516 |

Minmax strategy always wins.

Theory and part of the code: https://realpython.com/python-minimax-nim/#lose-the-game-of-nim-against-a-python-minimax-player

Theory about ALpha-beta pruning: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

## Task 3.4 - Reinforcement Learning
We have considered Q-learning and we have taken inspiration to bblais' Game setups.

Our accuracies are sampled and calculated for each 100 games.

We have used three hyperparameters:
- `alpha`: learning rate
- `gamma`: memory multiplier
- `epsilon`: the chance of making a random move

| `alpha` | `gamma` | `epsilon` |
|---------|---------|-----------|
| 0.3     | 0.9     | 0.1       |

Despite the previous methods, this requires many iteration to reach a sort of convergence. That's why we have iterated among 5000 games, and we have reached a suboptimal result against `gabriele` of 98% after 3500 iterations.

For what concerns our RL agent against `optimal_strategy`, there is a plateau due to continue loses of our agent, but this situation changes after almost 3kth iteration. 
It has turned out that for 10k iterations the max accuracy still increases, so we enhanced the iterations up to 30k and we obtained a max winrate of 81% after 28100 iterations. 

Please note: these values are mutable and they have to be considered as an approximation.

References: [Bblais'Game](https://github.com/bblais/Game)

# **Results**

These results are calculated over 100 games on average.

| **Strategy**        | **Opponent strategy** | **Average Win Rate %** |
|---------------------|-----------------------|------------------------|
| hard_coded_strategy | gabriele              | 100%                   |
| hard_coded_strategy | pure random           | 90%                    |
| strategy_0          | gabriele              | 85%                    |
| strategy_0          | pure random           | 45%                    |
| strategy_1          | gabriele              | 100%                   |
| strategy_1          | pure random           | 97%                    |
| strategy_2          | gabriele              | 98%                    |
| strategy_2          | pure random           | 98%                    |
| strategy_1          | strategy_0            | 80%                    |

Results for Q-learning agent:

| **Opponent strategy** | **Average Win Rate %** | **Average iterations** |
|-----------------------|------------------------|------------------------|
| gabriele              | 98%                    | 3500                   |
| pure random           | 81%                    | 28100                  |

# **Collaborators**
- s296138 Carachino Alessio
- s301665 Francesco Sorrentino
- s301793 Francesco Di Gangi
- s300733 Giuseppe Atanasio