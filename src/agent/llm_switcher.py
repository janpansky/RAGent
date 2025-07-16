# LLM switcher for Ollama/OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.llms import OpenAI, Ollama

def get_llm():
    llm_backend = os.environ.get("LLM_BACKEND", "ollama")
    if llm_backend == "openai":
        model_name = os.environ.get("OPENAI_MODEL")
        api_key = os.environ.get("OPENAI_API_KEY")
        if model_name and model_name.startswith("gpt-"):
            # Chat models (gpt-3.5-turbo, gpt-4, gpt-4o, etc)
            from langchain_community.chat_models import ChatOpenAI
            return ChatOpenAI(model=model_name, openai_api_key=api_key)
        else:
            # Completion models (text-davinci-003, etc)
            from langchain_community.llms import OpenAI
            return OpenAI(model_name=model_name, openai_api_key=api_key)
    elif llm_backend == "ollama":
        from langchain_community.llms import Ollama
        model_name = os.environ.get("OLLAMA_MODEL")
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        return Ollama(base_url=base_url, model=model_name)
    else:
        raise ValueError(f"Unknown LLM_BACKEND: {llm_backend}")
