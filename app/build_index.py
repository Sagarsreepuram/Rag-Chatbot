from loader import load_documents_eager
from splitter import split_with_recursive
from vectorstore import create_vectorstore

print("🔧 Building vector store (one time)...")

docs = load_documents_eager("data/docs")
chunks = split_with_recursive(docs)
create_vectorstore(chunks)

print("✅ Vector store built successfully.")
