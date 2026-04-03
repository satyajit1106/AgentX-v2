import json
import re
from langchain.tools import tool
from utils.model import llm
from core.config import TASKS_FILE


def extract_json(text: str) -> dict:
    """Extract JSON from LLM response that may contain extra text or markdown."""
    cleaned = text.replace("```json", "").replace("```", "").strip()
    # Try parsing the whole thing first
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    # Find the first { ... } block
    match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not extract valid JSON from LLM response: {cleaned[:200]}")


@tool
def extract_tasks(file_path: str) -> str:
    """
    Uses LLM to analyse instructions file and generate a structured task list as JSON.
    This is the first task to be executed.
    """
    with open(file_path, "r") as f:
        file_content = f.read()

    # Truncate to ~800 chars to stay within Groq free tier 6000 TPM limit
    if len(file_content) > 800:
        file_content = file_content[:800]

    prompt = f"""Break this SRD into tasks as JSON. No .scss/.html files (inline only). Angular project already set up. Skip styling tasks.
Format: {{"tasks":[{{"task":"...","completed":false,"subtasks":[{{"subtask":"...","completed":false,"microtasks":[{{"microtask":"...","completed":false}}]}}]}}]}}

{file_content}

JSON only:"""

    response = llm.invoke(prompt)
    tasks_json = extract_json(response.content)

    with open(TASKS_FILE, "w") as f:
        json.dump(tasks_json, f, indent=4)

    return "Written tasks in tasks.json"
