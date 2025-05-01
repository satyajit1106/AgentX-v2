from langchain_groq import ChatGroq
from core.config import settings

llm = ChatGroq(
    # model="Gemma2-9b-It",
    # model = "deepseek-r1-distill-qwen-32b",
    model = "llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=settings.GROQ_API_KEY,
)
