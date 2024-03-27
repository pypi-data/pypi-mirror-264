import html2text
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import requests
from .vector_store import Vectorstore
from langchain_community.vectorstores import FAISS
from ..embedder.text_embedder import TextEmbedder
import logging


class FAISSVectorstore(Vectorstore):
    """
    A class representing a vector store using FAISS.

    Attributes:
        embedder (TextEmbedder): The text embedder used for generating embeddings.
        texts (List[str]): List of texts whose embeddings are stored.
        _vector_store (FAISS): The FAISS database storing the embeddings.
    """

    def __init__(self, embedder: TextEmbedder) -> None:
        """
        Initializes the FAISSVectorstore with the given embedder and save type.

        Args:
            embedder (TextEmbedder): The text embedder used for generating embeddings.
        """
        self.embedder = embedder
        self.data = None
        self._vector_store = None

    @property
    def vector_store(self) -> FAISS:
        """
        Get the FAISS vector store.

        Returns:
            FAISS: The FAISS vector store.
        """
        return self._vector_store

    def create_vector_store(
        self, data: object, path: str, save_to_cloud: bool, from_urls=False
    ) -> None:
        """
        Set the vector store by embedding data and saving the FAISS database.

        Args:
            texts (obect):
                (str) String that is an absolute path to a folder containing a FAISS database that was saved to disk. OR
                (list) List of strings whose embeddings are stored in a FAISS database. OR
                (list) List of URLs whose HTML is scraped, embedded, and stored in a FAISS database
            path (str): The absolute path to the folder where the database should be saved. Does not save DB to disk if 'path' is None or empty string.
            save_to_cloud (bool): If True, then upload the vector database to the cloud.
        """
        self.data = data
        if isinstance(self.data, list):
            # TODO: Handle the case where at least one url is invalid.
            if all([self._is_valid_url(url) for url in self.data]):
                for i, url in enumerate(self.data):
                    # TODO: Protect against response being larger than available RAM
                    # TODO: Improve preprocessing
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, "html.parser")
                    text = html2text.html2text(str(soup))
                    # TODO: Find a better way to create and extend the datastore
                    if i == 0:
                        self._vector_store = FAISS.from_texts(
                            [text], self.embedder.embeddings, metadatas=[{"URL": url}]
                        )
                    else:
                        self._vector_store.add_texts([text], metadatas=[{"URL": url}])
            else:
                self._vector_store = FAISS.from_texts(
                    self.data, self.embedder.embeddings
                )
        elif isinstance(self.data, str):
            if os.path.isabs(self.data):
                self._vector_store = FAISS.load_local(
                    self.data,
                    self.embedder.embeddings,
                    allow_dangerous_deserialization=True,  # TODO: figure out how to get around this deserialization param
                )
            else:
                raise ValueError(
                    "Argument 'data' must be an absolute path to an existing vectorstore when its type is 'str'."
                )

        self._save(path, save_to_cloud)

    def _save(self, path: str, save_to_cloud: bool) -> None:
        """
        Save the FAISS database based on the save type.

        Args:
            path (str): The absolute path to the folder where the database should be saved. Does not save DB to disk if 'path' is None or empty string.
            save_to_cloud (bool): If True, then upload the vector database to the cloud.
        """
        if not (path in (None, "")):
            self.save_to_disk(path)
        if save_to_cloud:
            self.save_to_cloud()

    def save_to_disk(self, absolute_path: str) -> None:
        """
        Save the FAISS database to disk.

        Args:
            absolute_path (str): The absolute path to the folder where the database should be saved.
        """
        if absolute_path:
            self.vector_store.save_local(absolute_path)

    def save_to_cloud(self):
        pass  # TODO

    def as_retriever(self, k=4):
        """
        Get a retriever instance configured for vector search.

        Returns:
            langchain_core.vectorstores.VectorStoreRetriever: A retriever instance configured for vector search operations.

        Notes:
            This method returns a retriever instance tailored for vector search operations,
            specifically utilizing the FAISS library. The default behavior is to return the
            retriever with a search parameter 'k' set to 4, which determines the number of
            nearest neighbors to return in search results. Adjusting 'k' may optimize
            retrieval performance based on specific use cases or requirements.

            Considerations:
            - For tasks requiring broader context or more diverse results, increasing 'k'
            might yield better outcomes.
            - Conversely, for tasks where precision is crucial and computational resources
            are limited, reducing 'k' could improve efficiency.
        """
        return self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )  # NOTE: What if we asked another chatbot 'based on the question from the user, what would be the most optimal argument for "k"?'

    def _is_valid_url(self, url: str) -> bool:
        """
        TODO: consider moving into a utility file
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            logging.warning(f"Not a valid URL: {url}")
            return False
