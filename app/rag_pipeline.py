from retriever import get_retriever
from prompts import rag_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

DEBUG = True

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

FALLBACK_ANSWER = """Answer:
Answer not found in the provided data."""

def answer_question(question: str) -> str:
    # 1️⃣ Always retrieve (document-based assistant)
    print("🧠 Retrieval mode: DOCUMENT-ONLY")

    retriever = get_retriever()
    docs = retriever(question)

    # 📚 Collect sources
    sources = set()
    for doc in docs:
        meta = doc.metadata or {}
        source = meta.get("source", "unknown")
        page = meta.get("page")

        if page is not None:
            sources.add(f"{os.path.basename(source)} (page {page})")
        else:
            sources.add(os.path.basename(source))


    # 🚫 HARD GUARD: no documents retrieved
    if not docs:
        return FALLBACK_ANSWER

    # 2️⃣ Build context (deduplicated + non-empty)
    context = "\n\n".join(
        dict.fromkeys(
            doc.page_content.strip()
            for doc in docs
            if doc.page_content and doc.page_content.strip()
        )
    )

    # 🚫 HARD GUARD: empty context
    if not context:
        return FALLBACK_ANSWER

    # 3️⃣ DEBUG LOGS (optional)
    if DEBUG:
        print("🔎 Retrieved", len(docs), "documents")
        for i, doc in enumerate(docs):
            print(f"\n--- Doc {i+1} ---")
            print(doc.page_content)

        print("\n📄 Final context sent to LLM:\n")
        print(context)

    # 4️⃣ Build RAG prompt
    prompt = rag_prompt.invoke({
        "context": context,
        "question": question
    })

    # 5️⃣ Call LLM (SAFE — context guaranteed)
    response = llm.invoke(prompt)
    # Normalize LLM response content
    if isinstance(response.content, list):
        answer_text = response.content[0].get("text", "").strip()
    else:
        answer_text = response.content.strip()


    # 6️⃣ Final output (clean format)
    sources_text = "\n".join(f"- {s}" for s in sorted(sources))

    return f"""Answer:
{answer_text}

Sources:
{sources_text}"""
