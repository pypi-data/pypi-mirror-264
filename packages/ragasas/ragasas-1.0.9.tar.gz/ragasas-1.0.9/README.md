# Ragasas (Retrieval Augmented Generation as Software as a Service)

Example Usage: 
```python
from ragasas import Ragasas

# Data prep
openai_api_key = "YOUR_OPENAI_API_KEY"
data = [
    "Ragasas streamlines the RAG (Retrieval Augmented Generation) development process.",
    "Ragasas is a Python package.",
    "Ragasas was created by Eric Gustin.",
]
retriever_message = "Searches and returns documents regarding Ragasas."
system_message = "You are a helpful chatbot who is tasked with answering questions about Ragasas. Assume all questions are about Ragasas."

# Use Ragasas
ragasas = Ragasas(
    openai_api_key,
    data,
    retriever_message,
    system_message,
    embedding_model="text-embedding-ada-002",
    llm_model="gpt-3.5-turbo",
)
response = ragasas.ask("What is Ragasas?")
print(response["output"])

# Response: Ragasas is a Python package created by Eric Gustin. It streamlines the RAG (Retrieval Augmented Generation) development process.
```