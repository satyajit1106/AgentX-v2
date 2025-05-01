from core.config import settings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

llm = ChatGroq(
    model="Gemma2-9b-It",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=settings.GROQ_API_KEY,
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

connection = settings.DB_URL
collection_name = "test"

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

@tool
def agent_builder(query: str):
    """
    Use this tool to look up information from the langchain and langgraph handbook provided. 
    Any information related to langchain, langgraph, or building agents can be fetched from 
    this tool.
    """
    return vector_store.similarity_search(query, k=2)


tools = [agent_builder]

agent_builder_tool = ToolNode(tools)

llm_with_tools = llm.bind_tools(tools)

def coder(state: MessagesState):
    last_message = state["messages"]
    return {"messages": [llm_with_tools.invoke(last_message)]}


def router_function(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return last_message.tool_calls[0]["name"]
    return "response"


def response_agent(state: MessagesState):
    messages = state["messages"]
    prompt = f"""
    Use the messages below to generate a good user-friendly response 
    based on what the initial Human Message was.
    
    All Messages:
    {messages}
    """
    return {"messages": [llm.invoke(prompt)]}



builder = StateGraph(MessagesState)

builder.add_node("coder", coder)
builder.add_node("agent_builder", agent_builder_tool)
builder.add_node("response", response_agent)

builder.add_conditional_edges("coder", router_function, {"agent_builder": "agent_builder", "response": "response"})

builder.add_edge("agent_builder", "response")

builder.set_entry_point("coder")
builder.set_finish_point("response")

rag_graph = builder.compile(checkpointer=memory)
