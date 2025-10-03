import os
import time
import textwrap
import streamlit as st

# Optional UI helper (fallback)
try:
    from streamlit_extras.colored_header import colored_header
except Exception:
    def colored_header(label: str = "", description: str = "", color_name: str = None):
        st.markdown(f"### {label}\n{description}")

# Optional LangChain/FAISS imports
try:
    from langchain_community.document_loaders import TextLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    _LANGCHAIN_AVAILABLE = True
except Exception:
    TextLoader = None
    CharacterTextSplitter = None
    HuggingFaceEmbeddings = None
    FAISS = None
    _LANGCHAIN_AVAILABLE = False


def _load_raw_chunks(data_path: str):
    if not os.path.exists(data_path):
        # fallback to project root
        data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "medical.txt"))
    if not os.path.exists(data_path):
        return None, data_path
    with open(data_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    raw_chunks = [c.strip() for c in raw_text.split("\n\n") if c.strip()]
    return raw_chunks, data_path


def chat_bot():
    """Streamlit UI for a simple document-based chatbot.

    If LangChain and FAISS are available, we attempt a vector similarity search.
    Otherwise we fall back to a simple chunk-based text search.
    """
    # Ensure token env var is present if user intends to use HuggingFace embeddings
    os.environ.setdefault("HUGGINGFACEHUB_API_TOKEN", os.environ.get("HUGGINGFACEHUB_API_TOKEN", ""))

    # locate medical.txt
    data_path = os.path.join(os.path.dirname(__file__), "medical.txt")
    raw_chunks, resolved_path = _load_raw_chunks(data_path)
    if raw_chunks is None:
        st.error(f"medical.txt not found (checked {resolved_path}). Place medical.txt in the project root.")
        return

    db = None
    if _LANGCHAIN_AVAILABLE:
        try:
            loader = TextLoader(resolved_path)
            documents = loader.load()
            splitter = CharacterTextSplitter(chunk_size=160, chunk_overlap=0)
            docs = splitter.split_documents(documents)
            embeddings = HuggingFaceEmbeddings()
            db = FAISS.from_documents(docs, embeddings)
        except Exception:
            db = None

    def get_document_response(query: str) -> str:
        q = query.lower().strip()
        if db is not None:
            try:
                docs = db.similarity_search(query)
                if docs:
                    return str(docs[0].page_content)
            except Exception:
                pass

        # fallback simple search
        for chunk in raw_chunks:
            if all(word in chunk.lower() for word in q.split()):
                return chunk
        return raw_chunks[0][:800] if raw_chunks else "No information available."

    def wrap_text_preserve_newlines(text, width=110):
        lines = text.split("\n")
        wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
        return "\n".join(wrapped_lines)

    # UI
    st.title("Chat with Disease Chatbot")
    colored_header(label="", description="Ask about symptoms, causes, prevention and treatment.", color_name="red-70")

    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm Pete, your Disease ChatBot. How can I assist you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            response = get_document_response(prompt)
            full = ""
            for line in response.splitlines():
                full += line + "\n"
                placeholder.markdown(full)
                time.sleep(0.05)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    # For local debugging only
    pass