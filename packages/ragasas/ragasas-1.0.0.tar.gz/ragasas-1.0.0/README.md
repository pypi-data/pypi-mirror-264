# Ragasas
Ragasas -> RAGASaaS -> Retrieval Augmented Generation as Software as a Service


Intended use:  
Input: Data for a RAG  
Output: An object that has an LLM that has access to a RAG  


Usage: 
1. Install the package: `pip install ragasas`

2. Use RAGASAS in your Python application:
    ```
    import ragasas
    ragasas = Ragasas(api_key, data, embedding_model="text-embedding-ada-002", llm_model="gpt-3.5-turbo")
    response = ragasas.ask("What is the sum of all characters in your RAG?")
    print(response)
    ```