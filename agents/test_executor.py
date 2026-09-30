import json
import subprocess
import tempfile
from pathlib import Path


def execute_tests(code, tests):

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        test_file = temp_path / "test_generated.py"

        # Combine the generated solution code
        # and generated tests into one executable file.
        combined_code = f"""
{code}


{tests}
"""

        test_file.write_text(
            combined_code,
            encoding="utf-8"
        )

        # --------------------------------------------------
        # Step 1: Execute tests and collect coverage data
        # --------------------------------------------------

        result = subprocess.run(
            [
                "coverage",
                "run",
                "--branch",
                "-m",
                "pytest",
                str(test_file)
            ],
            capture_output=True,
            text=True,
            cwd=temp_path
        )

        # --------------------------------------------------
        # Step 2: Generate human-readable coverage report
        # --------------------------------------------------

        coverage_result = subprocess.run(
            [
                "coverage",
                "report"
            ],
            capture_output=True,
            text=True,
            cwd=temp_path
        )

        # --------------------------------------------------
        # Step 3: Generate machine-readable coverage report
        # --------------------------------------------------

        json_result = subprocess.run(
            [
                "coverage",
                "json"
            ],
            capture_output=True,
            text=True,
            cwd=temp_path
        )

        # Make sure coverage.json was generated successfully.
        coverage_file = temp_path / "coverage.json"

        if not coverage_file.exists():

            return {
                "pytest_return_code": result.returncode,
                "pytest_output": result.stdout,
                "pytest_error": result.stderr,
                "coverage_output": coverage_result.stdout,
                "branch_covered": 0,
                "branch_total": 0,
                "branch_coverage": 0.0,
                "coverage_error": json_result.stderr
            }

        # --------------------------------------------------
        # Step 4: Read coverage.json
        # --------------------------------------------------

        coverage_data = json.loads(
            coverage_file.read_text(
                encoding="utf-8"
            )
        )

        # There should normally be one generated Python file.
        file_data = next(
            iter(coverage_data["files"].values())
        )

        summary = file_data["summary"]

        branch_total = summary.get(
            "num_branches",
            0
        )

        branch_covered = summary.get(
            "covered_branches",
            0
        )

        # If there are no branches, we consider
        # branch coverage to be 100%.
        if branch_total == 0:

            branch_coverage = 100.0

        else:

            branch_coverage = (
                branch_covered / branch_total
            ) * 100

        # --------------------------------------------------
        # Step 5: Return structured execution result
        # --------------------------------------------------

        return {
            "pytest_return_code": result.returncode,
            "pytest_output": result.stdout,
            "pytest_error": result.stderr,
            "coverage_output": coverage_result.stdout,
            "branch_covered": branch_covered,
            "branch_total": branch_total,
            "branch_coverage": branch_coverage
        }


def parse_results(result):

    pytest_output = result["pytest_output"]

    tests_passed = 0
    tests_failed = 0

    # --------------------------------------------------
    # Parse pytest result
    # --------------------------------------------------

    for line in pytest_output.splitlines():

        parts = line.split()

        for i, part in enumerate(parts):

            if part == "passed" and i > 0:

                tests_passed = int(
                    parts[i - 1]
                )

            elif part == "failed" and i > 0:

                tests_failed = int(
                    parts[i - 1]
                )

    # --------------------------------------------------
    # Determine final verdict
    # --------------------------------------------------

    if result["pytest_return_code"] == 0:

        verdict = "PASS"

    else:

        verdict = "FAIL"

    # --------------------------------------------------
    # Return clean result for the pipeline
    # --------------------------------------------------

    return {
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "branch_covered": result["branch_covered"],
        "branch_total": result["branch_total"],
        "branch_coverage": round(
            result["branch_coverage"],
            2
        ),
        "verdict": verdict
    }


if __name__ == "__main__":

    code = """
def largest_element(lst):
    if not lst:
        return None

    max_val = lst[0]

    for num in lst:

        if num > max_val:
            max_val = num

    return max_val
"""

    tests = """
def test_empty():

    assert largest_element([]) is None


def test_increasing():

    assert largest_element([1, 2, 3]) == 3


def test_decreasing():

    assert largest_element([5, 3, 1]) == 5
"""

    # Execute the generated tests.
    result = execute_tests(
        code,
        tests
    )

    # Convert raw execution information
    # into our final structured result.
    parsed_result = parse_results(
        result
    )

    print("PYTEST OUTPUT")
    print(result["pytest_output"])

    print("PYTEST ERRORS")
    print(result["pytest_error"])

    print("COVERAGE")
    print(result["coverage_output"])

    print("FINAL RESULT")
    print(parsed_result)