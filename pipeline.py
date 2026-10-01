from agents.code_generator import generate_code
from agents.test_generator import generate_tests
from agents.review_agent import review_tests
from agents.test_executor import execute_tests

from dataset_loader import load_dataset
from reference_evaluator import evaluate_generated_code

from utils.dataset_contract import infer_contract
from utils.persistence import save_generated_artifacts
from utils.results_writer import (
    save_problem_result,
    save_all_results,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MAX_CODE_ATTEMPTS = 2


# ---------------------------------------------------------
# Run Pipeline for One Problem
# ---------------------------------------------------------

def run_pipeline(problem):
    task_id = problem["task_id"]

    print("=" * 60)
    print(f"PROCESSING PROBLEM {task_id}")
    print("=" * 60)

    # -----------------------------------------------------
    # Dataset Contract
    # -----------------------------------------------------

    contract = infer_contract(problem)

    function_name = contract["function_name"]

    reference_tests = problem.get(
        "test_list",
        [],
    )

    print("\n[Dataset Contract]")
    print(f"Function: {contract['function_name']}")
    print(f"Arguments: {contract['argument_count']}")
    print(f"Types: {contract['argument_types']}")

    # -----------------------------------------------------
    # Agent 1 - Code Generation
    # -----------------------------------------------------

    code = None
    reference_result = None

    print("\n[Agent 1] Generating code...")

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
                problem=problem,
                contract=contract,
                reference_tests=reference_tests,
            )

        except Exception as error:
            print("\nCode generation failed:")
            print(error)

            if code_attempt == MAX_CODE_ATTEMPTS:
                return {
                    "task_id": task_id,
                    "function_name": function_name,
                    "code": None,
                    "tests": None,
                    "reference": {
                        "passed": False,
                        "error": str(error),
                    },
                    "review": None,
                    "review_status": "NOT_RUN",
                    "result": {
                        "test_execution":
                            "CODE_GENERATION_FAILED",
                        "tests_passed": 0,
                        "tests_failed": 0,
                        "test_errors": 0,
                        "branch_covered": None,
                        "branch_total": None,
                        "branch_coverage": None,
                    },
                    "artifacts": {},
                }

            continue

        print("\nGenerated Code:")
        print(code)

        # -------------------------------------------------
        # Reference Evaluation
        # -------------------------------------------------

        print(
            "\n[Reference Evaluation] "
            "Checking generated code..."
        )

        reference_result = evaluate_generated_code(
            code,
            problem,
        )

        if reference_result["passed"]:
            print("Reference Code: PASS")
            break

        print("Reference Code: FAIL")

        if reference_result.get("stderr"):
            print(reference_result["stderr"])

        if code_attempt < MAX_CODE_ATTEMPTS:
            print(
                "\nGenerated code failed the "
                "reference tests."
            )
            print("Regenerating code...")

        else:
            print(
                "\nCode correctness could not "
                "be established."
            )

            return {
                "task_id": task_id,
                "function_name": function_name,
                "code": code,
                "tests": None,
                "reference": reference_result,
                "review": None,
                "review_status": "NOT_RUN",
                "result": {
                    "test_execution":
                        "CODE_CORRECTNESS_FAILED",
                    "tests_passed": 0,
                    "tests_failed": 0,
                    "test_errors": 0,
                    "branch_covered": None,
                    "branch_total": None,
                    "branch_coverage": None,
                },
                "artifacts": {},
            }

    # -----------------------------------------------------
    # Agent 2 - Test Generation
    # -----------------------------------------------------

    print("\n[Agent 2] Generating tests...")

    try:
        tests = generate_tests(
            problem=problem,
            code=code,
            function_name=function_name,
            reference_tests=reference_tests,
        )

        print("\nGenerated Tests:")
        print(tests)

    except Exception as error:
        print("\nTest Generator failed:")
        print(error)

        return {
            "task_id": task_id,
            "function_name": function_name,
            "code": code,
            "tests": None,
            "reference": reference_result,
            "review": None,
            "review_status": "NOT_RUN",
            "result": {
                "test_execution":
                    "TEST_GENERATION_FAILED",
                "tests_passed": 0,
                "tests_failed": 0,
                "test_errors": 0,
                "branch_covered": None,
                "branch_total": None,
                "branch_coverage": None,
            },
            "artifacts": {},
        }

    # -----------------------------------------------------
    # Agent 3 - Review Generated Tests
    # -----------------------------------------------------

    print(
        "\n[Agent 3] Reviewing generated tests..."
    )

    review = None
    review_status = "FAILED"

    try:
        review = review_tests(
            problem=problem,
            code=code,
            function_name=function_name,
            reference_tests=reference_tests,
            tests=tests,
        )

        review_status = review["verdict"]

        print("\nReview Verdict:")
        print(review["verdict"])

        print("\nReview Details:")
        print(review["response"])

    except Exception as error:
        print("\nReview Agent failed:")
        print(error)

        print(
            "\n[Pipeline] Agent 4 execution skipped."
        )

        return {
            "task_id": task_id,
            "function_name": function_name,
            "code": code,
            "tests": tests,
            "reference": reference_result,
            "review": {
                "verdict": None,
                "approved": False,
                "response": str(error),
                "attempts": 0,
            },
            "review_status": "FAILED",
            "result": {
                "test_execution":
                    "REVIEW_FAILED",
                "tests_passed": 0,
                "tests_failed": 0,
                "test_errors": 0,
                "branch_covered": None,
                "branch_total": None,
                "branch_coverage": None,
            },
            "artifacts": {},
        }

    # -----------------------------------------------------
    # Review Rejected
    # Regenerate Tests Once
    # -----------------------------------------------------

    if review_status == "REJECT":
        print(
            "\n[Agent 3] Tests rejected."
        )

        print(
            "[Agent 2] Regenerating tests..."
        )

        try:
            tests = generate_tests(
                problem=problem,
                code=code,
                function_name=function_name,
                reference_tests=reference_tests,
            )

            print("\nRegenerated Tests:")
            print(tests)

            print(
                "\n[Agent 3] "
                "Reviewing regenerated tests..."
            )

            review = review_tests(
                problem=problem,
                code=code,
                function_name=function_name,
                reference_tests=reference_tests,
                tests=tests,
            )

            review_status = review["verdict"]

            print("\nSecond Review Verdict:")
            print(review["verdict"])

            print("\nSecond Review Details:")
            print(review["response"])

        except Exception as error:
            print(
                "\nReview/regeneration failed:"
            )
            print(error)

            print(
                "\n[Pipeline] "
                "Agent 4 execution skipped."
            )

            return {
                "task_id": task_id,
                "function_name": function_name,
                "code": code,
                "tests": tests,
                "reference": reference_result,
                "review": {
                    "verdict": None,
                    "approved": False,
                    "response": str(error),
                    "attempts": 0,
                },
                "review_status": "FAILED",
                "result": {
                    "test_execution":
                        "REVIEW_FAILED",
                    "tests_passed": 0,
                    "tests_failed": 0,
                    "test_errors": 0,
                    "branch_covered": None,
                    "branch_total": None,
                    "branch_coverage": None,
                },
                "artifacts": {},
            }

    # -----------------------------------------------------
    # Review Must Approve Before Execution
    # -----------------------------------------------------

    if review_status != "APPROVE":
        print(
            "\n[Pipeline] Tests were not "
            "approved by the Review Agent."
        )

        print(
            "[Pipeline] Agent 4 execution skipped."
        )

        return {
            "task_id": task_id,
            "function_name": function_name,
            "code": code,
            "tests": tests,
            "reference": reference_result,
            "review": review,
            "review_status": review_status,
            "result": {
                "test_execution":
                    "REVIEW_NOT_APPROVED",
                "tests_passed": 0,
                "tests_failed": 0,
                "test_errors": 0,
                "branch_covered": None,
                "branch_total": None,
                "branch_coverage": None,
            },
            "artifacts": {},
        }

    # -----------------------------------------------------
    # Persistence
    # -----------------------------------------------------

    print(
        "\n[Persistence] "
        "Saving generated artifacts..."
    )

    artifacts = save_generated_artifacts(
        task_id,
        code,
        tests,
    )

    print(
        f"Solution saved to: "
        f"{artifacts['solution_file']}"
    )

    print(
        f"Tests saved to: "
        f"{artifacts['test_file']}"
    )

    # -----------------------------------------------------
    # Agent 4 - Test Execution
    # -----------------------------------------------------

    print(
        "\n[Agent 4] Executing generated tests..."
    )

    execution_result = execute_tests(
        code,
        tests,
    )

    # -----------------------------------------------------
    # Final Result
    # -----------------------------------------------------

    return {
        "task_id": task_id,
        "function_name": function_name,
        "code": code,
        "tests": tests,
        "reference": reference_result,
        "review": review,
        "review_status": review_status,
        "result": execution_result,
        "artifacts": artifacts,
    }


