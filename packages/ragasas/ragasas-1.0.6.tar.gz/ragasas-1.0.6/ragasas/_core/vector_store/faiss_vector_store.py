from .vector_store import Vectorstore
from langchain_community.vectorstores import FAISS
from ..embedder.text_embedder import TextEmbedder


class FAISSVectorstore(Vectorstore):
    def __init__(self, embedder: TextEmbedder) -> None:
        super().__init__()
        self.embedder = embedder
        self.texts = None
        self._vector_store = None

    @property
    def vector_store(self):
        return self._vector_store

    @vector_store.setter
    def vector_store(self, texts):
        self.texts = texts
        self._vector_store = FAISS.from_texts(texts, self.embedder.embeddings)

    def as_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs={"k": 20}
        )  # NOTE: What if we asked another chatbot 'based on the question from the user, what would be the most optimal argument for "k"?'
