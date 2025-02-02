"""LangChain setup and configurations."""
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory
from langsmith import Client
import logging
from config import settings

# Initialize logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize LangSmith client
langsmith_client = Client()

def get_llm(temperature: float = None, model_name: str = None) -> ChatOpenAI:
    """Get LLM instance with specified or default settings."""
    return ChatOpenAI(
        temperature=temperature or float(settings.TEMPERATURE),
        model_name=model_name or settings.MODEL_NAME,
        streaming=True
    )

def get_embeddings() -> OpenAIEmbeddings:
    """Get embeddings model instance."""
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL
    )

def get_vectorstore() -> Chroma:
    """Initialize or get existing vector store."""
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        embedding_function=get_embeddings()
    )

def create_agent_executor(
    tools: List[Tool],
    system_prompt: str,
    memory: ConversationBufferMemory = None
) -> AgentExecutor:
    """Create an agent executor with specified tools and prompt."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    llm = get_llm()
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=settings.DEBUG,
        max_iterations=settings.MAX_ITERATIONS
    )

def create_memory(memory_key: str = "chat_history") -> ConversationBufferMemory:
    """Create a conversation memory instance."""
    return ConversationBufferMemory(
        memory_key=memory_key,
        return_messages=True
    )

def create_output_parser() -> JsonOutputParser:
    """Create a JSON output parser."""
    return JsonOutputParser()

def format_chat_history(messages: List[Dict[str, Any]]) -> List[HumanMessage | AIMessage]:
    """Format chat history into LangChain message format."""
    formatted_messages = []
    for message in messages:
        if message["role"] == "human":
            formatted_messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "ai":
            formatted_messages.append(AIMessage(content=message["content"]))
    return formatted_messages 