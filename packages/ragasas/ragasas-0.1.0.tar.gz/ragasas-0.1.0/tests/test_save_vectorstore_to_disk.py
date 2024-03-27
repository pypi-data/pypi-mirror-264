import os
from dotenv import load_dotenv
from ragasas import Ragasas
import shutil


def test_save_vectorstore_to_disk():

    load_dotenv(".env")
    openai_api_key = os.environ["OPENAI_API_KEY"]
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_save_vectorstore_to_disk/"
    )

    data = [
        "2024-03-22 14:03:28.534008+00:00 (phx-1010-0202-t2): BGP session established with neighbor 203.0.113.1.",
        "2024-03-22 14:03:30.103579+00:00 (phx-1010-0202-t2): ALERT: Disk space on /var partition is at 95% capacity.",
        "2024-03-22 14:03:29.851895+00:00 (phx-1010-0202-t2): Syslog server connection established.",
    ]
    retriever_message = "Searches and returns syslogs that were emitted by a network device. The network device that emmitted the syslogs is a Arista 7500R Series modular switch. You do not know what the contents of the emmitted syslogs are, so you should always use this tool to retrieve them so that you can determine whether any of the emmitted syslogs should be alerted on."
    system_message = "You are a network device syslog alerting system who is tasked with understanding the syslogs that were emmitted by an Arista 7500R Series modular switch."
    ragasas = Ragasas(
        openai_api_key,
        data,
        retriever_message,
        system_message,
        path=output_path,
    )

    assert os.path.exists(output_path)
    assert os.path.isdir(output_path)
    files = os.listdir(output_path)
    assert len(files) == 2
    assert sorted(files) == ["index.faiss", "index.pkl"]

    shutil.rmtree(output_path)
    assert not os.path.exists(output_path)

    ragasas.ask(
        "Return all syslogs that should be alerted on. We only want to alert on syslogs that indicate that the network device should be taken out of the production network and into an in maintenance state. Provide the syslogs in a table that has three columns. The first column is the title of the alert and the second column is your reasoning for why it should be alerted on, and the third column is the associated syslog."
    )

    ragasas.ask("What did I just ask you?")
