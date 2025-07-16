import os

def load_prompt(prompt_name: str = "strict_context") -> str:
    """
    Loads a prompt template from the prompts/ directory by name (without extension).
    """
    prompt_path = os.path.join(os.path.dirname(__file__), "../prompts", f"{prompt_name}.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

# Default prompt (for direct import)
STRICT_CONTEXT_PROMPT = load_prompt("strict_context")
