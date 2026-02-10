import logging
import numpy as np
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from langchain_huggingface import HuggingFaceEmbeddings

from app.db.models import Query
from app.core.config import model_in_use

logger = logging.getLogger(__name__)

def perform_clustering(db: Session, num_clusters: int = 3):
    """
    fetch queries: embed -> update clusters in DB.
    Returns a dictionary with results.
    """
    # --- Fetch Data
    queries = db.query(Query).filter(Query.question != None).all()
    
    if len(queries) < num_clusters:
        return {
            "success": False, 
            "error": f"Not enough data. Need {num_clusters} queries, found {len(queries)}."
        }

    # --- Extract Text
    questions_text = [q.question for q in queries]
    
    # --- Generate Embeddings
    logger.info(f"Generating embeddings using {model_in_use}...")
    embeddings_model = HuggingFaceEmbeddings(model_name=model_in_use)
    vectors = embeddings_model.embed_documents(questions_text)
    X = np.array(vectors)

    # --- Run K-Means
    logger.info(f"Running K-Means with k={num_clusters}...")
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(X)
    labels = kmeans.labels_

    # --- Save to DB
    for i, query_obj in enumerate(queries):
        query_obj.cluster_label = int(labels[i])
    
    db.commit()

    return {
        "success": True,
        "total_questions": len(queries),
        "clusters_created": num_clusters
    }