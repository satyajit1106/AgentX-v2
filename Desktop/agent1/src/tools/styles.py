import os
from langchain.tools import tool
from utils.model import llm

@tool
def extract_styles(file_path: str):
    """
    Extracts design-related information (like color codes, font family, spacing) from the SRS document
    """
    # file_path = "src/res/instructions.txt"

    file = open(file_path, "r")
    file_content = file.read()
    file.close

    prompt = f"""
    Extract only the data under the UI/UX Design Guidelines section

    Focus on:
    - Color coding (primary, secondary, background, success, error colors)
    - Typography (font family, font sizes)
    - Components

    Format the output as valid CSS content.

    NOTE: Do not generate any comments or explanations. I want only valid CSS code. Nothing else

    SRD: {file_content}
    """

    response = llm.invoke(prompt)
    cleaned_response = response.content.replace("```css", "").replace("```", "").strip()
    return cleaned_response


@tool
def write_global_styles():
    """
    Writes global application styling into the styles.scss file
    """
    print(os.getcwd())

    file_path = "../../src/res/instructions.txt"

    css_content = extract_styles.invoke(file_path)

    styles_path = "./src/styles.scss"

    with open(styles_path, "w") as f:
        f.write(css_content)
        f.flush()
    
    return f"Global design styles written"
