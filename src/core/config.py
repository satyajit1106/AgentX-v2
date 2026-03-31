import os
from pathlib import Path
from dotenv import load_dotenv

# Project root is one level above src/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = SRC_DIR / "data"
RES_DIR = SRC_DIR / "res"
TASKS_FILE = BASE_DIR / "tasks.json"
OUTPUT_DIR = BASE_DIR / "angular_prj"

load_dotenv(BASE_DIR / ".env")


class Settings:
    GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
    DB_USER: str = os.environ.get("DB_USER", "postgres")
    DB_PASS: str = os.environ.get("DB_PASS", "postgres")
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: str = os.environ.get("DB_PORT", "5432")
    DB_NAME: str = os.environ.get("DB_NAME", "postgres")

    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Copy .env.example to .env and fill in your Groq API key."
            )


settings = Settings()
