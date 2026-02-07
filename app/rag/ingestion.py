# Chargement PDF -> Split -> ChromaDB
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# pdf_path="../data/The-IT-Support-Handbook.pdf"

# --- config path
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, "..","..", "data", "raw","The-IT-Support-Handbook.pdf")

# --- function
def ingest_document():
    # path checking
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF not found at path: {pdf_path}")
    
    print(f"starting digital typist for {pdf_path}")

    try:
        # --- LOAD
        loader=PyPDFLoader(pdf_path)
        raw_pages=loader.load()
        print(f"loaded {len(raw_pages)} page(s)")   # output : 199 pages


        # --- SPLIT
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks=splitter.split_documents(raw_pages)
        print(f"split document into {len(chunks)} chunks")  # output : 770 chunks

        # # --- INSPECT
        # print("--- 1st Chunk ---")
        # print(chunks[0].page_content)
        # print(f"metadata : {chunks[0].metadata}")
        
        # print("--- 2nd Chunk ---")
        # print(chunks[1].page_content)
        # print(f"metadata : {chunks[1].metadata}")
        
    except FileNotFoundError:
        print(f"I couldn't find {pdf_path}")

    except Exception as e:
        print(f"❌ an error occured {e}")

    return chunks

ingest_document()