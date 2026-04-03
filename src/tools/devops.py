from langchain.tools import tool
from utils.model import llm
from core.config import TASKS_FILE, OUTPUT_DIR


@tool
def init_docker() -> str:
    """Generates a Dockerfile for the Angular project."""
    with open(TASKS_FILE, "r") as f:
        file_content = f.read()

    # Truncate to stay within Groq free tier 6000 TPM limit
    if len(file_content) > 1000:
        file_content = file_content[:1000]

    prompt = f"""Generate a production Dockerfile for an Angular project. Output ONLY the Dockerfile content.

Tasks: {file_content}"""

    response = llm.invoke(prompt)
    cleaned = response.content.replace("```dockerfile", "").replace("```", "").strip()

    dockerfile_path = OUTPUT_DIR / "client" / "Dockerfile"
    dockerfile_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dockerfile_path, "w") as f:
        f.write(cleaned)

    print("Dockerfile generated successfully.")
    return "Project completed at: angular_prj/client"
