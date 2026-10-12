# focus_simulator.py
import random
import time

def get_focus_level():
    """Simulate brainwave signal as a float from 0 to 1."""
    return round(random.uniform(0.5, 0.95), 2)

def wait_for_focus(threshold=0.85):
    while True:
        focus = get_focus_level()
        print(f"Focus level: {focus}")
        if focus > threshold:
            print("🧠 Trigger: High focus detected!")
            return True
        time.sleep(1)
