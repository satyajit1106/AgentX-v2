"""Utility script to generate a workflow visualization image."""
from langchain_core.runnables.graph import MermaidDrawMethod
from workflow import graph
from core.config import BASE_DIR


if __name__ == "__main__":
    image = graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )

    output_path = BASE_DIR / "graph.png"
    with open(output_path, "wb") as f:
        f.write(image)

    print(f"Graph image saved to {output_path}")
