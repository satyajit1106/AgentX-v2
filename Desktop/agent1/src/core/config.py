import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.environ["GROQ_API_KEY"]
    
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]

    DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = Settings()
