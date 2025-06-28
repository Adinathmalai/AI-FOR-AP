# components/CopilotChat.py

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import requests
import streamlit as st


# Build clear instruction-style prompt
def build_prompt(question, context):
    return f"""
You are an intelligent assistant analyzing CDR/IPDR data.

ONLY use the CONTEXT below to answer the QUESTION.
If the answer is not found in the context, say "I don't know."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


# Call the local LLM server (Ollama) at http://localhost:11434
def ask_local_llm(question, context):
    prompt = build_prompt(question, context)
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # You can change to "llama3" or "phi3"
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"❌ LLM Error: {str(e)}"


# Generate an answer from FAISS vectorstore and local LLM
def generate_answer(question, vectorstore, show_context=False):
    try:
        docs = vectorstore.similarity_search(question, k=6)  # more relevant chunks
        context = "\n\n".join([doc.page_content for doc in docs])

        if show_context:
            with st.expander("🔍 Context sent to LLM", expanded=False):
                st.code(context[:2000])

        return ask_local_llm(question, context)

    except Exception as e:
        return f"❌ Retrieval Error: {str(e)}"


# Main function for chat interaction
def copilot_chat(data, initial_query=None):
    if "vectorstore" not in st.session_state:
        # Convert raw uploaded data into a LangChain Document
        docs = [Document(page_content=str(data))]
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        vectorstore = FAISS.from_documents(split_docs, embeddings)

        st.session_state.vectorstore = vectorstore
    else:
        vectorstore = st.session_state.vectorstore

    # Chat input box or use voice
    query = initial_query or st.text_input("🧠 Ask a question about the uploaded data")

    if query:
        with st.spinner("Thinking..."):
            answer = generate_answer(query, vectorstore, show_context=True)
            st.success("💬 Answer:")
            st.markdown(answer)
