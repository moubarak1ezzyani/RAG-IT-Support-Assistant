# Variables d'env (URL DB, Clés API)
import os
from dotenv import load_dotenv

load_dotenv()

# --- rag
# ingestion
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, "..","..", "data", "raw","The-IT-Support-Handbook.pdf")

# embeddings
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = os.path.join(CURRENT_DIR, "..", "..", "data", "chroma_langchain_db")
pdf_path = os.path.join(CURRENT_DIR, "..", "..", "data", "raw","The-IT-Support-Handbook.pdf")
model_in_use="BAAI/bge-m3"

# chain
hf_token = os.getenv("hf_token_embedding")
llm_in_use="Zephyr-7b"
repo_hugg_id="HuggingFaceH4/zephyr-7b-beta"