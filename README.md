# RAGent: Your Personal & Customer Knowledge Brain

**RAGent lets you store your own (or your customers') documents and use them as a smart helper for complex, context-specific questions.**

> Never struggle to remember all the details again—just upload your content, select the context, and ask! RAGent will answer strictly from your chosen documents, acting as an external brain for your projects, clients, or personal knowledge.

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

## Quick Start
1. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
2. **Configure environment**
   - Copy `.env.example` to `.env` and set your API keys and model names.
   - Example:
     ```
     OPENAI_API_KEY=sk-...
     LLM_BACKEND=openai   # or ollama
     OPENAI_MODEL=gpt-4o  # or gpt-4, etc.
     EMBEDDING_BACKEND=hf # or ollama/openai
     ```
3. **Add your customer or project content**
   - Place `.txt` files inside folders under `data/` (e.g., `data/ClientA/`, `data/ProjectX/`, `data/facts/`).
   - Each folder is a separate knowledge base (brain) for a client, project, or topic.
   - Example folder structure:
     ```
     data/
       Broadridge/
         onboarding.txt
         api_endpoints.txt
       facts/
         team.txt
         mission.txt
     ```
4. **Run the agent**
   ```sh
   python -m src.main
   ```
   - Select the context folder (e.g., `Broadridge`) at the prompt.
   - Ask your question. RAGent will answer using only the selected folder’s content.

## Example Usage
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