# ---------------------------------------------------------
# Main - Full Dataset Evaluation
# ---------------------------------------------------------

def main():
    dataset = load_dataset()

    # For development/testing:
    # Change this to the desired number when running
    # the complete evaluation.
    dataset = dataset[:5]

    results = []

    for problem in dataset:
        result = run_pipeline(problem)

        results.append(result)

        save_problem_result(result)

        print("\n" + "=" * 60)
        print(
            f"Completed Problem "
            f"{problem['task_id']}"
        )
        print("=" * 60)

        reference = result.get("reference") or {}
        execution = result.get("result") or {}

        code_correctness = (
            "PASS"
            if reference.get("passed")
            else "FAIL"
        )

        print(
            f"Code Correctness: "
            f"{code_correctness}"
        )

        print(
            f"Review Status: "
            f"{result.get('review_status')}"
        )

        print(
            f"Test Execution: "
            f"{execution.get('test_execution')}"
        )

        print(
            f"Branch Coverage: "
            f"{execution.get('branch_coverage')}"
        )

    # -----------------------------------------------------
    # Aggregate Results
    # -----------------------------------------------------

    aggregate_files = save_all_results(
        results
    )

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    for item in results:
        result = item.get("result") or {}
        reference = item.get("reference") or {}

        code_correctness = (
            "PASS"
            if reference.get("passed")
            else "FAIL"
        )

        print(
            f"Problem {item['task_id']}: "
            f"Code Correctness={code_correctness} | "
            f"Review Status={item.get('review_status')} | "
            f"Test Execution="
            f"{result.get('test_execution')} | "
            f"Branch Coverage="
            f"{result.get('branch_coverage')}"
        )

    print("\nResults saved to:")
    print(aggregate_files["json_file"])
    print(aggregate_files["csv_file"])


if __name__ == "__main__":
    main()
