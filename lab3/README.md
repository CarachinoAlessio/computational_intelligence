# Lab 3 - Alessio Carachino

You can find the solution in the `taskN_lib` for each task.

## **Problem**

Create four different agents for the game `Nim`, you can find the full description in `lab3_nim.ipynb`

## **Task 3.1**

The hardcoded strategy tries to exploit the number of object we could take depending on the number of `active_rows` left.
It is more of a late game oriented and it can easily loses versus early game strategy (check `nim-sum` based strategies).

Here is the workflow of the algorithm:
```
    if number of rows is odd:
        take all objects from a random row
    else if the number of rows is even and the longest row has more than one object:
        take objects-1 from a random row with more than one object
    else:
        take all objects from a random row
```

## **Task 3.2** 

### **Strategy 0**
It tries to tune three parameters:
1) **alpha**: it is employed until 'mid-game' finishes. It tries to guide the choice of `num_objects`.
2) **beta**: employed only in 'end-game'. It tries to guide the choice of `num_objects`.
3) **gamma**: employed only in 'eng-game'. It guides whether picking a row with `num_objects` over the average (otherwise below).

### **Strategy 1**
The idea behind this strategy is to use the parameters `alpha` and `beta` to tune the two part of the strategy:

```
    if cooked["num_obj"] / cooked["active_rows_number"] * alpha > beta:
```
The metric `cooked["num_obj"] / cooked["active_rows_number"]` is the non-weighted distribution of the objects over the rows, which means it doesn't take into account that the higher is the index of a row, the higher is the possibility that more object are in there.

The two branches of this strategy exploit the hard-coded strategy in `Task 3.1` but it changes the number of objects to take or from which row the objects have to be taken.

In the end it can achieves 100% winrate over 100 games versus the `pure_random`, and the average win rate is 95%.
It doesn't beat the `optimal_strategy` and that makes sense because we don't exploit `xor` operations or `nim-sum`.

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
| strategy_1          | strategy_0            | 80%                    |


# **Collaborators**
- s296138 Carachino Alessio
- s301665 Francesco Sorrentino
- s301793 Francesco Di Gangi
- s300733 Giuseppe Atanasio