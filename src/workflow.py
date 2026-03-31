from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from tools.extractor import extract_tasks
from tools.setup import setup_project
from tools.styles import write_global_styles
from tools.selector import task_selector
from tools.validator import validate_and_store_code
from tools.technical_writer import write_documentation
from tools.devops import init_docker
from utils.tasks import get_next_task


class AgentState(TypedDict):
    file_path: str
    status: str


def extractor_node(state: AgentState) -> AgentState:
    result = extract_tasks.invoke(state["file_path"])
    return {"file_path": state["file_path"], "status": result}


def setup_node(state: AgentState) -> AgentState:
    result = setup_project.invoke({})
    return {"file_path": state["file_path"], "status": result}


def styles_node(state: AgentState) -> AgentState:
    result = write_global_styles.invoke({})
    return {"file_path": state["file_path"], "status": result}


def docs_node(state: AgentState) -> AgentState:
    result = write_documentation.invoke({})
    return {"file_path": state["file_path"], "status": result}


def docker_node(state: AgentState) -> AgentState:
    result = init_docker.invoke({})
    return {"file_path": state["file_path"], "status": result}


def selector_node(state: AgentState) -> AgentState:
    result = task_selector.invoke({})
    status = str(result) if result else "No more tasks"
    return {"file_path": state["file_path"], "status": status}


def validator_node(state: AgentState) -> AgentState:
    result = validate_and_store_code(state)
    return {"file_path": state["file_path"], "status": result}


def routing_func(state: AgentState) -> str:
    next_task = get_next_task()
    if next_task:
        return "validator"
    return END


memory = MemorySaver()

builder = StateGraph(AgentState)

builder.add_node("extractor", extractor_node)
builder.add_node("setup", setup_node)
builder.add_node("styles", styles_node)
builder.add_node("selector", selector_node)
builder.add_node("validator", validator_node)
builder.add_node("docs", docs_node)
builder.add_node("docker", docker_node)

builder.add_edge("extractor", "setup")
builder.add_edge("setup", "styles")
builder.add_edge("styles", "docs")
builder.add_edge("docs", "docker")
builder.add_edge("docker", "selector")
builder.add_edge("selector", "validator")
builder.add_conditional_edges("validator", routing_func, {"validator": "validator", END: END})

builder.set_entry_point("extractor")

graph = builder.compile(checkpointer=memory)

workflow_config = {"recursion_limit": 200, "configurable": {"thread_id": "1"}}
