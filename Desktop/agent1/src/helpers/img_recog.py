from groq import Groq

def analyse_image(image: str):
    client = Groq()

    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "From the image below, extract the design language and other components that have to be developed. Return only the extracted useful information in a proper structured instruction based format"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}"
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    response = completion.choices[0].message.content
    with open("src/res/instructions.txt", "a+") as f:
        f.write("Image instructions: \n\n")
        f.write(response)
        f.write("\n")
        f.flush()
    
    return completion.choices[0].message.content
