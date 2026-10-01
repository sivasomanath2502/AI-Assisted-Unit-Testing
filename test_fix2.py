import json

from agents.test_generator import generate_tests
from utils.dataset_contract import infer_contract


with open("dataset/mbpp.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)


problem_data = next(
    p for p in dataset
    if p["task_id"] == 11
)

contract = infer_contract(problem_data)


code = """def remove_Occ(s, char):
    return s.replace(char, "", 1)
"""


tests = generate_tests(
    problem=problem_data["text"],
    code=code,
    function_name=contract["function_name"],
    reference_tests=problem_data["test_list"],
)


print("\n" + "=" * 60)
print("GENERATED TESTS")
print("=" * 60)
print(tests)