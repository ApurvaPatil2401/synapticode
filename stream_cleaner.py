# stream_cleaner.py
import re

def extract_code_from_markdown(text: str) -> str:
    """
    Extracts clean Python code from LLM markdown-style replies.
    Removes ```python and any explanation text.
    """
    # Remove markdown-style code block
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()

    # Fallback: strip leading explanations if code-like lines exist
    lines = text.splitlines()
    code_lines = [line for line in lines if line.strip().startswith(("import", "def", "#", "plt", "print", "np", "pd"))]
    return "\n".join(code_lines) if code_lines else text.strip()

def clean_thought(prompt: str):
    # Add rules for vague or lazy thought patterns
    if "that thing" in prompt or "like before" in prompt:
        return "Load previous CSV file and create a plot"
    if "plot it again" in prompt:
        return "Plot the last data again"

    # Default: return prompt as-is
    return prompt
