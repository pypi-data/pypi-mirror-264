from wikiwormhole.util.sinkset import SinkSet
from wikiwormhole.traverse.traverse import Traverse
from wikiwormhole import wikiapi
from typing import List
from datetime import datetime


class PopularTraverse(Traverse):
    def __init__(self, start_subject: str, pv_config_path: str, explore_per_traversal=5) -> None:
        """
        Constructor for Popular Traversal.

        This algorithm visits random pages stemming from a root page
        and records the connectivity of specific nodes. Operates under the assumption
        that a higher connectivity corresponds to a higher popularity.

        Args:
            start_subject (str): The root of our search for which all nodes must stem from.
            pv_config_path (str): path to the .yaml file configurations for pageviews API.
            explore_per_traversal (int): number of nodes to randomly explore on each traversal.
        """
        super(PopularTraverse, self).__init__(start_subject)

        self._active_page = wikiapi.generate_wiki_page_from_title(
            start_subject)
        self._frontier = SinkSet()
        self._frontier.fill([start_subject])

        self._explore_per_traversal = explore_per_traversal

        self._pv_config_path = pv_config_path

    def traverse(self) -> None:
        """
        Move to the next most popular node.

        Algorithm:
        1. Select k random nodes to explore from the SinkSet.
        2. Record each sampled node's outgoing connections in the graph.
        3. Identify the node with the highest connectivity, "popularity".
        4. Set the node as the current node.

        Raises:
            Exception: no nodes are available to be explored.
        """

        # Select nodes from the frontier to explore
        explore = self._frontier.sample(self._explore_per_traversal, True)

        if len(explore) == 0:
            raise Exception(
                "PopularTraverse.traverse: No nodes to be explored.")

        # Explore each node
        for node in explore:
            # Add outgoing connections to graph for current node
            page = wikiapi.generate_wiki_page_from_title(node)
            for link in wikiapi.retrieve_outgoing_links(page):
                if not Traverse.valid_page(link.title()):
                    continue
                self._graph.new_edge(node, link.title())
                self._frontier.fill([link.title()])

        # Identify most popular node
        max_refs, pop_node = -1, ""
        for node in self._graph.target_nodes():
            # Prevent revisiting nodes.
            if node in self._trace:
                continue
            # If the node has a higher connectivity set it as the most popular node.
            if self._graph.total_references(node) > max_refs:
                max_refs = self._graph.total_references(node)
                pop_node = node

        # Update state.
        self._trace.append(pop_node)
        self._active_page = wikiapi.generate_wiki_page_from_title(pop_node)
        self._subject = pop_node

    def most_popular_pathway(self) -> List[str]:
        """
        Identify the most popular node and the pathway from the root
        to get to it.

        Here popularity is determined by pageviews. By not using this metric
        in traverse we prevent a slew of API calls that can slowdown and prevent
        further access to the API.

        Returns:
            List[str]: the route from the root node to the most popular node.
        """

        # Identifiy the most popular node in the trace.
        # This metric uses pageviews instead.
        max_views, pop_page = -1, ""

        for page in self._trace:
            page = wikiapi.generate_wiki_page_from_title(page)
            try:
                views = sum(wikiapi.retreive_pageviews(
                    page, self._pv_config_path))
            except Exception as e:
                continue

            # Does page have the most views.
            if views > max_views:
                max_views = views
                pop_page = page

        return self._graph.unravel(pop_page.title())
