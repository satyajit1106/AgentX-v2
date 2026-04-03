from langchain.tools import tool
from utils.model import llm
from core.config import OUTPUT_DIR, RES_DIR


@tool
def extract_styles(file_path: str) -> str:
    """Extracts design-related information (like color codes, font family, spacing) from the SRS document."""
    with open(file_path, "r") as f:
        file_content = f.read()

    # Truncate to stay within Groq free tier 6000 TPM limit
    if len(file_content) > 800:
        file_content = file_content[:800]

    prompt = f"""Extract UI/UX design guidelines as valid CSS (colors, typography, components). CSS only, no comments.

SRD: {file_content}"""

    response = llm.invoke(prompt)
    cleaned_response = response.content.replace("```css", "").replace("```", "").strip()
    return cleaned_response


@tool
def write_global_styles() -> str:
    """Writes global application styling into the styles.scss file."""
    instructions_path = RES_DIR / "instructions.txt"
    styles_path = OUTPUT_DIR / "client" / "src" / "styles.scss"

    css_content = extract_styles.invoke(str(instructions_path))

    styles_path.parent.mkdir(parents=True, exist_ok=True)
    with open(styles_path, "w") as f:
        f.write(css_content)

    return "Global design styles written"
