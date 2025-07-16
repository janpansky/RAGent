# Retriever for RAG
from .vector_store import get_chroma_client
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

def retrieve(query, collection_name, k=3):
    client = get_chroma_client()
    collection = client.get_or_create_collection(collection_name)
    embedding_backend = os.environ.get("EMBEDDING_BACKEND", os.environ.get("LLM_BACKEND", "ollama"))
    if embedding_backend == "openai":
        embedder = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    elif embedding_backend == "hf":
        from ..utils import LocalHFEmbeddings
        embedder = LocalHFEmbeddings(model_name=os.environ.get("HF_EMBEDDING_MODEL", "all-MiniLM-L6-v2"))
    else:
        embedder = OllamaEmbeddings(
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=os.environ.get("OLLAMA_EMBEDDING_MODEL", os.environ.get("OLLAMA_MODEL", "llama2"))
        )
    query_emb = embedder.embed_query(query)
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    return results
