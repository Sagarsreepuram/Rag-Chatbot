# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# def get_embedding_model():
#     return GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001"
#     )

from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
