"""
One-time script to load PDF documents into the PGVector database.
Run this before using the RAG endpoint: python -m rag_loader
"""
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_postgres.vectorstores import PGVector

from core.config import settings, DATA_DIR


def load_and_store_pdfs():
    file_path = DATA_DIR / "result.pdf"

    print("Loading pdf file...", end="")
    loader = PyPDFLoader(str(file_path))
    print("Done")

    pages = []
    print("Extracting pages...", end="")
    for page in loader.load():
        pages.append(page)
    print("Done")

    print("Splitting pages...", end="")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunked_pages = splitter.split_documents(pages)
    print("Done")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    print("Attempting to connect to PGVector...", end="")
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="test",
        connection=settings.DB_URL,
        use_jsonb=True,
    )
    print("Connected!")

    documents = []
    ids = []
    for i, text in enumerate(chunked_pages):
        ids.append(i)
        documents.append(Document(page_content=text.page_content))

    print("Storing vectors...", end="")
    vector_store.add_documents(documents=documents, ids=ids)
    print("Vectors stored successfully!")

    print("Invoking similarity search test...", end="")
    results = vector_store.similarity_search(query="Add memory to an agent", k=2)
    print("Done")
    print(results)


if __name__ == "__main__":
    load_and_store_pdfs()
