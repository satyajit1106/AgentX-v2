from langchain.tools import tool
from utils.model import llm
from core.config import TASKS_FILE, OUTPUT_DIR


@tool
def write_documentation() -> str:
    """Writes the README.md file to document the project."""
    with open(TASKS_FILE, "r") as f:
        file_content = f.read()

    # Truncate to stay within Groq free tier 6000 TPM limit
    if len(file_content) > 1000:
        file_content = file_content[:1000]

    prompt = f"""Generate README.md for an Angular project based on these tasks. Output ONLY the README content.

Tasks: {file_content}"""

    response = llm.invoke(prompt)

    readme_path = OUTPUT_DIR / "client" / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    with open(readme_path, "w") as f:
        f.write(response.content)

    return "Documentation generated successfully."
