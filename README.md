
# 🧠 RAG Agent Framework

A modular, extensible Retrieval-Augmented Generation (RAG) framework with tool-based automation and workflow orchestration.

![RAG Graph](agent/graph.png)

---

## 🚀 Overview

This project is designed to build an intelligent agent system leveraging RAG pipelines, integrating diverse tools for tasks such as:

- Document retrieval & summarization
- Developer tooling automation (DevOps, validation, writing)
- Workflow orchestration
- PDF data merging & extraction

---

## ✨ Key Features

- ⚙️ **Modular Design** — Each component is independently testable and replaceable.
- 📚 **RAG Architecture** — Combines retrieval and generation from external sources.
- 🧰 **Custom Tools** — Plug-and-play support for a variety of tools (validator, writer, devops, etc.).
- 🖇️ **PDF & Workflow Utilities** — Built-in support for merging PDFs and structuring workflows.
- 🌐 **Extensible & Scalable** — Add your own tools or modify flows without touching the core.

---

## 🧩 Project Structure

```
agent/
├── .gitignore
├── graph.png                  # System architecture/flow diagram
├── requirements.txt           # Python package requirements
└── src/
    ├── main.py                # 🔹 Entry point for the RAG agent
    ├── rag.py                 # RAG core logic
    ├── rag_loader.py          # Loads data into the agent
    ├── workflow.py            # Orchestrates tasks between tools
    ├── pdf_merger.py          # Merges multiple PDFs
    ├── graph_img.py           # Graph generation utility
    ├── res/
    │   └── instructions.txt   # Agent input instructions
    └── tools/
        ├── devops.py
        ├── destination_finder.py
        ├── extractor.py
        ├── feedback.py
        ├── generator.py
        ├── selector.py
        ├── setup.py
        ├── styles.py
        ├── technical_writer.py
        └── validator.py
```

---

## 🔧 Installation

### 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/rag-agent.git
cd rag-agent/agent
```

### 🧱 Step 2: Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 📦 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚦 Usage

To start the RAG Agent:

```bash
python src/main.py
```

> Make sure `src/res/instructions.txt` exists and contains task prompts.

---

## 🛠️ Tool Descriptions

| Tool Name              | Purpose                                      |
|------------------------|----------------------------------------------|
| `generator.py`         | Generates content based on task             |
| `validator.py`         | Validates agent's output                    |
| `devops.py`            | Handles deployment-related automation       |
| `feedback.py`          | Integrates feedback for iterative learning  |
| `selector.py`          | Selects the appropriate tool                |
| `setup.py`             | Prepares environments/setup actions         |
| `extractor.py`         | Extracts relevant info from input           |
| `styles.py`            | Formats and styles outputs                  |
| `destination_finder.py`| Determines correct destination for content  |
| `technical_writer.py`  | Refines output for documentation            |

---

## 🧪 Testing

You can test individual components or run the whole system:

```bash
# Example: testing PDF merger
python src/pdf_merger.py

# Example: running workflow
python src/workflow.py
```

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 🙌 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 📬 Contact

For any queries or suggestions, reach out to:

**Satyajit Patra**  
📧 Email: satyajitpatra4002@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/satyajit-patra-b0801a242/)
