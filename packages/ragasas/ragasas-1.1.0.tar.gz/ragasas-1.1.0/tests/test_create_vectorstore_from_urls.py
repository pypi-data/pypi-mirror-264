import logging
import os
from dotenv import load_dotenv
from ragasas import Ragasas
import pytest
# TODO: Explore URL loader from langchain

def test_create_vectorstore_from_disk():

    load_dotenv(".env")
    openai_api_key = os.environ["OPENAI_API_KEY"]

    data = ["https://github.com/EricGustin"]
    retriever_message = "Searches and returns information about GitHub profiles. You should always use this tool to retrieve information about the profiles so that you can effectively answer any queries."
    system_message = "You are an expert on GitHub profiles and are tasks with answering any questions about them."

    ragasas = Ragasas(openai_api_key, data, retriever_message, system_message)

    response = ragasas.ask(
        "How many contributions has the GitHub user 'EricGustin' had in the last year?"
    )
    logging.info(response["output"])

    assert True
