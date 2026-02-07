import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from .ingestion import ingest_document

# paths 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = os.path.join(CURRENT_DIR, "..", "..", "data", "chroma_langchain_db")
PDF_PATH = os.path.join(CURRENT_DIR, "..", "..", "data", "raw","The-IT-Support-Handbook.pdf")

def get_vector_store():
    model_in_use="BAAI/bge-m3"
    print(f"⏳ Loading Embedding Model {model_in_use}...")
    embeddings = HuggingFaceEmbeddings(model_name=model_in_use)

    # DB exists  
    if os.path.exists(STORE_PATH) and os.listdir(STORE_PATH):
        print(f"📂 Loading existing Vector Store from: {STORE_PATH}")
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=STORE_PATH
        )
    # DB is empty        
    else:
        print(f"🆕 Creating NEW Vector Store at: {STORE_PATH}")
        chunks = ingest_document(PDF_PATH)
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=STORE_PATH
        )
        print("✅ Vector Store created and persisted.")
    
    return vector_store




# # Configuration du modèle HuggingFace
# #_____________________________________
# # from dotenv import load_dotenv
# # import os
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# # from ingestion import ingest_document
# from huggingface_hub import InferenceClient



# embeddings=HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

# chunks=ingest_document()
# chunk_text=[doc.page_content for doc in chunks]

# # --- implement Hugg Face

# # client = InferenceClient(
# #     provider="hf-inference",
# #     api_key=os.environ["hf_token_embedding"],
# # )

# # result = client.sentence_similarity(
# #     {
# #     "source_sentence": "That is a happy person",
# #     "sentences": [
# #         "That is a happy dog",
# #         "That is a very happy person",
# #         "Today is a sunny day"
# #     ]
# # },
# #     model="BAAI/bge-m3",
# # )
# #--------------------------------------
# # def embedding_data_file():
# #     hf_key=os.getenv("hf_token_embedding")
# #     embeddings=HuggingFaceEmbeddings(
# #         api_key=hf_key,
# #         model_name="BAAI/bge-m3")
# #     chunks=ingest_document()
# #     chunk_text=[doc.page_content for doc in chunks]

# #     vectors=embeddings.embed_documents(chunk_text)     # embed_query() | documents
# #     chunk_text[:3]

# #     print(f"Number of chunks vectorized {len(vectors)}")
# #     print(f"dim of 1st chunk {len(vectors[0])}")
# #     return vectors

# # # Model loader (BGE-M3)
# # import os
# # from huggingface_hub import InferenceClient
# # from ingestion import chunks
# # from dotenv import load_dotenv
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_chroma import Chroma

# # load_dotenv()
# # # --- exetrnal model
# # # -> var
# # hf_token=os.getenv("HF_TOKEN")
# # embedding_model_id="BAAI/bge-m3"

# # client = InferenceClient(
# #     provider="hf-inference",
# #     # api_key=os.environ["HF_TOKEN"],
# #     api_key=hf_token
# # )
# # text_source=input("Type a sentence to start embedding:")

# # # --- convert to vectors
# # embeddings=HuggingFaceEmbeddings(model_name=embedding_model_id)
# # query_result=embeddings.embed_documents(text_source)  # query : embed_query() | doc : embed_documents()
# # print(str(query_result)[:100])  # 100 characters


# # # --- chroma db


# # # --- searching for similarity
# # for chunk in chunks:
# #     result = client.sentence_similarity(
# #         {
# #         "source_sentence": text_source,
# #         "sentences": chunks
# #     },  
# #         model=embedding_model_id,
# #     )






# # vectors = client.feature_extraction(
# #     # "Today is a sunny day and I will get some ice cream.",
# #     text_source,
# #     model=EMBEDDING_MODEL_ID
# # )

# # print("--- Generated vector ---")
# # print(f"dimensions : {len(vectors)} ")
# # print(f"preview {vectors[:5]}")

# # embedding_model = HuggingFaceEndpointEmbeddings(
# #         model=EMBEDDING_MODEL_ID,
# #         task="feature-extraction", 
# #         huggingfacehub_api_token=hf_token
# #     )
# # #----------------------------------------------------

