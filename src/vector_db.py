# vector db
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from ingestion import ingest_document  


load_dotenv()

def main():
    # --- CONFIG
    # model <-> transaltor
    print("⏳ Chargement du modèle d'embedding...")
    hf_token=os.getenv("hf_token_embedding")
    embeddings = HuggingFaceEmbeddings(api_key=hf_token, model_name="BAAI/bge-m3")

    # chemin du stockager : chroma db
    store_path = "../data/chroma_langchain_db"


    # --- CHARGEMENT DE LA BASE 
    if os.path.exists(store_path) and os.listdir(store_path):
        print("📂 Base de données existante détectée. Chargement...")
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=store_path
        )

    # --- CRÉATION           
    else:
        print("🆕 Création d'une nouvelle base de données...")
        chunks = ingest_document()  
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=store_path
        )
        print(f"✅ {len(chunks)} chunks ont été vectorisés et sauvegardés.")

    # --- INTERACTION UTILISATEUR 
    user_query = input("\n🔎 Posez votre question : ")
    
    # --- RECHERCHE DE SIMILARITÉ 
    # Chroma : sentence_similarity -> datafile vs query
    print("⚙️ Recherche des passages pertinents...")
    results = vector_store.similarity_search(user_query, k=3) # k : Top 3 résultats

    # --- AFFICHAGE DES RÉSULTATS 
    print(f"\n--- Top 3 des passages trouvés pour : '{user_query}' ---")    
    for i, doc in enumerate(results):   # enumerate : volume (low, medium, high)x
        print(f"\n📄 RÉSULTAT #{i+1} (Source: {doc.metadata.get('source', 'Inconnue')})")
        print("-" * 50)
        print(doc.page_content)  # chunk in doc loaded
        print("-" * 50)

if __name__ == "__main__":
    main()
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