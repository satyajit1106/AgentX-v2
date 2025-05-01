from langchain.tools import tool
from utils.model import llm

@tool
def critique_tool(task, subtask, microtask, code):
    """
    Reviews the code, provides a rating (1 - 10), and also suggests improvements
    """

    prompt = f"""
    Review the following Angular code and provide:
    1. A rating between 1 to 10 (if it matches the requirements in microtask, give it an 8).
    2. A brief explanation of the rating
    3. Specific feedback for improvements (keep the feedback limited)

    Task: {task}
    Subtask: {subtask}
    Microtask: {microtask}

    Code:
    {code}

    Important: Don't inject any code or invalid character in the response

    Important: If the code uses any other component, make sure it is imported properly within the same file.
    
    Format the response as:
    ```
    {{
        "score": <rating>,
        "explanation": <brief_explanation>,
        "feedback": <improvements_needed>
    }}
    ```
    """

    response = llm.invoke(prompt)
    cleaned_response = response.content.replace("```json", "").replace("```", "")
    print(cleaned_response)
    return cleaned_response
