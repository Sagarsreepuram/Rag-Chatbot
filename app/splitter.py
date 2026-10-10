from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

def split_with_character(documents: List[Document])-> List[Document]:
    splitter = CharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )

    return splitter.split_documents(documents)

def split_with_recursive(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    return splitter.split_documents(documents)

