# Variables d'env (URL DB, Clés API)
from dotenv import load_dotenv
import os

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
hf_token = os.getenv("hf_token_env")
llm_in_use="Zephyr-7b"
repo_hugg_id="HuggingFaceH4/zephyr-7b-beta"

# --- Backend
# db    
DB_USER = os.getenv("db_user_env", "postgres")
DB_PASSWORD = os.getenv("db_password_env", "password")
DB_HOST = os.getenv("db_host_env", "localhost")
DB_PORT = os.getenv("db_port_env", "5432")
DB_NAME = os.getenv("db_name_env", "postgres")

# link db : protocol://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY_env", "supersecretkey") 
ALGORITHM = os.getenv("ALGO_env", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30