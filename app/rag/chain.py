# La chaîne RetrievalQA + Prompt
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from embeddings import get_vector_store
from ..core.config import hf_token, llm_in_use, repo_hugg_id



def build_rag_chain():
    """
    full RAG pipeline: Retriever -> LLM -> Answer
    """
    # --- Get Vector Store & Retriever
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # --- Connect to LLM
    if not hf_token:
        raise ValueError("❌ Environment variable 'hf_token_env' is missing.")

    
    print(f"🧠 Connecting to LLM {llm_in_use}...")
    llm = HuggingFaceEndpoint(
        repo_id=repo_hugg_id,
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