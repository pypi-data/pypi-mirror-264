from langchain_openai import OpenAIEmbeddings
from .text_embedder import TextEmbedder


class OpenAITextEmbedder(TextEmbedder):
    """
    Responsible for providing an OpenAI Embeddings model.
    """

    def __init__(self, api_key: str, model: str = "text-embedding-ada-002"):
        super().__init__()
        self.api_key = api_key
        self.model = model
        self._embeddings = OpenAIEmbeddings(api_key=self.api_key, model=self.model)

    @property
    def embeddings(self):
        return self._embeddings

    def embed(self, text):
        """Implementation of embedding using OpenAI."""
        # Implement the logic to embed text using the provided embedding_model
        # NOTE: I actually don't think this will be needed.
        pass
