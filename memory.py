# memory.py
history = []

def save_history(prompt, code):
    history.append({"prompt": prompt, "code": code})

def get_last_prompt():
    return history[-1]["prompt"] if history else None
