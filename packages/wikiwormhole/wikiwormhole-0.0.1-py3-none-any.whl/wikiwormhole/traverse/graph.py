from typing import Set, List


class SearchGraph(object):
    class Node(object):
        def __init__(self, source_node: str) -> None:
            """
            Constructor for TableEntry, a class for recording what and how many nodes have 
            referenced this node.

            Args:
                source_node (str): the node from which this node was referenced.
            """

            self._count = 1
            self._first = source_node
            self._all_sources = set(source_node)

        def new_reference(self, source_node: str) -> None:
            """
            This subject was referenced by the source node.

            Args:
                source_node (str): the node from which this node was referenced.
            """

            if source_node not in self._all_sources:
                self._count += 1
                self._all_sources.add(source_node)

        def total_references(self) -> int:
            """
            Returns the total number of unique source nodes that reference this node.

            Returns:
                int: The total number of unique source nodes that reference this node.
            """

            return self._count

        def first_reference(self) -> str:
            """
            Returns the last node to reference this subject.

            Returns:
                str: The last node to reference this subject.
            """

            return self._first

        def all_references(self) -> Set[str]:
            """
            Returns all nodes that have referenced this node.

            Returns:
                List[str]: All nodes that have referenced this node.
            """

            return self._all_sources

    def __init__(self, root: str) -> None:
        """
        Constructor for search graph.

        Args:
            root (str): the first node from which all target nodes can be
                connected to. 
        """

        self._graph = dict()
        self._root = root

    def new_edge(self, source_node: str, target_node: str) -> None:
        """
        Adds a new edge in the search graph going from the source to the target node.

        Args:
            source_node (str): node from which edge originates.
            target_node (str): node that edge points to.

        Raises:
            Exception: Invalid source or target node. 
        """

        if source_node == "" or target_node == "":
            raise Exception(
                "SearchGraph.new_edge: please provide a valid source and target node.")

        if target_node in self._graph.keys():
            self._graph[target_node].new_reference(source_node)
        else:
            self._graph[target_node] = self.Node(source_node)

    def node_exists(self, node: str) -> bool:
        """
        Does the node exist?

        Args:
            node (str): node we are checking the existence of.

        Returns:
            bool: does the node exist in the graph?
        """

        return node in self._graph.keys() or node == self._root

    def total_references(self, node: str) -> int:
        """
        Returns the total number of unique source nodes that reference this node.

        Args:
            node (str): the node being referred.

        Returns:
            int:  number of unique source nodes that reference this node.
        """

        return self._graph[node].total_references() if self.node_exists(node) else 0

    def parent(self, node: str) -> str:
        """
        Returns the last node pointing at this node.

        Args:
            node (str): the node that is being referenced.

        Returns:
            str: the last node pointing at this node.
        """

        return self._graph[node].first_reference() if self.node_exists(node) else ""

    def unravel(self, final_node: str) -> List[str]:
        """
        Find the path from the root node to the final node.

        Args:
            final_node (str): the final node in the path.

        Returns:
            List[str]: a list of the nodes connecting the root to the path.
        """

        trace = [final_node]
        curr_node = final_node

        while curr_node != self._root:
            curr_node = self._graph[curr_node].first_reference()
            trace.append(curr_node)

        trace.append(self._root)

        return trace[::-1]

    def __len__(self):
        return len(self._graph)

    def target_nodes(self):
        return self._graph.keys()
