import csv
import json
from pathlib import Path


RESULTS_DIR = Path("results")


def save_problem_result(result):
    task_id = result["task_id"]

    problem_dir = RESULTS_DIR / f"problem_{task_id}"
    problem_dir.mkdir(parents=True, exist_ok=True)

    result_file = problem_dir / "result.json"

    result_file.write_text(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return str(result_file)


def save_all_results(results):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    json_file = RESULTS_DIR / "results.json"
    csv_file = RESULTS_DIR / "results.csv"

    json_file.write_text(
        json.dumps(
            results,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    rows = []

    for item in results:
        result = item.get("result") or {}
        reference = item.get("reference") or {}
        artifacts = item.get("artifacts") or {}

        rows.append({
            "task_id": item.get("task_id"),
            "function_name": item.get("function_name"),
            "code_correct": reference.get("passed"),
            "tests_passed": result.get("tests_passed"),
            "tests_failed": result.get("tests_failed"),
            "test_errors": result.get("test_errors"),
            "branch_covered": result.get("branch_covered"),
            "branch_total": result.get("branch_total"),
            "branch_coverage": result.get("branch_coverage"),
            "test_execution": result.get("test_execution"),
            "solution_file": artifacts.get("solution_file"),
            "test_file": artifacts.get("test_file"),
        })

    fieldnames = [
        "task_id",
        "function_name",
        "code_correct",
        "tests_passed",
        "tests_failed",
        "test_errors",
        "branch_covered",
        "branch_total",
        "branch_coverage",
        "test_execution",
        "solution_file",
        "test_file",
    ]

    with csv_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    return {
        "json_file": str(json_file),
        "csv_file": str(csv_file),
    }