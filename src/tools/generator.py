from langchain.tools import tool
from utils.model import llm


@tool
def generate_code(task: str, subtask: str, microtask: str, feedback: str | None) -> str:
    """Generates Angular code for the given task using LLM."""
    # Truncate inputs to stay within Groq free tier 6000 TPM limit
    task = task[:200] if len(task) > 200 else task
    subtask = subtask[:200] if len(subtask) > 200 else subtask
    microtask = microtask[:200] if len(microtask) > 200 else microtask

    prompt = f"""Generate Angular .ts code with inline template and styling. Full code, no comments, no explanation. One file only.

Task: {task}
Subtask: {subtask}
Microtask: {microtask}"""

    if feedback:
        feedback = feedback[:300] if len(feedback) > 300 else feedback
        prompt += f"\n\nFeedback to apply: {feedback}"

    response = llm.invoke(prompt)
    cleaned_response = (
        response.content
        .replace("```html", "")
        .replace("```css", "")
        .replace("```scss", "")
        .replace("```typescript", "")
        .replace("```", "")
        .strip()
    )
    print(cleaned_response)
    return cleaned_response
