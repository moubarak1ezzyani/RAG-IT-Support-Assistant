from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import endpoints
from app.rag.chain import build_rag_chain

# Create Tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    print("⏳ Initializing RAG Pipeline...")
    try:
        # We store the pipeline in app.state so endpoints can see it
        app.state.rag_pipeline = build_rag_chain()
        print("✅ RAG Pipeline successfully loaded.")
    except Exception as e:
        print(f"⚠️ Warning: RAG pipeline failed to initialize: {e}")
        app.state.rag_pipeline = None
    
    yield
    
    # --- SHUTDOWN ---
    print("🛑 Shutting down application...")

app = FastAPI(lifespan=lifespan)

# Connect the routes
app.include_router(endpoints.router)