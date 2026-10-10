from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List
from embeddings import get_embedding_model
import os

FAISS_PATH = "data/faiss_index"

def create_vectorstore(chunks: List[Document]):
    embedding = get_embedding_model()

    vectordb = FAISS.from_documents(
        documents=chunks,
        embedding=embedding
    )

    vectordb.save_local(FAISS_PATH)
    return vectordb


def load_vectorstore():
    embedding = get_embedding_model()

    vectordb = FAISS.load_local(
        FAISS_PATH,
        embedding,
        allow_dangerous_deserialization=True
    )
    return vectordb
