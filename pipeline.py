from agents.code_generator import generate_code
from agents.test_generator import generate_tests
from agents.test_executor import (
    execute_tests,
    parse_results,
)
from dataset_loader import load_dataset
from reference_evaluator import (
    evaluate_generated_code,
)
from utils.dataset_contract import (
    infer_contract,
)
from utils.persistence import save_generated_artifacts
from utils.results_writer import (
    save_problem_result,
    save_all_results,
)

def run_pipeline(problem_data):

    task_id = problem_data["task_id"]
    problem = problem_data["text"]

    contract = infer_contract(
        problem_data
    )

    print("=" * 60)
    print(
        f"PROCESSING PROBLEM {task_id}"
    )
    print("=" * 60)

    print("\n[Dataset Contract]")

    print(
        f"Function: "
        f"{contract['function_name']}"
    )

    print(
        f"Arguments: "
        f"{contract['argument_count']}"
    )

    print(
        f"Types: "
        f"{contract['argument_types']}"
    )

    # --------------------------------------------------
    # Agent 1
    # --------------------------------------------------

    print(
        "\n[Agent 1] Generating code..."
    )

    try:

        code = generate_code(
            problem,
            contract,
        )

    except Exception as error:

        print(f"\n{error}")

        return {
        "task_id": task_id,
        "function_name": contract["function_name"],
        "code": None,
        "tests": None,
        "reference": None,
        "result": {
            "tests_passed": 0,
            "tests_failed": 0,
            "test_errors": 0,
            "branch_covered": 0,
            "branch_total": 0,
            "branch_coverage": None,
            "verdict": "CODE_GENERATION_FAILED",
        },
        "artifacts": None,
    }

    print("\nGenerated Code:")
    print(code)

    # --------------------------------------------------
    # Reference Evaluation
    # --------------------------------------------------

    print(
        "\n[Reference Evaluation] "
        "Checking generated code..."
    )

    reference = evaluate_generated_code(
        code,
        problem_data,
    )

    print(
        "Reference Code: "
        + (
            "PASS"
            if reference["passed"]
            else "FAIL"
        )
    )

    if reference["stdout"]:
        print(reference["stdout"])

    if reference["stderr"]:
        print(reference["stderr"])

    # --------------------------------------------------
    # Agent 2
    # --------------------------------------------------

    print("\n[Agent 2] Generating tests...")

    reference_tests = problem_data.get("test_list", [])

    try:
        tests = generate_tests(
            problem=problem,
            code=code,
            function_name=contract["function_name"],
            reference_tests=reference_tests,
        )
    except Exception as error:

        print(f"\n{error}")

        return {
        "task_id": task_id,
        "function_name": contract["function_name"],
        "code": code,
        "tests": None,
        "reference": reference,
        "result": {
            "tests_passed": 0,
            "tests_failed": 0,
            "test_errors": 0,
            "branch_covered": 0,
            "branch_total": 0,
            "branch_coverage": None,
            "verdict": "TEST_GENERATION_FAILED",
        },
        "artifacts": None,
    }

    print("\nGenerated Tests:")
    print(tests)

    print("\n[Persistence] Saving generated artifacts...")

    artifacts = save_generated_artifacts(
        task_id=task_id,
        code=code,
        tests=tests,
    )

    print(f"Solution saved to: {artifacts['solution_file']}")
    print(f"Tests saved to: {artifacts['test_file']}")

    print("\n[Agent 3] Executing generated tests...")

    execution = execute_tests(
        code,
        tests,
    )

    result = parse_results(
        execution
    )

    print("\nExecution Output:")
    print(
        execution["pytest_output"]
    )

    if execution["pytest_error"]:
        print("\nExecution Errors:")
        print(
            execution["pytest_error"]
        )

    print("\nCoverage:")
    print(
        execution["coverage_output"]
    )

    print("\nFinal Result:")

    code_correctness = (
        "PASS"
        if reference["passed"]
        else "FAIL"
    )

    test_execution = result.get(
        "test_execution",
        "UNKNOWN",
    )

    print(
        f"Code Correctness: {code_correctness}"
    )

    print(
        f"Test Execution:   {test_execution}"
    )

    print(
        "Branch Coverage:  "
        f"{_coverage_text(result.get('branch_coverage'))}"
    )

    print(
        f"Tests Passed:     "
        f"{result.get('tests_passed', 0)}"
    )

    print(
        f"Tests Failed:     "
        f"{result.get('tests_failed', 0)}"
    )

    print(
        f"Test Errors:      "
        f"{result.get('test_errors', 0)}"
    )

    return {
    "task_id": task_id,
    "function_name": contract["function_name"],
    "code": code,
    "tests": tests,
    "reference": reference,
    "result": result,
    "artifacts": artifacts,
    }


def _coverage_text(value):

    if value is None:
        return "N/A"

    return f"{value}%"


if __name__ == "__main__":

    dataset = load_dataset()

    print(
        f"\nLoaded {len(dataset)} problems"
    )

    results = []

    for problem_data in dataset:
        problem_result = run_pipeline(problem_data)

        results.append(problem_result)

        save_problem_result(problem_result)

    aggregate_files = save_all_results(results)

    print("\nAggregate results saved:")
    print(f"JSON: {aggregate_files['json_file']}")
    print(f"CSV:  {aggregate_files['csv_file']}")
    print("\n")
    print("=" * 60)
    print("ALL PROBLEMS COMPLETED")
    print("=" * 60)

    for item in results:

        result = item["result"]
        reference = item["reference"]

        reference_text = (
            "N/A"
            if reference is None
            else (
                "PASS"
                if reference["passed"]
                else "FAIL"
            )
        )

        print(
        f"Problem {item['task_id']}: "
        f"Code Correctness={reference_text} | "
        f"Test Execution="
        f"{result.get('test_execution', 'N/A')} | "
        f"Branch Coverage="
        f"{_coverage_text(result.get('branch_coverage'))}"
    )