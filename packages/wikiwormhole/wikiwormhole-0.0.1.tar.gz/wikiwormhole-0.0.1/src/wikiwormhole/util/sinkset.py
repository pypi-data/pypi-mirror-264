import random
from typing import List


class SinkSet(object):
    def __init__(self):
        self._filled = set()
        self._pool = dict()

    def fill(self, items: List[str]):
        for item in items:
            self._filled.add(item)
            self._pool[item] = True

    def drain(self, items: List[str]):
        if type(items) == str:
            items = list(items)

        for item in items:
            del self._pool[item]

    def sample(self, k: int, drop=False):
        k = min(k, len(self._pool.keys()))
        sampled = random.sample(list(self._pool.keys()), k)

        if drop:
            self.drain(sampled)

        return sampled

    def __len__(self):
        return len(self._pool.keys())
