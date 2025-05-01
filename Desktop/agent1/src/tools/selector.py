from langchain.tools import tool
from utils.tasks import get_next_task

@tool
def task_selector():
    """
    Assigns the next pending task to a worker agent.
    """

    task_info = get_next_task()
    if task_info:
        return {"task": task_info[0], "subtask": task_info[1], "microtask": task_info[2], "feedback": None}
    return None

