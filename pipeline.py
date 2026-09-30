from agents.code_generator import generate_code
from agents.test_generator import generate_tests
from agents.test_executor import execute_tests, parse_results


def run_pipeline(problem):

    print("=" * 60)
    print("STARTING UNIT TESTING PIPELINE")
    print("=" * 60)

    # Agent 1: Generate code
    print("\n[Agent 1] Generating code...")

    code = generate_code(problem)

    print("\nGenerated Code:")
    print(code)

    # Agent 2: Generate tests
    print("\n[Agent 2] Generating test cases...")

    tests = generate_tests(code)

    print("\nGenerated Tests:")
    print(tests)

    # Agent 3: Execute tests
    print("\n[Agent 3] Executing tests...")

    execution_result = execute_tests(
        code,
        tests
    )

    # Parse execution result
    final_result = parse_results(
        execution_result
    )

    print("\nExecution Output:")
    print(execution_result["pytest_output"])

    print("\nCoverage:")
    print(execution_result["coverage_output"])

    print("\nFinal Result:")
    print(final_result)

    return {
        "problem": problem,
        "code": code,
        "tests": tests,
        "result": final_result
    }


if __name__ == "__main__":

    problem = """
Write a function that takes a list of integers
and returns the largest element in the list.
"""

    result = run_pipeline(problem)