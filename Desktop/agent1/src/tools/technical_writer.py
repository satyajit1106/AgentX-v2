from langchain.tools import tool
from utils.model import llm

@tool
def write_documentation():
    """
    Writes the README.md file to document the project.
    """
    tasks_path = "../../tasks.json"

    with open(tasks_path, "r") as f:
        file_content = f.read()
        f.close

    prompt = f"""
    You are an expert technical writer capable of writing good documentations.
    Your task is to use the completed tasks below to create a industry-grade
    README.md file for a frontend Angular project.

    Tasks: {file_content}

    Your response should only include the contents of README.md and nothing else.
    Don't return any other text content or comments
    """
    response = llm.invoke(prompt)

    print(response.content)

    with open("README.md", "w") as f:
        f.write(response.content)
        f.flush()
    
    return "Documentation generated successfully."
