# Variables d'env (URL DB, Clés API)
from dotenv import load_dotenv
import os

# var
load_dotenv()
DB_USER=os.getenv("db_user_env")
DB_PASSWORD=os.getenv("db_password_env")
DB_HOST=os.getenv("db_host_env")
DB_PORT=os.getenv("db_port_env","5432")
DB_NAME=os.getenv("db_name_env")

# link db : protocol://username:password@host:port/database_name
db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
