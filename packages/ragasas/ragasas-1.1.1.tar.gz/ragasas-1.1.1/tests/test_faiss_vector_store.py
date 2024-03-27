# import logging
# import os
# import pytest
# from unittest.mock import Mock
# from ragasas._core import FAISSVectorstore

# TEST_OUTPUT_DATA_PATH = os.path.join(
#     os.path.abspath(__file__), "../", "test_output_data/"
# )


# @pytest.fixture
# def mock_text_embedder():
#     # Mocking the TextEmbedder
#     mock_embedder = Mock()
#     mock_embedder.embeddings = Mock(
#         return_value=[[1, 2, 3], [4, 5, 6]]
#     )  # Mock embeddings
#     return mock_embedder


# def test_create_vector_store_with_list(mock_text_embedder):
#     # Test creating vector store with a list of texts
#     vectorstore = FAISSVectorstore(mock_text_embedder)
#     vectorstore.create_vector_store(["text1", "text2"], os.path.join(TEST_OUTPUT_DATA_PATH), False)
