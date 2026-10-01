import json
from pathlib import Path


DATASET_FILE = Path(__file__).parent / "dataset" / "mbpp.json"


def load_dataset():
    with DATASET_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)