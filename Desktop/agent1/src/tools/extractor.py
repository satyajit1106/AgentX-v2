import json
from langchain.tools import tool
from utils.model import llm
from langgraph.graph import MessagesState

@tool
def extract_tasks(file_path: str) -> str:
    """
    This is the first task to be executed
    Uses LLM to analyse instructions file and generate a structured task list as JSON
    """
    file = open(file_path, "r")
    file_content = file.read()
    file.close

    prompt = f"""
    Analyse the following Software Requirements Document (SRD) and break it down into:
    - High-level tasks
    - Subtasks for each task
    - Microtasks for each subtask (be extremely detailed)

    Tasks should be crisp and clear. Don't create unnecessary tasks, only create it if it's required.

    Important: Never create tasks to create .scss and .html files because inline templates and styling is used.

    Strictly output the result in a JSON format like this:
    You cannot add or remove any keys in this format
    {{
        "tasks": [
            {{
                "task": "Setup Angular Project",
                "completed": false,
                "subtasks": [
                    {{
                        "subtask": "Initialize project",
                        "completed": false,
                        "microtasks": [{{
                            "microtask": "Run ng new",
                            "completed": false,
                        }}, {{
                            "microtask": "Configure tsconfig.json",
                            "completed: false,
                        }}]
                    }}
                ]
            }}
        ]
    }}

    Here is the SRD:
    {file_content}

    Attention: Assume that the initial angular project setup has been completed and you are 
    in that working directory with the following files:
    1. src/app/components (empty directory)
    2. src/app/services (empty directory)
    3. src/app/pages (empty directory)
    4. src/app/app.component.ts
    5. src/app/app.routes.ts
    6. src/index.html
    7. src/styles.scss
    8. src/main.ts

    Rule: Global styles (color codes, font family, etc.) are configured already. Do not generate any task related to colors, typography, etc.

    Mandatory: Do not generate things like 'Here is the ...' or 'Sure, ...'. Don't give anything except the json content as response.
    """

    response = llm.invoke(prompt)
    print(response)
    cleaned_response = response.content.replace("```json", "").replace("```", "").strip()
    # print(cleaned_response)
    tasks_json = json.loads(cleaned_response)
    with open("tasks.json", "w") as f:
        json.dump(tasks_json, f, indent=4)

    return "Written tasks in tasks.json"
