from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
from workflow import graph

image = graph.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API,
)

with open("graph.png", "wb") as file:
    file.write(image)
    file.flush()
    file.close()
