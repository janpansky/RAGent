# Utility functions for the RAGent project

from typing import List

class LocalHFEmbeddings:
    """
    Local HuggingFace embedding model using sentence-transformers.
    Usage:
        embedder = LocalHFEmbeddings(model_name='all-MiniLM-L6-v2')
        vecs = embedder.embed_documents(["text1", "text2"])
        qvec = embedder.embed_query("query text")
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    def embed_documents(self, docs: List[str]):
        return self.model.encode(docs).tolist()
    def embed_query(self, query: str):
        return self.model.encode([query])[0].tolist()

def print_chroma_contents():
    """
    Prints all collections and their ids, documents, and metadatas from the Chroma vector DB.
    """
    from .rag.vector_store import get_chroma_client
    client = get_chroma_client()
    collections = client.list_collections()
    print(f"Collections: {[c.name for c in collections]}")
    for coll in collections:
        c = client.get_or_create_collection(coll.name)
        out = c.get(include=["ids", "documents", "metadatas"])
        print(f"\nCollection: {coll.name}")
        for i, doc in enumerate(out.get('documents', [])):
            print(f"  ID: {out['ids'][i]}")
            print(f"  Document: {doc}")
            print(f"  Metadata: {out['metadatas'][i]}")
