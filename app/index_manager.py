import os
import shutil
from loader import load_documents_eager
from splitter import split_with_recursive
from vectorstore import create_vectorstore

FAISS_INDEX_DIR = "data/faiss_index"
FAISS_INDEX_FILE = os.path.join(FAISS_INDEX_DIR, "index.faiss")
DOCS_DIR = "data/docs"


def ensure_index_exists(force_rebuild: bool = False):
    """
    Ensures FAISS index exists.
    If force_rebuild=True, deletes old index and rebuilds.
    """

    if force_rebuild and os.path.exists(FAISS_INDEX_DIR):
        print("Force rebuild requested. Removing old index...")
        shutil.rmtree(FAISS_INDEX_DIR)

    if os.path.exists(FAISS_INDEX_FILE):
        print("Vector store exists. Loading...")
        return

    print("Vector store missing. Building now...")
    docs = load_documents_eager(DOCS_DIR)

    if not docs:
        print("No documents found. Index not created.")
        return

    chunks = split_with_recursive(docs)
    create_vectorstore(chunks)

    print("Vector store created.")
