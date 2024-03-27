from abc import ABC, abstractmethod
import stat
from wikiwormhole.traverse.graph import SearchGraph


class Traverse(ABC):
    def __init__(self, start_subject: str):
        self._subject = start_subject
        self._trace = [start_subject]
        self._graph = SearchGraph(start_subject)

    @abstractmethod
    def traverse(self):
        pass

    @staticmethod
    def valid_page(title: str):
        title = title.lower()
        if 'wayback' in title or 'identifier' in title:
            return False
        return True
