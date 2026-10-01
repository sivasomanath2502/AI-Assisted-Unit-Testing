from pathlib import Path

from llm_client import ask_llm
from utils.artifact_validator import validate_tests


PROMPT_FILE = (
    Path(__file__).parent.parent
    / "prompts"
    / "test_generator_prompt.txt"
)


def generate_tests(
    problem,
    code,
    function_name,
    reference_tests,
    max_attempts=3,
):
    prompt_template = PROMPT_FILE.read_text(
        encoding="utf-8"
    )

    reference_examples = "\n".join(reference_tests)

    base_prompt = prompt_template.format(
        problem=problem,
        code=code,
        function_name=function_name,
        reference_tests=reference_examples,
    )

    prompt = base_prompt

    for attempt in range(1, max_attempts + 1):

        raw = ask_llm(prompt)

        valid, cleaned, error = validate_tests(
            raw,
            required_function_name=function_name,
        )

        if valid:
            return cleaned

        if attempt == max_attempts:
            raise RuntimeError(
                f"TEST_GENERATION_FAILED: {error}"
            )

        prompt = (
            base_prompt
            + "\n\n"
            "Your previous response was rejected by "
            "the validator.\n"
            + f"Validation error: {error}\n"
            + "\nRegenerate the complete pytest file.\n"
            + f"Import exactly '{function_name}' from solution.\n"
            + "Return only valid Python source code."
        )