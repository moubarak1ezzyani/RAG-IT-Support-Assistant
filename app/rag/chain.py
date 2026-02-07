# La chaîne RetrievalQA + Prompt
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from .embeddings import get_vector_store

load_dotenv()

def build_rag_chain():
    """
    full RAG pipeline: Retriever -> LLM -> Answer
    """
    # --- Get Vector Store & Retriever
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # --- Connect to LLM
    hf_token = os.getenv("hf_token_embedding")
    if not hf_token:
        raise ValueError("❌ Environment variable 'hf_token_env' is missing.")

    llm_in_use="Zephyr-7b"
    print(f"🧠 Connecting to LLM {llm_in_use}...")
    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        huggingfacehub_api_token=hf_token,
        temperature=0.1,
        max_new_tokens=512
    )

    # --- Define the Prompt
    system_prompt = (
        "You are an expert IT Support Assistant. "
        "Use the provided context chunks to answer the user's question clearly and concisely. "
        "If the answer is not in the context, strictly say 'I don't have enough information'. "
        "\n\n--- Context ---\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # --- Build the Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    print("✅ RAG Chain ready.")
    return rag_chain