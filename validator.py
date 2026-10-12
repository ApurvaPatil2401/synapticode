# validator.py

import ast
import re

SAFE_MODULES = {"math", "numpy", "pandas", "matplotlib", "seaborn", "random"}

# Scan for dangerous code
def is_code_safe(code: str) -> bool:
    banned_keywords = ['eval', 'exec', 'os.remove', 'open(', '__import__', 'subprocess']
    return not any(kw in code for kw in banned_keywords)

# Add common missing imports
def auto_fix_code(code: str) -> str:
    fixed_code = code.strip()

    if "np." in code and "import numpy" not in code:
        fixed_code = "import numpy as np\n" + fixed_code

    if "pd." in code and "import pandas" not in code:
        fixed_code = "import pandas as pd\n" + fixed_code

    if "plt." in code and "import matplotlib.pyplot" not in code:
        fixed_code = "import matplotlib.pyplot as plt\n" + fixed_code

    if "math." in code and "import math" not in code:
        fixed_code = "import math\n" + fixed_code

    return fixed_code

# Optionally validate AST syntax
def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
