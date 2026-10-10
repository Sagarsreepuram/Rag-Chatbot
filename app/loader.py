import os
from typing import List, Iterator
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader


def load_documents_eager(path: str) -> List[Document]:
    documents: List[Document] = []

    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        try:
            if file.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
                documents.extend(loader.load())

            elif file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

        except Exception as e:
            print(f"⚠️ Skipping file due to error: {file}")
            print(f"   Reason: {e}")

    return documents


def load_documents_lazy(path: str) -> Iterator[Document]:
    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        try:
            if file.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
                yield from loader.lazy_load()

            elif file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                yield from loader.lazy_load()

        except Exception as e:
            print(f"⚠️ Skipping file due to error: {file}")
            print(f"   Reason: {e}")
            continue
