from heapq import heappush, heappop, nlargest
from typing import Tuple, Any
import bisect


class FixedPriorityQueue(object):
    def __init__(self, k: int, max_priority=False) -> None:
        if k <= 0:
            raise Exception(
                "FixedPriorityQueue.__init__: k must be greater than 0")
        self._max_size = k
        self._pq = list()
        self._vals = set()
        self._max_priorty = max_priority

    def push(self, order: float, val: Any) -> None:
        if val in self._vals:
            return

        bisect.insort(self._pq, (order, val))
        self._vals.add(val)

        if len(self._pq) > self._max_size:
            _, val_pop = self._pq.pop(0)
            self._vals.remove(val_pop)

    def pop(self) -> Tuple[float, Any]:
        if len(self._pq) == 0:
            return 0, None

        idx_pop = -1 if self._max_priorty else 0
        ord_pop, val_pop = self._pq.pop(idx_pop)
        self._vals.remove(val_pop)

        return ord_pop, val_pop

    def max_size(self) -> int:
        return self._max_size

    def __len__(self) -> int:
        return len(self._pq)
