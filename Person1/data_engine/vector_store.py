import os
import ssl
import json
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from data_engine.matcher import load_all_schemes

os.environ["CURL_CA_BUNDLE"] = ""
os.environ["PYTHONHTTPSVERIFY"] = "0"
ssl._create_default_https_context = ssl._create_unverified_context

INDEX_PATH = "data_engine/vector_index.npz"
META_PATH = "data_engine/vector_meta.json"

_model = None

def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return _model

def build_vector_index():
    schemes = load_all_schemes()
    documents, metadatas = [], []

    for s in schemes:
        sid = s["scheme_id"]
        base_meta = {
            "scheme_id": sid,
            "scheme_name": s["scheme_name"],
            "source_url": s["source_url"],
            "date_checked": s["date_checked"]
        }

        doc1 = (
            f"Scheme: {s['scheme_name']} ({s['ministry']}). Benefits: {s['benefits_summary']}. "
            f"Exclusions: {'; '.join(s.get('exclusions', []))}."
        )
        documents.append(doc1)
        metadatas.append({**base_meta, "section": "benefits_and_exclusions", "text_chunk": doc1})

        doc2 = (
            f"Scheme: {s['scheme_name']}. Required Documents: {', '.join(s['documents_required'])}. "
            f"Application Steps: {' '.join(s['application_steps'])}"
        )
        documents.append(doc2)
        metadatas.append({**base_meta, "section": "documents_and_steps", "text_chunk": doc2})

    if documents:
        model = get_embedder()
        embeddings = model.encode(documents, normalize_embeddings=True)
        np.savez(INDEX_PATH, embeddings=embeddings)
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(metadatas, f, indent=2, ensure_ascii=False)
    print(f"Indexed {len(documents)} chunks across {len(schemes)} schemes into {INDEX_PATH}.")

def retrieve_scheme_context(user_query: str, scheme_ids: List[str] = None, top_k: int = 3) -> List[Dict]:
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        build_vector_index()

    data = np.load(INDEX_PATH)
    embeddings = data["embeddings"]
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadatas = json.load(f)

    model = get_embedder()
    query_vec = model.encode([user_query], normalize_embeddings=True)[0]

    scores = np.dot(embeddings, query_vec)
    ranked_indices = np.argsort(scores)[::-1]

    grounded_chunks = []
    for idx in ranked_indices:
        meta = metadatas[idx]
        score = float(scores[idx])
        if scheme_ids and meta["scheme_id"] not in scheme_ids:
            continue
        if score > 0.25:
            grounded_chunks.append({
                "text_chunk": meta["text_chunk"],
                "scheme_name": meta["scheme_name"],
                "source_url": meta["source_url"],
                "date_checked": meta["date_checked"],
                "similarity_score": round(score, 3)
            })
        if len(grounded_chunks) >= top_k:
            break

    return grounded_chunks

if __name__ == "__main__":
    build_vector_index()
    print("Sample RAG Retrieval:", retrieve_scheme_context("How much money do farmers get?"))
