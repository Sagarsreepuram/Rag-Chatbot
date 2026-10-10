from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a strict document-based assistant.\n"
        "Rules:\n"
        "- Answer ONLY using the provided context.\n"
        "- Do NOT use prior knowledge or assumptions.\n"
        "- If a date range is given and the question asks for completion year, use the END year.\n"
        "- Answer in ONE clear sentence.\n"
        "- If the answer is not explicitly present in the context, reply exactly:\n"
        "  Answer not found in the provided data."
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion:\n{question}"
    )
])



direct_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Answer the question directly."
    ),
    (
        "human",
        "{question}"
    )
])
