from utils.model import llm
from core.config import RES_DIR


def generate_instructions(doc_content, img1_content, img2_content):
    """Converts SRD document + image analysis into an instructions file."""
    # Truncate inputs to stay within Groq free tier 6000 TPM limit
    doc_content = doc_content[:1000] if len(doc_content) > 1000 else doc_content
    img1_content = img1_content[:300] if len(img1_content) > 300 else img1_content
    img2_content = img2_content[:300] if len(img2_content) > 300 else img2_content

    prompt = f"""Combine into a concise SRD. Output ONLY the instructions.

Doc: {doc_content}
Design 1: {img1_content}
Design 2: {img2_content}"""

    response = llm.invoke(prompt)

    RES_DIR.mkdir(parents=True, exist_ok=True)
    instructions_path = RES_DIR / "instructions.txt"

    with open(instructions_path, "w") as f:
        f.write(response.content)
        f.write("\n")

    return str(instructions_path)
