import os
import json
from tools.generator import generate_code
from tools.feedback import critique_tool
from tools.destination_finder import determine_file_path
from utils.tasks import mark_microtask_complete
from utils.tasks import get_next_task
from pathlib import Path

def validate_and_store_code(state):
    """
    Generates code, critiques it and refines it based on feedback until approved.
    """
    next_task = get_next_task()

    print(next_task)

    task = next_task[0]
    subtask = next_task[1]
    microtask = next_task[2]

    feedback = None

    while True:
        next_task = {
            "task": task,
            "subtask": subtask,
            "microtask": microtask,
            "feedback": feedback
        }

        code = generate_code.invoke(next_task)

        input_to_critique = {
            "task": task,
            "subtask": subtask,
            "microtask": microtask,
            "code": code
        }

        critique_response = critique_tool.invoke(input_to_critique)

        changes = json.loads(critique_response)

        code_rating = changes["score"]
        feedback = changes["feedback"]

        if code_rating >= 8:
            full_path = determine_file_path.invoke(code)

            print("Attempting to write to: " + full_path)

            # os.makedirs(full_path, exist_ok=True)

            
            filename = Path(full_path)
            filename.touch(exist_ok=True)

            with open(full_path, "w+") as f:
                f.write(code)


            mark_microtask_complete(task, subtask, microtask)
            print("Task tracker updated.")

            return f"Code written successfully to {full_path}"
