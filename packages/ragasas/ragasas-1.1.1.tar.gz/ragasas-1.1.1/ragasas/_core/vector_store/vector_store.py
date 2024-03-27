from abc import ABC, abstractmethod


class Vectorstore(ABC):
    @abstractmethod
    def __init__(self, embedder, save_type=None):
        pass

    @abstractmethod
    def as_retriever(self):
        """Abstract method to"""
        pass
