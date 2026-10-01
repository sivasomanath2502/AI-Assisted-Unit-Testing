from agents.code_generator import generate_code
from agents.test_generator import generate_tests
from agents.review_agent import review_tests
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

from utils.persistence import (
    save_generated_artifacts,
)

from utils.results_writer import (
    save_problem_result,
    save_all_results,
)


def run_pipeline(problem_data):

    task_id = problem_data["task_id"]
    problem = problem_data["text"]

    contract = infer_contract(problem_data)

    print("=" * 60)
    print(f"PROCESSING PROBLEM {task_id}")
    print("=" * 60)

    # --------------------------------------------------
    # Dataset Contract
    # --------------------------------------------------

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
    # Agent 1 — Code Generator
    # --------------------------------------------------

    print("\n[Agent 1] Generating code...")

    MAX_CODE_ATTEMPTS = 2

    code = None
    reference = None

    for code_attempt in range(
        1,
        MAX_CODE_ATTEMPTS + 1,
    ):

        print(
            f"\nCode generation attempt "
            f"{code_attempt}/{MAX_CODE_ATTEMPTS}"
        )

        try:

            code = generate_code(
                problem,
                contract,
            )

        except Exception as error:

            print(
                f"\nCode generation failed: "
                f"{error}"
            )

            if code_attempt == MAX_CODE_ATTEMPTS:

                return {
                    "task_id": task_id,
                    "function_name": contract[
                        "function_name"
                    ],
                    "code": None,
                    "tests": None,
                    "reference": None,
                    "review": None,
                    "review_status": "NOT_RUN",
                    "result": {
                        "tests_passed": 0,
                        "tests_failed": 0,
                        "test_errors": 0,
                        "branch_covered": 0,
                        "branch_total": 0,
                        "branch_coverage": None,
                        "test_execution":
                            "CODE_GENERATION_FAILED",
                    },
                    "artifacts": None,
                }

            continue

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
            print(
                reference["stdout"]
            )

        if reference["stderr"]:
            print(
                reference["stderr"]
            )

        # --------------------------------------------------
        # Correct code → continue to Agent 2
        # --------------------------------------------------

        if reference["passed"]:

            break

        # --------------------------------------------------
        # Incorrect code → regenerate
        # --------------------------------------------------

        if code_attempt < MAX_CODE_ATTEMPTS:

            print(
                "\n[Agent 1] Generated code "
                "failed reference evaluation."
            )

            print(
                "[Agent 1] Regenerating "
                "the implementation..."
            )

        else:

            print(
                "\n[Agent 1] Code generation "
                "failed reference evaluation "
                "after all attempts."
            )

    # --------------------------------------------------
    # Stop if final implementation is incorrect
    # --------------------------------------------------

    if reference is None or not reference["passed"]:

        return {
            "task_id": task_id,
            "function_name": contract[
                "function_name"
            ],
            "code": code,
            "tests": None,
            "reference": reference,
            "review": None,
            "review_status": "NOT_RUN",
            "result": {
                "tests_passed": 0,
                "tests_failed": 0,
                "test_errors": 0,
                "branch_covered": 0,
                "branch_total": 0,
                "branch_coverage": None,
                "test_execution":
                    "CODE_CORRECTNESS_FAILED",
            },
            "artifacts": None,
        }

    # --------------------------------------------------
    # Agent 2 — Test Generator
    # --------------------------------------------------

    print("\n[Agent 2] Generating tests...")

    reference_tests = problem_data.get(
        "test_list",
        [],
    )

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
            "review": None,
            "review_status": "NOT_RUN",
            "result": {
                "tests_passed": 0,
                "tests_failed": 0,
                "test_errors": 0,
                "branch_covered": 0,
                "branch_total": 0,
                "branch_coverage": None,
                "test_execution": "TEST_GENERATION_FAILED",
            },
            "artifacts": None,
        }

    print("\nGenerated Tests:")
    print(tests)

    # --------------------------------------------------
    # Agent 3 — Review Agent
    # --------------------------------------------------

    print(
        "\n[Agent 3] Reviewing generated tests..."
    )

    review = None
    review_status = "NOT_RUN"

    try:

        review = review_tests(
            problem=problem,
            code=code,
            function_name=contract["function_name"],
            reference_tests=reference_tests,
            tests=tests,
        )

        review_status = review["verdict"]

        print("\nReview Verdict:")
        print(review["verdict"])

        print("\nReview Details:")
        print(review["response"])

    except Exception as error:

        review_status = "FAILED"

        print(
            f"\nReview Agent failed: {error}"
        )

    # --------------------------------------------------
    # One-Time Test Regeneration
    # --------------------------------------------------

    if (
        review is not None
        and review["verdict"] == "REJECT"
    ):

        print(
            "\n[Agent 3] Review rejected "
            "the generated tests."
        )

        print(
            "[Agent 2] Regenerating tests once..."
        )

        try:

            tests = generate_tests(
                problem=problem,
                code=code,
                function_name=contract["function_name"],
                reference_tests=reference_tests,
            )

            print("\nRegenerated Tests:")
            print(tests)

            print(
                "\n[Agent 3] Reviewing "
                "regenerated tests..."
            )

            review = review_tests(
                problem=problem,
                code=code,
                function_name=contract["function_name"],
                reference_tests=reference_tests,
                tests=tests,
            )

            review_status = review["verdict"]

            print("\nSecond Review Verdict:")
            print(review["verdict"])

            print("\nSecond Review Details:")
            print(review["response"])

        except Exception as error:

            review_status = "FAILED"

            print(
                f"\nReview/regeneration failed: "
                f"{error}"
            )

    # --------------------------------------------------
    # Persistence
    # --------------------------------------------------

    print(
        "\n[Persistence] "
        "Saving generated artifacts..."
    )

    artifacts = save_generated_artifacts(
        task_id=task_id,
        code=code,
        tests=tests,
    )

    print(
        f"Solution saved to: "
        f"{artifacts['solution_file']}"
    )

    print(
        f"Tests saved to: "
        f"{artifacts['test_file']}"
    )

    # --------------------------------------------------
    # Agent 4 — Test Executor
    # --------------------------------------------------

    print(
        "\n[Agent 4] Executing generated tests..."
    )

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

    # --------------------------------------------------
    # Final Result
    # --------------------------------------------------

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
        f"Code Correctness: "
        f"{code_correctness}"
    )

    print(
        f"Test Execution:   "
        f"{test_execution}"
    )

    print(
        f"Review Status:    "
        f"{review_status}"
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
        "review": review,
        "review_status": review_status,
        "result": result,
        "artifacts": artifacts,
    }


def _coverage_text(value):

    if value is None:
        return "N/A"

    return f"{value}%"


if __name__ == "__main__":

    dataset = load_dataset()[:5]

    print(
        f"\nLoaded {len(dataset)} problems"
    )

    results = []

    for problem_data in dataset:

        problem_result = run_pipeline(
            problem_data
        )

        results.append(
            problem_result
        )

        save_problem_result(
            problem_result
        )

    aggregate_files = save_all_results(
        results
    )

    print("\nAggregate results saved:")

    print(
        f"JSON: "
        f"{aggregate_files['json_file']}"
    )

    print(
        f"CSV:  "
        f"{aggregate_files['csv_file']}"
    )

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
            f"Review Status="
            f"{item.get('review_status', 'N/A')} | "
            f"Test Execution="
            f"{result.get('test_execution', 'N/A')} | "
            f"Branch Coverage="
            f"{_coverage_text(result.get('branch_coverage'))}"
        )