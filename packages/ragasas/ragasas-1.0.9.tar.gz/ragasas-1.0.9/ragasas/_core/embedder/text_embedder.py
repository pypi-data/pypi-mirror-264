from abc import ABC, abstractmethod


class TextEmbedder(ABC):
    @property
    @abstractmethod
    def embeddings(self):
        pass

    @abstractmethod
    def embed(self, text):
        """Abstract method to embed text."""
        pass
