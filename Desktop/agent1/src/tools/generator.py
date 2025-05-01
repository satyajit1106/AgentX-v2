from utils.model import llm
from langchain.tools import tool
from pydantic import BaseModel

@tool
def generate_code(task: str, subtask: str, microtask: str, feedback: str | None):
    """
    Generates code for the given task using LLM.
    """

    prompt = f"""
    Generate high-quality Angular code for the following task.
    
    Important: You can only write to .ts files. You cannot generate just html or scss individually
    You need to generate single .ts file with template and styling defined inline.

    Important: Always give the contents of the full code. No partial code has to be returned.

    Task: {task}
    Subtask: {subtask}
    Microtask: {microtask}

    Rules:
    1. Ensure the code follows best practices and is production-ready.
    2. Write inline template and styling
    3. Do not generate any kind of comments or explanation. Just give the raw code.
    
    Mandatory: You must write only one file at a time. And don't add a single comment in it
    """

    if feedback:
        prompt += f"\n\nModify the existing code based on following feedback: \n\n{feedback}"

    response = llm.invoke(prompt)
    cleaned_response = response.content.replace("```html", "").replace("```css", "").replace("```scss", "").replace("```typescript", "").replace("```", "").strip()
    print(cleaned_response)
    return cleaned_response

