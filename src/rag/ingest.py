# Ingest documents into the vector store
import os
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
from .vector_store import get_chroma_client

def ingest_documents(folder_path=None, collection_name="default"):
    if folder_path is None:
        folder_path = os.environ.get("DATA_ROOT", "data")
    client = get_chroma_client()
    # Drop the collection if it exists (to avoid stale data)
    try:
        client.delete_collection(collection_name)
        print(f"[INFO] Reset collection '{collection_name}'.")
    except Exception as e:
        if "does not exist" not in str(e).lower():
            print(f"[WARN] Could not delete collection '{collection_name}': {e}")
    collection = client.get_or_create_collection(collection_name)
    docs = []
    metadatas = []
    ids = []
    for fname in os.listdir(folder_path):
        if fname.endswith(".txt"):
            with open(os.path.join(folder_path, fname), "r") as f:
                text = f.read()
                docs.append(text)
                metadatas.append({"source": fname, "document": text})
                ids.append(fname)
    if not docs:
        print("No documents found to ingest.")
        return
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
    embeddings = embedder.embed_documents(docs)
    collection.add(
        embeddings=embeddings,
        documents=docs,
        metadatas=metadatas,
        ids=ids,
    )
    print(f"Ingested {len(docs)} documents into collection '{collection_name}'.")
