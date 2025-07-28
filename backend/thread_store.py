import json
from pathlib import Path

STORE_PATH = Path("thread_store.json")

def load_threads():
    if STORE_PATH.exists():
        with open(STORE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_threads(mapping):
    with open(STORE_PATH, "w") as f:
        json.dump(mapping, f, indent=2)
