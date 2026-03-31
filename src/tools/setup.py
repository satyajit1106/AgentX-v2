import os
import subprocess
from langchain.tools import tool
from core.config import OUTPUT_DIR


@tool
def setup_project() -> str:
    """
    Sets up the Angular project by creating folders, initializing Angular, and installing dependencies.
    Invoke this only after extractor has finished setting up the task list.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Project directory ready at: {OUTPUT_DIR}")

    client_dir = OUTPUT_DIR / "client"

    if not client_dir.exists():
        result = subprocess.run(
            ["ng", "new", "client", "--style=scss", "--skip-git",
             "--server-routing=true", "--inline-style", "--inline-template",
             "--ssr=false", "--standalone=false"],
            cwd=str(OUTPUT_DIR),
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Angular CLI error: {result.stderr}")
            return f"Project setup failed: {result.stderr}"
        print("Angular project created successfully.")
    else:
        print("Client directory already exists, skipping ng new.")

    # Install Angular Material
    result = subprocess.run(
        ["npm", "install", "@angular/material"],
        cwd=str(client_dir),
        shell=True,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"npm install error: {result.stderr}")
    else:
        print("Angular Material installed successfully.")

    # Create standard directories
    for subdir in ["src/app/services", "src/app/components", "src/app/pages"]:
        (client_dir / subdir).mkdir(parents=True, exist_ok=True)
        print(f"Directory: {subdir} created")

    return "Project setup completed successfully."
