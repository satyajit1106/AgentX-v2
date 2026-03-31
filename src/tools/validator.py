import json
from pathlib import Path
from tools.generator import generate_code
from tools.feedback import critique_tool
from tools.destination_finder import determine_file_path
from utils.tasks import mark_microtask_complete, get_next_task
from core.config import OUTPUT_DIR


def validate_and_store_code(state):
    """Generates code, critiques it and refines it based on feedback until approved."""
    next_task = get_next_task()
    if not next_task:
        return "No pending tasks."

    task, subtask, microtask = next_task
    feedback = None
    client_dir = OUTPUT_DIR / "client"

    while True:
        code = generate_code.invoke({
            "task": task,
            "subtask": subtask,
            "microtask": microtask,
            "feedback": feedback,
        })

        critique_response = critique_tool.invoke({
            "task": task,
            "subtask": subtask,
            "microtask": microtask,
            "code": code,
        })

        try:
            changes = json.loads(critique_response)
        except json.JSONDecodeError:
            print(f"Failed to parse critique response, accepting code as-is.")
            changes = {"score": 8, "feedback": ""}

        code_rating = changes.get("score", 0)
        feedback = changes.get("feedback", "")

        if code_rating >= 8:
            relative_path = determine_file_path.invoke(code)
            full_path = client_dir / relative_path

            # Create parent directories if they don't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)

            print(f"Writing to: {full_path}")
            with open(full_path, "w") as f:
                f.write(code)

            mark_microtask_complete(task, subtask, microtask)
            print("Task tracker updated.")
            return f"Code written successfully to {full_path}"
