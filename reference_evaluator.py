import subprocess
import tempfile
from pathlib import Path

from utils.dataset_contract import infer_contract


def build_reference_tests(problem):
    setup = problem.get(
        "test_setup_code",
        ""
    ).strip()

    tests = problem.get(
        "test_list",
        []
    )

    parts = []

    if setup:
        parts.append(setup)

    parts.extend(tests)

    return "\n\n".join(parts) + "\n"


def evaluate_generated_code(code, problem):
    """
    Evaluate the generated solution against the executable
    assertions provided by the MBPP dataset.

    The dataset's expected outputs are not sent to the LLM.
    """

    contract = infer_contract(problem)

    function_name = contract["function_name"]

    reference_tests = build_reference_tests(problem)

    # The MBPP test_list contains executable assertions.
    # Import the generated function before executing them.
    import_line = (
        f"from solution import {function_name}\n"
    )

    test_source = (
        import_line
        + "\n"
        + reference_tests
    )

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        solution_file = (
            temp_path / "solution.py"
        )

        reference_file = (
            temp_path / "reference_test.py"
        )

        solution_file.write_text(
            code,
            encoding="utf-8"
        )

        reference_file.write_text(
            test_source,
            encoding="utf-8"
        )

        try:

            result = subprocess.run(
                [
                    "python",
                    "reference_test.py"
                ],
                cwd=temp_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            return {
                "passed": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "passed": False,
                "return_code": -1,
                "stdout": "",
                "stderr": (
                    "Reference evaluation timed out."
                )
            }

        except Exception as error:

            return {
                "passed": False,
                "return_code": -1,
                "stdout": "",
                "stderr": str(error)
            }