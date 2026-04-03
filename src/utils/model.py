import time
import functools
from langchain_groq import ChatGroq
from core.config import settings

settings.validate()

_base_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=4096,
    timeout=None,
    max_retries=5,
    api_key=settings.GROQ_API_KEY,
)


class RateLimitedLLM:
    """Wrapper that adds delay between calls to respect Groq free tier rate limits."""

    def __init__(self, llm, min_delay=5.0):
        self._llm = llm
        self._min_delay = min_delay
        self._last_call = 0.0

    def _wait(self):
        elapsed = time.time() - self._last_call
        if elapsed < self._min_delay:
            time.sleep(self._min_delay - elapsed)
        self._last_call = time.time()

    def invoke(self, *args, **kwargs):
        self._wait()
        return self._llm.invoke(*args, **kwargs)

    def bind_tools(self, *args, **kwargs):
        return self._llm.bind_tools(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._llm, name)


llm = RateLimitedLLM(_base_llm, min_delay=12.0)
