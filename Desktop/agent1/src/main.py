import base64
from fastapi import FastAPI, File, UploadFile
from helpers.img_recog import analyse_image
from helpers.gen_instructions import generate_instructions
from workflow import graph, config
from rag import rag_graph
from pydantic import BaseModel

class InputState(BaseModel):
    query: str


api = FastAPI(title="Final Assignment", version="1.0.0")

@api.get("/")
def read_root():
    return {"message": "Hello world!"}

@api.post("/code")
def generate_code(state: InputState):
    config = {"configurable":{"thread_id": "1"}}

    messages = rag_graph.invoke({"messages": [state.query]}, config=config)
    return { "response": messages["messages"][-1].content }


@api.post("/upload")
async def requirement_parser(document: UploadFile = File(...), image1: UploadFile = File(...), image2: UploadFile = File(...)):
    print("Invoked")
    doc_content = await document.read()
    img1 = await image1.read()
    img2 = await image2.read()

    print(document.filename)
    print(image1.filename)
    print(image2.filename)

    base64_img1 = base64.b64encode(img1).decode("utf-8")
    base64_img2 = base64.b64encode(img2).decode("utf-8")

    img1_features = analyse_image(base64_img1)
    img2_features = analyse_image(base64_img2)

    file_path = generate_instructions(doc_content, img1_features, img2_features)

    graph.invoke({"file_path": file_path}, config=config)

    return {"file_path": "Application created successfully."}


# from workflow import graph, config

# for event in graph.stream({"file_path": "src/res/instructions.txt"}, config=config):
#     for key, value in event.items():
#         print(key)
#         print(value)
#         print("-" * 50)
