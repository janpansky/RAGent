# Chroma vector store setup and management
import chromadb
import os
from dotenv import load_dotenv
load_dotenv()

def get_chroma_client():
    return chromadb.PersistentClient(path=os.environ.get("CHROMA_DB_DIR", "chroma_db"))
