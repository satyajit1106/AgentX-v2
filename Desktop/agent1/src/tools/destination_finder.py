from langchain.tools import tool
from utils.model import llm

@tool
def determine_file_path(code):
    """
    Identifies the file path where the code has to be written
    """

    prompt = f"""
    Based on the code below, tell me the path where I need to write this.

    I have an Angular project set up already with src/app, src/app/components, src/app/pages and src/app/services.

    Output example: 'src/app/components/app.component.ts'

    Rules:
    1. Don't generate any comments or explanation
    2. Just return a single line containing the path
    3. Don't format anything
    4. Return the absolute file path, ending with an extension. Don't return paths that do not lead to a file.

    Important: You can only generate the output path for 1 file at a time.

    Don't generate folders inside components/ or services/ just write the files
    For example:
    src/app/components/primary-color-button.ts - is valid
    src/app/components/primary-color-button/primary-color-button.ts - is invalid

    Code:
    {code}
    """

    response = llm.invoke(prompt)
    cleaned_response = response.content.replace("\n", "").strip()
    print(cleaned_response)
    return cleaned_response
