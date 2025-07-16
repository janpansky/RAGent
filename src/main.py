import os
from dotenv import load_dotenv, dotenv_values
import argparse

# Load .env and force override
DOTENV_PATH = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(DOTENV_PATH):
    env_vars = dotenv_values(DOTENV_PATH)
    for k, v in env_vars.items():
        os.environ[k] = v
load_dotenv(override=True)

from .rag.ingest import ingest_documents
from .rag.retriever import retrieve
from .agent.llm_switcher import get_llm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["ollama", "openai"], help="LLM backend to use")
    parser.add_argument("--model", help="Model name for the backend (e.g. llama2, gpt-3.5-turbo)")
    parser.add_argument("--show-config", action="store_true", help="Show effective config and exit")
    args = parser.parse_args()

    # Determine backend source
    backend_source = None
    if args.backend:
        backend = args.backend
        backend_source = "CLI argument"
    elif os.environ.get("LLM_BACKEND"):
        backend = os.environ.get("LLM_BACKEND")
        backend_source = "environment variable or .env"
    else:
        backend = "ollama"
        backend_source = "default"
    model = args.model

    # Show config if requested
    if args.show_config:
        print("--- Effective Configuration ---")
        print(f"Backend: {backend} (source: {backend_source})")
        print(f"Model: {model or os.environ.get('OLLAMA_MODEL') or os.environ.get('OPENAI_MODEL')}")
        print(f"OLLAMA_MODEL: {os.environ.get('OLLAMA_MODEL')}")
        print(f"OPENAI_MODEL: {os.environ.get('OPENAI_MODEL')}")
        print(f"OPENAI_API_KEY: {'set' if os.environ.get('OPENAI_API_KEY') else 'NOT SET'}")
        print(f"DATA_ROOT: {os.environ.get('DATA_ROOT')}")
        print(f"CHROMA_DB_DIR: {os.environ.get('CHROMA_DB_DIR')}")
        print(f".env loaded from: {DOTENV_PATH if os.path.exists(DOTENV_PATH) else 'not found'}")
        exit(0)

    # Warn if shell/env variable is overriding .env
    if 'LLM_BACKEND' in os.environ and backend != env_vars.get('LLM_BACKEND', 'ollama'):
        print(f"[WARNING] LLM_BACKEND from environment is overriding .env value: {os.environ['LLM_BACKEND']} (env) vs {env_vars.get('LLM_BACKEND')} (.env)")

    print(f"[INFO] Using backend: {backend} (source: {backend_source})")

    if backend not in ("ollama", "openai"):
        print("Unknown backend, defaulting to ollama.")
        backend = "ollama"

    if backend == "ollama":
        model = model or os.environ.get("OLLAMA_MODEL")
        if not model:
            model = input("Ollama model name (e.g. llama2, mistral): ").strip() or "llama2"
        os.environ["OLLAMA_MODEL"] = model
        os.environ["LLM_BACKEND"] = backend
        print(f"Using backend: {backend}, model: {model}")
        # 1. Ingest documents (if not already ingested)
        kb_folder = os.environ.get("DATA_ROOT", "data") + "/facts"
        collection_name = "facts"
        ingest_documents(kb_folder, collection_name)
        # 2. Interactive loop
        llm = get_llm()
        print("\nAsk a question about the knowledge base (type 'exit' to quit):")
        while True:
            query = input("You: ").strip()
            if query.lower() in ("exit", "quit"): break
            # Retrieve context
            results = retrieve(query, collection_name, k=3)
            docs = results.get("documents", [[]])[0]
            print(f"\n[Retrieved context]: {len(docs)} document(s) retrieved.")
            context = "\n".join(docs)
            print("[DEBUG] Actual context sent to LLM:\n" + context)
            from langchain_core.messages import SystemMessage, HumanMessage
            from src.prompts import STRICT_CONTEXT_PROMPT
            system_prompt = STRICT_CONTEXT_PROMPT.strip()
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}\nAnswer:")
            ]
            print("[DEBUG] Full prompt messages sent to LLM:")
            for m in messages:
                print(f"[{m.__class__.__name__}] {m.content}")
            answer = llm.invoke(messages)
            # Only print the answer content, not token usage or metadata
            if hasattr(answer, 'content'):
                print(f"\nAgent: {answer.content}\n")
            else:
                print(f"\nAgent: {answer}\n")
    else:
        if not os.environ.get("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY is not set. Please set it in your environment or .env file.")
            exit(1)
        model = model or os.environ.get("OPENAI_MODEL") or "gpt-4o"
        os.environ["OPENAI_MODEL"] = model
        os.environ["LLM_BACKEND"] = backend
        print(f"Using backend: {backend}, model: {model}")
        # 1. Prompt user to select a knowledge base folder
        data_root = os.environ.get("DATA_ROOT", "data")
        kb_folders = [f for f in os.listdir(data_root) if os.path.isdir(os.path.join(data_root, f))]
        print("Available knowledge base folders:")
        for idx, folder in enumerate(kb_folders):
            print(f"  [{idx+1}] {folder}")
        default_idx = kb_folders.index("facts") if "facts" in kb_folders else 0
        sel = input(f"Select folder for context [default: {kb_folders[default_idx]}]: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(kb_folders):
            kb_folder = os.path.join(data_root, kb_folders[int(sel)-1])
            collection_name = kb_folders[int(sel)-1]
        else:
            kb_folder = os.path.join(data_root, kb_folders[default_idx])
            collection_name = kb_folders[default_idx]
        print(f"Using knowledge base folder: {kb_folder}")
        ingest_documents(kb_folder, collection_name)
        # 2. Interactive loop
        llm = get_llm()
        print("\nAsk a question about the knowledge base (type 'exit' to quit):")
        while True:
            query = input("You: ").strip()
            if query.lower() in ("exit", "quit"): break
            # Retrieve context
            results = retrieve(query, collection_name, k=3)
            docs = results.get("documents", [[]])[0]
            print(f"\n[Retrieved context]: {len(docs)} document(s) retrieved.")
            context = "\n".join(docs)
            print("[DEBUG] Actual context sent to LLM:\n" + context)
            from langchain_core.messages import SystemMessage, HumanMessage
            from src.prompts import STRICT_CONTEXT_PROMPT
            system_prompt = STRICT_CONTEXT_PROMPT.strip()
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}\nAnswer:")
            ]
            print("[DEBUG] Full prompt messages sent to LLM:")
            for m in messages:
                print(f"[{m.__class__.__name__}] {m.content}")
            answer = llm.invoke(messages)
            # Only print the answer content, not token usage or metadata
            if hasattr(answer, 'content'):
                print(f"\nAgent: {answer.content}\n")
            else:
                print(f"\nAgent: {answer}\n")

if __name__ == "__main__":
    main()
