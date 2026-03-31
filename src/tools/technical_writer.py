from langchain.tools import tool
from utils.model import llm
from core.config import TASKS_FILE, OUTPUT_DIR


@tool
def write_documentation() -> str:
    """Writes the README.md file to document the project."""
    with open(TASKS_FILE, "r") as f:
        file_content = f.read()

    prompt = f"""
    You are an expert technical writer capable of writing good documentation.
    Your task is to use the completed tasks below to create an industry-grade
    README.md file for a frontend Angular project.

    Tasks: {file_content}

    Your response should only include the contents of README.md and nothing else.
    Don't return any other text content or comments.
    """

    response = llm.invoke(prompt)

    readme_path = OUTPUT_DIR / "client" / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(readme_path, "w") as f:
        f.write(response.content)

    return "Documentation generated successfully."
