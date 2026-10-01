import json
from pathlib import Path


DATASET_FILE = Path(__file__).parent / "dataset" / "mbpp.json"


def load_dataset():

    with DATASET_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


if __name__ == "__main__":

    dataset = load_dataset()

    print(f"Loaded {len(dataset)} problems")

    for problem in dataset:

        print(
            f"{problem['task_id']}: "
            f"{problem['text']}"
        )