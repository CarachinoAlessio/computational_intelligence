# Collaborators
Giuseppe Atanasio s300733, Francesco Di Gangi s301793

# What we did
In the current version of the notebook, it has been reported a version of generative search with Breadth First.
In this version we tweaked according to our needs the provided search function in the 8-puzzle example, implementing the Breadth First algorythm.

These are the tweaks:
- `problem()`
- `possible_actions()`: returns a list of tuples with elements not in the previous state;
- `is_valid()`: check if the element to be added is full contained, for each value, in the state "internal" values
- `goal_test()`: generate a set from the state and check if it contains all the values between 0 and N-1

We struggled to try implementing the A* algorithm on the search function of the Professor. It will be tweaked as soon as possible.

# Results
With the implemented "version of generative search with Breadth First", we got the following results:

|**N**|**State visited**|**Nodes**|**n.elements (w)**|
|---|---|---|---|
| 5 | 329 | 79 | 5 |
| 10 | 50.250 | 2372 | 10 |
| 20 | 361.995 | 26556 | 27 |
| 100 | N.D. | N.D. | N.D. |
| 500 | N.D. | N.D. | N.D. |
| 1000 | N.D. | N.D. | N.D. |

For values of N greater than 20 (in particular [100, 500, 1000]), the algorithm seems to spend too much time. For this reason, the results has not been reported in the upper table.