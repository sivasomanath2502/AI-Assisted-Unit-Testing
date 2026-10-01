from agents.code_generator import generate_code
from agents.test_generator import generate_tests
from agents.test_executor import execute_tests, parse_results
from dataset_loader import load_dataset


def run_pipeline(problem_data):
    task_id = problem_data["task_id"]
    problem = problem_data["text"]

    print("\n" + "=" * 60)
    print(f"PROCESSING PROBLEM {task_id}")
    print("=" * 60)

    # --------------------------------------------------
    # Agent 1: Code generation
    # --------------------------------------------------

    print("\n[Agent 1] Generating code...")

    try:
        code = generate_code(problem)
    except Exception as error:
        print(f"CODE_GENERATION_FAILED: {error}")

        return {
            "task_id": task_id,
            "problem": problem,
            "code": None,
            "tests": None,
            "result": {
                "verdict": "CODE_GENERATION_FAILED",
                "error": str(error),
            },
        }

    print("\nGenerated Code:")
    print(code)

    # --------------------------------------------------
    # Agent 2: Test generation
    # --------------------------------------------------

    print("\n[Agent 2] Generating tests...")

    try:
        tests = generate_tests(code)
    except Exception as error:
        print(f"TEST_GENERATION_FAILED: {error}")

        return {
            "task_id": task_id,
            "problem": problem,
            "code": code,
            "tests": None,
            "result": {
                "verdict": "TEST_GENERATION_FAILED",
                "error": str(error),
            },
        }

    print("\nGenerated Tests:")
    print(tests)

    # --------------------------------------------------
    # Agent 3: Test execution
    # --------------------------------------------------

    print("\n[Agent 3] Executing tests...")

    execution_result = execute_tests(code, tests)
    final_result = parse_results(execution_result)

    print("\nExecution Output:")
    print(execution_result["pytest_output"])

    if execution_result["pytest_error"]:
        print("\nExecution Errors:")
        print(execution_result["pytest_error"])

    print("\nCoverage:")
    print(execution_result["coverage_output"])

    print("\nFinal Result:")
    print(final_result)

    return {
        "task_id": task_id,
        "problem": problem,
        "code": code,
        "tests": tests,
        "result": final_result,
    }


if __name__ == "__main__":
    dataset = load_dataset()

    print(f"Loaded {len(dataset)} problems")

    results = []

    for problem_data in dataset:
        result = run_pipeline(problem_data)
        results.append(result)

    print("\n" + "=" * 60)
    print("ALL PROBLEMS COMPLETED")
    print("=" * 60)

    for result in results:
        summary = result["result"]

        print(
            f"Problem {result['task_id']}: "
            f"{summary['verdict']} | "
            f"Branch Coverage: "
            f"{summary.get('branch_coverage', 0)}%"
        )