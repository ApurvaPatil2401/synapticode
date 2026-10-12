# executor.py

import ast
import re
import os

try:
    import black
    BLACK_AVAILABLE = True
except ImportError:
    BLACK_AVAILABLE = False


def is_code_safe(code: str) -> bool:
    """Block unsafe keywords or functions"""
    banned = ['eval', 'exec(', '__import__', 'os.remove', 'open(', 'subprocess']
    return not any(word in code for word in banned)


def auto_fix_code(code: str) -> str:
    """Add missing imports based on code usage"""
    fixed = code.strip()

    if "np." in code and "import numpy" not in code:
        fixed = "import numpy as np\n" + fixed

    if "pd." in code and "import pandas" not in code:
        fixed = "import pandas as pd\n" + fixed

    if "plt." in code and "import matplotlib.pyplot" not in code:
        fixed = "import matplotlib.pyplot as plt\n" + fixed

    if "math." in code and "import math" not in code:
        fixed = "import math\n" + fixed
    

    if "seaborn" in code and "import seaborn" not in code:
        fixed = "import seaborn as sns\n" + fixed

    return fixed


def is_valid_python(code: str) -> bool:
    """Check syntax with AST"""
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        return False


def format_code(code: str) -> str:
    """Format code with Black if available"""
    if BLACK_AVAILABLE:
        try:
            return black.format_str(code, mode=black.Mode())
        except Exception as e:
            print(f"⚠️ Black formatting failed: {e}")
    return code


def run_code(code: str):
    """Full pipeline: fix, check, validate, run"""
    print("🧪 Validating generated code...")

    if not is_code_safe(code):
        print("❌ Unsafe code detected. Execution aborted.")
        return

    code = auto_fix_code(code)

    if not is_valid_python(code):
        print("❌ Invalid Python syntax.")
        return

    code = format_code(code)

    print("⚙️ Executing Code...\n")
    try:
        exec(code, globals())
    except Exception as e:
        print(f"❌ Runtime Error: {e}")
