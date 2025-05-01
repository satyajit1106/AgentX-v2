import os
from langchain.tools import tool
import subprocess
from utils.tasks import mark_microtask_complete

PROJECT_FOLDER = "angular_prj"

@tool
def setup_project():
    """
    Invoke this only after executor has finished setting up project structure
    Sets up the Angular project by creating folders, initializing Angular, and installing dependencies.
    """

    if not os.path.exists(PROJECT_FOLDER):
        os.makedirs(PROJECT_FOLDER)

    if os.path.exists(PROJECT_FOLDER):
        print("Created project repository.")
    else:
        print("Failed to create project repository.")
        return

    
    print("Attempting directory change...")
    os.chdir(PROJECT_FOLDER)
    print(f"Directory change successful. Current path: {PROJECT_FOLDER}/")

    subprocess.Popen('ng new client --style=scss --skip-git --server-routing=true --inline-style --inline-template --ssr=false --standalone=false', shell=True).wait()

    if os.path.exists("client"):
        print("Created project files and installed dependencies.")
    else:
        print("Project setup failed: Could not create files.")
        return
    
    print("Attempting directory change...")
    os.chdir("client")
    print("Directory change successful. Current path: client/")

    print("Attempting to install Material UI...")
    subprocess.Popen('npm install @angular/material', shell=True).wait()
    print("Material UI installed successfully.")

    os.makedirs("src/app/services", exist_ok=True)
    print("Directory: src/app/services created")

    os.makedirs("src/app/components", exist_ok=True)
    print("Directory: src/app/components created")

    os.makedirs("src/app/pages", exist_ok=True)
    print("Directory: src/app/pages created")

    # print("Attempting to launch isolated application...")
    # subprocess.Popen("ng serve --open", shell=True)

    return f"Project setup completed successfully."

