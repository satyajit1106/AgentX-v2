from langchain.tools import tool
from utils.model import llm


@tool
def determine_file_path(code: str) -> str:
    """Identifies the file path where the code has to be written."""
    # Truncate to stay within Groq free tier 6000 TPM limit
    if len(code) > 800:
        code = code[:800]

    prompt = f"""Return the file path for this Angular code. One line only, e.g. src/app/components/name.ts
No folders inside components/services. No comments.

{code}"""

    response = llm.invoke(prompt)
    cleaned_response = response.content.replace("\n", "").strip()
    print(cleaned_response)
    return cleaned_response
