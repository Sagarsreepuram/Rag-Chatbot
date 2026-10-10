# AI Document Assistant - Project Overview

This document provides a comprehensive overview of the AI Document Assistant, detailing its technology stack, project architecture, and the complete application workflow. It functions as a Retrieval-Augmented Generation (RAG) system designed to let users securely upload custom documents (PDFs, text files) and restrict the chatbot to answering exclusively based on the provided information.

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.x | Core programming language for the backend and UI. |
| **Web UI** | [Streamlit](https://streamlit.io/) | Fast frontend framework for building the chat UI and file uploader. |
| **Orchestration Framework** | [LangChain](https://www.langchain.com/) | Managing document loading, text splitting, embedding pipelines, prompts, and vector store integrations. |
| **Large Language Model (LLM)** | Google Gemini 2.5 Flash | The primary reasoning and generating model underlying the assistant, via the `langchain-google-genai` package. |
| **Embedding Model** | HuggingFace (`all-MiniLM-L6-v2`) | Local open-source model used to map text data into dense vectors. |
| **Vector Database** | [FAISS](https://faiss.ai/) (CPU) | Facebook AI Similarity Search. Serves as the efficient local database to store and retrieve document embeddings. |
| **Document Parsers** | `PyPDFLoader` & `TextLoader` | Tools for extracting raw text from PDFs and TXT files. |

---

## 📂 Project Architecture

The `app/` directory houses the modular logic for the system:

- **`ui.py`**: The main presentation layer built with Streamlit. Manages UI elements (chatbox, sidebars), session states, file uploading, removing uploaded files, and coordinating backend execution.
- **`loader.py`**: Handles locating and extracting text from unstructured documents `.pdf` and `.txt` locally from the `data/docs` folder.
- **`splitter.py`**: Contains recursive text-splitting configurations to divide massive documents into smaller, meaningful 500-character chunks to optimize embedding quality and LLM context window limits.
- **`embeddings.py`**: Exposes the HuggingFace `SentenceTransformer` locally without relying on external API credits to vectorize chunks.
- **`vectorstore.py`**: Manages creating and saving the FAISS index database to disk, and retrieving it into memory.
- **`index_manager.py`**: Orchestrator that strings together the loader, splitter, and vectorstore to form a completed index. Handles wiping out old indexes if new uploads dictate a rebuild.
- **`retriever.py`**: Contains the semantic search function. It notably uses dynamic top-K results and similarity thresholds (adapting tightly to shorter vs. longer queries).
- **`rag_pipeline.py`**: The core AI logic. When a user asks a question, this script polls the `retriever`, gathers the context, injects it into a prompt, invokes the `Gemini` LLM, and formats the response along with explicit source filenames and page citations.
- **`prompts.py`**: Contains strict `ChatPromptTemplate` configurations that forcefully ground the LLM's responses entirely in the uploaded files, discouraging hallucinations.
- **`agent_logic.py` & `tools.py`**: Contains experimental logic acting strictly as classifiers or secondary functions to determine if a question *requires* document retrieval versus general knowledge.

---

## 🔄 Project Workflow

How the project fulfills its requirements from start to finish:

1. **User Upload & Document Ingestion**
   - The user opens the Streamlit app and uses the sidebar to upload a handful of PDFs or text files.
   - `ui.py` saves the raw files to the local folder at `data/docs/`.
   - Any prior existing chat history or indexed vector stores are wiped clean so the session only considers the current batch of files.

2. **Index Building (Document Processing & Embedding)**
   - The UI spins a loader to "build the index". `index_manager.py` kicks into action.
   - `loader.py` loops through the newly uploaded files. Let's say a 10-page PDF is scanned.
   - `splitter.py` breaks these pages up cleanly into ~500-character overlapping chunks.
   - `embeddings.py` downloads/initializes the HuggingFace MiniLM model which computes vector representations for every chunk.
   - `vectorstore.py` binds these representations together and drops a `FAISS` structure into the `data/faiss_index/` directory.

3. **User Prompting & Similarity Search**
   - The user submits a query via the chatbox (e.g., "From the document, what is the revenue goal?").
   - `rag_pipeline.py` starts and forwards the prompt to `retriever.py`.
   - The query itself is vectorized using the precise same local MiniLM model.
   - FAISS executes a Similarity Search, calculating the mathematically closest chunk vectors to the question. It returns the top `k` passages that breach the threshold, bringing their metadata (source file, page) with them.

4. **Generation & Citation Formulation**
   - If no relevant text passes the similarity threshold, a Hard Guard halts generation and forces a fallback ("Answer not found in the provided data").
   - If useful text is found, it is aggregated into a single formatted contextual reference.
   - The application fetches the strict prompt template from `prompts.py` ("You are a strict document-based assistant. Answer ONLY using the provided context").
   - Gemini 2.5 Flash is invoked via the Gemini API, reviewing the prompt and the provided document chunks simultaneously to carefully extract the targeted answer.
   - The LLM's raw text response is caught. The system attaches the source citations (like "Report.pdf (page 6)") mapping them to where the context chunks originated.
   
5. **Output Display**
   - Streamlit pushes the finalized answer + sources onto the chat interface. It caches this back-and-forth into the session history, allowing conversation to accrue sequentially.
