from collections import namedtuple
from copy import deepcopy
from itertools import accumulate
from operator import xor

Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k
        self.state_history = [(self.rows, None)]

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    @property
    def last_state_action(self):
        if self.state_history:
            print('state, action', self.state_history[-1])
            return self.state_history[-1]
        else:
            return self.rows, None

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        if self.k is not None:
            num_objects = min(num_objects, self.k)
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects
        self.state_history.append((self.rows, (row,num_objects)))

    def get_reward(self):
        *_, result = accumulate(self.rows, xor)
        if result == 0:
            return 0
        else:
            return -1


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result

def sum_with_op(state: Nim, op) -> int:
    *_, result = accumulate(state.rows, op)
    return result


def cook_status_t1(state: Nim) -> dict:
    cooked = dict()

    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    # cooked["nim_sum"] = nim_sum(state)
    cooked["avg_objects"] = sum(i for i in state.rows) / len(state.rows)
    cooked["over_avg_rows"] = list(i for i, e in enumerate(state.rows) if e >= cooked["avg_objects"])
    cooked["under_avg_rows"] = list(i for i, e in enumerate(state.rows) if e <= cooked["avg_objects"] and e != 0)

    if cooked["active_rows_number"] / len(state.rows) > 0.8:
        cooked["game_type"] = "early"
    elif cooked["active_rows_number"] <= 3:
        cooked["game_type"] = "end"
    else:
        cooked["game_type"] = "mid"

    brute_force = list()
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked["brute_force"] = brute_force

    return cooked


def cook_status_t2(state: Nim) -> dict:
    cooked = dict()

    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)
    cooked["num_obj"] = sum(o for o in state.rows)

    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
    # cooked["nim_sum"] = nim_sum(state)
    cooked["avg_objects"] = sum(i for i in state.rows if i > 0) / cooked["active_rows_number"]
    cooked["over_avg_rows"] = list(i for i, e in enumerate(state.rows) if e >= cooked["avg_objects"])
    cooked["under_avg_rows"] = list(i for i, e in enumerate(state.rows) if e <= cooked["avg_objects"] and e != 0)

    if cooked["active_rows_number"] / len(state.rows) > 0.8:
        cooked["game_type"] = "early"
    elif cooked["active_rows_number"] / len(state.rows) > 0.2:
        cooked["game_type"] = "mid"
    else:
        cooked["game_type"] = "end"

    return cooked
