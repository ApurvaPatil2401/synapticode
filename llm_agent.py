# llm_agent.py
import subprocess
import re

def extract_code_blocks(text):
    """Extracts code blocks from Ollama output."""
    code_blocks = re.findall(r"```(?:python)?(.*?)```", text, re.DOTALL)
    return "\n\n".join(code_blocks).strip() if code_blocks else text

def generate_code(prompt: str) -> str:
    try:
        model = "gemma:2b"
        print(f"🧠 Generating code using Ollama model: {model}")

        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',  # Fix UnicodeDecodeError on Windows
            timeout=90
        )

        if result.returncode != 0:
            return f"# Ollama error:\n{result.stderr}"

        return result.stdout.strip()

    except Exception as e:
        return f"# Exception occurred: {e}"
