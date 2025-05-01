from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

from core.config import settings

file_path = "./src/data/result.pdf"

print("Loading pdf file...", end="")
loader = PyPDFLoader(file_path)
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

connection = settings.DB_URL
collection_name = "test"

print("Attempting to connect to PGVector...", end="")
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)
print("Connected!")

def store_into_vectordb(split_pages):
    documents = []
    ids = []
    for i, text in enumerate(split_pages):
        ids.append(i)
        documents.append(Document(page_content=text.page_content))
    vector_store.add_documents(documents=documents, ids=ids)

print("Storing vectors...", end="")
store_into_vectordb(chunked_pages)
print("Vectors stored successfully!")


print("Invoking similarity search...", end="")
results = vector_store.similarity_search(query="Add memory to an agent",k=2)
print("Done")
print(results)
