import langgraph
import langgraph.graph
from tools.extractor import extract_tasks
from tools.setup import setup_project
from tools.styles import write_global_styles
from tools.selector import task_selector
from tools.validator import validate_and_store_code
from utils.tasks import get_next_task
from tools.technical_writer import write_documentation
from tools.devops import init_docker
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from utils.model import llm
from langgraph.graph import END

tools = [extract_tasks, setup_project, write_global_styles, task_selector, validate_and_store_code, write_documentation, init_docker]

extract_task_tool = ToolNode(tools)
setup_project_tool = ToolNode(tools)
write_styles_tool = ToolNode(tools)
task_selector_tool = ToolNode(tools)
validated_writer_tool = ToolNode(tools)

llm_with_tools = llm.bind_tools(tools)

memory = MemorySaver()

builder = langgraph.graph.Graph()

builder.add_node("extractor", extract_tasks)
builder.add_node("setup", setup_project)
builder.add_node("styles", write_global_styles)
builder.add_node("selector", task_selector)
builder.add_node("validator", validate_and_store_code)
builder.add_node("docs", write_documentation)
builder.add_node("docker", init_docker)

builder.add_edge("extractor", "setup")
builder.add_edge("setup", "styles")
builder.add_edge("styles", "docs")
builder.add_edge("docs", "docker")
builder.add_edge("docker", "selector")
builder.add_edge("selector", "validator")

def routing_func(state):
    print(state)
    next_task = get_next_task()
    
    if next_task:
        return "validator"
    return END

builder.add_conditional_edges("validator", routing_func, {"validator": "validator", END: END})

builder.set_entry_point("extractor")

graph = builder.compile(checkpointer=memory)

config = { "recursion_limit": 200, "configurable": { "thread_id": 1 } }
