import time

from groq import Groq
from core.config import settings, RES_DIR

_last_groq_call = 0.0


def analyse_image(image: str) -> str:
    """Analyzes a base64-encoded image using Groq Vision to extract design information."""
    global _last_groq_call
    # Rate limit: wait 20s between Groq API calls to respect 6000 TPM free tier
    elapsed = time.time() - _last_groq_call
    if elapsed < 12.0:
        time.sleep(12.0 - elapsed)

    client = Groq(api_key=settings.GROQ_API_KEY)

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract design components from this image. Return a brief structured list.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image}"},
                    },
                ],
            }
        ],
        temperature=1,
        max_completion_tokens=512,
        top_p=1,
        stream=False,
        stop=None,
    )
    _last_groq_call = time.time()

    response = completion.choices[0].message.content

    RES_DIR.mkdir(parents=True, exist_ok=True)
    instructions_path = RES_DIR / "instructions.txt"

    with open(instructions_path, "w") as f:
        f.write(response)
        f.write("\n")

    return response
