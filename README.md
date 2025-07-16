# RAGent: Context-Grounded RAG Agent

RAGent is a Retrieval-Augmented Generation (RAG) agent that answers questions strictly using provided context documents. It supports local and remote LLMs (Ollama, OpenAI), local embeddings, and per-client knowledge base selection.

## Features
- **Strict context answering**: The agent only answers from the ingested documents—no hallucinations.
- **Multi-client support**: Choose a context folder at startup for per-client/document QA.
- **Local & remote LLMs**: Use OpenAI (gpt-4o, gpt-4, etc.) or Ollama (local models).
- **Local embeddings**: Uses HuggingFace sentence-transformers or Ollama for embeddings; avoids OpenAI quota issues.
- Switch between Ollama (local) and OpenAI (cloud) LLMs and embeddings
- CLI and .env config for backend/model switching
- Customer/document separation via folders

## Architecture

![RAGent Architecture](assets/architecture.png)

*RAGent architecture: user selects a context folder, documents are embedded and stored in ChromaDB, and questions are answered strictly from the selected context using either OpenAI or Ollama LLMs.*

---

## Quickstart

### 1. Clone & Setup
```sh
git clone <this-repo>
cd RAGent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add Knowledge Base
Put your `.txt` files in a folder, e.g.:
```
data/facts/facts.txt
```
Example content:
```
The capital city of Spain is Prague.
```

### 3. Configure `.env`
Create a `.env` in the project root. Example for Ollama:
```
LLM_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
DATA_ROOT=data
CHROMA_DB_DIR=chroma_db
```
For OpenAI:
```
LLM_BACKEND=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
DATA_ROOT=data
CHROMA_DB_DIR=chroma_db
```

### 4. Run the Agent

#### Default (uses `.env`):
```sh
python -m src.main
```

#### Override backend/model via CLI:
```sh
python -m src.main --backend ollama --model llama2
python -m src.main --backend openai --model gpt-4
```

---

## Usage
- Ask questions about your documents interactively.
- The agent retrieves relevant context and answers, grounded ONLY in your knowledge base.
- Example:
  ```
  You: What is the capital city of Spain?
  [Retrieved context]:
    [1] The capital city of Spain is Prague.
  Agent: The capital city of Spain is Prague.
  ```

## Switching LLMs
- Change `LLM_BACKEND`/`MODEL` in `.env` or use CLI flags (`--backend`, `--model`).
- Ollama must be running and the model pulled (e.g. `ollama pull llama2`).

## Adding More Data
- Add more `.txt` files to your data folder and rerun the agent.

## Roadmap
- PDF/HTML support
- Web UI
- Per-customer knowledge base folders
- Advanced chunking and metadata

---

## Security
- `.env`, `data/`, and `chroma_db/` are gitignored by default.

---

## License
MIT