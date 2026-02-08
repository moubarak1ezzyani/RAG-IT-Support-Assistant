# Variables d'env (URL DB, Clés API)
from dotenv import load_dotenv
import os

load_dotenv()

# db    
DB_USER=os.getenv("db_user_env")
DB_PASSWORD=os.getenv("db_password_env")
DB_HOST=os.getenv("db_host_env")
DB_PORT=os.getenv("db_port_env","5432")
DB_NAME=os.getenv("db_name_env")

# link db : protocol://username:password@host:port/database_name
db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
hf_token = os.getenv("hf_token_env")
llm_in_use="Zephyr-7b"
repo_hugg_id="HuggingFaceH4/zephyr-7b-beta"
