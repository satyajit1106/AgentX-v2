import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from helpers.img_recog import analyse_image
from helpers.gen_instructions import generate_instructions
from workflow import graph, workflow_config
from rag import rag_graph


class InputState(BaseModel):
    query: str


api = FastAPI(title="AgentX - Angular Project Generator", version="1.0.0")


@api.get("/")
def read_root():
    return {"message": "AgentX API is running."}


@api.post("/code")
def generate_code(state: InputState):
    """Query the RAG system for code generation guidance."""
    rag_config = {"configurable": {"thread_id": "rag-1"}}
    messages = rag_graph.invoke({"messages": [state.query]}, config=rag_config)
    return {"response": messages["messages"][-1].content}


@api.post("/upload")
async def requirement_parser(
    document: UploadFile = File(...),
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
):
    """Upload SRD + 2 design images to generate a complete Angular project."""
    try:
        doc_content = await document.read()
        img1 = await image1.read()
        img2 = await image2.read()

        print(f"Document: {document.filename}")
        print(f"Image 1: {image1.filename}")
        print(f"Image 2: {image2.filename}")

        base64_img1 = base64.b64encode(img1).decode("utf-8")
        base64_img2 = base64.b64encode(img2).decode("utf-8")

        img1_features = analyse_image(base64_img1)
        img2_features = analyse_image(base64_img2)

        file_path = generate_instructions(
            doc_content.decode("utf-8"), img1_features, img2_features
        )

        graph.invoke({"file_path": file_path, "status": ""}, config=workflow_config)

        return {"message": "Application created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
