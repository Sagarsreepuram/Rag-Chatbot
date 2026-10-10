🤖 AI Document Assistant (RAG-Based)

A ChatGPT-style AI Document Assistant that allows users to upload documents (.pdf, .txt) and ask questions strictly based on the uploaded content using Retrieval-Augmented Generation (RAG).

The system is designed to avoid hallucinations, provide source-based answers, and offer a clean, user-friendly chat interface.

✨ Features

📂 Upload multiple documents (PDF, TXT)

🔍 Retrieval-Augmented Generation (RAG) using FAISS

🧠 Answers strictly based on uploaded documents

🚫 No hallucinations (returns “Answer not found” when data is missing)

📑 Source attribution for every answer

💬 ChatGPT-style UI using Streamlit

🗑️ Delete individual files with automatic reindexing

🧹 Clear chat without affecting uploaded documents

⚡ Efficient local embeddings (no API cost for indexing)

🏗️ Architecture Overview
User Question
   ↓
FAISS Retriever (Local Embeddings)
   ↓
Relevant Document Chunks
   ↓
Gemini LLM (Answer generation)
   ↓
Final Answer + Sources

🧠 How RAG Works in This Project

Uploaded documents are loaded and split into chunks

Chunks are converted into vector embeddings using a local HuggingFace model

Vectors are stored in a FAISS index

When a question is asked:

Relevant chunks are retrieved from FAISS

Only those chunks are sent to the LLM

The LLM answers strictly from the retrieved context

If the answer is not found in documents, the system responds safely:

Answer not found in the provided data.

🛠️ Tech Stack

Python

Streamlit – UI

LangChain – RAG pipeline

FAISS – Vector database

HuggingFace Embeddings – Local embeddings

Google Gemini – LLM for answering

PyPDF – PDF parsing

📁 Project Structure
app/
├── ui.py                # Streamlit UI
├── rag_pipeline.py      # Core RAG logic
├── retriever.py         # FAISS retriever
├── index_manager.py     # Index creation & rebuild logic
├── loader.py            # PDF/TXT loaders (fault-tolerant)
├── splitter.py          # Text chunking
├── embeddings.py        # HuggingFace embeddings
├── vectorstore.py       # FAISS vector store
├── prompts.py           # Strict RAG prompt
├── agent_logic.py       # (Removed / simplified)
data/
├── docs/                # Uploaded documents
├── faiss_index/         # FAISS index files


▶️ How to Run the Project
1️⃣ Clone the repository
git clone <your-repo-url>
cd Ai-Assitant

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add environment variables

Create a .env file:

GOOGLE_API_KEY=your_gemini_api_key

5️⃣ Run the app
streamlit run app/ui.py

🧪 Example Usage

Upload files:

resume.pdf

notes.txt

Ask questions:

Who is Sagar Sreepuram?


Response:

Answer:
Sagar Sreepuram is a Software Engineering Intern with experience in AI and web development.

Sources:
- resume.pdf (page 0)

🔒 Safety & Reliability

❌ No guessing

❌ No internet knowledge

✅ Document-grounded answers only

✅ Transparent sources

✅ Robust handling of broken PDFs


🚀 Future Enhancements (Optional)

Multi-session support

OCR for scanned PDFs

FastAPI backend

Docker deployment

Authentication