from utils.model import llm
from core.config import RES_DIR


def generate_instructions(doc_content, img1_content, img2_content):
    """Converts SRD document + image analysis into an instructions file."""
    prompt = f"""
    Based on the given content below, generate an instructions.txt file which contains detailed instructions
    about the project that has to be built.

    Document content: {doc_content}
    Content from image 1: {img1_content}
    Content from image 2: {img2_content}

    Rule: Don't give anything else except just the contents of the file.

    Example structure:
    Software Requirements Document (SRD)
    1. Overview
    This document outlines the requirements for the frontend development.
    2. UI/UX Design Guidelines
    2.1 Color Scheme
    - Primary Color: #007bff
    - Secondary Color: #6c757d
    2.2 Typography
    - Font Family: "Inter", sans-serif
    2.3 Components
    - Buttons: Rounded corners (8px)
    3. Application Features
    ...
    """

    response = llm.invoke(prompt)

    RES_DIR.mkdir(parents=True, exist_ok=True)
    instructions_path = RES_DIR / "instructions.txt"

    with open(instructions_path, "a+") as f:
        f.write(response.content)
        f.write("\n")

    return str(instructions_path)
