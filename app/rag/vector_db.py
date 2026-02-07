# vector db
# import os
# from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
# from langchain_chroma import Chroma
# from ingestion import ingest_document  
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_classic.chains import create_retrieval_chain
# from langchain_classic.chains.combine_documents import create_stuff_documents_chain


# load_dotenv()

# def main():
#     # --- CONFIG
#     # model <-> transaltor
#     print("⏳ Chargement du modèle d'embedding...")
#     hf_token=os.getenv("hf_token_embedding")
#     embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

#     # chemin du stockager : chroma db
#     store_path = "../data/chroma_langchain_db"


#     # --- CHARGEMENT DE LA BASE 
#     if os.path.exists(store_path) and os.listdir(store_path):
#         print("📂 Base de données existante détectée. Chargement...")
#         vector_store = Chroma(
#             embedding_function=embeddings,
#             persist_directory=store_path
#         )

#     # --- CRÉATION           
#     else:
#         print("🆕 Création d'une nouvelle base de données...")
#         chunks = ingest_document()  
#         vector_store = Chroma.from_documents(
#             documents=chunks,
#             embedding=embeddings,
#             persist_directory=store_path
#         )
#         print(f"✅ {len(chunks)} chunks ont été vectorisés et sauvegardés.")

#     # --- INTERACTION UTILISATEUR 
#     user_query = input("\n🔎 Posez votre question : ")
    
#     # --- RECHERCHE DE SIMILARITÉ 
#     # Chroma : sentence_similarity -> datafile vs query
#     print("⚙️ Recherche des passages pertinents...")
#     results = vector_store.similarity_search(user_query, k=3) # k : Top 3 résultats

#     # --- AFFICHAGE DES RÉSULTATS 
#     print(f"\n--- Top 3 des passages trouvés pour : '{user_query}' ---")    
#     for i, doc in enumerate(results):   # enumerate : volume (low, medium, high)
#         print(f"\n📄 RÉSULTAT #{i+1} (Source: {doc.metadata.get('source', 'Inconnue')})")
#         print("-" * 50)
#         print(doc.page_content)  # chunk in doc loaded
#         print("-" * 50)

    
#     # Retriever : searching Tool
#     retriever = vector_store.as_retriever(search_kwargs={"k": 3})   # k : top k results

#     # LLM 
#     # Mistral-7B -> Hugging Face
#     print("🧠 Connexion au LLM (Mistral-7B)...")
#     llm = HuggingFaceEndpoint(
#         # repo_id="mistralai/Mistral-7B-Instruct-v0.3",
#         repo_id="HuggingFaceH4/zephyr-7b-beta",
#         huggingfacehub_api_token=hf_token,
#         temperature=0.1,    # 0.1 : precision, pas de créativité folle
#         max_new_tokens=512      # Longueur max de la réponse
#     )

#     # La consigne
#     system_prompt = (
#         f"You are an expert IT Support Assistant. "
#         "Use the provided context chunks to answer the user's question clearly and concisely. "
#         "If the answer is not in the context, say 'I don't have enough information in my documents'. "
#         "Do not invent information."
#         "\n\n"
#         "--- Context ---\n"
#         "{context}"
#     )
    
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ])

#     # D. La Chaîne (L'assemblage)
#     # 1. Chain pour insérer les docs dans le prompt
#     question_answer_chain = create_stuff_documents_chain(llm, prompt)
#     # 2. Chain globale (Retrieval + QA)
#     rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#     # --- ÉTAPE 3 : INTERACTION ---
#     while True:
#         user_query = input("\n🔎 Posez votre question IT (ou 'q' pour quitter) : ")
#         if user_query.lower() == 'q':
#             break
            
#         print("🤖 L'IA réfléchit...")
        
#         # Lancement de la chaîne
#         response = rag_chain.invoke({"input": user_query})
        
#         print("\n" + "="*50)
#         print("💡 RÉPONSE GÉNÉRÉE :")
#         print("="*50)
#         print(response["answer"])
#         print("\n" + "-"*20)
        
#         # Optionnel : Afficher les sources utilisées
#         print("📚 Sources utilisées :")
#         for i, doc in enumerate(response["context"]):
#             print(f"- Page {doc.metadata.get('page_label', '?')}")

# if __name__ == "__main__":
#     main()
#-----------------------------
# from langchain_chroma import Chroma
# # from embedding import embedding_data_file
# from dotenv import load_dotenv
# import os
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from ingestion import ingest_document

# # --- embedding data file
# def embedding_data_file():
#     hf_key=os.getenv("hf_token_embedding")
#     global embeddings
#     embeddings=HuggingFaceEmbeddings(
#         api_key=hf_key,
#         model_name="BAAI/bge-m3")
#     chunks=ingest_document()
#     chunk_text=[doc.page_content for doc in chunks]

#     vectors=embeddings.embed_documents(chunk_text)     # embed_query() | documents
#     chunk_text[:3]

#     print(f"Number of chunks vectorized {len(vectors)}")
#     print(f"dim of 1st chunk {len(vectors[0])}")
#     return vectors

# # --- store vectors in chroma db
# vector_store=Chroma(
#     # collection_name="example_collection",
#     embedding_function=embeddings,
#     persist_directory="./data/chroma_langchain_db", 
# )