from langchain.tools import tool
from utils.model import llm


@tool
def critique_tool(task: str, subtask: str, microtask: str, code: str) -> str:
    """Reviews the code, provides a rating (1-10), and suggests improvements."""
    # Truncate inputs to stay within Groq free tier 6000 TPM limit
    task = task[:150] if len(task) > 150 else task
    subtask = subtask[:150] if len(subtask) > 150 else subtask
    microtask = microtask[:150] if len(microtask) > 150 else microtask
    code = code[:800] if len(code) > 800 else code

    prompt = f"""Review Angular code. Return JSON only: {{"score":<1-10>,"explanation":"...","feedback":"..."}}
Give 8+ if it matches the microtask. Ensure imports are correct.

Task: {task}
Subtask: {subtask}
Microtask: {microtask}
Code:
{code}"""

    response = llm.invoke(prompt)
    cleaned_response = response.content.replace("```json", "").replace("```", "").strip()
    print(cleaned_response)
    return cleaned_response
