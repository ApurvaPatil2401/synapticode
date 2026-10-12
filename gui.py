import streamlit as st
import random
import time
import io
import contextlib
from ollama import Client

client = Client()

# Simulate focus level
def get_focus_level():
    return round(random.uniform(0.5, 0.95), 2)

# Predefined thoughts
thought_prompts = [
    "Sort a list of numbers and plot them as a bar chart.",
    "Create a sine wave plot using matplotlib.",
    "Read a CSV file and show the first 5 rows.",
    "Generate a random dataset and visualize it with a scatter plot.",
    "Plot a histogram of normally distributed data.",
    "Display a pie chart of categories and values."
]

# Generate code using Ollama
@st.cache_data(show_spinner=False)
def generate_code(prompt):
    response = client.chat(
        model="gemma:2b",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response['message']['content']
    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("python"):
            content = content[len("python"):].strip()
    return content.strip()

# Validate and execute generated code with retry logic
def execute_code(code, retry=False):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    code = code.replace("plt.show()", "")  # prevent blocking
    local_env = {}
    stdout = io.StringIO()
    fig = None

    with contextlib.redirect_stdout(stdout):
        try:
            exec(code, {"plt": plt, "np": np, "pd": pd}, local_env)
            fig = plt.gcf()
        except Exception as e:
            if not retry:
                return execute_code(auto_fix_code(code, str(e)), retry=True)
            return f"❌ Execution Error: {str(e)}"
    
    output = stdout.getvalue()
    if fig and fig.axes:
        st.pyplot(fig)
    return output if output else " Code executed with a plot."

# Very basic auto-fix (e.g. for autopct bug in pie chart)
def auto_fix_code(code, error_msg):
    if "autopct" in error_msg:
        return code.replace('autopct="%1.1f%%" % round(data[\'value\'])', 'autopct="%1.1f%%"')
    return code

# --- Streamlit UI ---
st.set_page_config(page_title="🧠 SynaptiCode", layout="centered")
st.title("🧠 SynaptiCode: Brain-to-Code Simulator")

if 'log' not in st.session_state:
    st.session_state.log = []
if 'focus' not in st.session_state:
    st.session_state.focus = 0
if 'triggered' not in st.session_state:
    st.session_state.triggered = False
if 'thought' not in st.session_state:
    st.session_state.thought = ""

if st.button("🌀 Begin Focus Scan"):
    st.session_state.focus = get_focus_level()
    st.session_state.log.append(f"🧠 Focus Level: {st.session_state.focus}")
    if st.session_state.focus > 0.8:
        st.session_state.triggered = True
        st.success(f"High focus detected! Level: {st.session_state.focus}")
    else:
        st.session_state.triggered = False
        st.info("Focus not high enough. Try again.")

st.metric("🧠 Current Focus Level", st.session_state.focus)

# Triggered logic
if st.session_state.triggered:
    st.session_state.thought = random.choice(thought_prompts)
    st.session_state.log.append(f"📝 Thought Prompt: {st.session_state.thought}")
    st.info(f"💭 Thought: *{st.session_state.thought}*")

    with st.spinner("🛠 Generating code..."):
        code = generate_code(st.session_state.thought)
    st.session_state.log.append(f"📜 Generated Code:\n```python\n{code}\n```")

    with st.expander("🔍 View Generated Code"):
        st.code(code, language="python")

    with st.spinner("⚙️ Executing code..."):
        result = execute_code(code)
    st.session_state.log.append(f"⚙️ Execution Result:\n{result}")
    st.text_area("🧪 Output", value=result, height=200)

    st.session_state.triggered = False

# History log
st.markdown("---")
st.subheader("🧠 Interaction Log")
st.text("\n".join(st.session_state.log[-6:]))
