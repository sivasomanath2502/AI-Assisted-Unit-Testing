import json
import re
import subprocess
import tempfile
from pathlib import Path


def execute_tests(code, tests):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        solution_file = temp_path / "solution.py"
        test_file = temp_path / "test_generated.py"

        solution_file.write_text(code, encoding="utf-8")
        test_file.write_text(tests, encoding="utf-8")

        result = subprocess.run(
            [
                "coverage",
                "run",
                "--branch",
                "--source=solution",
                "-m",
                "pytest",
                "test_generated.py"
            ],
            capture_output=True,
            text=True,
            cwd=temp_path
        )

        coverage_result = subprocess.run(
            ["coverage", "report"],
            capture_output=True,
            text=True,
            cwd=temp_path
        )

        json_result = subprocess.run(
            ["coverage", "json"],
            capture_output=True,
            text=True,
            cwd=temp_path
        )

        coverage_file = temp_path / "coverage.json"

        base_result = {
            "pytest_return_code": result.returncode,
            "pytest_output": result.stdout,
            "pytest_error": result.stderr,
            "coverage_output": coverage_result.stdout,
        }

        if not coverage_file.exists():
            return {
                **base_result,
                "branch_covered": 0,
                "branch_total": 0,
                "branch_coverage": 0.0,
                "coverage_error": json_result.stderr,
            }

        coverage_data = json.loads(
            coverage_file.read_text(encoding="utf-8")
        )

        file_data = None

        for filename, data in coverage_data.get("files", {}).items():
            if filename.endswith("solution.py"):
                file_data = data
                break

        if file_data is None:
            return {
                **base_result,
                "branch_covered": 0,
                "branch_total": 0,
                "branch_coverage": 0.0,
                "coverage_error": "solution.py not found in coverage report",
            }

        summary = file_data["summary"]

        branch_total = summary.get("num_branches", 0)
        branch_covered = summary.get("covered_branches", 0)

        if branch_total == 0:
            branch_coverage = 100.0
        else:
            branch_coverage = (branch_covered / branch_total) * 100

        return {
            **base_result,
            "branch_covered": branch_covered,
            "branch_total": branch_total,
            "branch_coverage": branch_coverage,
        }


def parse_results(result):
    pytest_output = result["pytest_output"]

    passed_match = re.search(r"(\d+)\s+passed", pytest_output)
    failed_match = re.search(r"(\d+)\s+failed", pytest_output)
    error_match = re.search(r"(\d+)\s+error", pytest_output)

    tests_passed = int(passed_match.group(1)) if passed_match else 0
    tests_failed = int(failed_match.group(1)) if failed_match else 0
    test_errors = int(error_match.group(1)) if error_match else 0

    if result["pytest_return_code"] == 0:
        verdict = "PASS"
    else:
        verdict = "FAIL"

    return {
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "test_errors": test_errors,
        "branch_covered": result["branch_covered"],
        "branch_total": result["branch_total"],
        "branch_coverage": round(result["branch_coverage"], 2),
        "verdict": verdict,
    }
