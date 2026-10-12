# main.py

from focus_simulator import wait_for_focus
from llm_agent import generate_code
from executor import run_code 
from prompt_templates import thought_prompts
import random
from stream_cleaner import extract_code_from_markdown
from stream_cleaner import clean_thought
from memory import save_history

def retry_with_error_context(prompt, error_msg, retry_fn):
    retry_prompt = f"The previous code failed. Prompt was: '{prompt}'. Error was: '{error_msg}'. Please fix it."
    return retry_fn(retry_prompt)

def main():
    print("🧠 SynaptiCode: Simulated Brain-to-Code Interface")
    
    wait_for_focus()

    # Simulate a stream-of-thought
    prompt = random.choice(thought_prompts)
    print(f"\n📝 Thought Prompt: {prompt}")
    cleaned_prompt = clean_thought(prompt)
    code = generate_code(cleaned_prompt)
    #code = generate_code(prompt)
    print("\n📜 Generated Code:\n", code)
    save_history(cleaned_prompt, code)
    clean_code = extract_code_from_markdown(code)

    try:
        exec(clean_code, globals())
    except Exception as e:
        print("🔁 Retrying with fix due to error:", e)
        clean_code = retry_with_error_context(cleaned_prompt, str(e), generate_code)
        exec(clean_code, globals())

    # Remove ``` wrappers if any
    if code.startswith("```"):
        code = "\n".join(line for line in code.splitlines() if not line.strip().startswith("```"))

    #  Validate, auto-correct, and run safely
    run_code(clean_code)


if __name__ == "__main__":
    main()
