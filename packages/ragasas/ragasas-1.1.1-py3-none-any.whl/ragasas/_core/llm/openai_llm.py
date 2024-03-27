from langchain.agents import (
    OpenAIFunctionsAgent,
    AgentExecutor,
    create_openai_functions_agent,
)
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
    AgentTokenBufferMemory,
)
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from .llm import LLM


class OpenAILLM(LLM):
    def __init__(self, api_key, retriever, retriever_message, system_message) -> None:
        self.api_key = api_key
        self.retriever = retriever
        self.retriever_message = retriever_message
        self.system_message = system_message
        # Set up Conversation Retrieval Chain
        self.retriever_tool = create_retriever_tool(
            retriever,
            "network_device_syslog_retriever",
            self.retriever_message,
        )
        self.tools = [self.retriever_tool]
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key, streaming=True, model="gpt-3.5-turbo"
        )
        self.message = SystemMessage(content=(self.system_message))
        # RAG prompt
        self.prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=self.message,
            extra_prompt_messages=[MessagesPlaceholder(variable_name="history")],
        )
        agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
        )
        self.memory = AgentTokenBufferMemory(llm=self.llm)

    def ask(self, message):
        response = self.agent_executor(
            {
                "input": message,
                "history": self.memory.buffer,
            },
            callbacks=None,
            include_run_info=False,
        )

        self.memory.save_context({"input": message}, response)

        return response
