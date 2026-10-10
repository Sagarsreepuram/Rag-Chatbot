# from vectorstore import load_vectorstore

# def get_retriever():
#     vectordb = load_vectorstore()
#     return vectordb.as_retriever(
#         search_type = "similarity",
#         search_kwargs = {"k":5}
#     )

from vectorstore import load_vectorstore

SIMILARITY_THRESHOLD = 0.35

def get_retriever():
    vectordb = load_vectorstore()

    def retrieve(query: str):
        word_count = len(query.split())

        # Dynamic k
        if word_count <= 4:
            k = 7
            threshold = 0.25   # 🔥 LOWER for short queries
        elif word_count <= 10:
            k = 5
            threshold = 0.35
        else:
            k = 3
            threshold = 0.4

        results = vectordb.similarity_search_with_score(query, k=k)

        filtered_docs = []
        for doc, score in results:
            if score >= threshold:
                filtered_docs.append(doc)

        return filtered_docs

    return retrieve

