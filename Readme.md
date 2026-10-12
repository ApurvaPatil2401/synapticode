🧠 SynaptiCode: Brain-to-Code Simulator (with Ollama + Streamlit)
SynaptiCode is an experimental interface that simulates a brain-to-code experience. It mimics real-time neural focus using simulated EEG signals to trigger code generation using local LLMs via Ollama, and visualizes the results interactively with Streamlit.

⚡ This is a simulation prototype — no EEG hardware is required.

🚀 Features
🧠 Focus-triggered prompts based on simulated attention levels

💭 Thought-driven coding using natural language + LLM (e.g., gemma:2b)

🎨 Auto-executes and visualizes generated Python code (plots, outputs)

✅ Validator to fix code errors like missing imports before execution

🧪 Streamlit GUI for an interactive experience

📦 Installation
You need Python 3.9+ and Ollama installed locally.

bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/yourname/synapticode.git
cd synapticode

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Ollama and pull a model
ollama run gemma:2b

# 5. Run the app
streamlit run main.py
🧪 How It Works
Simulated EEG → Randomized "focus" levels.

If focus exceeds threshold (> 0.8), it selects a random thought prompt.

The prompt is passed to an Ollama LLM (like gemma:2b) for code generation.

Code is validated, then executed in a sandboxed environment.

Output (plots or text) is shown live in the Streamlit GUI.

📸 Screenshot

(Add a screenshot of your Streamlit interface here)

💡 Future Directions
Real EEG support (e.g., OpenBCI, Muse)

Memory + adaptive thought modeling

Live feedback loop from code output to model

Stream-of-consciousness parsing

🧠 Inspired by
Neural decoding, LLM-agent architectures, brain-computer interfaces (BCIs)

📄 License
MIT — open for experimentation and learning.

✅ Okay to Push?
Yes, your project is in a good enough state to go public. Just:

Add .gitignore (for venv, __pycache__, etc.)

Make sure no personal secrets or tokens are hardcoded

Include requirements.txt (you can generate with: pip freeze > requirements.txt)