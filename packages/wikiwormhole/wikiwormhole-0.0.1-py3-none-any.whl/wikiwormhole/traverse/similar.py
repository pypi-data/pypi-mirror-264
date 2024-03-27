from wikiwormhole import wikiapi
from wikiwormhole.title2vec import Title2Vec, EmbeddedTitle
import numpy as np
from wikiwormhole.traverse.traverse import Traverse
from wikiwormhole.util.fixedpq import FixedPriorityQueue


class SimilarTraverse(Traverse):
    def __init__(self, start_subject: str, target_subject: str, t2v: Title2Vec, priority_queue_size=10, decay_factor=0.9) -> None:
        """
        Constructor for SimilarTraverse.

        This algorithm uses the pretrained gensim Word2Vec model
        to estimate the similarities between two titles and move accordingly.

        Args:
            start_subject (str): the starting subject to navigate to the target subject from. 
            target_subject (str): the subject we are trying to get to from the starting point.
            t2v (Title2Vec): a Word2Vec model for embedding titles.
            priority_queue_size (int): size of fixed priority queue. A smaller size promotoes emphasis on
                depth over breadth.
            decay_factor (float): the decay factor used for calculating similarity between two titles. 
        """

        super(SimilarTraverse, self).__init__(start_subject)
        self._target = target_subject

        self._active_page = wikiapi.generate_wiki_page_from_title(
            start_subject)
        self._t2v = t2v

        self._target_embedded = self._t2v.embed_title(target_subject)
        self._blacklist = list()
        self._sim_scores = dict()
        self._fixpq = FixedPriorityQueue(priority_queue_size, True)

        self._decay_factor = decay_factor

    def target_found(self) -> bool:
        """
        Has the target been reached in the graph?

        Returns:
            bool: the target has been reached if true.
        """

        return self._graph.node_exists(self._target)

    def traverse(self):
        """
        This algorithm works as follows:
        1. Loop through all outgoing links for the current page.
        2. For each link do steps 3-6
        3. Add link to the graph.
        4. Embed the link using pre-trained Word2Vec model.
        5. Calculate similarity between link and title.
        6. Save link if its the most similar page encountered so far.
        7. Select the most similar page as the next node.

        Sometimes dead ends will be encountered so this algorithm backtracks
        until it escapes the dead end.
        """

        success_traverse = False
        while not success_traverse:
            try:
                self._attempt_traverse()
                success_traverse = True
            except Exception:
                failed_subject = self._trace.pop()
                prev_subject = self._trace[-1]

                # Undo traversal.
                self._subject = prev_subject
                self._active_page = wikiapi.generate_wiki_page_from_title(
                    prev_subject)

                # Remember the failed page.
                self._blacklist.append(failed_subject)

    def _attempt_traverse(self):
        """
        This algorithm works as follows:
        1. Loop through all outgoing links for the current page.
        2. For each link do steps 3-6
        3. Add link to the graph.
        4. Embed the link using pre-trained Word2Vec model.
        5. Calculate similarity between link and title.
        6. Save link if its the most similar page encountered so far.
        7. Select the most similar page as the next node.
        """

        # Find the node connected to this page with the highest similarity
        for link in wikiapi.retrieve_outgoing_links(self._active_page):
            title = link.title()

            # Don't vist past, failed, or invalid nodes.
            if (title in self._trace or
                title in self._blacklist or
                    not Traverse.valid_page(title)):
                continue

            # Inform the graph of this new connection
            self._graph.new_edge(self._subject, title)

            if title not in self._sim_scores.keys():

                # Embed the title.
                embedded_title = self._t2v.embed_title(title)
                if len(embedded_title) == 0:
                    continue

                # Calculate the similarity between the two titles.
                sim_score = self.title_sim_score(
                    self._target_embedded, embedded_title)

                self._sim_scores[title] = sim_score

            sim_score = self._sim_scores[title]

            self._fixpq.push(sim_score, title)

        # Move to the most similar page.
        if len(self._fixpq) > 0:
            _, self._subject = self._fixpq.pop()
            self._active_page = wikiapi.generate_wiki_page_from_title(
                self._subject)
            self._trace.append(self._subject)
        else:
            raise Exception("SimilarTraverse.traverse: no valid pages found.")

    def title_sim_score(self, title1: EmbeddedTitle, title2: EmbeddedTitle) -> float:
        """
        For the NLP domain, this code utilizes the cosine similarity.

        Args:
            title1 (EmbeddedTitle): the first embedded title.
            title2 (EmbeddedTitle): the second embedded title.

        Returns:
            float: the cosine similarity between the two given titles.
        """

        A = title1.get_vectors()
        B = title2.get_vectors()

        dot = np.dot(A, B.T)

        A_norm = np.linalg.norm(A, axis=1)
        B_norm = np.linalg.norm(B, axis=1)

        A_norm = A_norm.reshape(-1, 1)
        B_norm = B_norm.reshape(1, -1)

        sim_mat = dot / A_norm
        sim_mat = sim_mat / B_norm

        similarity = 0

        sim_scores = sorted(sim_mat.reshape(-1))
        prop_rem = 1
        for i, sim_score in enumerate(sim_scores[::-1]):
            if i == len(sim_scores)-1:
                similarity += sim_score * prop_rem
            else:
                similarity += sim_score * (self._decay_factor*prop_rem)
                prop_rem -= self._decay_factor * prop_rem

        return similarity
