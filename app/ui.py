import os
import streamlit as st
from index_manager import ensure_index_exists
from rag_pipeline import answer_question

# ---------------- Session State Initialization ----------------
if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = []

if "index_ready" not in st.session_state:
    st.session_state.index_ready = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Paths ----------------
DATA_DIR = "data/docs"
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Document Assistant")
st.caption("Ask questions strictly based on uploaded documents")

# ================= SIDEBAR =================
st.sidebar.header("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload .txt or .pdf files",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

# ---------------- Detect NEW Upload ----------------
current_files = [file.name for file in uploaded_files] if uploaded_files else []

if current_files != st.session_state.last_uploaded_files:
    # 🔄 Documents changed → reset everything
    st.session_state.index_ready = False
    st.session_state.messages = []

    # 🧹 Clear old documents
    for f in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, f))

    # 💾 Save new files
    for file in uploaded_files:
        file_path = os.path.join(DATA_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

    # Remember uploaded files
    st.session_state.last_uploaded_files = current_files

# ---------------- Uploaded File List + Delete ----------------
st.sidebar.subheader("📄 Uploaded Files")
existing_files = os.listdir(DATA_DIR)

if existing_files:
    for filename in existing_files:
        col1, col2 = st.sidebar.columns([4, 1])
        col1.write(filename)

        if col2.button("❌", key=f"delete_{filename}"):
            os.remove(os.path.join(DATA_DIR, filename))

            # Reset state after delete
            st.session_state.index_ready = False
            st.session_state.messages = []

            st.sidebar.success(f"Deleted {filename}")
            st.rerun()
else:
    st.sidebar.info("No files uploaded yet.")

# ---------------- Clear Chat Button (STEP 3) ----------------
st.sidebar.divider()

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.sidebar.success("Chat cleared!")

# ---------------- Build Index When Needed ----------------
if existing_files and not st.session_state.index_ready:
    with st.spinner("Building index from uploaded documents..."):
        ensure_index_exists(force_rebuild=True)

    st.session_state.index_ready = True
    st.sidebar.success("Files indexed successfully!")

# ================= CHAT =================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a question based on uploaded documents...")

if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = answer_question(user_input)
            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
