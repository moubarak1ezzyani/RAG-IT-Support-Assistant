# Script KMeans pour regrouper les questions
import sys
import os
import logging
sys.path.append(os.getcwd())    # Ensure we can import app modules
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Query
from app.core.config import model_in_use 
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.cluster import KMeans
import numpy as np

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
EMBEDDING_MODEL_NAME = model_in_use
NUM_CLUSTERS = 3  # Start with 3 topics, increase as data grows

def run_clustering():
    db: Session = SessionLocal()
    
    try:
        # --- Extraction: Get all questions
        logger.info("🔍 Fetching questions from PostgreSQL...")
        queries = db.query(Query).filter(Query.question != None).all()
        
        if len(queries) < NUM_CLUSTERS:
            logger.warning(f"⚠️ Not enough data to cluster. Need at least {NUM_CLUSTERS} questions.")
            return

        questions_text = [q.question for q in queries]
        logger.info(f"✅ Found {len(questions_text)} questions.")

        # --- Embedding: Transform text to vectors
        logger.info(f"🧠 Loading Embedding Model ({EMBEDDING_MODEL_NAME})...")
        embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
        logger.info("🔢 Generating embeddings (this may take a moment)...")
        vectors = embeddings_model.embed_documents(questions_text)
        X = np.array(vectors)

        # --- Clustering: Apply K-Means
        logger.info(f"🤖 Running K-Means with k={NUM_CLUSTERS}...")
        kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42, n_init=10)
        kmeans.fit(X)
        
        labels = kmeans.labels_

        # --- Storage: Update Database
        logger.info("💾 Saving cluster labels to database...")
        for i, query_obj in enumerate(queries):
            query_obj.cluster_label = int(labels[i])
        
        db.commit()
        logger.info("🎉 Clustering complete! Database updated.")

    except Exception as e:
        logger.error(f"❌ Error during clustering: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_clustering()