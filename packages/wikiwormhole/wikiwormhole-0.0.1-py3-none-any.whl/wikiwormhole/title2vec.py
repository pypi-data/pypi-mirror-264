from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import numpy as np
from typing import List
import string
import nltk
import os

# constants
W2V_PRETRAINED_MODEL = "fasttext-wiki-news-subwords-300"
W2V_KEY_LIMIT = 200000


class EmbeddedTitle(object):
    def __init__(self):
        self.vectors = list()
        self.tokens = list()
        self.size = 0

    def add(self, token, vector):
        self.tokens.append(token)
        self.vectors.append(vector)
        self.size += 1

    def get_vectors(self):
        return np.array(self.vectors)

    def get_tokens(self):
        return self.tokens

    def __len__(self):
        return self.size


class Title2Vec(object):
    def __init__(self, download_path: str):
        """
        Constructor for Title2Vec.

        Downloads the Word2Vec model along with the natural language toolkit.
        """

        # Load the W2V model into embedder
        pretrained_path = os.path.join(
            download_path, "w2v", W2V_PRETRAINED_MODEL, f"{W2V_PRETRAINED_MODEL}.gz")

        if not os.path.exists(pretrained_path):
            raise Exception(
                "Title2Vec.__init__: please download pretrained model.")

        self._embedder = KeyedVectors.load_word2vec_format(pretrained_path,
                                                           binary=False,
                                                           limit=W2V_KEY_LIMIT)

        # Ensure directory for holding nltk stopwords exists.
        nltk_path = os.path.join(download_path, "nltk")

        # load the stopwords
        nltk.data.path.append(nltk_path)
        self._stopwords = set(stopwords.words("english"))

    def embed_title(self, title: str) -> EmbeddedTitle:
        """
        Returns the embedding of the title using W2V model.

        Args:
            title (str): the title to be embedded.

        Returns:
            _type_: a Vectorized title representing the title.
        """

        tokens = Title2Vec._tokenize_string(title)
        tokens = self._remove_stopwords(tokens)

        vectors = self._embedder.vectors_for_all(tokens)

        embedded_title = EmbeddedTitle()
        for token in tokens:
            if vectors.has_index_for(token):
                embedded_title.add(token, vectors[token])

        return embedded_title

    def embed_word(self, word: str) -> np.ndarray:
        """
        Returns the embedding of the word using W2V model.

        Args:
            word (str): the word to be embedded.

        Returns:
            _type_: an embedded vector representing the provided word.
        """

        try:
            return self._embedder.get_vector(word.lower())
        except KeyError:
            return np.empty((0, 0))

    def _remove_stopwords(self, tokens: List[str]):
        """
        Remove insignificant stop words from list of tokens.

        Args:
            tokens (list): a list of tokens.

        Returns:
            _type_: a list of tokens with no insignificant stop words.
        """

        return [token for token in tokens if not token in self._stopwords]

    @staticmethod
    def _tokenize_string(s: str, lower=True) -> List[str]:
        """
        Tokenize the given string

        Args:
            s (str): the string to be tokenized.
            lower (bool, optional): output all tokens as lowercase. Defaults to True.

        Returns:
            _type_: a list of tokens.
        """

        # Split string into tokens.
        tokens = nltk.tokenize.word_tokenize(s)
        # Remove invalid tokens.
        tokens = [t for t in tokens if t[0] not in string.punctuation]

        # Put all tokens in lowercase
        if lower:
            tokens = [t.lower() for t in tokens]

        return tokens
