from pathlib import Path


GENERATED_DIR = Path("generated")


def save_generated_artifacts(task_id, code, tests):
    problem_dir = GENERATED_DIR / f"problem_{task_id}"
    problem_dir.mkdir(parents=True, exist_ok=True)

    solution_file = problem_dir / "solution.py"
    test_file = problem_dir / "test_generated.py"

    solution_file.write_text(
        code,
        encoding="utf-8",
    )

    test_file.write_text(
        tests,
        encoding="utf-8",
    )

    return {
        "solution_file": str(solution_file),
        "test_file": str(test_file),
    }