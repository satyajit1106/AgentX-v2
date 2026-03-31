from groq import Groq
from core.config import settings, RES_DIR


def analyse_image(image: str) -> str:
    """Analyzes a base64-encoded image using Groq Vision to extract design information."""
    client = Groq(api_key=settings.GROQ_API_KEY)

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "From the image below, extract the design language and other components "
                            "that have to be developed. Return only the extracted useful information "
                            "in a proper structured instruction based format."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image}"},
                    },
                ],
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    response = completion.choices[0].message.content

    RES_DIR.mkdir(parents=True, exist_ok=True)
    instructions_path = RES_DIR / "instructions.txt"

    with open(instructions_path, "a+") as f:
        f.write("Image instructions: \n\n")
        f.write(response)
        f.write("\n")

    return response
