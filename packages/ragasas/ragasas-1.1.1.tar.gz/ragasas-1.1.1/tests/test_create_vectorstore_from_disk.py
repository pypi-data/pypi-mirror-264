import os
from dotenv import load_dotenv
from ragasas import Ragasas


def test_create_vectorstore_from_disk():

    load_dotenv(".env")
    openai_api_key = os.environ["OPENAI_API_KEY"]
    vectorstore_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data/vectorstore"
    )

    data = vectorstore_path
    retriever_message = "Searches and returns syslogs that were emitted by a network device. The network device that emmitted the syslogs is a Arista 7500R Series modular switch. You do not know what the contents of the emmitted syslogs are, so you should always use this tool to retrieve them so that you can determine whether any of the emmitted syslogs should be alerted on."
    system_message = "You are a network device syslog alerting system who is tasked with understanding the syslogs that were emmitted by an Arista 7500R Series modular switch."
    ragasas = Ragasas(openai_api_key, data, retriever_message, system_message)

    ragasas.ask(
        "Return all syslogs that should be alerted on. We only want to alert on syslogs that indicate that the network device should be taken out of the production network and into an in maintenance state. Provide the syslogs in a table that has three columns. The first column is the title of the alert and the second column is your reasoning for why it should be alerted on, and the third column is the associated syslog."
    )

    response = ragasas.ask("What did I just ask you?")

    assert True
