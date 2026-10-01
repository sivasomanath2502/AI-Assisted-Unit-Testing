from pathlib import Path

from llm_client import ask_llm
from utils.artifact_validator import validate_code


PROMPT_FILE = (
    Path(__file__).parent.parent
    / "prompts"
    / "code_generator_prompt.txt"
)


def generate_code(problem, contract, max_attempts=3):

    prompt_template = PROMPT_FILE.read_text(
        encoding="utf-8"
    )

    base_prompt = prompt_template.format(
        problem=problem,
        function_name=contract["function_name"],
        argument_count=contract["argument_count"],
        argument_types=", ".join(
            contract["argument_types"]
        ),
    )

    prompt = base_prompt

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        raw = ask_llm(prompt)

        valid, cleaned, error = validate_code(
            raw,
            required_function_name=(
                contract["function_name"]
            ),
        )

        if valid:
            return cleaned

        if attempt == max_attempts:
            raise RuntimeError(
                f"CODE_GENERATION_FAILED: {error}"
            )

        prompt = (
            base_prompt
            + "\n\n"
            + "Your previous response was rejected "
            + "by the validator.\n"
            + f"Validation error: {error}\n"
            + (
                "Regenerate the complete solution using "
                f"the exact function name "
                f"'{contract['function_name']}'.\n"
            )
            + "Return only raw Python source code."
        )