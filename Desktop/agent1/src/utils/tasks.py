import os
import json

TASKS_FILE = "../../tasks.json"

def load_tasks():
    """
    Loads tasks.json into a Python dictionary
    """

    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return {"tasks": []}


def save_tasks(tasks):
    """
    Saves the updated task list to tasks.json
    """
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def mark_microtask_complete(task_name, subtask_name, microtask_name):
    """
    Marks a microtask as completed in tasks.json
    """

    tasks = load_tasks()

    for task in tasks["tasks"]:
        if task["task"] == task_name:
            for subtask in task["subtasks"]:
                if subtask["subtask"] == subtask_name:
                    for microtask in subtask["microtasks"]:
                        if microtask["microtask"] == microtask_name:
                            microtask["completed"] = True

                    if all(mt["completed"] for mt in subtask["microtasks"]):
                        subtask["completed"] = True
            if all(st["completed"] for st in task["subtasks"]):
                task["completed"] = True

    save_tasks(tasks)


def get_next_task():
    """
    Fetches the next available microtask.
    """

    tasks = load_tasks()

    for task in tasks["tasks"]:
        if not task["completed"]:
            for subtask in task["subtasks"]:
                if not subtask["completed"]:
                    for microtask in subtask["microtasks"]:
                        if not microtask["completed"]:
                            return (task["task"], subtask["subtask"], microtask["microtask"])
    return None

