from abc import ABC, abstractmethod


class Vectorstore(ABC):
    @abstractmethod
    def as_retriever(self):
        """Abstract method to"""
        pass
