import streamlit as st
from streamlit_extras.colored_header import colored_header
from langchain_community.document_loaders import TextLoader
import textwrap
import os
import time

def chat_bot():
    # Set environment variable for Hugging Face API token
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

    # Load the text document
    loader = TextLoader("Disease Data\medical.txt")
    document = loader.load()

    # Preprocessing function to wrap text
    def wrap_text_preserve_newlines(text, width=110):
        lines = text.split("\n")
        wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
        wrapped_text = "\n".join(wrapped_lines)
        return wrapped_text

    # Text Splitting
    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(chunk_size=160, chunk_overlap=0)
    text_splitter.split_documents(document)
    docs = text_splitter.split_documents(document)

    # Embeddings 
    from langchain_community.embeddings import HuggingFaceEmbeddings 
    from langchain.vectorstores import FAISS
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    def get_document_response(query):
        doc = db.similarity_search(query)
        response = str(doc[0].page_content)
        return response
    
    # Greeting message
    st.title("Chat with Disease Chatbot")
    colored_header(
        label="",
        description="Chat about your health, ask any question related to healthcare such as symptoms, disease causes, preventive measures, and associated treatment.",
        color_name="red-70",
    )
    
    st.write("\n")
    st.write("\n")
    
    # Initial greeting message
    st.session_state.messages = [{"role": "assistant", "content": "Hi, i'm Pete, your Disease ChatBot. How can I assist you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me Anything "):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Retrieve response from document based on user query
            response = get_document_response(prompt)
            lines = response.splitlines()

            # Display the response line by line
            for line in lines:
                full_response += line + "\n"
                message_placeholder.markdown(full_response)
                time.sleep(0.3)  # Add a delay of 1 second between API requests

            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    chat_bot()
