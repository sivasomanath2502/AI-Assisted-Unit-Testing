from utils.results_writer import (
    save_problem_result,
    save_all_results,
)


problem_result = {
    "task_id": 11,
    "function_name": "remove_Occ",
    "code": """def remove_Occ(s, char):
    return s.replace(char, "", 1)
""",
    "tests": """from solution import remove_Occ

def test_example():
    assert remove_Occ("hello", "l") == "helo"
""",
    "reference": {
        "passed": True,
        "return_code": 0,
        "stdout": "",
        "stderr": "",
    },
    "result": {
        "tests_passed": 1,
        "tests_failed": 0,
        "test_errors": 0,
        "branch_covered": 2,
        "branch_total": 2,
        "branch_coverage": 100.0,
        "verdict": "PASS",
    },
    "artifacts": {
        "solution_file": "generated/problem_11/solution.py",
        "test_file": "generated/problem_11/test_generated.py",
    },
}


print("=" * 60)
print("SAVING INDIVIDUAL PROBLEM RESULT")
print("=" * 60)

problem_file = save_problem_result(problem_result)

print(f"Problem result saved to: {problem_file}")


print("\n" + "=" * 60)
print("SAVING ALL RESULTS")
print("=" * 60)

all_results = [
    problem_result,
]

files = save_all_results(all_results)

print(f"Aggregate JSON: {files['json_file']}")
print(f"Aggregate CSV:  {files['csv_file']}")