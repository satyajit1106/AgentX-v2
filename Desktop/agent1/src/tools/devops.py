from langchain.tools import tool
from utils.model import llm

@tool
def init_docker():
    """
    Writes the README.md file to document the project.
    """
    tasks_path = "../../tasks.json"

    with open(tasks_path, "r") as f:
        file_content = f.read()
        f.close

    prompt = f"""
    You are a Devops expert capable of writing production grade dockerfiles.
    Your task is to use the completed tasks below to create a industry-grade
    Dockerfile for a frontend Angular project.

    Tasks: {file_content}

    Your response should only include the contents of Dockerfile and nothing else.
    Don't return any other text content or comments
    """
    response = llm.invoke(prompt)

    print(response.content)

    with open("Dockerfile", "w") as f:
        f.write(response.content.replace("```dockerfile", "").replace("```", ""))
        f.flush()
    
    print("Dockerfile generated successfully.")

    return "Project completed at: angular_prj/client"
